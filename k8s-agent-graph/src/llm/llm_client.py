#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
from typing import Dict, Optional

from openai import OpenAI
from dotenv import load_dotenv
from ..core.types import CommandAnalysis, ResultAnalysis

load_dotenv()


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found in environment variables")

        self.client = OpenAI(
            api_key="sk-l3WytTQtQnrtrXINA22c07C3Ba694d87A3F0B218Bc7509F1",
            base_url=self.base_url if self.base_url else None
        )

    def _clean_json_response(self, content: str) -> str:
        """清理LLM响应中的Markdown格式，提取JSON内容"""
        # 移除可能的代码块标记
        content = re.sub(r'^```\w*\n', '', content)
        content = re.sub(r'\n```$', '', content)
        # 确保内容是一个有效的JSON字符串
        content = content.strip()
        return content

    def analyze_command(self, user_input: str, kubectl_help: str) -> CommandAnalysis:
        """分析用户输入，生成kubectl命令"""
        prompt = f"""
        作为一个Kubernetes运维专家，请分析以下用户需求，并生成相应的kubectl命令。
        请参考以下kubectl帮助文档来确保生成的命令是正确的：

        {kubectl_help}

        直接返回一个JSON对象（不要包含markdown格式），格式如下：
        {{
            "command": "具体的kubectl命令",
            "description": "命令说明",
            "safety_level": "安全等级(safe/medium/risky)"
        }}
        
        用户需求: {user_input}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个Kubernetes运维专家，负责生成安全的kubectl命令。直接返回JSON对象，不要使用markdown格式。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            content = response.choices[0].message.content.strip()
            content = self._clean_json_response(content)
            data = json.loads(content)
            return CommandAnalysis(**data)

        except Exception as e:
            raise Exception(f"LLM API调用失败: {str(e)}")

    def analyze_result(self, command: str, result: str) -> ResultAnalysis:
        """分析命令执行结果"""
        prompt = f"""
        分析以下kubectl命令的执行结果，并提供专业的分析和建议。
        直接返回一个JSON对象（不要包含markdown格式），格式如下：
        {{
            "status": "执行状态(success/warning/error)",
            "analysis": "结果分析",
            "suggestions": "改进建议"
        }}
        
        命令: {command}
        结果: {result}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个Kubernetes运维专家，负责分析命令执行结果。直接返回JSON对象，不要使用markdown格式。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            content = response.choices[0].message.content.strip()
            content = self._clean_json_response(content)
            data = json.loads(content)
            return ResultAnalysis(**data)

        except Exception as e:
            raise Exception(f"LLM API调用失败: {str(e)}")
