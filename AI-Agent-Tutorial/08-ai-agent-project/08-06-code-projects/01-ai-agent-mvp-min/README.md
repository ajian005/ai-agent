# AI Agent MVP-MIN

最小可工作的 CLI 编码 Agent。6 个源文件，~350 行 TypeScript，支持 Anthropic / 阿里云千问 / DeepSeek 等多模型。

## 快速开始
cd AI-Agent-Tutorial/08-ai-agent-project/08-06-code-projects/01-ai-agent-mvp-min


```bash
# 1. 安装依赖
pnpm install
or
npm install


# 2. 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 3. 启动
pnpm start
or
npm start

```

## 配置模型

编辑 `.env` 文件切换 LLM 提供商：

**阿里云千问（默认）**：
```bash
AGENT_PROVIDER=qwen
AGENT_MODEL=qwen-max
AGENT_API_KEY=sk-your-dashscope-key
```

**Anthropic Claude**：
```bash
AGENT_PROVIDER=anthropic
AGENT_MODEL=claude-sonnet-4-20250514
AGENT_API_KEY=sk-ant-your-key
```

**DeepSeek**：
```bash
AGENT_PROVIDER=deepseek
AGENT_MODEL=deepseek-chat
AGENT_API_KEY=sk-your-deepseek-key
```

**其他 OpenAI 兼容模型**：
```bash
AGENT_PROVIDER=custom
AGENT_MODEL=your-model-id
AGENT_API_KEY=your-key
AGENT_BASE_URL=https://api.your-provider.com/v1
```

## 功能

- 流式 ReAct 循环（感知 -> 推理 -> 行动 -> 观察）
- 3 个核心工具：读取文件、写入文件、执行命令
- 命令执行需用户确认（Y/n）
- 安全规则：禁止 rm -rf、禁止读写 .env
- 多模型切换：通过环境变量一键切换

## 命令

| 命令 | 功能 |
|------|------|
| `/exit` | 退出 |
| `/clear` | 清空对话历史 |
| `/help` | 显示帮助 |

## 使用示例

```
You: 读取 package.json 的内容
Agent: [调用 read_file] ...

You: 在 scripts 中添加 "build": "tsc"
Agent: [调用 read_file] → [调用 write_file] ...

You: 运行 npm test
Agent: [调用 run_command] → 确认? (Y/n)
```

## 项目结构

```
src/
├── index.ts       # CLI 入口（交互循环）
├── agent.ts       # 核心 ReAct 循环引擎
├── provider.ts    # LLM 提供商创建（多模型切换）
├── tools.ts       # 3 个工具（read_file / write_file / run_command）
├── prompt.ts      # 系统提示词模板
└── security.ts    # 安全检查 + 用户确认
```

## 设计文档

- [MVP-MIN 技术落地方案](../../08-05-domain-design/mvp-min-implementation.md)
- [领域设计](../../08-05-domain-design/domain-design.md)
- [架构方案](../../08-04-system-architecture/ai-agent-general-design-v0.3.md)
