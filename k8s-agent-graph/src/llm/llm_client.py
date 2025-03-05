#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
from typing import Dict, Optional

from openai import OpenAI
from dotenv import load_dotenv
from ..core.types import CommandAnalysis, ResultAnalysis, ExecutionResult

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

        注意:
        1. 对于get类命令,未明确namespace的用户输入,默认使用 --all-namespaces 参数,并使用grep命令来筛查，eg： kubectl get pods --all-namespaces | grep "[pod_name]"

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

    def is_followup_question(self, user_input: str, last_command: str, last_analysis: Optional[ResultAnalysis]) -> bool:
        """判断是否为追问"""
        prompt = f"""
        判断用户的输入是否是对上一个命令结果的追问。

        上一个命令: {last_command}
        上一次分析: {last_analysis.analysis if last_analysis else 'None'}
        用户输入: {user_input}

        直接返回 true 或 false，不要包含其他内容。
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的对话分类器，负责判断用户输入是否为追问。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0
            )

            content = response.choices[0].message.content.strip().lower()
            return content == "true"

        except Exception as e:
            raise Exception(f"LLM API调用失败: {str(e)}")

    def answer_followup(self, user_input: str, last_command: str, last_result: Optional[ExecutionResult], last_analysis: Optional[ResultAnalysis]) -> str:
        """回答追问"""
        prompt = f"""
        作为Kubernetes运维专家，请回答用户的追问。

        上一个命令: {last_command}
        命令输出: {last_result.stdout if last_result and last_result.stdout else 'None'}
        上一次分析: {last_analysis.analysis if last_analysis else 'None'}
        用户追问: {user_input}

        请提供专业、详细的回答。回答应该：
        1. 直接针对用户的问题
        2. 基于上下文提供具体解释
        3. 如果需要，可以建议下一步操作

        不要返回JSON格式，直接返回自然语言回答。
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个Kubernetes运维专家，负责回答用户的追问。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"LLM API调用失败: {str(e)}")
