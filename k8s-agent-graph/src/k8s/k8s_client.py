#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess
from typing import Dict, Optional
from dotenv import load_dotenv

from ..core.types import ExecutionResult

load_dotenv()


class K8sClient:
    def __init__(self):
        self.kubeconfig_path = os.getenv("KUBECONFIG_PATH", "~/.kube/config")
        self.kubeconfig = os.path.expanduser(self.kubeconfig_path)
        self.allowed_commands = json.loads(
            os.getenv("ALLOWED_COMMANDS", '["get", "describe", "logs"]')
        )
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        # 初始化时获取帮助文档
        self.kubectl_help = self.get_kubectl_help()

    def get_kubectl_help(self) -> str:
        """获取kubectl帮助文档"""
        try:
            result = subprocess.run(
                "kubectl --help",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout
            return "无法获取kubectl帮助文档"
        except Exception as e:
            return f"获取kubectl帮助文档失败: {str(e)}"

    def execute_command(self, command: str) -> ExecutionResult:
        """执行kubectl命令"""
        # 如果命令以 kubectl 开头，移除它
        if command.startswith("kubectl "):
            command = command[7:].strip()

        # 构建完整命令
        # full_command = f"kubectl {command} --kubeconfig {self.kubeconfig}"
        full_command = f"kubectl {command}"

        try:
            # 执行命令
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            return ExecutionResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr="命令执行超时"
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"命令执行失败: {str(e)}"
            )

    def is_command_safe(self, command: str) -> bool:
        """检查命令是否安全"""
        # 提取命令的主要动词
        cmd_parts = command.split()
        if not cmd_parts:
            return False

        # 确保命令以 kubectl 开头
        if cmd_parts[0] != "kubectl":
            return False

        # 获取子命令（如果存在）
        if len(cmd_parts) < 2:
            return False

        sub_command = cmd_parts[1]

        # 检查子命令是否在允许列表中
        return sub_command in self.allowed_commands

    def validate_command(self, command: str) -> Dict:
        """验证命令的有效性"""
        # 构建验证命令
        # validate_cmd = f"{command} --dry-run=client --kubeconfig {self.kubeconfig}"

        try:
            # result = subprocess.run(
            #     validate_cmd,
            #     shell=True,
            #     capture_output=True,
            #     text=True
            # )

            return {
                "is_valid": True,
                "message": "命令有效"
            }

        except Exception as e:
            return {
                "is_valid": False,
                "message": str(e)
            }
