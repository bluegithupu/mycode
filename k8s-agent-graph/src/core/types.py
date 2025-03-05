from typing import TypedDict, Optional, Dict, List
from pydantic import BaseModel


class CommandAnalysis(BaseModel):
    command: str
    description: str
    safety_level: str


class SafetyCheck(BaseModel):
    is_safe: bool
    reason: Optional[str] = None


class ValidationResult(BaseModel):
    is_valid: bool
    message: str


class ExecutionResult(BaseModel):
    success: bool
    stdout: str
    stderr: str


class ResultAnalysis(BaseModel):
    status: str
    analysis: str
    suggestions: str


class AgentState(TypedDict):
    """工作流状态定义"""
    # 输入状态
    user_input: str
    kubectl_help: str

    # 处理状态
    command_analysis: Optional[CommandAnalysis]
    safety_check: Optional[SafetyCheck]
    validation_result: Optional[ValidationResult]
    execution_result: Optional[ExecutionResult]
    result_analysis: Optional[ResultAnalysis]

    # 错误状态
    error: Optional[str]

    # 元数据
    metadata: Dict

    # 重试相关
    retry_count: Optional[int]
    max_retries: Optional[int]
