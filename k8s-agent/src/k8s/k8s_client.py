#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess
from typing import Dict, Optional

from dotenv import load_dotenv

load_dotenv()


class K8sClient:
    def __init__(self):
        kubeconfig_path = os.getenv("KUBECONFIG_PATH", "~/.kube/config")
        self.kubeconfig = os.path.expanduser(kubeconfig_path)
        self.allowed_commands = json.loads(
            os.getenv("ALLOWED_COMMANDS", '["get", "describe", "logs"]'))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))

    def execute_command(self, command: str) -> Dict:
        """执行kubectl命令"""
        # 验证命令安全性
        if not self._is_command_safe(command):
            raise ValueError("命令不在允许列表中")

        # 如果命令以 kubectl 开头，移除它
        if command.startswith("kubectl "):
            command = command[7:].strip()

        # 构建完整命令
        full_command = f"kubectl {command} --kubeconfig {self.kubeconfig}"

        try:
            # 执行命令
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired:
            raise TimeoutError("命令执行超时")
        except Exception as e:
            raise Exception(f"命令执行失败: {str(e)}")

    def _is_command_safe(self, command: str) -> bool:
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
        print(
            f"检查命令安全性: command={command}, parts={cmd_parts}, sub_command={sub_command}, allowed_commands={self.allowed_commands}")

        # 检查子命令是否在允许列表中
        return sub_command in self.allowed_commands

    def validate_command(self, command: str) -> Dict:
        """验证命令的有效性"""
        # 构建验证命令
        validate_cmd = f"kubectl {command} --dry-run=client --kubeconfig {self.kubeconfig}"

        try:
            result = subprocess.run(
                validate_cmd,
                shell=True,
                capture_output=True,
                text=True
            )

            return {
                "valid": result.returncode == 0,
                "message": result.stdout if result.returncode == 0 else result.stderr
            }

        except Exception as e:
            return {
                "valid": False,
                "message": str(e)
            }
