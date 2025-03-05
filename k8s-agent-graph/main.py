#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt

from src.core.nodes import create_workflow, k8s_client
from src.core.types import ChatSession
from src.utils.logger import setup_logger

# 设置日志记录器
logger = setup_logger("k8s_agent_cli")
console = Console()


@click.group()
def cli():
    """K8s-Agent: Kubernetes运维助手 (LangGraph版本)"""
    logger.info("K8s-Agent CLI启动")
    pass


@cli.command()
def version():
    """显示版本信息"""
    logger.info("显示版本信息")
    console.print(Panel(
        Text("K8s-Agent v0.2.0 (LangGraph)", style="bold green"),
        title="版本信息",
        border_style="blue"
    ))


@cli.command()
@click.argument('command')
def run(command):
    """执行Kubernetes运维命令"""
    asyncio.run(_run_async(command))


@cli.command()
def chat():
    """进入交互式对话模式"""
    console.print(Panel(
        Text("进入交互式对话模式\n输入 exit 退出", style="bold blue"),
        title="K8s-Agent Chat",
        border_style="blue"
    ))

    # 创建会话
    chat_session = ChatSession(messages=[])

    while True:
        try:
            # 获取用户输入
            user_input = Prompt.ask("\n[bold blue]>>[/bold blue]")

            # 检查是否退出
            if user_input.lower() == "exit":
                console.print("[bold blue]再见！[/bold blue]")
                break

            # 执行命令
            asyncio.run(_run_async(user_input, chat_session))

        except KeyboardInterrupt:
            console.print("\n[bold blue]再见！[/bold blue]")
            break
        except Exception as e:
            logger.exception("对话过程中发生错误")
            console.print(Panel(
                Text(str(e), style="bold red"),
                title="错误",
                border_style="red"
            ))


async def _run_async(command: str, chat_session: ChatSession = None):
    """异步执行Kubernetes运维命令"""
    logger.info(f"接收到命令执行请求: {command}")
    try:
        # 创建工作流
        workflow = create_workflow()

        # 准备初始状态
        initial_state = {
            "user_input": command,
            "kubectl_help": k8s_client.kubectl_help,
            "metadata": {},
            "error": None,
            "chat_session": chat_session
        }

        # 执行工作流
        logger.debug("开始执行工作流...")
        result = await workflow.ainvoke(initial_state)

        if result.get("error"):
            logger.error(f"工作流执行失败: {result['error']}")
            console.print(Panel(
                Text(result["error"], style="bold red"),
                title="执行失败",
                border_style="red"
            ))
            return

        # 如果是追问，显示回答
        if result.get("followup_answer"):
            logger.info("显示追问回答")
            console.print(Panel(
                Text(result["followup_answer"], style="bold green"),
                title="回答",
                border_style="blue"
            ))
            return

        # 显示命令信息
        logger.info("显示命令执行信息")
        command_analysis = result["command_analysis"]
        console.print(Panel(
            Text(
                f"命令: {command_analysis.command}\n描述: {command_analysis.description}",
                style="bold blue"
            ),
            title="命令信息",
            border_style="blue"
        ))

        # 显示执行结果
        execution_result = result.get("execution_result")
        if execution_result and execution_result.stdout:
            logger.debug("显示命令输出")
            console.print(Panel(
                Text(execution_result.stdout, style="green"),
                title="执行输出",
                border_style="green"
            ))

        # 显示分析结果
        if result.get("result_analysis"):
            logger.debug("显示分析结果")
            analysis = result["result_analysis"]
            table = Table(title="分析结果")
            table.add_column("项目", style="cyan")
            table.add_column("内容", style="yellow")

            table.add_row("状态", analysis.status)
            table.add_row("分析", analysis.analysis)
            table.add_row("建议", analysis.suggestions)

            console.print(table)

        logger.info("命令执行完成")

    except Exception as e:
        error_message = f"发生错误: {str(e)}"
        logger.exception(error_message)
        console.print(Panel(
            Text(error_message, style="bold red"),
            title="错误",
            border_style="red"
        ))


if __name__ == '__main__':
    cli()
