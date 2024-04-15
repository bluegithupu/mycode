#使用 Python f 字符串模板：
from langchain.prompts import PromptTemplate
fstring_template = """Tell me a {adjective} joke about {content}"""
prompt = PromptTemplate.from_template(fstring_template)
print(prompt.format(adjective="funny", content="chickens"))




#ChatPromptTemplate.from_messages 接受各种消息表示形式。
from langchain.prompts import ChatPromptTemplate
template = ChatPromptTemplate.from_messages([
("system", "You are a helpful AI bot. Your name is {name}."),
("human", "Hello, how are you doing?"),
("ai", "I'm doing well, thanks!"),
("human", "{user_input}"),
])
messages = template.format_messages(
name="Bob",
user_input="What is your name?"
)
print(messages)


#模型调用
from langchain.llms import OpenAI
llm = OpenAI()
print(llm('你是谁'))





#fake model call
# 从langchain.llms.fake模块导入FakeListLLM类，此类可能用于模拟或伪造某种行为
from langchain.llms.fake import FakeListLLM
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

# 调用load_tools函数，加载"python_repl"的工具
tools = load_tools(["python_repl"])
# 定义一个响应列表，这些响应可能是模拟LLM的预期响应
responses = ["Action: Python REPL\nAction Input: print(2 + 2)", "Final Answer: 4"]
# 使用上面定义的responses初始化一个FakeListLLM对象
llm = FakeListLLM(responses=responses)
# 调用initialize_agent函数，使用上面的tools和llm，以及指定的代理类型和verbose参数来初始化一个代理
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
# 调用代理的run方法，传递字符串"whats 2 + 2"作为输入，询问代理2加2的结果
agent.run("whats 2 + 2")




#chain

from langchain import PromptTemplate, OpenAI, LLMChain

prompt_template = "What is a good name for a company that makes {product}?"

llm = OpenAI(temperature=0)
chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template)
)
print(chain("colorful socks")) 