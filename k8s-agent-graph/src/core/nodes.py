#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Annotated
import traceback
from langgraph.graph import StateGraph, END
from .types import AgentState
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
        logger.debug(f"用户输入: {state.get('user_input')}")
        command_analysis = llm_client.analyze_command(
            state["user_input"],
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

        # 设置边和条件
        workflow.add_edge("analyze", "check_safety")
        workflow.add_edge("check_safety", "validate")

        # 添加条件路由
        workflow.add_conditional_edges(
            "validate",
            should_execute,
            {
                "execute": "execute",
                "end": END
            }
        )

        workflow.add_edge("execute", "analyze_result")
        workflow.add_edge("analyze_result", END)

        # 设置入口
        workflow.set_entry_point("analyze")

        logger.info("工作流创建完成")
        return workflow.compile()
    except Exception as e:
        error_msg = f"工作流创建失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise
