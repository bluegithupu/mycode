import os
import json
import asyncio
import operator
from typing import TypedDict, List, Annotated, Literal, Dict, Union, Optional 
from datetime import datetime

from tavily import AsyncTavilyClient, TavilyClient

from langchain_core.tools import tool
from langchain_core.messages import AnyMessage, AIMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.pydantic_v1 import BaseModel, Field, conlist
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, add_messages


# 在文件顶部添加以下硬编码的 API 密钥
import os
os.environ['TAVILY_API_KEY'] = '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'
os.environ['OPENAI_API_KEY'] = 'sk-cdjsim5KBne5thQJ2bF279E94fEa487aA347A7D85747Af10'
os.environ['OPENAI_API_BASE'] = 'https://api.rcouyi.com/v1'
# PDF生成代码
import re
from fpdf import FPDF

import logging

# 设置日志记录器
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def sanitize_content(content):
    try:
        encoded_content = content.encode('utf-8', 'ignore').decode('utf-8')
        return encoded_content
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        sanitized_content = content.encode('ascii', 'ignore').decode('ascii')
        return sanitized_content

def replace_problematic_characters(content):
    replacements = {
        '\u2013': '-',
        '\u2014': '--',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2026': '...',
        '\u2010': '-',
        '\u2022': '*',
        '\u2122': 'TM'
    }

    for char, replacement in replacements.items():
        content = content.replace(char, replacement)

    return content

def generate_pdf_from_md(content, filename='output.pdf'):
    try:
        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font('Arial', '', 12)

        sanitized_content = sanitize_content(content)
        sanitized_content = replace_problematic_characters(sanitized_content)

        lines = sanitized_content.split('\n')

        for line in lines:
            if line.startswith('#'):
                header_level = min(line.count('#'), 4)
                header_text = re.sub(r'\*{2,}', '', line.strip('# ').strip())
                pdf.set_font('Arial', 'B', 12 + (4 - header_level) * 2)
                pdf.multi_cell(0, 10, header_text)
                pdf.set_font('Arial', '', 12)
            else:
                parts = re.split(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*|\[.*?\]\(.*?\)|\([^ ]+?\))', line)
                for part in parts:
                    if re.match(r'\*\*\*.*?\*\*\*', part):
                        text = part.strip('*')
                        pdf.set_font('Arial', 'BI', 12)
                        pdf.write(10, text)
                    elif re.match(r'\*\*.*?\*\*', part):
                        text = part.strip('*')
                        pdf.set_font('Arial', 'B', 12)
                        pdf.write(10, text)
                    elif re.match(r'\*.*?\*', part):
                        text = part.strip('*')
                        pdf.set_font('Arial', 'I', 12)
                        pdf.write(10, text)
                    elif re.match(r'\[.*?\]\(.*?\)', part):
                        display_text = re.search(r'\[(.*?)\]', part).group(1)
                        url = re.search(r'\((.*?)\)', part).group(1)
                        pdf.set_text_color(0, 0, 255)
                        pdf.set_font('', 'U')
                        pdf.write(10, display_text, url)
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font('Arial', '', 12)
                    else:
                        pdf.write(10, part)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font('Arial', '', 12)

                pdf.ln(10)

        pdf.output(filename)
        return f"PDF generated: {filename}"

    except Exception as e:
        return f"Error generating PDF: {e}"

# 定义研究状态
class ResearchState(TypedDict):
    company: str
    company_keywords: str
    exclude_keywords: str
    report: str
    documents: Dict[str, Dict[Union[str, int], Union[str, float]]]
    RAG_docs: Dict[str, Dict[Union[str, int], Union[str, float]]]
    messages: Annotated[list[AnyMessage], add_messages]

# 定义模型响应的结构,包括引用
class Citation(BaseModel):
    source_id: str = Field(
        ...,
        description="The url of a SPECIFIC source which justifies the answer.",
    )
    quote: str = Field(
        ...,
        description="The VERBATIM quote from the specified source that justifies the answer.",
    )

class QuotedAnswer(BaseModel):
    """Answer the user question based only on the given sources, and cite the sources used."""
    answer: str = Field(
        ...,
        description="The answer to the user question, which is based only on the given sources. Include any relevant sources in the answer as markdown hyperlinks. For example: 'This is a sample text ([url website](url))'"
    )
    citations: List[Citation] = Field(
        ..., description="Citations from the given sources that justify the answer."
    )
    
# 添加Tavily的参数以增强网络搜索工具的功能
class TavilyQuery(BaseModel):
    query: str = Field(description="web search query")
    topic: str = Field(description="type of search, should be 'general' or 'news'. Choose 'news' ONLY when the company you searching is publicly traded and is likely to be featured on popular news")
    days: int = Field(description="number of days back to run 'news' search")
    domains: Optional[List[str]] = Field(default=None, description="list of domains to include in the research. Useful when trying to gather information from trusted and relevant domains")

# 为tavily_search工具定义args_schema,使用多查询方法,使Tavily的查询更精确
class TavilySearchInput(BaseModel):
    sub_queries: List[TavilyQuery] = Field(description="set of sub-queries that can be answered in isolation")

class TavilyExtractInput(BaseModel):
    urls: List[str] = Field(description="list of a single or several URLs for extracting raw content to gather additional information")

@tool("tavily_search", args_schema=TavilySearchInput, return_direct=True)
async def tavily_search(sub_queries: List[TavilyQuery]):
    """Perform searches for each sub-query using the Tavily search tool concurrently."""  
    async def perform_search(itm):
        try:
            query_with_date = f"{itm.query} {datetime.now().strftime('%m-%Y')}"
            response = await tavily_client.search(query=query_with_date, topic=itm.topic, days=itm.days, max_results=10)
            return response['results']
        except Exception as e:
            print(f"Error occurred during search for query '{itm.query}': {str(e)}")
            return []
    
    search_tasks = [perform_search(itm) for itm in sub_queries]
    search_responses = await asyncio.gather(*search_tasks)
    
    search_results = []
    for response in search_responses:
        search_results.extend(response)
    
    return search_results

tools = [tavily_search]
tools_by_name = {tool.name: tool for tool in tools}
tavily_client = AsyncTavilyClient()

# 定义一个异步自定义研究工具节点,用于存储Tavily的搜索结果,以便更好地处理和后续过滤
async def tool_node(state: ResearchState):
    # docs = state.get('documents',{})

    logging.info("Entering tool_node function")
    
    if state is None:
        logging.error("State is None")
        return {"messages": [], "documents": {}}
    
    logging.debug(f"State keys: {state.keys()}")
    
    docs = state.get('documents')
    logging.info(f"Retrieved documents from state: {type(docs)}")
    
    if docs is None:
        logging.warning("Documents is None, initializing as empty dict")
        docs = {}
    
    logging.debug(f"Documents content: {docs}")

    # print("Debug - Documents:")
    # for url, doc in docs.items():
    #     print("=====================")
    #     print(f"URL: {url}")
    #     print(f"Title: {doc.get('title', 'N/A')}")
    #     print(f"Content: {doc.get('content', 'N/A')[:100]}...")  # 只打印前100个字符
    #     print("-" * 50)

    docs_str = ""
    msgs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        new_docs = await tool.ainvoke(tool_call["args"])
        for doc in new_docs:
            # Make sure that this document was not retrieved before
            if not docs or doc['url'] not in docs:
                docs[doc['url']] = doc
                docs_str += json.dumps(doc)
            # For Tavily Extract tool, checking if raw_content was retrieved a document
            # if doc.get('raw_content', None) and doc['url'] in docs:
            #     docs[doc['url']]['raw_content'] = doc['raw_content'] # add raw content retrieved by extract
            #     docs_str += json.dumps(doc)
        msgs.append(ToolMessage(content=f"Found the following new documents/information: {docs_str}", tool_call_id=tool_call["id"]))
    return {"messages": msgs, "documents": docs}
    
# 调用模型与研究工具收集公司数据
def research_model(state: ResearchState):
    prompt = f"""Today's date is {datetime.now().strftime('%d/%m/%Y')}.\n
You are an expert researcher tasked with gathering information for a weekly report on recent developments in portfolio companies.\n
Your current objective is to gather documents about any significant events that occurred in the past week for the following company: {state['company']}.\n
The user has provided the following company keywords: {state['company_keywords']} to help you find documents relevant to the correct company.\n     
**Instructions:**\n
- Use the 'tavily_search' tool to search for relevant documents
- Focus on gathering documents by making appropriate tool calls
- If you believe you have gathered enough information, state 'I have gathered enough information and am ready to proceed.'
"""
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini",temperature=0)
    response = model.bind_tools(tools).invoke(messages)
    return {"messages": [response]}

# 定义函数,决定是继续使用工具进行研究还是进行报告撰写
def should_continue(state: ResearchState) -> Literal["tools", "curate"]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "curate"

async def select_and_process(state: ResearchState):
    msg = "Curating Documents ...\n"
    prompt = f"""You are an expert researcher specializing in analyzing portfolio companies.\n
Your current task is to review a list of documents and select the most relevant URLs related to recent developments for the following company: {state['company']}.\n
Be aware that some documents may refer to other companies with similar or identical names, potentially leading to conflicting information.\n
Your objective is to choose the documents that pertain to the correct company and provide the most consistent and synchronized information, using the following keywords provided by the user to help identify the correct company as a guide:{state['company_keywords']}.\n"""
    if state['exclude_keywords'] != "":
        prompt += f"""Additionally, if any form of the following exclusion words are present in the documents, do not include them and filter out those documents: {state['exclude_keywords']}.\n"""
    prompt += f"""\nHere is the list of documents gathered for your review:\n{state['documents']}\n\n"""

    messages = [SystemMessage(content=prompt)]  
    model = ChatOpenAI(model="gpt-4o-mini",temperature=0)
    relevant_urls = model.with_structured_output(TavilyExtractInput).invoke(messages)
    
    RAG_docs = {url: state['documents'][url] for url in relevant_urls.urls if url in state['documents']}

    try:
        response = await tavily_client.extract(urls=relevant_urls.urls)
        
        msg += "Extracted raw content for:\n"
        for itm in response['results']:
            url = itm['url']
            msg += f"{url}\n" 
            raw_content = itm['raw_content']
            RAG_docs[url]['raw_content'] = raw_content
    except Exception as e:
        print(f"Error occurred during Tavily Extract request")
        
    msg += f"ֿֿ\n\nState of RAG documents that will be used for the report:\n\n{RAG_docs}"
        
    return {"messages": [AIMessage(content=msg)],"RAG_docs": RAG_docs}
            
# 定义函数,根据检索到的文档撰写报告
def write_report(state: ResearchState):
    prompt = f"""Today's date is {datetime.now().strftime('%d/%m/%Y')}\n.
You are an expert researcher, writing a weekly report about recent events in portfolio companies.\n
Your task is to write an in-depth, well-written, and detailed report on the following company: {state['company']}. in markdown syntax\n
Here are all the documents you should base your answer on:\n{state['RAG_docs']}\n""" 
    messages = [SystemMessage(content=prompt)] 
    model = ChatOpenAI(model="gpt-4o-mini",temperature=0)
    response = model.with_structured_output(QuotedAnswer).invoke(messages)
    full_report = response.answer
    full_report += "\n\n### Citations\n"
    for citation in response.citations:
        doc = state['RAG_docs'].get(citation.source_id)
        full_report += f"- [{doc.get('title',citation.source_id)}]({citation.source_id}): \"{citation.quote}\"\n"
    return {"messages": [AIMessage(content=f"Generated Report:\n{full_report}")], "report": full_report}

def generete_pdf(state: ResearchState):
    directory = "reports"
    file_name = f"{state['company']} Weekly Report {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    msg = generate_pdf_from_md(state['report'], filename=f'{directory}/{file_name}.pdf')
    return {"messages": [AIMessage(content=msg)]}

# 定义图
workflow = StateGraph(ResearchState)

# 添加节点
workflow.add_node("research", research_model)
workflow.add_node("tools", tool_node)
workflow.add_node("curate", select_and_process)
workflow.add_node("write", write_report)
workflow.add_node("publish", generete_pdf)
workflow.set_entry_point("research")

workflow.add_conditional_edges(
    "research",
    should_continue,
)

workflow.add_edge("tools", "research")
workflow.add_edge("curate","write")
workflow.add_edge("write", "publish")
workflow.add_edge("publish", END)

app = workflow.compile()

# 运行研究
async def run_research(company, company_keywords, exclude_keywords=""):
    messages = [
        SystemMessage(content="You are an expert researcher ready to begin the information gathering process.")
    ]
    async for s in app.astream({"company": company, "company_keywords": company_keywords, "exclude_keywords": exclude_keywords, "messages":messages}, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

if __name__ == "__main__":
    company = "Athena Intelligence"
    company_keywords = "data analyst, AI-native analyst platform"
    exclude_keywords = "wildfire"
    
    asyncio.run(run_research(company, company_keywords, exclude_keywords))
