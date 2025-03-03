#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from typing import Dict, Optional
from functools import wraps

from ..k8s.k8s_client import K8sClient
from ..llm.llm_client import LLMClient
from ..utils.logger import setup_logger

# 设置日志记录器
logger = setup_logger("k8s_agent")


def log_execution_time(func):
    """函数执行时间装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} 执行完成，耗时: {execution_time:.2f}秒")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"{func.__name__} 执行失败，耗时: {execution_time:.2f}秒，错误: {str(e)}")
            raise
    return wrapper


class CommandProcessor:
    def __init__(self):
        logger.info("初始化CommandProcessor")
        try:
            self.llm_client = LLMClient()
            self.k8s_client = K8sClient()
            logger.info("CommandProcessor初始化成功")
        except Exception as e:
            logger.error(f"CommandProcessor初始化失败: {str(e)}")
            raise

    @log_execution_time
    def process_command(self, user_input: str) -> Dict:
        """处理用户输入的命令"""
        logger.info(f"开始处理命令: {user_input}")
        try:
            # 1. 使用LLM分析用户输入
            logger.debug("正在分析用户输入...")
            command_data = self.llm_client.analyze_command(user_input)
            logger.info(
                f"命令分析结果: {json.dumps(command_data, ensure_ascii=False)}")

            # 2. 验证命令安全性
            if command_data["safety_level"] == "risky":
                logger.warning(f"命令安全级别过高: {command_data['command']}")
                return {
                    "success": False,
                    "message": "命令风险等级过高，已拒绝执行",
                    "analysis": command_data
                }

            # 3. 执行命令
            logger.info(f"开始执行命令: {command_data['command']}")
            execution_result = self.k8s_client.execute_command(
                command_data["command"])

            if execution_result["success"]:
                logger.info("命令执行成功")
                logger.debug(f"执行输出: {execution_result['stdout']}")
            else:
                logger.error(f"命令执行失败: {execution_result['stderr']}")

            # 4. 分析执行结果
            logger.debug("正在分析执行结果...")
            result_analysis = self.llm_client.analyze_result(
                command_data["command"],
                execution_result["stdout"] if execution_result["success"] else execution_result["stderr"]
            )
            logger.info("结果分析完成")

            return {
                "success": execution_result["success"],
                "command": command_data["command"],
                "description": command_data["description"],
                "execution_result": execution_result,
                "analysis": result_analysis
            }

        except Exception as e:
            logger.exception(f"命令处理过程中发生错误: {str(e)}")
            return {
                "success": False,
                "message": f"处理失败: {str(e)}"
            }
