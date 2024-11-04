# HTTP API 连通性检测与智能分析工具

## 1. 项目概述

**目标**：实现一个智能 HTTP API 连通性检测工具，自动检查给定 URL 的状态。如果返回状态不是 200，则进行多维度分析并使用 AI 提供专业的故障诊断和解决方案。

**技术栈**：
- Python
- 命令行工具（curl、nslookup、ping 等）
- OpenAI API / Azure OpenAI API
- LangChain（用于 AI 分析）

---

## 2. 功能模块

### 2.1 基础检测模块
1. **HTTP 请求检测**
   - 使用 requests 库发送 HTTP 请求
   - 检查返回状态码
   - 记录响应时间和头信息

2. **DNS 检查**
   - 检查域名解析
   - 验证 DNS 配置

3. **网络连通性检查**
   - Ping 测试
   - TCP 连接测试

4. **端口检查**
   - 检查指定端口开放状态
   - 支持 HTTP(80) 和 HTTPS(443)

5. **SSL/TLS 检查**
   - 证书有效性验证
   - SSL 配置检查

### 2.2 AI 分析模块（新增）

1. **检测结果分析**
   - 收集所有检测数据
   - 构建结构化的分析报告
   - 识别潜在问题点

2. **智能诊断**
   - 使用 LLM 分析检测结果
   - 提供专业的技术诊断
   - 生成可能的故障原因

3. **解决方案生成**
   - 基于诊断结果提供解决方案
   - 按优先级排序建议
   - 提供具体的操作步骤

4. **历史数据分析**
   - 记录历史检测数据
   - 分析故障模式和趋势
   - 提供预防性建议

---

## 3. AI 分析流程

### 3.1 数据收集与预处理
```python
{
    "url": "https://example.com",
    "timestamp": "2024-01-01 12:00:00",
    "checks": {
        "http_status": {"success": true, "message": "...", "details": {...}},
        "dns": {"success": true, "message": "...", "details": {...}},
        "ping": {"success": false, "message": "...", "details": {...}},
        "port": {"success": true, "message": "...", "details": {...}},
        "ssl": {"success": true, "message": "...", "details": {...}}
    }
}
```

### 3.2 AI 分析提示模板
```
系统：你是一个专业的网络诊断专家，请分析以下 API 连通性检测报告并提供专业诊断。

检测报告：
{detailed_report}

请提供：
1. 问题概述
2. 详细原因分析
3. 建议的解决方案（按优先级排序）
4. 预防措施
```

### 3.3 输出格式
```json
{
    "summary": "简要问题描述",
    "analysis": {
        "root_cause": "根本原因",
        "affected_components": ["组件1", "组件2"],
        "severity": "严重程度"
    },
    "solutions": [
        {
            "priority": 1,
            "description": "解决方案描述",
            "steps": ["步骤1", "步骤2"]
        }
    ],
    "prevention": [
        "预防建议1",
        "预防建议2"
    ]
}
```

---

## 4. 实现细节

### 4.1 AI 分析器类
```python
class ConnectivityAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.llm = OpenAI(api_key=api_key)
        self.model = model
        
    def analyze_report(self, check_results: dict) -> dict:
        # 构建分析提示
        # 调用 AI 进行分析
        # 格式化输出结果
        pass
```

### 4.2 结果处理
- 生成结构化的 JSON 报告
- 支持 Markdown 格式的可读性报告
- 可选的 HTML 报告生成

### 4.3 历史记录
- 保存检测和分析结果
- 支持查询历史记录
- 趋势分析功能

---

## 5. 使用示例

```bash
# 基础检查
python -m connect_check https://api.example.com

# 带 AI 分析的完整检查
python -m connect_check https://api.example.com --analyze

# 生成详细报告
python -m connect_check https://api.example.com --analyze --report pdf
```

---

## 6. 配置项

```yaml
ai:
  provider: "openai"  # or "azure"
  api_key: "your-api-key"
  model: "gpt-3.5-turbo"
  temperature: 0.7

analysis:
  max_history: 100
  report_format: "markdown"
  save_path: "./reports"

logging:
  level: "INFO"
  file: "connectivity_check.log"
```

---

## 7. 输出示例

```markdown
# API 连通性分析报告

## 检测结果
- HTTP 状态: ✓ 200 OK
- DNS 解析: ✓ 正常
- Ping 测试: ✗ 超时
- 端口检查: ✓ 443端口开放
- SSL 证书: ✓ 有效

## AI 诊断
### 问题概述
检测发现目标服务器禁用了 ICMP 协议，导致 ping 测试失败。

### 原因分析
服务器可能出于安全考虑禁用了 ICMP 协议，这是一种常见的安全实践。

### 解决方案
1. 确认是否为安全策略要求
2. 如需启用 ICMP，请检查防火墙配置
3. 考虑使用其他方式进行存活性检测

### 预防建议
- 建立服务器配置文档
- 实施监控告警机制
- 定期进行连通性测试
```

---

## 8. 后续优化

1. 支持更多检测项
2. 添加并发检测能力
3. 实现 Web 界面
4. 支持自定义检测规则
5. 添加告警通知功能
6. 支持更多 AI 模型