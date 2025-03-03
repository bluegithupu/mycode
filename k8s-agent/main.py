#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from src.core.processor import CommandProcessor
from src.utils.logger import setup_logger

# 设置日志记录器
logger = setup_logger("k8s_agent_cli")
console = Console()


@click.group()
def cli():
    """K8s-Agent: Kubernetes运维助手"""
    logger.info("K8s-Agent CLI启动")
    pass


@cli.command()
def version():
    """显示版本信息"""
    logger.info("显示版本信息")
    console.print(Panel(
        Text("K8s-Agent v0.1.0", style="bold green"),
        title="版本信息",
        border_style="blue"
    ))


@cli.command()
@click.argument('command')
def run(command):
    """执行Kubernetes运维命令"""
    logger.info(f"接收到命令执行请求: {command}")
    try:
        processor = CommandProcessor()
        logger.debug("开始处理命令...")
        result = processor.process_command(command)

        if not result["success"]:
            error_message = result.get("message") or result.get(
                "execution_result", {}).get("stderr", "未知错误")
            logger.error(f"命令执行失败: {error_message}")
            console.print(Panel(
                Text(error_message, style="bold red"),
                title="执行失败",
                border_style="red"
            ))
            return

        # 显示命令信息
        logger.info("显示命令执行信息")
        console.print(Panel(
            Text(
                f"命令: {result['command']}\n描述: {result['description']}", style="bold blue"),
            title="命令信息",
            border_style="blue"
        ))

        # 显示执行结果
        if result["execution_result"]["stdout"]:
            logger.debug("显示命令输出")
            console.print(Panel(
                Text(result["execution_result"]["stdout"], style="green"),
                title="执行输出",
                border_style="green"
            ))

        # 显示分析结果
        logger.debug("显示分析结果")
        analysis = result["analysis"]
        table = Table(title="分析结果")
        table.add_column("项目", style="cyan")
        table.add_column("内容", style="yellow")

        table.add_row("状态", analysis["status"])
        table.add_row("分析", analysis["analysis"])
        table.add_row("建议", analysis["suggestions"])

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
