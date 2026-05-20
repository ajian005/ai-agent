# ai-agent

## ai-agent-simplest

本目录用**最少代码**演示「对话 + 工具循环 + LLM」的 AI Agent 骨架，并说明如何从玩具脚本**逐步进化**到接近 **Claude Code**、**OpenClaw** 一类「在真实仓库里干活」的编程 Agent。

更完整的目录说明与进化路线见 [ai-agent-simplest/README.md](ai-agent-simplest/README.md)；原理（三循环、CoT/ToT、与代码对照）见 [ai-agent-simplest.md](ai-agent-simplest/ai-agent-simplest.md)。

### 文件一览

| 文件 | 说明 |
|------|------|
| [minimal_agent.py](ai-agent-simplest/minimal_agent.py) | 最小可运行示例：双工具、自定义 `tool:` 文本协议、环境变量配置 |
| [simple-claude-code.py](ai-agent-simplest/simple-claude-code.py) | 读/列/编辑文件的「类 Claude Code」极简骨架 |
| [langchain_claude_code.py](ai-agent-simplest/langchain_claude_code.py) | LangChain 封装同一思路 |
| [langgraph_claude_code.py](ai-agent-simplest/langgraph_claude_code.py) | LangGraph 封装同一思路 |
| [test_claude_agent_sdk.py](ai-agent-simplest/test_claude_agent_sdk.py) | Claude Agent SDK 示例 |
| [deep_agent_claude_code.py](ai-agent-simplest/deep_agent_claude_code.py) | 更深一层编排示例（规划、记忆或多步分解） |
| [requirements.txt](ai-agent-simplest/requirements.txt) | Python 依赖 |
| [.env.example](ai-agent-simplest/.env.example) | 环境变量模板（如 `ANTHROPIC_API_KEY`） |
| [README.md](ai-agent-simplest/README.md) | 最小 Agent 五块组成、进化阶段、与 Claude Code/OpenClaw 对照 |
| [ai-agent-simplest.md](ai-agent-simplest/ai-agent-simplest.md) | 工作原理：人机对话 / Agent / LLM 三循环、ReAct、CoT/ToT |

### 最小 Agent 五块（对照代码）

| 部分 | 作用 | 对应文件 |
|------|------|----------|
| 对话状态 | `system` + 多轮 `user` / `assistant`，工具结果写回上下文 | `minimal_agent.py`、`simple-claude-code.py` |
| 工具协议 | 单行 `tool: name({JSON})` 或厂商原生 function calling | 各 `.py` 示例 |
| 工具注册与执行 | 名字 → 函数，解析参数并返回结果 | `TOOL_REGISTRY` 等 |
| 双循环 | 外层人机多轮；内层「LLM → 工具 → 再 LLM」直到本轮结束 | `run_*_loop` |
| LLM 客户端 | 单次 `messages.create` 等 API 调用 | `execute_llm_call` 等 |

### 快速开始

```bash
cd ai-agent-simplest
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入 ANTHROPIC_API_KEY
python minimal_agent.py
```

## AI-Agent-Tutorial

### 01-ai-agent-tutotial

[01-AI Agent（智能体） 教程.md](AI-Agent-Tutorial/01-ai-agent-tutorial/01-AI%20Agent(智能体)%20教程.md)

[02-AI Agent 简介.md](AI-Agent-Tutorial/01-ai-agent-tutorial/02-AI%20Agent%20简介.md)

[03-AI Agent 核心组件.md](AI-Agent-Tutorial/01-ai-agent-tutorial/03-AI%20Agent%20核心组件.md)

[04-AI Agent 工作原理.md](AI-Agent-Tutorial/01-ai-agent-tutorial/04-AI%20Agent%20工作原理.md)

[05-大语言模型基础(LLM).md](AI-Agent-Tutorial/01-ai-agent-tutorial/05-大语言模型基础(LLM).md)

[06-提示词工程(PromptEngineering).md](AI-Agent-Tutorial/01-ai-agent-tutorial/06-提示词工程(PromptEngineering).md)

### 02-ai-agent-tools

[01-第一个 AI Agent.md](AI-Agent-Tutorial/02-ai-agent-tools/01-第一个 AI Agent.md)

[02-01-OpenClaw (Clawdbot) 教程.md](AI-Agent-Tutorial/02-ai-agent-tools/02-01-OpenClaw (Clawdbot) 教程.md)

[02-02-OpenClaw 一键部署.md](AI-Agent-Tutorial/02-ai-agent-tools/02-02-OpenClaw 一键部署.md)

[02-03-RoxyBrowser(openclaw)教程.md](AI-Agent-Tutorial/02-ai-agent-tools/02-03-RoxyBrowser(openclaw)教程.md)

[02-04-Manus(开源)智能体教程.md](AI-Agent-Tutorial/02-ai-agent-tools/02-04-Manus(开源)智能体教程.md)

[03-CrewAI 制作智能体.md](AI-Agent-Tutorial/02-ai-agent-tools/03-CrewAI 制作智能体.md)

[04-LangChain 制作智能体.md](AI-Agent-Tutorial/02-ai-agent-tools/04-LangChain 制作智能体.md)

[05-Claude Code入门教程.md](AI-Agent-Tutorial/02-ai-agent-tools/05-Claude Code入门教程.md)

[0X-AI软件开发工具 ai-code-tools](https://github.com/ajian005/ai-code-tools)

[06-OpenCode 入门教程.md](AI-Agent-Tutorial/02-ai-agent-tools/06-OpenCode 入门教程.md)

[07-Agent Skills教程(含ClaudeCode Skills).md](AI-Agent-Tutorial/02-ai-agent-tools/07-Agent Skills教程(含ClaudeCode Skills).md)

[07-Agent Skills开放标准.md](AI-Agent-Tutorial/02-ai-agent-tools/07-Agent Skills开放标准.md)

[08-OpenCode Skills.md](AI-Agent-Tutorial/02-ai-agent-tools/08-OpenCode Skills.md)

[09-Qoder CLI.md](AI-Agent-Tutorial/02-ai-agent-tools/09-Qoder CLI.md)

[10-Trae Solo.md](AI-Agent-Tutorial/02-ai-agent-tools/10-Trae Solo.md)

[11-Google Gemini CLI.md](AI-Agent-Tutorial/02-ai-agent-tools/11-Google Gemini CLI.md)

[12-OpenAI CodeX.md](AI-Agent-Tutorial/02-ai-agent-tools/12-OpenAI CodeX.md)

### 03-ai-agent-develop 智能体开发

[01-Python 实现 AI Agent.md](AI-Agent-Tutorial/03-ai-agent-develop/01-Python 实现 AI Agent.md)

[02-工具调用（Function Calling）.md](AI-Agent-Tutorial/03-ai-agent-develop/02-工具调用（Function Calling）.md)

[03-记忆系统.md](AI-Agent-Tutorial/03-ai-agent-develop/03-记忆系统.md)

[04-Python 智能体环境配置.md](AI-Agent-Tutorial/03-ai-agent-develop/04-Python 智能体环境配置.md)

[05-AI Agent 问答实例.md](AI-Agent-Tutorial/03-ai-agent-develop/05-AI Agent 问答实例.md)

### 04-ai-agent-skills 智能体技能

[0-software-engineering-agent-skills-guilde-by-role](AI-Agent-Tutorial/04-ai-agent-skills/0-software-engineering-agent-skills-guilde-by-role)

[claude-code-skills](AI-Agent-Tutorial/04-ai-agent-skills/claude-code-skills)

[trae-skills](AI-Agent-Tutorial/04-ai-agent-skills/trae-skills)

## Claude-Project

Claude Code 能力与工作流配置文档、Agent SDK 示例。

| 文件 | 说明 |
|------|------|
| [Claude-Code全能力操作手册.md](Claude-Project/Claude-Code全能力操作手册.md) | 官方能力 + Skills/Workflows/Plugins/Hooks/MCP/Agents/Commands 索引 |
| [Claude-Code-AI工作流配置指南-20260409-1710.md](Claude-Project/Claude-Code-AI工作流配置指南-20260409-1710.md) | 全局/项目级配置、Skills、Hooks、跨会话记忆、双 IDE 协作 |
| [test_claude_agent_sdk.py](Claude-Project/test_claude_agent_sdk.py) | `claude_agent_sdk` 异步 `query` 示例 |

相关教程：[05-Claude Code入门教程.md](AI-Agent-Tutorial/02-ai-agent-tools/05-Claude%20Code入门教程.md)、[claude-code-skills](AI-Agent-Tutorial/04-ai-agent-skills/claude-code-skills)

---

## LangChain

LangChain Python **How-to guides** 学习与示例（约 100+ 个 `.py`），对照 [官方文档](https://python.langchain.com/docs/how_to/)。目录索引见 [LangChain.md](LangChain/LangChain.md)。

### 目录结构

| 路径 | 说明 |
|------|------|
| `chap001_*` / `chap002_*` / `chap003_*` | 入门：OpenAI 工具调用、流式、调试、多模型 |
| [howToGuide_Components_*](LangChain/) | 组件示例（见下表） |
| [howToGuide_keyFeature_*](LangChain/) | 结构化输出、工具调用、调试等关键能力 |
| [UseCases/](LangChain/UseCases/) | RAG、SQL/图数据库问答、抽取链、聊天机器人等完整用例 |
| [LangChain_1.0_demo.py](LangChain/LangChain_1.0_demo.py) | LangChain 1.0 综合演示 |

### 组件示例（`howToGuide_Components_*`）

| 前缀 | 主题 |
|------|------|
| `Agents_*` | Legacy Agent / 迁移到 LangGraph |
| `ChatModels_*` | 模型初始化、流式、工具调用、结构化输出、缓存 |
| `LLMs_*` | 自定义 LLM、本地模型、Token 统计 |
| `PromptTemplate_*` / `ExampleSelectors_*` | 提示词、Few-shot |
| `RAG_*` | DocumentLoader、Embedding、VectorStore、Retriever、Index、TextSplitters |
| `OutputParser_*` / `Callbacks_*` / `Custom_*` | 解析器、回调、自定义组件 |
| `Messages_*` / `Multimodal_*` | 消息合并、多模态 |

相关教程：[04-LangChain 制作智能体.md](AI-Agent-Tutorial/02-ai-agent-tools/04-LangChain%20制作智能体.md)

---

## LangChain-DeepAgents

基于 [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/quickstart) 的编排示例（`deepagents` + 搜索等工具）。

| 文件 | 说明 |
|------|------|
| [QuickStart_DeepAgent.py](LangChain-DeepAgents/QuickStart_DeepAgent.py) | 快速开始：Tavily 搜索 + `create_deep_agent` |
| [QuickStart_DeepAgent_Customization001.py](LangChain-DeepAgents/QuickStart_DeepAgent_Customization001.py) | 自定义 Deep Agent |
| [CoreCapabilities_AgentHarness.py](LangChain-DeepAgents/CoreCapabilities_AgentHarness.py) | Agent Harness 核心能力 |

同思路极简版：[deep_agent_claude_code.py](ai-agent-simplest/deep_agent_claude_code.py)

---

## LangGraph

LangGraph **工作流与 Agent** 示例：入门、自定义图、预置 Agent、生产与 Studio。

### 目录结构

| 路径 | 说明 |
|------|------|
| [GetStarted/](LangGraph/GetStarted/) | 入门、自定义工作流（状态/工具/记忆/人机协同/时间旅行）、工作流模式（路由/并行/编排者-工作者等） |
| [Guides/](LangGraph/Guides/) | Agent 开发、Graph/Functional API、持久化、流式、子图、中断、Studio、生产结构 |
| [LangGraphAppDir/](LangGraph/LangGraphAppDir/) | 可部署应用模板（`my-LangGraph-App-001`、`Studio-App-002`） |

### 代表性文件

| 文件 | 说明 |
|------|------|
| [LangGraph_GetStarted_001.py](LangGraph/GetStarted/LangGraph_GetStarted_001.py) | 入门 |
| [LangGraph_StartWithAPrebuiltAgent_002.py](LangGraph/GetStarted/LangGraph_StartWithAPrebuiltAgent_002.py) | 预置 Agent |
| [LangGraph_BuildACustomWorkflow_003*.py](LangGraph/GetStarted/) | 自定义工作流系列 |
| [LangGraph_WorkflowsAndAgents_005*.py](LangGraph/GetStarted/) | 工作流与 Agent 模式（Graph API） |
| [LangGraph_AgentArchitectures_006.md](LangGraph/GetStarted/LangGraph_AgentArchitectures_006.md) | Router / ReAct / Plan-and-Execute 等架构说明 |
| [LangGraph_1.0_Demo.py](LangGraph/Guides/LangGraph_1.0_Demo.py) | LangGraph 1.0 演示 |
| [my-LangGraph-App-001/README.md](LangGraph/LangGraphAppDir/my-LangGraph-App-001/README.md) | 标准应用脚手架 |

相关教程：[04-LangChain 制作智能体.md](AI-Agent-Tutorial/02-ai-agent-tools/04-LangChain%20制作智能体.md)（含 LangGraph 迁移）

---

## LLAMAINDEX-RAG

使用 **LlamaIndex** 构建本地 RAG 知识库（Embedding + 向量检索 + Web 问答）。

| 文件 | 说明 |
|------|------|
| [readme.md](LLAMAINDEX-RAG/readme.md) | 环境、模型下载、建库与 Web 应用步骤 |
| [llamaindex_RAG.py](LLAMAINDEX-RAG/llamaindex_RAG.py) | RAG 主流程 |
| [llamaindex_internlm.py](LLAMAINDEX-RAG/llamaindex_internlm.py) | InternLM 直连问答对比 |
| [app.py](LLAMAINDEX-RAG/app.py) | Web 应用入口 |
| [download_hf.py](LLAMAINDEX-RAG/download_hf.py) / [download_internlm1.8_chat.py](LLAMAINDEX-RAG/download_internlm1.8_chat.py) | 模型下载脚本 |
| [data/](LLAMAINDEX-RAG/data/) | 知识库文档（如 `RAG.md`） |
| [requirements.txt](LLAMAINDEX-RAG/requirements.txt) | Python 依赖 |

```bash
cd LLAMAINDEX-RAG
conda create -n rag python=3.10 && conda activate rag
pip install -r requirements.txt
```

---

## Spring-AI-Alibaba-Java

Java 侧 **Spring AI Alibaba** 学习索引（链接至 [java2ai.com](https://java2ai.com/docs) 官方教程）。

| 文件 | 说明 |
|------|------|
| [使用教程_基础框架.md](Spring-AI-Alibaba-Java/使用教程_基础框架.md) | ChatModel/ChatClient、RAG、MCP、Tool Calling、Graph 编排等文档索引 |

涵盖：核心对话与提示词、RAG/向量存储、MCP 客户端与服务端、可观测性与评估、**Spring AI Alibaba Graph** 工作流。

---

## CrewAI

仓库内暂无独立 `CrewAI/` 代码目录；教程与概念见 AI-Agent-Tutorial：

| 文档 | 说明 |
|------|------|
| [03-CrewAI 制作智能体.md](AI-Agent-Tutorial/02-ai-agent-tools/03-CrewAI%20制作智能体.md) | 多 Agent 角色协作、Crew/Process 编排入门 |

---

## OpenClaw

仓库内暂无独立 `OpenClaw/` 代码目录；平台能力与配置见教程：

| 文档 | 说明 |
|------|------|
| [02-01-OpenClaw (Clawdbot) 教程.md](AI-Agent-Tutorial/02-ai-agent-tools/02-01-OpenClaw%20(Clawdbot)%20教程.md) | OpenClaw / Clawdbot 入门 |
| [02-02-OpenClaw 一键部署.md](AI-Agent-Tutorial/02-ai-agent-tools/02-02-OpenClaw%20一键部署.md) | 部署 |
| [02-03-RoxyBrowser(openclaw)教程.md](AI-Agent-Tutorial/02-ai-agent-tools/02-03-RoxyBrowser(openclaw)教程.md) | 托管浏览器与 MCP 自动化 |

对照：[ai-agent-simplest](ai-agent-simplest/) 中「进化到 Claude Code / OpenClaw」；官方 [OpenClaw 文档](https://docs.openclaw.ai/)

---

## Hermes

待补充（仓库内暂无 `Hermes/` 目录与示例代码）。

---

## 其他

| 路径 | 说明 |
|------|------|
| [moltbook/moltbook_skill.md](moltbook/moltbook_skill.md) | Moltbook 面向 AI Agent 的社交网络 Skill 说明 |

---

Large Language Model Agent: A Survey on Methodology, Applications and Challenges