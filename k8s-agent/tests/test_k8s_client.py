#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from src.k8s.k8s_client import K8sClient


def test_command_safety():
    """测试命令安全性检查"""
    client = K8sClient()

    # 测试安全命令
    assert client._is_command_safe("get pods") == True
    assert client._is_command_safe("describe node") == True

    # 测试不安全命令
    assert client._is_command_safe("delete pod") == False
    assert client._is_command_safe("apply -f") == False


def test_command_validation():
    """测试命令验证"""
    client = K8sClient()

    # 测试有效命令
    result = client.validate_command("get pods")
    assert result["valid"] == True

    # 测试无效命令
    result = client.validate_command("invalid command")
    assert result["valid"] == False


def test_command_execution():
    """测试命令执行"""
    client = K8sClient()

    # 测试安全命令执行
    result = client.execute_command("get pods")
    assert isinstance(result, dict)
    assert "success" in result
    assert "stdout" in result
    assert "stderr" in result

    # 测试不安全命令执行
    with pytest.raises(ValueError):
        client.execute_command("delete pod")
