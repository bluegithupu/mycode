from typing import Dict, Any
import json
from datetime import datetime
import os
from openai import OpenAI
import markdown


class ConnectivityAnalyzer:
    def __init__(self):
        """初始化分析器，使用环境变量中的 API key"""
        self.client = OpenAI(
            api_key="sk-ac431075ac6347eea455c180d4d59217", base_url="https://api.deepseek.com")
        self.model = "deepseek-chat"
        self.temperature = 0.7
        self.save_path = "./reports"
        self.log_file = "connectivity_check.log"

    def _read_recent_logs(self) -> str:
        """读取最近的日志记录"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = f.read().strip()

            # 只获取最近一次检查的日志（通过分隔符分割）
            log_entries = logs.split('-' * 40)
            if log_entries:
                return log_entries[-1].strip()
            return ""
        except Exception:
            return ""

    def _prepare_analysis_prompt(self, check_results: Dict[str, Any]) -> str:
        """准备分析提示"""
        # 获取详细日志
        detailed_logs = self._read_recent_logs()

        # 构建基本检查报告
        report_lines = [
            "# API 连通性检测报告",
            f"\n## 检测URL: {check_results.get('url', 'Unknown')}",
            f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## 检查结果概览:"
        ]

        for check_name, result in check_results.get('checks', {}).items():
            status = "✓" if result['success'] else "✗"
            report_lines.append(
                f"- {check_name}: {status} {result['message']}")

        # 添加详细日志信息
        if detailed_logs:
            report_lines.extend([
                "\n## 详细执行日志:",
                detailed_logs
            ])

        report = "\n".join(report_lines)

        # 构建完整的提示
        prompt = f"""作为网络诊断专家，请分析以下 API 连通性检测报告并提供专业诊断。
报告包含了检查结果概览和详细的执行日志，请仔细分析日志中的具体错误信息。

检测报告：
{report}

请基于检查结果和详细日志，严格按照以下 JSON 格式返回分析结果（确保返回的是有效的 JSON 格式）：

{{
    "summary": "问题概述，包括成功和失败的检查项",
    "analysis": {{
        "root_cause": "根据日志分析得出的根本原因",
        "affected_components": ["受影响的组件"],
        "severity": "严重程度(low/medium/high)",
        "details": "基于日志的详细分析说明"
    }},
    "solutions": [
        {{
            "priority": 1,
            "description": "解决方案描述",
            "steps": ["具体步骤1", "具体步骤2"]
        }}
    ],
    "prevention": ["预防建议1", "预防建议2"]
}}

注意：
1. 请确保返回的是合法的 JSON 格式
2. 不要包含任何其他文本或说明
3. 使用双引号而不是单引号
4. 分析时要充分利用日志中的详细信息"""

        return prompt

    def analyze_report(self, check_results: Dict[str, Any]) -> Dict[str, Any]:
        """分析检查报告并生成诊断结果"""
        prompt = self._prepare_analysis_prompt(check_results)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的网络诊断专家，请用专业的角度分析问题。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )

            # 获取响应内容
            response_content = response.choices[0].message.content.strip()
            
            try:
                # 尝试解析 JSON
                analysis_result = json.loads(response_content)
            except json.JSONDecodeError as je:
                print(f"JSON 解析错误: {str(je)}")
                print(f"原始响应内容: {response_content}")
                return {
                    "error": "Invalid JSON response from AI",
                    "raw_response": response_content,
                    "raw_results": check_results
                }

            self._save_analysis(check_results, analysis_result)
            return analysis_result

        except Exception as e:
            print(f"API 调用错误: {str(e)}")
            return {
                "error": f"AI analysis failed: {str(e)}",
                "raw_results": check_results
            }

    def _save_analysis(self, check_results: Dict[str, Any], analysis: Dict[str, Any]):
        """保存分析结果"""
        os.makedirs(self.save_path, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"analysis_{timestamp}.json"

        with open(os.path.join(self.save_path, filename), 'w', encoding='utf-8') as f:
            json.dump({
                "check_results": check_results,
                "analysis": analysis,
                "timestamp": timestamp
            }, f, ensure_ascii=False, indent=2)

    def generate_report(self, check_results: Dict[str, Any], analysis: Dict[str, Any],
                        format: str = "markdown") -> str:
        """生成格式化的报告"""
        if format == "markdown":
            return self._generate_markdown_report(check_results, analysis)
        elif format == "html":
            return self._generate_html_report(check_results, analysis)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_markdown_report(self, check_results: Dict[str, Any],
                                  analysis: Dict[str, Any]) -> str:
        """生成 Markdown 格式的报告"""
        lines = [
            "# API 连通性分析报告",
            f"\n## 检测URL: {check_results.get('url', 'Unknown')}",
            f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## 检测结果"
        ]

        # 添加检查结果
        for check_name, result in check_results.get('checks', {}).items():
            status = "✓" if result['success'] else "✗"
            lines.append(f"- {check_name}: [{status}] {result['message']}")

        # 添加分析结果
        lines.extend([
            "\n## AI 诊断",
            f"### 问题概述\n{analysis.get('summary', 'N/A')}",
            f"\n### 原因分析",
            f"- 根本原因: {analysis.get('analysis', {}).get('root_cause', 'N/A')}",
            f"- 影响范围: {', '.join(analysis.get('analysis', {}).get('affected_components', []))}",
            f"- 严重程度: {analysis.get('analysis', {}).get('severity', 'N/A')}",
            f"\n- 详细分析:\n  {analysis.get('analysis', {}).get('details', 'N/A')}"
        ])

        # 添加解决方案
        lines.append("\n### 解决方案")
        for solution in analysis.get('solutions', []):
            lines.extend([
                f"\n{solution['priority']}. {solution['description']}",
                "   步骤:",
                *[f"   - {step}" for step in solution['steps']]
            ])

        # 添加预防建议
        lines.extend([
            "\n### 预防建议",
            *[f"- {suggestion}" for suggestion in analysis.get('prevention', [])]
        ])

        return "\n".join(lines)

    def _generate_html_report(self, check_results: Dict[str, Any],
                              analysis: Dict[str, Any]) -> str:
        """生成 HTML 格式的报告"""
        md_content = self._generate_markdown_report(check_results, analysis)
        return markdown.markdown(md_content)
