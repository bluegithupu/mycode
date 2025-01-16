from sqlalchemy import create_engine, text
import json
from data.query import execute_query, get_database_schema_string

# 在tools列表前添加数据库配置
DATABASE_URLS = {
    "chinook": "sqlite:///data/Chinook.db"  # 使用Chinook数据库
}

# 数据库连接池
_engines = {}


def get_db_engine(database):
    """获取数据库连接引擎"""
    if database not in _engines:
        if database not in DATABASE_URLS:
            raise ValueError(f"未知数据库: {database}")
        _engines[database] = create_engine(DATABASE_URLS[database])
    return _engines[database]


# 计算器工具
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "A simple calculator that performs basic arithmetic operations.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate (e.g., '2 + 3 * 4')."
                }
            },
            "required": ["expression"]
        }
    }
}

# 天气查询工具
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather of an location, the user shoud supply a location first",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"]
        },
    }
}

# Tavily搜索工具
tavily_search_tool = {
    "type": "function",
    "function": {
        "name": "tavily_search",
        "description": "Search the internet using Tavily API to get real-time, up-to-date information from across the web.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up information about",
                }
            },
            "required": ["query"]
        }
    }
}

# print(get_database_schema_string())

# 在tools列表前添加SQL查询工具定义
ask_database_tool = {
    "type": "function",
    "function": {
        "name": "ask_database",
        "description": "Use this function to answer user questions about music. Input should be a fully formed SQL query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                            SQL query extracting info to answer the user's question.
                            SQL should be written using this database schema:
                            {get_database_schema_string()}
                            The query should be returned in plain text, not in JSON.
                            """,
                }
            },
            "required": ["query"],
        },
    }
}

# 工具列表
tools = [calculator_tool, weather_tool, tavily_search_tool, ask_database_tool]


def calculator(expression):
    """计算器函数实现"""
    try:
        # 使用 eval 计算表达式,仅支持基本运算
        result = eval(expression)
        return str(result)
    except:
        return "计算错误,请检查表达式格式"


def get_weather(location):
    """天气查询函数实现"""
    # 这里应该调用实际的天气 API,这里只返回模拟数据
    weather_data = {
        "temperature": "25°C",
        "condition": "晴天",
        "humidity": "65%"
    }
    return f"{location}的天气: 温度{weather_data['temperature']}, {weather_data['condition']}, 湿度{weather_data['humidity']}"


def sql_query(query, database="chinook"):
    """SQL查询函数实现"""
    return execute_query(query, database)


def call_tool(tool_name, **params):
    """统一的工具调用接口
    Args:
        tool_name: 工具名称
        params: 工具参数
    Returns:
        工具执行结果
    """
    try:
        if tool_name == "calculator":
            return calculator(params["expression"])
        elif tool_name == "get_weather":
            return get_weather(params["location"])
        elif tool_name == "tavily_search":
            from .tavily_search import tavily_search
            return tavily_search(params["query"])
        elif tool_name == "ask_database":
            return sql_query(params["query"])
        else:
            return f"未找到工具: {tool_name}"
    except Exception as e:
        return f"工具调用出错: {str(e)}"
