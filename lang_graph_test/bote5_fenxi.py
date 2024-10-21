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
    industry: str
    search_results: Dict[str, Any]
    messages: Annotated[list[AnyMessage], add_messages]

# 定义搜索节点
async def search_node(state: AnalysisState):
    tavily_tool = TavilySearchResults(max_results=5)
    queries = [
        f"{state['company']} 行业竞争",
        f"{state['industry']} 新进入者威胁",
        f"{state['industry']} 替代品威胁",
        f"{state['company']} 供应商议价能力",
        f"{state['company']} 客户议价能力"
    ]
    results = []
    for query in queries:
        results.extend(await tavily_tool.ainvoke({"query": query}))
    
    return {"search_results": results, "messages": [AIMessage(content=f"搜索完成，找到 {len(results)} 条结果。")]}

# 定义波特五力分析模型
async def porter_five_forces_model(state: AnalysisState):
    prompt = f"""今天的日期是 {datetime.now().strftime('%Y年%m月%d日')}。
您是一位专业的战略分析师，负责使用波特五力模型分析公司的竞争环境。
您当前的任务是分析以下公司及其所在行业：{state['company']}（{state['industry']}行业）。

以下是搜索到的相关信息：
{state['search_results']}

**指示：**
请基于搜索结果和您的专业知识，对以下五个方面进行深入分析：
1. 同业竞争者的竞争程度
2. 潜在进入者的威胁
3. 替代品的威胁
4. 供应商的议价能力
5. 购买者的议价能力

对于每个方面，请提供详细的分析和具体的例子。如果您认为已经进行了充分的分析，请说"我已经完成波特五力分析，准备继续下一步。"
"""
    
    print(prompt)
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    
    return {"messages": [response]}

# 定义报告撰写函数
def write_report(state: AnalysisState):
    prompt = f"""今天的日期是 {datetime.now().strftime('%Y年%m月%d日')}。
您是一位专业的战略分析师，正在撰写一份基于波特五力模型的公司竞争环境分析报告。
您的任务是使用Markdown语法为以下公司撰写一份深入、详细的报告：{state['company']}（{state['industry']}行业）。
请基于您之前的波特五力分析和搜索结果撰写报告。

请确保您的报告：
1. 简要介绍公司和行业背景
2. 详细分析五个力量：同业竞争、潜在进入者、替代品、供应商议价能力、购买者议价能力
3. 对每个力量的强度进行评估（高、中、低）
4. 提供对公司战略定位的建议
5. 总结公司在行业中的整体竞争地位
6. 使用适当的标题和子标题组织信息
7. 在报告中引用搜索结果作为信息来源
"""
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    
    # 生成文件名
    filename = f"{state['company']}_波特五力分析_{datetime.now().strftime('%Y%m%d')}.md"
    
    # 将报告写入本地文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.content)
    
    return {
        "messages": [AIMessage(content=f"生成的波特五力分析报告已保存到文件：{filename}\n\n报告内容:\n{response.content}")],
        "report": response.content
    }

# 定义图
workflow = StateGraph(AnalysisState)

# 添加节点
workflow.add_node("search", search_node)
workflow.add_node("analysis", porter_five_forces_model)
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
async def run_analysis(company, industry):
    messages = [
        SystemMessage(content="您是一位专业的战略分析师，准备开始进行波特五力分析。")
    ]
    async for s in app.astream({"company": company, "industry": industry, "messages": messages}, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
            if "生成的波特五力分析报告已保存到文件" in message.content:
                print("\n" + message.content.split("\n")[0])  # 打印文件保存信息

if __name__ == "__main__":
    company = "片仔癀"
    industry = "中药"
    
    asyncio.run(run_analysis(company, industry))
