import os
import asyncio
from typing import TypedDict, Annotated, List
from datetime import datetime

from langchain_core.messages import AnyMessage, AIMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, add_messages
import subprocess

# 设置API密钥
os.environ['OPENAI_API_KEY'] = 'sk-cdjsim5KBne5thQJ2bF279E94fEa487aA347A7D85747Af10'
os.environ['OPENAI_API_BASE'] = 'https://api.rcouyi.com/v1'
os.environ['TAVILY_API_KEY'] = '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'
# 添加LangChain追踪配置
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = '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'

# 修改操作状态，添加用户确认字段
class OperationState(TypedDict):
    user_input: str
    kubectl_commands: List[str]
    user_confirmation: bool
    execution_results: List[str]
    messages: Annotated[list[AnyMessage], add_messages]
    command_explanations: List[str]

# 定义命令生成节点
async def generate_commands(state: OperationState):
    prompt = f"""今天的日期是 {datetime.now().strftime('%Y年%m月%d日')}。
您是一位Kubernetes专家,精通kubectl命令。请根据用户的输入生成相应的kubectl命令。
用户输入: {state['user_input']}

请生成一个或多个kubectl命令来完成用户的请求。每个命令应该单独列出,并使用以下格式:
COMMAND: <kubectl命令>
EXPLANATION: <命令的简短解释>

如果您需要更多信息来生成准确的命令,请说明您需要什么信息。
"""
    
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    
    # 从响应中提取kubectl命令
    commands = []
    explanations = []
    lines = response.content.split('\n')
    for i in range(0, len(lines), 2):
        if i+1 < len(lines) and lines[i].startswith("COMMAND:") and lines[i+1].startswith("EXPLANATION:"):
            command = lines[i].replace("COMMAND:", "").strip()
            explanation = lines[i+1].replace("EXPLANATION:", "").strip()
            commands.append(command)
            explanations.append(explanation)
    
    return {
        "kubectl_commands": commands,
        "command_explanations": explanations,
        "messages": [response]
    }

# 修改用户确认节点
async def user_confirmation(state: OperationState):
    print("生成的kubectl命令:")
    for i, (command, explanation) in enumerate(zip(state['kubectl_commands'], state['command_explanations']), 1):
        print(f"{i}. 命令: {command}")
        print(f"   解释: {explanation}\n")
    
    confirmation = input("是否执行这些命令？(y/n): ").lower().strip()
    confirmed = confirmation == 'y'
    return {
        "user_confirmation": confirmed,
        "messages": [HumanMessage(content=f"用户{'确认' if confirmed else '拒绝'}执行命令。")]
    }

# 修改命令执行节点
async def execute_commands(state: OperationState):
    if not state['user_confirmation']:
        return {
            "execution_results": ["用户取消了命令执行。"],
            "messages": [AIMessage(content="命令执行被用户取消。")],
            "end_execution": True
        }
    
    results = []
    for command in state['kubectl_commands']:
        # 去除命令两端可能存在的反引号
        command = command.strip('`')
        try:
            print(f"执行命令: {command}")  # 添加这行来显示正在执行的命令
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            output = result.stdout.strip()
            if output:
                results.append(f"命令 '{command}' 执行成功:\n{output}")
            else:
                results.append(f"命令 '{command}' 执行成功,但没有输出。")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() if e.stderr else str(e)
            results.append(f"命令 '{command}' 执行失败:\n{error_message}")
        except Exception as e:
            results.append(f"执行命令 '{command}' 时发生未知错误:\n{str(e)}")
    
    print("执行结果:")  # 添加这行来显示执行结果
    for result in results:
        print(result)
    
    return {
        "execution_results": results,
        "messages": [AIMessage(content="命令执行完成。以下是执行结果:\n" + "\n".join(results))],
        "end_execution": False
    }

# 新增结束节点
async def end_execution(state: OperationState):
    return {"messages": [AIMessage(content="操作已结束。")]}

# 定义结果解释节点
async def interpret_results(state: OperationState):
    prompt = f"""作为Kubernetes专家,请解释以下kubectl命令的执行结果:

用户原始输入: {state['user_input']}

执行的命令和结果:
{' '.join(state['execution_results'])}

请提供一个简洁明了的解释,使非技术用户也能理解操作的结果和影响。如果有任何错误或警告,请解释其可能的原因和解决方法。
"""
    
    messages = state['messages'] + [SystemMessage(content=prompt)]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = model.invoke(messages)
    
    return {"messages": [response]}

# 定义图
workflow = StateGraph(OperationState)

# 添加节点
workflow.add_node("generate", generate_commands)
workflow.add_node("confirm", user_confirmation)
workflow.add_node("execute", execute_commands)
workflow.add_node("interpret", interpret_results)
workflow.add_node("end", end_execution)  # 新增结束节点

# 设置入口点
workflow.set_entry_point("generate")

# 添加边
workflow.add_edge("generate", "confirm")
workflow.add_conditional_edges(
    "confirm",
    lambda x: "execute" if x["user_confirmation"] else "end"
)
workflow.add_conditional_edges(
    "execute",
    lambda x: "end" if x.get("end_execution") else "interpret"
)
workflow.add_edge("interpret", "end")
workflow.add_edge("end", END)

# 编译图
app = workflow.compile()

# 修改运行操作函数
async def run_k8s_operation(user_input: str):
    initial_state = {
        "user_input": user_input, 
        "messages": [SystemMessage(content="您是一位Kubernetes专家,准备协助用户进行Kubernetes操作。")],
        "user_confirmation": False,
        "kubectl_commands": [],
        "command_explanations": [],
        "execution_results": []
    }
    
    async for s in app.astream(initial_state, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

# 修改主函数
if __name__ == "__main__":
    while True:
        user_input = input("请描述您想在Kubernetes集群上执行的操作 (输入'退出'结束程序): ")
        if user_input.lower() in ['退出', 'exit', 'quit']:
            print("程序已退出。")
            break
        asyncio.run(run_k8s_operation(user_input))
        print("\n" + "="*50 + "\n")  # 添加分隔线
