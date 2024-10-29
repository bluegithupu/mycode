import os
import logging
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, AIMessage, SystemMessage, HumanMessage
from langchain_core.pydantic_v1 import BaseModel
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
    reflection_needed: bool
    iterations: int
    user_continue: bool

# 定义初始响应节点
def initial_response(state: ConversationState):
    logging.info("进入初始响应节点")
    messages = state['messages']
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    logging.info(f"初始响应: {response.content}")
    
    # 检查响应是否需要反思
    if "不清楚" in response.content or "需要更多信息" in response.content:
        # 如果是请求澄清的回答，就不需要反思
        return {"messages": [response], "reflection_needed": False, "iterations": 0, "user_continue": False}
    return {"messages": [response], "reflection_needed": True, "iterations": 0, "user_continue": False}

# 定义反思节点
def reflection_node(state: ConversationState):
    logging.info("进入反思节点")
    last_response = state['messages'][-1].content
    original_question = state['messages'][0].content
    
    reflection_prompt = f"""原始问题：{original_question}
    原始回答：{last_response}
    
    请从以下几个方面改进回答：
    0. 回答是否存在逻辑漏洞或常识错误
    1. 是否直接回答了用户的问题
    2. 回答是否准确完整
    3. 表达是否清晰简洁
    4. 是否有必要的解释
    
    请直接提供改进后的回答，无需解释改进过程。
    """
    
    messages = [SystemMessage(content=reflection_prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    improved_response = model.invoke(messages)
    logging.info(f"反思后的改进回答: {improved_response.content}")
    
    # 如果改进后的回答与原回答基本相同，就不需要继续反思
    if improved_response.content.strip() == last_response.strip():
        reflection_needed = False
    else:
        reflection_needed = True
    
    return {
        "messages": [AIMessage(content=improved_response.content)],
        "reflection_needed": reflection_needed,
        "iterations": state['iterations'] + 1,
        "user_continue": state['user_continue']
    }

# 定义反思决策函数
def should_reflect(state: ConversationState) -> bool:
    if not state['reflection_needed']:
        return False
    
    if state['iterations'] >= 1:
        # 第一次反思后，询问用户是否继续
        if not state.get('user_continue', False):
            user_input = input("\n是否需要继续改进回答？(y/n): ").lower().strip()
            return user_input == 'y'
    return True

# 定义图
workflow = StateGraph(ConversationState)

# 添加节点
workflow.add_node("initial_response", initial_response)
workflow.add_node("reflection", reflection_node)

# 设置入口点
workflow.set_entry_point("initial_response")

# 添加条件边
workflow.add_conditional_edges(
    "initial_response",
    should_reflect,
    {
        True: "reflection",
        False: END
    }
)

workflow.add_conditional_edges(
    "reflection",
    should_reflect,
    {
        True: "reflection",
        False: END
    }
)

# 编译图
app = workflow.compile()

# 运行对话
async def run_conversation(user_input: str):
    logging.info(f"用户输入: {user_input}")
    messages = [HumanMessage(content=user_input)]
    initial_state = {
        "messages": messages, 
        "reflection_needed": True,
        "iterations": 0,
        "user_continue": False
    }
    
    last_response = None
    async for s in app.astream(initial_state, stream_mode="values"):
        if "messages" in s and s["messages"]:
            current_response = s["messages"][-1].content
            # 只有当响应内容发生变化时才打印
            if current_response != last_response:
                iteration_text = f"(第 {s.get('iterations', 0)} 次反思)" if s.get('iterations', 0) > 0 else ""
                print(f"\nAI {iteration_text}: {current_response}")
                last_response = current_response

# 主函数
if __name__ == "__main__":
    import asyncio
    
    user_input = input("请输入您的问题: ")
    asyncio.run(run_conversation(user_input))
