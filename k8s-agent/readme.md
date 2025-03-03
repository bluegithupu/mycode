# K8s-Agent

K8s-Agent 是一个基于大语言模型(LLM)和kubectl的Kubernetes运维助手，旨在简化Kubernetes运维工作。系统能够理解用户的自然语言描述，自动规划并执行相应的kubectl命令，分析执行结果，并提供专业的解决方案。

## 功能特点

- 自然语言交互：使用自然语言描述运维需求
- 智能命令生成：自动生成合适的kubectl命令
- 安全执行：内置安全检查机制
- 结果分析：自动分析执行结果并提供建议

## 环境要求

- Python 3.8+
- Kubernetes 1.18+
- kubectl 命令行工具
- OpenAI API 访问权限

## 快速开始

1. 克隆项目
```bash
git clone [项目地址]
cd k8s-agent
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

4. 运行程序
```bash
python main.py
```

## 项目结构

```
k8s-agent/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   ├── llm/               # LLM相关模块
│   ├── k8s/               # Kubernetes操作模块
│   └── utils/             # 工具函数
├── tests/                 # 测试目录
├── docs/                  # 文档目录
├── requirements.txt       # 项目依赖
└── main.py               # 程序入口
```

## 开发计划

- [x] 项目初始化
- [ ] 基础框架搭建
- [ ] 核心功能实现
- [ ] 测试与文档
- [ ] 部署准备

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License
