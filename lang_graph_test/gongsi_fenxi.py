import os
import asyncio
from typing import TypedDict, Annotated, Dict, Any
from datetime import datetime

from langchain_core.messages import AnyMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, add_messages
from langchain.tools.tavily_search import TavilySearchResults

# 设置API密钥
os.environ['OPENAI_API_KEY'] = 'sk-cdjsim5KBne5thQJ2bF279E94fEa487aA347A7D85747Af10'
os.environ['OPENAI_API_BASE'] = 'https://api.rcouyi.com/v1'
os.environ['TAVILY_API_KEY'] = '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'
# 添加LangChain追踪配置
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = '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'


# 定义分析状态
class AnalysisState(TypedDict):
    company: str
    company_keywords: str
    report: str
    search_results: Dict[str, Any]
    messages: Annotated[list[AnyMessage], add_messages]

# 定义搜索节点
async def search_node(state: AnalysisState):
    tavily_tool = TavilySearchResults(max_results=5)
    query = f"{state['company']} {state['company_keywords']} 最新动态"
    results = await tavily_tool.ainvoke({"query": query})
    
    return {"search_results": results, "messages": [AIMessage(content=f"搜索完成，找到 {len(results)} 条结果。")]}  # Changed here

# 定义分析模型
async def analysis_model(state: AnalysisState):
    prompt = f"""今天的日期是 {datetime.now().strftime('%Y年%m月%d日')}。
您是一位专业的研究员，负责分析投资组合公司的最近发展，以编写周报。
您当前的任务是分析以下公司在过去一周发生的重大事件：{state['company']}。
用户提供了以下公司关键词来帮助您进行分析：{state['company_keywords']}。

以下是搜索到的相关信息：
{state['search_results']}

**指示：**
- 基于搜索结果和您对该公司和行业的了解，分析重要事件
- 考虑公司的主要业务领域、市场趋势和行业动态
- 如果您认为已经进行了充分的分析，请说"我已经完成初步分析，准备继续下一步。"
"""
    
    print(prompt)
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    
    return {"messages": [response]}

# 定义报告撰写函数
def write_report(state: AnalysisState):
    prompt = f"""今天的日期是 {datetime.now().strftime('%Y年%m月%d日')}。
您是一位专业的研究员，正在撰写关于投资组合公司最近事件的周报。
您的任务是使用Markdown语法为以下公司撰写一份深入、详细的报告：{state['company']}。
请基于您之前的分析和搜索结果撰写报告。

请确保您的报告：
1. 概述公司的最新发展和重要事件
2. 分析这些事件对公司的潜在影响
3. 提供对公司未来发展的见解
4. 使用适当的标题和子标题组织信息
5. 在报告中引用搜索结果作为信息来源
"""
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    
    # 生成文件名
    filename = f"{state['company']}_{datetime.now().strftime('%Y%m%d')}_report.md"
    
    # 将报告写入本地文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.content)
    
    return {
        "messages": [AIMessage(content=f"生成的报告已保存到文件：{filename}\n\n报告内容:\n{response.content}")],
        "report": response.content
    }

# 定义图
workflow = StateGraph(AnalysisState)

# 添加节点
workflow.add_node("search", search_node)
workflow.add_node("analysis", analysis_model)
workflow.add_node("writer", write_report)

# 设置入口点
workflow.set_entry_point("search")

# 添加边
workflow.add_edge("search", "analysis")
workflow.add_edge("analysis", "writer")
workflow.add_edge("writer", END)

# 编译图
app = workflow.compile()

# 运行分析
async def run_analysis(company, company_keywords):
    messages = [
        SystemMessage(content="您是一位专业的研究员，准备开始分析公司信息。")
    ]
    async for s in app.astream({"company": company, "company_keywords": company_keywords, "messages": messages}, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
            if "生成的报告已保存到文件" in message.content:
                print("\n" + message.content.split("\n")[0])  # 打印文件保存信息

if __name__ == "__main__":
    company = "腾讯"
    company_keywords = "游戏"
    
    asyncio.run(run_analysis(company, company_keywords))
