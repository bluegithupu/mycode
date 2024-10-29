import os
import logging
from typing import List, Optional, TypedDict, Union, Dict, Any
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ValidationNode
from langgraph.graph import StateGraph, END, add_messages
import json
from pydantic import ValidationError

# 设置日志和API
logging.basicConfig(level=logging.INFO)
os.environ['OPENAI_API_KEY'] = 'sk-cdjsim5KBne5thQJ2bF279E94fEa487aA347A7D85747Af10'
os.environ['OPENAI_API_BASE'] = 'https://api.rcouyi.com/v1'

class MessageState(TypedDict):
    messages: List[AnyMessage]
    attempt_count: int
    encoded_input: Dict[str, Any]
    message_count: int
    current_output: Optional[Dict[str, Any]]

class ResponseFormat(BaseModel):
    """定义响应格式"""
    content: str = Field(description="回复的主要内容")
    sentiment: str = Field(description="情感倾向分析 (positive/negative/neutral)")
    confidence: float = Field(description="置信度 (0-1)", ge=0, le=1)

def encode_input(state: MessageState) -> MessageState:
    """将输入消息编码为结构化格式"""
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""
    
    encoded = {
        "raw_input": last_message,
        "timestamp": "current_time",
        "format_version": "1.0"
    }
    
    return {
        **state,
        "encoded_input": encoded
    }

def count_messages(state: MessageState) -> MessageState:
    """计算消息数量"""
    return {
        **state,
        "message_count": len(state["messages"])
    }

def llm_node(state: MessageState) -> MessageState:
    """LLM处理节点"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = state["messages"]
    
    # 添加系统提示
    system_prompt = """请分析用户输入并提供结构化输出，包含以下内容：
    1. 主要回复内容
    2. 情感倾向分析
    3. 置信度评分
    请确保输出符合ResponseFormat格式。
    """
    
    messages = [SystemMessage(content=system_prompt)] + messages
    response = llm.invoke(messages)
    
    return {
        **state,
        "messages": state["messages"] + [response],
        "attempt_count": state.get("attempt_count", 0) + 1
    }

def validation_node(state: MessageState) -> Union[MessageState, str]:
    """验证输出是否符合预期格式"""
    try:
        last_message = state["messages"][-1].content
        # 尝试解析输出为ResponseFormat
        parsed_response = ResponseFormat.parse_raw(last_message)
        state["current_output"] = parsed_response.dict()
        return state
    except (ValidationError, json.JSONDecodeError) as e:
        if state["attempt_count"] >= 3:
            return "fallback"
        return state

def fallback_node(state: MessageState) -> MessageState:
    """当验证失败时的后备处理"""
    fallback_response = ResponseFormat(
        content="抱歉，我无法正确处理您的请求。",
        sentiment="neutral",
        confidence=0.5
    )
    
    return {
        **state,
        "current_output": fallback_response.dict()
    }

def finalizer_node(state: MessageState) -> MessageState:
    """最终处理节点"""
    return state

def decode_output(state: MessageState) -> Dict[str, Any]:
    """将输出解码为最终格式"""
    if not state.get("current_output"):
        return {"error": "No valid output generated"}
    
    return {
        "result": state["current_output"],
        "message_count": state["message_count"],
        "attempts": state["attempt_count"]
    }

def create_graph() -> StateGraph:
    """创建工作流图"""
    workflow = StateGraph(MessageState)
    
    # 添加所有节点
    workflow.add_node("encode_input", encode_input)
    workflow.add_node("count_messages", count_messages)
    workflow.add_node("llm", llm_node)
    workflow.add_node("validator", validation_node)
    workflow.add_node("fallback", fallback_node)
    workflow.add_node("finalizer", finalizer_node)
    workflow.add_node("decode", decode_output)
    
    # 设置入口点
    workflow.set_entry_point("encode_input")
    
    # 添加边
    workflow.add_edge("encode_input", "count_messages")
    workflow.add_edge("count_messages", "llm")
    workflow.add_edge("llm", "validator")
    workflow.add_edge("validator", "finalizer")
    workflow.add_edge("fallback", "finalizer")
    workflow.add_edge("finalizer", "decode")
    workflow.add_edge("decode", END)
    
    # 添加条件边
    workflow.add_conditional_edges(
        "validator",
        lambda x: "fallback" if isinstance(x, str) and x == "fallback" else "finalizer",
        {
            "fallback": "fallback",
            "finalizer": "finalizer"
        }
    )
    
    return workflow.compile()

async def run_conversation(user_input: str):
    """运行对话"""
    app = create_graph()
    
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "attempt_count": 0,
        "encoded_input": {},
        "message_count": 0,
        "current_output": None
    }
    
    async for state in app.astream(initial_state):
        if "current_output" in state and state["current_output"]:
            print(f"输出: {json.dumps(state['current_output'], ensure_ascii=False, indent=2)}")

if __name__ == "__main__":
    import asyncio
    
    user_input = input("请输入您的问题: ")
    asyncio.run(run_conversation(user_input)) 