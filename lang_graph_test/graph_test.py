import os
import logging
import random
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import AnyMessage, AIMessage, SystemMessage, HumanMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, add_messages

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置环境变量
os.environ['OPENAI_API_KEY'] = 'sk-cdjsim5KBne5thQJ2bF279E94fEa487aA347A7D85747Af10'
os.environ['OPENAI_API_BASE'] = 'https://api.rcouyi.com/v1'

# 定义状态
class ConversationState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    color: str

# 定义路由节点
def router(state: ConversationState):
    logging.info("进入路由节点")
    prompt = """分析用户输入的情绪倾向。如果情绪偏消极,回复"negative"。如果情绪偏积极,回复"positive"。只回复"negative"或"positive"。"""
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    logging.info(f"路由节点分析结果: {response.content}")
    return {"messages": [response]}

# 定义黑色节点
def black_node(state: ConversationState):
    logging.info("进入黑色节点")
    happy_emojis = ["😊", "😄", "😃", "😁", "😆", "😍", "🥰", "😎", "🤗", "🌈", "🌞", "✨", "🎉", "🎈"]
    chosen_emoji = random.choice(happy_emojis)
    response_content = f"看起来你可能心情不太好。希望这个表情能让你开心起来: {chosen_emoji}"
    logging.info(f"黑色节点回复: {response_content}")
    return {"messages": [AIMessage(content=response_content)], "color": "black"}

# 定义白色节点
def white_node(state: ConversationState):
    logging.info("进入白色节点")
    prompt = """用户的情绪偏积极。给出一个赞美和鼓励的回复。"""
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    logging.info(f"白色节点回复: {response.content}")
    return {"messages": [response], "color": "white"}

# 定义路由决策函数
def route_decision(state: ConversationState) -> Literal["black", "white"]:
    last_message = state['messages'][-1].content.strip().lower()
    if last_message == "negative":
        logging.info("路由决策: 选择黑色节点")
        return "black"
    elif last_message == "positive":
        logging.info("路由决策: 选择白色节点")
        return "white"
    else:
        logging.error(f"无效的路由响应: {last_message}")
        raise ValueError("Invalid router response")

# 定义图
workflow = StateGraph(ConversationState)

# 添加节点
workflow.add_node("router", router)
workflow.add_node("black", black_node)
workflow.add_node("white", white_node)

# 设置入口点
workflow.set_entry_point("router")

# 添加条件边
workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "black": "black",
        "white": "white"
    }
)

# 添加结束边
workflow.add_edge("black", END)
workflow.add_edge("white", END)

# 编译图
app = workflow.compile()

# 运行对话
async def run_conversation(user_input: str):
    logging.info(f"用户输入: {user_input}")
    messages = [HumanMessage(content=user_input)]
    async for s in app.astream({"messages": messages, "color": ""}, stream_mode="values"):
        if "color" in s and s["color"]:
            # logging.info(f"最终颜色: {s['color']}")
            print(f"Final color: {s['color']}")
        for message in s["messages"]:
            if isinstance(message, AIMessage):
                # logging.info(f"AI回复: {message.content}")
                print(f"AI: {message.content}")

# 主函数
if __name__ == "__main__":
    import asyncio
    
    user_input = input("请输入您的消息: ")
    asyncio.run(run_conversation(user_input))
