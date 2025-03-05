#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Annotated
import traceback
from langgraph.graph import StateGraph, END
from .types import AgentState, ChatMessage, ChatSession
from ..k8s.k8s_client import K8sClient
from ..llm.llm_client import LLMClient
from ..utils.logger import setup_logger

# 初始化客户端和日志记录器
k8s_client = K8sClient()
llm_client = LLMClient()
logger = setup_logger("workflow")


def log_state(state: AgentState, node_name: str) -> None:
    """记录当前状态信息"""
    logger.debug(f"节点 [{node_name}] 的状态: {state}")


def analyze_command(state: AgentState) -> AgentState:
    """分析用户输入，生成kubectl命令"""
    logger.info("开始分析用户输入...")
    try:
        user_input = state["user_input"]
        chat_session = state.get("chat_session")

        # 构建完整的输入上下文
        context_parts = []

        # 添加历史命令和结果信息
        if chat_session:
            if chat_session.last_command:
                context_parts.append(f"上一次执行的命令: {chat_session.last_command}")

            if chat_session.last_result:
                result_text = chat_session.last_result.stdout if chat_session.last_result.success else chat_session.last_result.stderr
                context_parts.append(
                    f"上一次执行结果: {'成功' if chat_session.last_result.success else '失败'}")
                context_parts.append(f"输出内容: {result_text[:200]}...")  # 限制输出长度

            if chat_session.last_analysis:
                context_parts.append(
                    f"上一次分析结果: {chat_session.last_analysis.analysis}")
                if chat_session.last_analysis.suggestions:
                    context_parts.append(
                        f"改进建议: {chat_session.last_analysis.suggestions}")

            # 添加最近的对话历史
            if chat_session.messages:
                recent_messages = []
                for msg in chat_session.messages[-4:]:  # 只取最近4条消息
                    if msg.role == "user":
                        recent_messages.append(f"用户: {msg.content}")
                    else:
                        # 对助手消息进行简化，只保留关键信息
                        content = msg.content.split(
                            '\n')[0] if '\n' in msg.content else msg.content
                        recent_messages.append(f"助手: {content}")
                if recent_messages:
                    context_parts.append("最近的对话:")
                    context_parts.extend(recent_messages)

        # 构建完整输入
        if context_parts:
            full_input = "历史上下文:\n" + \
                "\n".join(context_parts) + "\n\n当前输入:\n" + user_input
        else:
            full_input = user_input

        logger.debug(f"完整输入上下文: {full_input}")
        command_analysis = llm_client.analyze_command(
            full_input,
            state["kubectl_help"]
        )
        logger.info(f"命令分析完成: {command_analysis}")
        result_state = {"command_analysis": command_analysis}
        log_state(result_state, "analyze_command")
        return result_state
    except KeyError as e:
        error_msg = f"缺少必要的状态键: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"命令分析失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"error": error_msg}


def check_safety(state: AgentState) -> AgentState:
    """检查命令安全性"""
    logger.info("开始安全性检查...")
    try:
        command = state["command_analysis"].command
        logger.debug(f"检查命令安全性: {command}")
        is_safe = k8s_client.is_command_safe(command)
        result_state = {
            "safety_check": {
                "is_safe": is_safe,
                "reason": None if is_safe else "命令不在允许列表中"
            }
        }
        logger.info(f"安全检查结果: {'通过' if is_safe else '未通过'}")
        log_state(result_state, "check_safety")
        return result_state
    except KeyError as e:
        error_msg = f"缺少必要的状态键: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"安全检查失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"error": error_msg}


def validate_command(state: AgentState) -> AgentState:
    """验证命令有效性"""
    logger.info("开始验证命令...")
    try:
        command = state["command_analysis"].command
        logger.debug(f"验证命令: {command}")
        result = k8s_client.validate_command(command)
        logger.info(f"命令验证结果: {result}")
        result_state = {"validation_result": result}
        log_state(result_state, "validate_command")
        return result_state
    except KeyError as e:
        error_msg = f"缺少必要的状态键: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"命令验证失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"error": error_msg}


def execute_command(state: AgentState) -> AgentState:
    """执行命令"""
    logger.info("开始执行命令...")
    try:
        command = state["command_analysis"].command
        logger.debug(f"执行命令: {command}")
        result = k8s_client.execute_command(command)
        logger.info(f"命令执行完成，状态: {'成功' if result.success else '失败'}")
        result_state = {"execution_result": result}
        log_state(result_state, "execute_command")
        return result_state
    except KeyError as e:
        error_msg = f"缺少必要的状态键: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"命令执行失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"error": error_msg}


def analyze_result(state: AgentState) -> AgentState:
    """分析执行结果"""
    logger.info("开始分析执行结果...")
    try:
        command = state["command_analysis"].command
        result = state["execution_result"]
        output = result.stdout if result.success else result.stderr
        logger.debug(f"分析命令输出: {output[:200]}...")  # 只记录前200个字符
        analysis = llm_client.analyze_result(command, output)
        logger.info("结果分析完成")
        result_state = {"result_analysis": analysis}
        log_state(result_state, "analyze_result")
        return result_state
    except KeyError as e:
        error_msg = f"缺少必要的状态键: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"结果分析失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"error": error_msg}


def should_execute(state: AgentState) -> str:
    """决定是否执行命令"""
    logger.debug("开始检查执行条件...")
    logger.debug(f"完整状态: {state}")

    # 检查错误
    if state.get("error"):
        logger.warning(f"检测到错误，终止执行: {state['error']}")
        return "end"

    # 检查安全结果
    safety_check = state.get("safety_check", {})
    logger.debug(f"安全检查状态: {safety_check}")
    if not safety_check:
        logger.warning("未找到安全检查结果，终止执行")
        return "end"
    if not safety_check.get("is_safe"):
        logger.warning(f"安全检查未通过，原因: {safety_check.get('reason')}")
        return "end"
    logger.info("安全检查通过")

    # 检查验证结果
    validation_result = state.get("validation_result", {})
    logger.debug(f"验证状态: {validation_result}")
    if not validation_result:
        logger.warning("未找到验证结果，终止执行")
        return "end"
    if not validation_result.get("is_valid"):
        logger.warning(f"命令验证未通过，原因: {validation_result.get('message')}")
        return "end"
    logger.info("命令验证通过")

    logger.info("所有检查通过，继续执行")
    return "execute"


def should_retry(state: AgentState) -> str:
    """决定是否需要重试"""
    logger.debug("检查是否需要重试...")

    # 获取结果分析
    result_analysis = state.get("result_analysis")
    if not result_analysis:
        logger.warning("未找到结果分析，终止执行")
        return "end"

    # 检查执行状态
    if result_analysis.status != "error":
        logger.info("执行成功或警告，无需重试")
        return "end"

    # 检查重试次数
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)

    if retry_count >= max_retries:
        logger.warning(f"已达到最大重试次数 {max_retries}，终止执行")
        return "end"

    logger.info(f"准备进行第 {retry_count + 1} 次重试")
    return "retry"


def prepare_retry(state: AgentState) -> AgentState:
    """准备重试状态"""
    logger.info("准备重试状态...")
    try:
        # 增加重试计数
        retry_count = state.get("retry_count", 0) + 1

        # 获取原始用户输入和建议
        original_input = state.get("user_input", "")
        suggestions = state.get("result_analysis").suggestions
        analysis = state.get("result_analysis").analysis

        # 构建新的用户输入
        new_input = f"{original_input}\n[重试 {retry_count}] 根据建议: {suggestions}\n[分析结果] {analysis}"

        # 更新状态
        return {
            "user_input": new_input,
            "kubectl_help": state["kubectl_help"],
            "retry_count": retry_count,
            "max_retries": state.get("max_retries", 3)
        }
    except Exception as e:
        error_msg = f"准备重试状态失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"error": error_msg}


def handle_followup(state: AgentState) -> AgentState:
    """处理追问"""
    logger.info("开始处理追问...")
    try:
        # 获取用户输入和会话状态
        user_input = state["user_input"]
        chat_session = state["chat_session"]

        # 生成回答
        try:
            answer = llm_client.answer_followup(
                user_input,
                chat_session.last_command,
                chat_session.last_result,
                chat_session.last_analysis
            )
        except Exception as e:
            logger.error(f"生成回答失败: {str(e)}")
            answer = "抱歉，我暂时无法回答这个问题。请稍后再试或换个方式提问。"

        # 更新会话状态
        chat_session.messages.append(
            ChatMessage(role="user", content=user_input))
        chat_session.messages.append(
            ChatMessage(role="assistant", content=answer))

        return {
            "chat_session": chat_session,
            "followup_answer": answer
        }

    except Exception as e:
        error_msg = f"处理追问失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"error": error_msg}


def update_chat_session(state: AgentState) -> AgentState:
    """更新会话状态"""
    logger.info("开始更新会话状态...")
    try:
        # 获取当前状态
        user_input = state["user_input"]
        command_analysis = state.get("command_analysis")
        execution_result = state.get("execution_result")
        result_analysis = state.get("result_analysis")

        # 获取或创建会话
        chat_session = state.get("chat_session") or ChatSession(messages=[])

        # 更新会话状态
        chat_session.last_command = command_analysis.command if command_analysis else None
        chat_session.last_result = execution_result
        chat_session.last_analysis = result_analysis

        # 添加消息记录
        chat_session.messages.append(
            ChatMessage(role="user", content=user_input))

        # 构建助手回复
        if command_analysis and result_analysis:
            try:
                assistant_content = (
                    f"命令: {command_analysis.command}\n"
                    f"分析: {result_analysis.analysis}\n"
                    f"建议: {result_analysis.suggestions}"
                )
            except Exception as e:
                logger.error(f"构建助手回复失败: {str(e)}")
                assistant_content = "抱歉，处理结果时出现错误。请重试或换个方式提问。"
        else:
            assistant_content = "抱歉，无法处理这个命令。请重试或换个方式提问。"

        chat_session.messages.append(
            ChatMessage(role="assistant", content=assistant_content))

        return {"chat_session": chat_session}

    except Exception as e:
        error_msg = f"更新会话状态失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return {"error": error_msg}


def create_workflow() -> StateGraph:
    """创建工作流图"""
    logger.info("开始创建工作流...")
    try:
        # 创建工作流
        workflow = StateGraph(AgentState)

        # 添加节点
        workflow.add_node("analyze", analyze_command)
        workflow.add_node("check_safety", check_safety)
        workflow.add_node("validate", validate_command)
        workflow.add_node("execute", execute_command)
        workflow.add_node("analyze_result", analyze_result)
        workflow.add_node("prepare_retry", prepare_retry)
        workflow.add_node("update_chat_session", update_chat_session)
        workflow.add_node("handle_followup", handle_followup)

        # 设置边和条件
        workflow.add_edge("analyze", "check_safety")
        workflow.add_edge("check_safety", "validate")

        workflow.add_conditional_edges(
            "validate",
            should_execute,
            {
                "execute": "execute",
                "end": END
            }
        )

        workflow.add_edge("execute", "analyze_result")
        workflow.add_edge("analyze_result", "update_chat_session")

        # workflow.add_conditional_edges(
        #     "analyze_result",
        #     should_retry,
        #     {
        #         "retry": "prepare_retry",
        #         "end": END
        #     }
        # )

        workflow.add_edge("prepare_retry", "analyze")
        workflow.add_edge("handle_followup", END)

        # 设置入口
        workflow.set_entry_point("analyze")

        logger.info("工作流创建完成")
        return workflow.compile()

    except Exception as e:
        error_msg = f"工作流创建失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise
