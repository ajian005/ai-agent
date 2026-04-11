# 通用 AI Agent 完整设计方案 V0.3

> 基于对 Claude Code、Cursor、OpenAI Codex CLI、Gemini CLI、OpenCode、OpenClaw/OpenHands 六大主流 Agent 的深度分析，综合提示词工程、上下文工程、Harness 工程三大领域研究成果，形成**通用 AI Agent 的统一设计方案**。
>
> 本文档整合 V0.1（核心需求/架构/领域/MVP）与 V0.2（技能/MCP/插件/自动化/搜索）为单一完整版本。

---

## 目录

- [一、跨领域分析总结](#一跨领域分析总结)
- [二、需求方案](#二需求方案)
- [三、架构方案](#三架构方案)
- [四、领域设计（DDD）](#四领域设计ddd)
- [五、MVP 方案与实施路线图](#五mvp-方案与实施路线图)

---

## 一、跨领域分析总结

### 1.1 三大工程支柱

```
提示词工程                上下文工程                Harness 工程
"告诉模型怎么做"          "控制模型看到什么"         "围绕模型构建执行基础设施"

├ 3层提示词架构           ├ 4层上下文管理            ├ 流式 ReAct 循环
├ 多模型适配策略          ├ 3级压缩系统              ├ 工具注册与执行
├ 安全红线设计            ├ 混合检索(RAG)管线        ├ 双层安全控制
└ 评测框架                ├ Token预算分配            ├ 多Agent协调
                          └ 分层记忆系统             ├ 错误恢复与自愈
                                                    └ 验证闭环
```

### 1.2 六大 Agent 能力全景


| 维度       | Claude Code  | Cursor      | Codex CLI  | Gemini CLI    | OpenCode | OpenClaw      |
| -------- | ------------ | ----------- | ---------- | ------------- | -------- | ------------- |
| 提示词规模    | ~30K tokens  | ~5-8K       | ~3-5K      | ~8-15K        | ~1.2K 词  | 150KB+        |
| Agent 循环 | 流式 ReAct     | IDE-ReAct   | App Server | Core ReAct    | 基础循环     | ACP           |
| 工具系统     | 26+工具+MCP    | IDE原生       | Shell+权限   | 注册+MCP        | 基础+MCP   | 工具+52技能       |
| 权限控制     | 5级+钩子        | Visual Diff | 沙箱+审批      | Policy Engine | 基础       | ACP策略         |
| 多Agent   | 子Agent+Teams | 并行Tab       | 子Agent隔离   | 基础子Agent      | 3种会话模式   | ACP+Cron      |
| 钩子       | 12事件         | 有限          | 6事件        | 8事件           | 插件钩子     | ContextEngine |
| 压缩       | 3层压缩         | 内建          | 服务端自动      | ContextFlow   | Agent驱动  | compact()钩子   |
| 记忆       | 5层记忆         | 索引持久化       | 无          | 分层GEMINI.md   | 基本       | 4层记忆栈         |


### 1.3 12 条统一设计原则


| #   | 原则                      | 说明                   |
| --- | ----------------------- | -------------------- |
| P1  | Agent = Model + Harness | 模型提供智能，Harness 提供可靠性 |
| P2  | 安全是不可协商的基线              | 沙箱+策略引擎双层控制          |
| P3  | 流式优先                    | 所有响应和工具执行流式化         |
| P4  | 引擎与表面解耦                 | Agent 循环引擎独立于客户端     |
| P5  | Token 即货币               | 每个 token 必须证明其价值     |
| P6  | 零成本压缩优先                 | 先清理工具结果，再 LLM 摘要     |
| P7  | 渐进式披露                   | 预加载描述，按需加载完整内容       |
| P8  | 隔离防污染                   | 子 Agent 独立上下文        |
| P9  | 验证驱动                    | 每次修改后自动验证            |
| P10 | 失败即学习                   | 注入失败历史，避免重复犯错        |
| P11 | 钩子可扩展                   | 所有关键决策点暴露钩子          |
| P12 | 渐进式自动化                  | 多级权限，用户可控            |


---

## 二、需求方案

### 2.1 用户画像


| 画像     | 角色      | 场景             | 交互方式        |
| ------ | ------- | -------------- | ----------- |
| 个人开发者  | 全栈开发者   | 日常编码、Bug 修复、重构 | CLI / IDE   |
| DevOps | 平台工程师   | 代码审查、PR 处理、部署  | API / CI/CD |
| 技术团队   | 技术 Lead | 大型特性、跨模块重构     | 多 Agent 并行  |


### 2.2 功能需求全表（14 域）

#### FR-1: Agent 循环引擎


| ID     | 描述                        | 优先级 |
| ------ | ------------------------- | --- |
| FR-1.1 | 流式 ReAct 循环               | P0  |
| FR-1.2 | 流式中途检测 tool_use 块         | P0  |
| FR-1.3 | 单次 API 多个 tool_use（顺序执行）  | P1  |
| FR-1.4 | 无 tool_use 时终止循环          | P0  |
| FR-1.5 | 中断和恢复（Checkpoint）         | P2  |
| FR-1.6 | Plan / Build / Debug 工作模式 | P1  |


#### FR-2: 工具系统


| ID     | 描述                                       | 优先级 |
| ------ | ---------------------------------------- | --- |
| FR-2.1 | 内建工具：Read, Write, Edit, Bash, Glob, Grep | P0  |
| FR-2.2 | 工具 Schema 校验（Zod）                        | P0  |
| FR-2.3 | 工具风险分级（safe/medium/high/forbidden）       | P0  |
| FR-2.4 | MCP 动态工具注册                               | P1  |
| FR-2.5 | 工具执行超时                                   | P1  |
| FR-2.6 | 工具健康检查和版本管理                              | P2  |
| FR-2.7 | 工具并行执行                                   | P2  |


#### FR-3: 提示词系统


| ID     | 描述                       | 优先级 |
| ------ | ------------------------ | --- |
| FR-3.1 | 3 层提示词架构（核心/场景/动态）       | P0  |
| FR-3.2 | 静态/动态分离支持 Prompt Caching | P0  |
| FR-3.3 | 多模型提供商适配（Provider 文件）    | P1  |
| FR-3.4 | 用户自定义指令文件（AGENTS.md）     | P1  |
| FR-3.5 | 环境信息动态注入                 | P0  |


#### FR-4: 上下文管理


| ID     | 描述                           | 优先级 |
| ------ | ---------------------------- | --- |
| FR-4.1 | Token 预算管理器                  | P0  |
| FR-4.2 | 工具结果 Hot Tail + Cold Storage | P0  |
| FR-4.3 | 自动压缩（LLM 摘要）                 | P1  |
| FR-4.4 | 手动压缩（/compact）               | P1  |
| FR-4.5 | 8 段结构化压缩模板                   | P1  |
| FR-4.6 | 代码库语义索引（Tree-sitter+向量）      | P2  |
| FR-4.7 | 混合检索（向量+BM25）                | P2  |


#### FR-5: 权限与安全


| ID     | 描述                          | 优先级 |
| ------ | --------------------------- | --- |
| FR-5.1 | 工具级权限检查（allow/deny/ask）     | P0  |
| FR-5.2 | 3 级权限模式                     | P0  |
| FR-5.3 | 安全红线规则                      | P0  |
| FR-5.4 | 沙箱隔离（FS+网络+进程）              | P1  |
| FR-5.5 | 策略引擎（规则+优先级+决策）             | P1  |
| FR-5.6 | 审批工作流（once/session/persist） | P1  |


#### FR-6: 多 Agent 协调


| ID     | 描述                   | 优先级 |
| ------ | -------------------- | --- |
| FR-6.1 | Controller-Worker 模式 | P2  |
| FR-6.2 | 子 Agent 上下文隔离        | P2  |
| FR-6.3 | 子 Agent 摘要汇报         | P2  |
| FR-6.4 | 深度限制（默认 2 层）         | P2  |
| FR-6.5 | Worker 独立预算和超时       | P2  |


#### FR-7: 记忆系统


| ID     | 描述              | 优先级 |
| ------ | --------------- | --- |
| FR-7.1 | 会话持久化（恢复/续接）    | P0  |
| FR-7.2 | MEMORY.md 持久化记忆 | P1  |
| FR-7.3 | 跨会话记忆语义检索       | P2  |
| FR-7.4 | 记忆类型区分          | P2  |


#### FR-8: 验证闭环


| ID     | 描述                       | 优先级 |
| ------ | ------------------------ | --- |
| FR-8.1 | 修改后自动 Lint               | P1  |
| FR-8.2 | Build→Verify→Self-Fix 循环 | P1  |
| FR-8.3 | 结构化错误上下文注入               | P1  |
| FR-8.4 | 自动运行测试                   | P2  |


#### FR-9: 生命周期钩子


| ID     | 描述                       | 优先级 |
| ------ | ------------------------ | --- |
| FR-9.1 | 8 个最小钩子集                 | P1  |
| FR-9.2 | Shell 命令 + HTTP 端点钩子     | P2  |
| FR-9.3 | exit code 控制（0=允许, 2=阻止） | P1  |


#### FR-10: 技能系统（Skills）


| ID      | 描述                               | 优先级 |
| ------- | -------------------------------- | --- |
| FR-10.1 | 技能注册表（发现 + 加载 + 匹配）              | P1  |
| FR-10.2 | Markdown + YAML Frontmatter 技能格式 | P1  |
| FR-10.3 | 4 种触发方式（模式/事件/自主/命令）             | P1  |
| FR-10.4 | 技能内容按需加载/卸载（渐进式披露）               | P1  |
| FR-10.5 | 15 个内建技能                         | P2  |
| FR-10.6 | 远程技能安装（npm/git）                  | P3  |


#### FR-11: MCP 集成


| ID      | 描述                                     | 优先级 |
| ------- | -------------------------------------- | --- |
| FR-11.1 | MCP Manager（配置加载 + Server 生命周期）        | P1  |
| FR-11.2 | MCP Client（stdio/SSE 传输 + 工具发现 + 调用转发） | P1  |
| FR-11.3 | MCP 工具注册到 ToolRegistry + 权限集成          | P1  |
| FR-11.4 | MCP 多 Server 并行                        | P2  |
| FR-11.5 | MCP 健康管理 + 崩溃自动重连                      | P2  |


#### FR-12: 插件系统（Plugin）


| ID      | 描述                                   | 优先级 |
| ------- | ------------------------------------ | --- |
| FR-12.1 | PluginHost（发现 + 加载 + 激活 + 停用）        | P2  |
| FR-12.2 | Plugin API（上下文修改 + 工具扩展 + 行为拦截）      | P2  |
| FR-12.3 | 插件 Manifest 声明式配置                    | P2  |
| FR-12.4 | 内建插件（eslint, prettier, cost-tracker） | P2  |
| FR-12.5 | 插件沙箱隔离（错误不崩主循环）                      | P3  |


#### FR-13: 自动化与定时任务


| ID      | 描述                            | 优先级 |
| ------- | ----------------------------- | --- |
| FR-13.1 | Scheduler（Cron 调度）            | P2  |
| FR-13.2 | FileWatcher（文件变更监听 + 防抖）      | P2  |
| FR-13.3 | TaskRunner（独立会话执行 + 隔离）       | P2  |
| FR-13.4 | 任务历史记录 + 执行报告                 | P2  |
| FR-13.5 | Webhook 接收器（GitHub/GitLab 事件） | P3  |
| FR-13.6 | 多渠道通知（Slack/Discord/邮件）       | P3  |


#### FR-14: 搜索能力


| ID      | 描述                           | 优先级 |
| ------- | ---------------------------- | --- |
| FR-14.1 | Web 搜索（搜索 API + 结果摘要）        | P1  |
| FR-14.2 | URL 抓取（→ Markdown + 截断 + 缓存） | P1  |
| FR-14.3 | Git 历史搜索（log/blame/diff）     | P1  |
| FR-14.4 | 语义搜索（向量+BM25 混合）             | P2  |
| FR-14.5 | 依赖图搜索（调用者/导入）                | P2  |
| FR-14.6 | 搜索结果缓存（TTL 5 分钟）             | P2  |


### 2.3 非功能需求


| 维度  | 指标                | 目标      | 优先级 |
| --- | ----------------- | ------- | --- |
| 性能  | 首 token 延迟        | < 2s    | P0  |
| 性能  | 工具执行响应            | < 5s    | P0  |
| 安全  | 安全红线违反率           | 0%      | P0  |
| 成本  | Prompt Caching 降本 | > 80%   | P1  |
| 可靠性 | pass@5            | > 80%   | P1  |
| 可靠性 | 错误自动恢复率           | > 80%   | P2  |
| 可扩展 | 新工具接入             | < 1h    | P1  |
| 可扩展 | 新模型提供商接入（官方 Provider）| < 1d | P1 |
| 可扩展 | OpenAI 兼容模型接入（千问/文心等）| < 1h（仅需配置）| P0 |
| 可扩展 | 新技能创建             | < 30min | P1  |
| 可扩展 | MCP Server 接入     | < 1h    | P1  |
| 可观测 | Token 消耗追踪        | 每请求可查   | P1  |


### 2.4 优先级矩阵

```
P0（MVP, 第 1-2 周）            P1（第 3-4 周）
─────────────────────           ─────────────────────────────
• 流式 ReAct 循环                • MCP 基础（Manager+Client）
• 5 个核心工具                   • 技能系统核心 + 5 个内建技能
• 3 层提示词架构                 • Web 搜索 / URL 抓取 / Git 搜索
• Token 预算 + Hot Tail          • 沙箱 + 策略引擎 + 审批工作流
• 3 级权限 + 安全红线            • 自动压缩 + 8 段摘要模板
• Prompt Caching                 • 多模型适配 + Build→Verify→Fix
• 会话持久化 + 环境注入          • 生命周期钩子（8 个）+ MEMORY.md

P2（第 5-8 周）                 P3（第 9-12+ 周）
─────────────────────           ─────────────────────────────
• 多 Agent（Controller-Worker）  • Agent Teams 对等协作
• 插件系统 + 3 个内建插件        • 远程技能市场 / 插件市场
• MCP 多 Server + 健康管理       • 守护进程模式 / Webhook
• 语义搜索 + 依赖图搜索          • 多渠道通知 / 插件沙箱
• 技能扩展到 15 个 + 事件触发    • 浏览器自动化 / 跨项目共享
• Cron 定时任务 + FileWatcher    • 定时任务可视化面板
• 可观测性（OpenTelemetry）      • 知识图谱 / 多租户
```

---

## 三、架构方案

### 3.1 分层架构（6 层）

```
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 1: 客户端层                                                   │
│  CLI │ Web UI │ IDE 插件 │ CI/CD │ API │ Webhook 入口               │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 2: 协议层                                                     │
│  JSON-RPC 2.0 (stdio/WebSocket) │ SSE 流式 │ Webhook Handler        │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 3: 核心引擎层                                                 │
│  Agent循环 │ 提示词构建 │ 上下文管理 │ 工具注册 │ 策略引擎            │
│  错误恢复 │ 生命周期钩子 │ Agent协调 │ 技能引擎 │ 插件宿主           │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 4: 工具层                                                     │
│  内建工具(Read/Write/Edit/Bash/Glob/Grep)                           │
│  搜索工具(WebSearch/WebFetch/SemanticSearch/GitSearch)               │
│  MCP动态工具(MCPManager → MCPClient → MCP Server)                   │
│  子Agent工具(Task/Explore/General)                                   │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 5: 数据层                                                     │
│  向量索引 │ 记忆存储 │ 会话存储 │ 搜索缓存 │ 任务历史               │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 6: 自动化层                                                   │
│  Scheduler(Cron) │ FileWatcher │ WebhookReceiver │ TaskRunner       │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 核心数据流

```
用户输入
    │
    ▼
1. 上下文组装
   ├── 提示词（核心层↔缓存 + 场景层↔按需 + 动态层↔每次变化）
   ├── Token 预算分配
   ├── 对话历史（经 MicroCompaction 清理）
   ├── 技能描述索引（轻量注入）
   └── 工具定义（内建 + MCP 动态）
    │
    ▼
2. LLM 推理（流式 SSE）
   ├── 文本块 → 增量渲染
   └── tool_use 块 → 流式中途检测
    │
    ▼
3. 工具执行管线
   ├ PreToolUse 钩子 → 插件拦截
   ├ 策略引擎权限检查 → allow / deny / ask_user
   ├ 技能匹配 → 如命中则注入技能内容
   ├ 执行工具（内建直调 / MCP 协议转发）
   ├ PostToolUse 钩子 → 插件后处理
   └ 工具结果管理（Hot Tail / Cold Storage）
    │
    ▼
4. 循环决策
   ├ 含 tool_use → 回到步骤 2
   ├ 不含 → 进入步骤 5
   └ StuckDetector: Repeater → 注入提示
                    Wanderer → 重申目标
                    Looper → 中断换策略
    │
    ▼
5. 验证与输出
   ├ 代码修改 → Build→Verify→Self-Fix 循环
   ├ 最终响应 → 流式输出
   └ 异步: 会话持久化 + 记忆更新 + 自动化触发检查
```

### 3.3 技术选型


| 层次     | 选型                          | 理由                  |
| ------ | --------------------------- | ------------------- |
| 语言     | TypeScript + Node.js 22 LTS | 主流 Agent 标准栈，生态丰富   |
| LLM 抽象 | Vercel AI SDK (`ai`) | 多提供商统一接口，流式+工具调用+结构化输出（详见 3.3.1）|
| Schema | Zod                         | 运行时类型安全，与 AI SDK 集成 |
| 代码解析   | Tree-sitter (WASM)          | 语义级代码块提取            |
| 向量存储   | pgvector / Qdrant（MVP: 内存）  | 语义搜索后端              |
| 协议     | JSON-RPC 2.0 (stdio) + SSE  | 双向通信，支持审批请求         |
| 存储     | SQLite（MVP: JSON 文件）        | 零依赖本地存储             |
| 文件监听   | chokidar                    | 文件变更监听（自动化层）        |
| 可观测    | OpenTelemetry               | 行业标准追踪              |
| 包管理    | pnpm + turborepo monorepo   | 多包管理，构建高效           |


#### 3.3.1 LLM 抽象层：Vercel AI SDK 多模型提供商方案

**选型核心理由**：Vercel AI SDK (`ai`) 提供统一的 TypeScript 接口，一套代码同时支持国内外多家 LLM 提供商的流式响应、工具调用（function calling）和结构化输出，切换模型仅需更换 provider 实例，无需修改 Agent 核心逻辑。

**支持的提供商矩阵**：

| 提供商 | npm 包 | 接入方式 | 流式 | 工具调用 | 优先级 |
|--------|--------|---------|------|---------|--------|
| **Anthropic（Claude）** | `@ai-sdk/anthropic` | 官方 Provider | Yes | Yes | P0（MVP 默认）|
| **阿里云通义千问（Qwen）** | `@ai-sdk/openai-compatible` | OpenAI 兼容接口 | Yes | Yes | P1 |
| **OpenAI（GPT）** | `@ai-sdk/openai` | 官方 Provider | Yes | Yes | P1 |
| **Google（Gemini）** | `@ai-sdk/google-generative-ai` | 官方 Provider | Yes | Yes | P1 |
| **DeepSeek** | `@ai-sdk/deepseek` | 官方 Provider | Yes | Yes | P1 |
| **xAI（Grok）** | `@ai-sdk/xai` | 官方 Provider | Yes | Yes | P2 |
| **Groq** | `@ai-sdk/groq` | 官方 Provider | Yes | Yes | P2 |
| **Mistral** | `@ai-sdk/mistral` | 官方 Provider | Yes | Yes | P2 |
| **Azure OpenAI** | `@ai-sdk/azure` | 官方 Provider | Yes | Yes | P2 |
| **其他 OpenAI 兼容** | `@ai-sdk/openai-compatible` | 通用兼容层 | Yes | Yes | P2 |

> 任何支持 OpenAI Chat Completions API 的国内模型（百度文心、智谱 GLM、月之暗面 Kimi、零一万物 Yi 等）均可通过 `@ai-sdk/openai-compatible` 接入。

**Provider 注册架构**：

```
┌─────────────────────────────────────────────────────────────────┐
│                  LLM Provider 注册架构                            │
│                                                                 │
│  ┌─ ProviderRegistry（提供商注册表）──────────────────────────┐  │
│  │                                                            │  │
│  │  配置文件: .agent/providers.json                           │  │
│  │  {                                                         │  │
│  │    "default": "anthropic:claude-sonnet-4-20250514",        │  │
│  │    "providers": {                                          │  │
│  │      "anthropic": {                                        │  │
│  │        "package": "@ai-sdk/anthropic",                     │  │
│  │        "apiKey": "${ANTHROPIC_API_KEY}",                   │  │
│  │        "promptFile": "prompts/providers/anthropic.txt"     │  │
│  │      },                                                    │  │
│  │      "qwen": {                                             │  │
│  │        "package": "@ai-sdk/openai-compatible",             │  │
│  │        "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1", │
│  │        "apiKey": "${DASHSCOPE_API_KEY}",                   │  │
│  │        "promptFile": "prompts/providers/qwen.txt",         │  │
│  │        "models": {                                         │  │
│  │          "default": "qwen-max",                            │  │
│  │          "fast": "qwen-turbo",                             │  │
│  │          "reasoning": "qwen-plus"                          │  │
│  │        }                                                   │  │
│  │      },                                                    │  │
│  │      "openai": {                                           │  │
│  │        "package": "@ai-sdk/openai",                        │  │
│  │        "apiKey": "${OPENAI_API_KEY}",                      │  │
│  │        "promptFile": "prompts/providers/openai.txt"        │  │
│  │      },                                                    │  │
│  │      "deepseek": {                                         │  │
│  │        "package": "@ai-sdk/deepseek",                      │  │
│  │        "apiKey": "${DEEPSEEK_API_KEY}",                    │  │
│  │        "promptFile": "prompts/providers/deepseek.txt"      │  │
│  │      },                                                    │  │
│  │      "gemini": {                                           │  │
│  │        "package": "@ai-sdk/google-generative-ai",          │  │
│  │        "apiKey": "${GOOGLE_API_KEY}",                      │  │
│  │        "promptFile": "prompts/providers/gemini.txt"        │  │
│  │      }                                                     │  │
│  │    }                                                       │  │
│  │  }                                                         │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                 │
│  运行时切换:                                                     │
│  ├── CLI 参数: agent --model qwen:qwen-max                     │
│  ├── 环境变量: AGENT_MODEL=deepseek:deepseek-chat              │
│  ├── 会话内切换: /model qwen:qwen-turbo                        │
│  └── 子 Agent 可独立选择模型（廉价模型做搜索，强模型做编码）      │
└─────────────────────────────────────────────────────────────────┘
```

**核心接口**：

```typescript
import { createAnthropic } from '@ai-sdk/anthropic';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { createOpenAI } from '@ai-sdk/openai';
import { createDeepSeek } from '@ai-sdk/deepseek';
import { createGoogleGenerativeAI } from '@ai-sdk/google-generative-ai';

interface ProviderRegistry {
  register(name: string, config: ProviderConfig): void;
  get(modelId: string): LanguageModel;
  getDefault(): LanguageModel;
  setDefault(modelId: string): void;
  list(): ProviderInfo[];
}

interface ProviderConfig {
  package: string;
  apiKey?: string;
  baseURL?: string;
  promptFile?: string;
  models?: Record<string, string>;
}

// 创建各提供商实例示例
function createProviders(config: ProvidersConfig) {
  const providers: Record<string, any> = {};

  // Anthropic（官方 Provider）
  if (config.anthropic) {
    providers.anthropic = createAnthropic({
      apiKey: config.anthropic.apiKey,
    });
  }

  // 阿里云通义千问（OpenAI 兼容接口）
  if (config.qwen) {
    providers.qwen = createOpenAICompatible({
      name: 'qwen',
      apiKey: config.qwen.apiKey,
      baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    });
  }

  // DeepSeek（官方 Provider）
  if (config.deepseek) {
    providers.deepseek = createDeepSeek({
      apiKey: config.deepseek.apiKey,
    });
  }

  // OpenAI（官方 Provider）
  if (config.openai) {
    providers.openai = createOpenAI({
      apiKey: config.openai.apiKey,
    });
  }

  // Google Gemini（官方 Provider）
  if (config.gemini) {
    providers.gemini = createGoogleGenerativeAI({
      apiKey: config.gemini.apiKey,
    });
  }

  // 通用 OpenAI 兼容（百度文心、智谱 GLM、Kimi 等）
  if (config.custom) {
    for (const [name, custom] of Object.entries(config.custom)) {
      providers[name] = createOpenAICompatible({
        name,
        apiKey: custom.apiKey,
        baseURL: custom.baseURL,
      });
    }
  }

  return providers;
}
```

**模型选择策略**：

```
任务类型 → 推荐模型策略:

高质量编码:     anthropic:claude-sonnet-4  或  qwen:qwen-max
快速轮询/搜索:  qwen:qwen-turbo  或  deepseek:deepseek-chat
长上下文分析:    gemini:gemini-2.5-pro (1M 窗口)
推理密集:       deepseek:deepseek-reasoner  或  openai:o3
成本敏感:       qwen:qwen-turbo  或  deepseek:deepseek-chat

子 Agent 策略:
├── 主 Agent（编码）: 使用高质量模型
├── Explore 子 Agent: 使用快速模型（降低成本）
└── 搜索/摘要子 Agent: 使用最廉价模型
```


### 3.4 关键架构决策（ADR）


| ADR   | 决策                          | 参考                   |
| ----- | --------------------------- | -------------------- |
| ADR-1 | 引擎与客户端解耦（App Server 模式）     | Codex App Server     |
| ADR-2 | 流式优先 Agent 循环（SSE + 中途工具检测） | Claude Code          |
| ADR-3 | 双层安全（OS 沙箱 + 规则策略引擎）        | Codex + Gemini       |
| ADR-4 | 多模型 Provider 注册表 + 提示词文件适配 | OpenCode + Vercel AI SDK |
| ADR-5 | 技能/MCP/插件三层扩展体系             | OpenClaw 技能 + MCP 标准 |


**ADR-5 三层扩展体系说明**：

```
技能 = Markdown 指导文件 → 教 Agent "何时做、怎么做"（纯提示词注入）
MCP  = 标准化外部工具协议 → 给 Agent 新的"手脚"（新工具能力）
插件 = TypeScript 代码扩展 → 改变 Agent "大脑回路"（拦截/修改核心流程）

创建难度: 技能(最易) < MCP(中等) < 插件(最复杂)
能力深度: 技能(提示词级) < MCP(工具级) < 插件(引擎级)
```

---

## 四、领域设计（DDD）

### 4.1 十大限界上下文

```
                    ┌──────────────────┐
                    │  BC-1 Agent Core │
                    └────────┬─────────┘
                             │
        ┌──────────┬─────────┼──────────┬──────────┐
        │          │         │          │          │
   ┌────▼───┐ ┌───▼────┐ ┌──▼───┐ ┌───▼────┐ ┌───▼──────┐
   │BC-2    │ │BC-3    │ │BC-4  │ │BC-5    │ │BC-6      │
   │Tool    │ │Context │ │Secur.│ │Memory  │ │Coordinat.│
   └────────┘ └────────┘ └──────┘ └────────┘ └──────────┘
        │          │                    │
   ┌────▼───┐ ┌───▼────┐          ┌───▼──────┐
   │BC-7    │ │BC-8    │          │BC-10     │
   │Skill   │ │MCP     │          │Automation│
   └────────┘ └────────┘          └──────────┘
                    │
               ┌────▼───┐
               │BC-9    │
               │Plugin  │
               └────────┘

上下文间通信:
├── Core → Tool/Context/Security: 同步调用（关键路径）
├── Core → Memory/Automation: 异步事件
├── Core → Coordination: 同步调用（子Agent生成）
├── Tool ↔ MCP: 同步调用（工具转发）
├── Core ↔ Skill: 同步调用（技能注入/卸载）
└── Core ↔ Plugin: 钩子回调（同步拦截）
```

### 4.2 各限界上下文设计

#### BC-1: Agent Core

```
聚合根: AgentLoop
├── 实体: Turn, Session
├── 值对象: Message, ToolCall, ToolResult, WorkMode, Checkpoint, SessionConfig
领域事件: TurnStarted/Completed, ToolCallRequested, ToolResultReceived,
         SessionCreated/Resumed/Ended, AgentStuck
```

```typescript
interface AgentLoop {
  readonly sessionId: string;
  readonly mode: WorkMode;
  run(input: UserInput): AsyncGenerator<StreamEvent>;
  interrupt(): void;
  resume(checkpoint: Checkpoint): AsyncGenerator<StreamEvent>;
  switchMode(mode: WorkMode): void;
}

type WorkMode = 'plan' | 'build' | 'debug';

type StreamEvent =
  | { type: 'text'; content: string }
  | { type: 'tool_call'; id: string; tool: string; input: unknown }
  | { type: 'tool_result'; id: string; tool: string; output: unknown }
  | { type: 'approval_request'; id: string; tool: string; reason: string }
  | { type: 'error'; error: AgentError }
  | { type: 'done'; summary: string };
```

#### BC-2: Tool

```
聚合根: ToolRegistry
├── 实体: Tool, MCPConnection
├── 值对象: ToolSchema, RiskLevel, ToolHealth
├── 服务: ToolExecutor
领域事件: ToolRegistered, ToolExecutionStarted/Completed/Failed,
         MCPServerConnected/Disconnected, ToolHealthChanged
```

```typescript
interface Tool {
  readonly name: string;
  readonly description: string;
  readonly schema: ZodSchema;
  readonly riskLevel: RiskLevel;
  readonly timeout: number;
  execute(input: unknown, ctx: ExecutionContext): Promise<ToolResult>;
}

type RiskLevel = 'safe' | 'medium' | 'high' | 'forbidden';

interface ToolRegistry {
  register(tool: Tool): void;
  unregister(name: string): void;
  get(name: string): Tool | undefined;
  list(): ToolDescriptor[];
  registerMCP(server: MCPServerConfig): Promise<void>;
  healthCheck(): Promise<Map<string, ToolHealth>>;
}
```

#### BC-3: Context Management

```
聚合根: ContextManager
├── 实体: PromptBuilder, TokenBudgetManager, Compactor, ToolResultManager
├── 值对象: CorePrompt, ScenarioPrompt, DynamicPrompt, TokenBudget,
           CompactionTemplate, HotTail, ColdReference
领域事件: ContextAssembled, CompactionTriggered/Completed,
         TokenBudgetExceeded, ToolResultOffloaded
```

```typescript
interface ContextManager {
  bootstrap(config: ProjectConfig): Promise<void>;
  assemble(query: string, history: Message[]): Promise<AssembledContext>;
  compact(strategy: 'micro' | 'auto' | 'full'): Promise<void>;
  getTokenUsage(): TokenUsageReport;
}

interface TokenBudget {
  total: number;
  systemPrompt: number;
  tools: number;
  memory: number;
  history: number;
  toolResults: number;
  retrieval: number;
  outputReserve: number;
}
```

#### BC-4: Security

```
聚合根: PolicyEngine
├── 实体: PolicyRule, ApprovalRecord, Sandbox
├── 值对象: RuleCondition, RuleDecision, ApprovalScope,
           FileSystemPolicy, NetworkPolicy, ProcessPolicy
├── 服务: PermissionChecker
领域事件: PermissionGranted/Denied, ApprovalRequested/Received,
         SecurityViolationAttempted
```

```typescript
interface PolicyEngine {
  addRule(rule: PolicyRule): void;
  evaluate(toolCall: ToolCall, ctx: SecurityContext): Decision;
  recordApproval(toolCall: ToolCall, scope: 'once'|'session'|'persist'): void;
}

type Decision =
  | { type: 'allow' }
  | { type: 'deny'; reason: string }
  | { type: 'ask_user'; reason: string };

interface Sandbox {
  validateFileAccess(path: string, mode: 'read'|'write'|'delete'): boolean;
  validateNetworkAccess(url: string): boolean;
  validateProcessExecution(command: string): boolean;
}
```

#### BC-5: Memory

```
聚合根: MemoryStore
├── 实体: SessionRecord, PersistentMemory, CodeIndex(P2)
├── 值对象: SessionSummary, MemoryType, MemoryTTL, CodeChunk, Embedding
├── 服务: MemoryRetriever
领域事件: SessionPersisted/Restored, MemoryCreated/Updated/Expired, CodeIndexUpdated
```

```typescript
interface MemoryStore {
  persistSession(session: Session): Promise<void>;
  restoreSession(sessionId: string): Promise<Session | null>;
  listSessions(limit: number): Promise<SessionSummary[]>;
  saveMemory(entry: MemoryEntry): Promise<void>;
  searchMemory(query: string, limit: number): Promise<MemoryEntry[]>;
}

type MemoryType = 'durable_fact' | 'execution_state' | 'distilled_knowledge';
```

#### BC-6: Coordination

```
聚合根: AgentCoordinator
├── 实体: WorkerAgent
├── 值对象: WorkerConfig, WorkerStatus, WorkerResult, TaskDescription, DepthLimit
领域事件: WorkerSpawned/Completed/Failed/TimedOut, TaskDelegated, ResultAggregated
```

```typescript
interface AgentCoordinator {
  spawnWorker(task: TaskDescription, config: WorkerConfig): Promise<WorkerHandle>;
  awaitWorker(handle: WorkerHandle): Promise<WorkerResult>;
  cancelWorker(handle: WorkerHandle): Promise<void>;
  listWorkers(): WorkerInfo[];
}

interface WorkerConfig {
  model: string;
  maxTokens: number;
  timeout: number;
  tools: string[];
  depthLimit: number;
  isolateContext: boolean;
}
```

#### BC-7: Skill

```
聚合根: SkillRegistry
├── 实体: Skill
├── 值对象: SkillTrigger, SkillRequirement, SkillContent
├── 服务: SkillMatcher, SkillInstaller
领域事件: SkillRegistered, SkillTriggered, SkillContentInjected/Evicted, SkillInstalled
```

```typescript
interface SkillRegistry {
  register(skill: Skill): void;
  discover(directories: string[]): Promise<Skill[]>;
  match(input: string): Skill | null;
  matchEvent(event: HookEvent, data: HookData): Skill | null;
  getDescriptors(): SkillDescriptor[];
  getFullContent(name: string): string;
  install(source: string): Promise<Skill>;
}

type SkillTrigger =
  | { type: 'pattern'; pattern: string | RegExp }
  | { type: 'event'; event: HookEvent; tool?: string }
  | { type: 'command'; command: string };
```

**内建技能（15 个）**：code-review, refactor, add-tests, git-commit, create-pr, resolve-conflict, init-project, update-deps, generate-docs, explain-codebase, debug-error, performance-profile, security-audit, deploy, deep-research

#### BC-8: MCP

```
聚合根: MCPManager
├── 实体: MCPConnection
├── 值对象: MCPServerConfig, MCPServerStatus, MCPTransport
├── 服务: MCPClient, MCPHealthMonitor
领域事件: MCPServerStarted/Stopped, MCPToolDiscovered, MCPToolCallForwarded,
         MCPServerCrashed/Restarted
```

```typescript
interface MCPManager {
  loadConfig(paths: string[]): Promise<MCPConfig>;
  startServer(name: string): Promise<MCPClient>;
  startAll(): Promise<Map<string, MCPClient>>;
  stopAll(): Promise<void>;
  listServers(): MCPServerStatus[];
}

interface MCPClient {
  readonly serverName: string;
  readonly status: 'starting' | 'ready' | 'error' | 'closed';
  initialize(): Promise<void>;
  listTools(): Promise<MCPToolDescriptor[]>;
  callTool(name: string, args: unknown): Promise<MCPToolResult>;
  close(): Promise<void>;
}
```

#### BC-9: Plugin

```
聚合根: PluginHost
├── 实体: PluginInstance
├── 值对象: PluginManifest, PluginStatus, PluginConfig
├── 服务: PluginLoader, PluginSandbox
领域事件: PluginDiscovered/Loaded, PluginActivated/Deactivated, PluginError, PluginHookFired
```

```typescript
interface Plugin {
  readonly name: string;
  readonly version: string;
  activate(ctx: PluginContext): Promise<void>;
  deactivate?(): Promise<void>;
}

interface PluginContext {
  hooks: HookSystem;
  tools: ToolRegistry;
  memory: MemoryStore;
  onSystemPromptBuild(handler: (prompt: string) => string): void;
  onContextAssemble(handler: (ctx: AssembledContext) => AssembledContext): void;
}

interface PluginHost {
  discover(sources: PluginSource[]): Promise<PluginManifest[]>;
  load(manifest: PluginManifest): Promise<Plugin>;
  activate(plugin: Plugin): Promise<void>;
  deactivate(name: string): Promise<void>;
  listActive(): PluginInfo[];
}
```

**内建插件**：eslint, prettier, git-guard, cost-tracker, changelog, notify, telemetry, i18n

#### BC-10: Automation

```
聚合根: Scheduler
├── 实体: ScheduledTask, TaskExecution
├── 值对象: CronExpression, WatchPattern, WebhookTrigger, TaskConfig, TaskStatus
├── 服务: TaskRunner, FileWatcher, NotificationService
领域事件: TaskScheduled/Cancelled, TaskExecutionStarted/Completed/Failed,
         FileChangeDetected, WebhookReceived, NotificationSent
```

```typescript
interface Scheduler {
  loadConfig(path: string): Promise<AutomationConfig>;
  scheduleTask(task: ScheduledTask): string;
  cancelTask(taskId: string): void;
  listTasks(): TaskInfo[];
  getTaskHistory(taskId: string): TaskExecution[];
}

interface TaskRunner {
  execute(task: ScheduledTask, ctx: AutomationContext): Promise<TaskResult>;
  executeInBackground(task: ScheduledTask): Promise<TaskHandle>;
}

interface TaskResult {
  taskId: string;
  status: 'success' | 'failure' | 'timeout' | 'skipped';
  output: string;
  tokenUsed: number;
  durationMs: number;
  reportPath?: string;
}
```

### 4.3 模块包依赖

```
@agent/core          ← 核心引擎
  ├── @agent/tools   ← 工具系统
  ├── @agent/context ← 上下文管理
  ├── @agent/security← 安全系统
  ├── @agent/memory  ← 记忆系统
  ├── @agent/coord   ← 协调系统
  ├── @agent/skills  ← 技能系统
  ├── @agent/mcp     ← MCP 集成
  └── @agent/plugins ← 插件系统

@agent/automation    ← 自动化（依赖 core + skills）
@agent/search        ← 搜索能力（依赖 tools）
@agent/protocol      ← 协议层（依赖 core）
@agent/cli           ← CLI 客户端（依赖 protocol）
@agent/shared        ← 共享类型（全部包依赖）
```

---

## 五、MVP 方案与实施路线图

### 5.1 MVP（第 1-2 周）—— P0 功能

**目标**：可工作的 CLI 编码 Agent，完成单/多文件代码修改。

```
MVP 包含（P0）:                     MVP 不包含:
├── 流式 ReAct 循环                  ├── MCP / 技能 / 插件 / 自动化
├── 5 个核心工具(R/W/E/Bash/Glob)   ├── 沙箱 / 策略引擎
├── 3 层提示词 + Prompt Caching      ├── 多 Agent / 错误恢复
├── Token 预算 + Hot Tail            ├── 代码索引 / 自动压缩
├── 3 级权限 + 安全红线（硬编码）    ├── 搜索（Web/语义）
├── 会话持久化 + 环境注入            └── 可观测性
└── 默认 Anthropic Claude（可切换千问/DeepSeek）
```

**MVP 技术选型**：TypeScript + Vercel AI SDK（`ai` + `@ai-sdk/anthropic` + `@ai-sdk/openai-compatible`）+ Zod + readline + chalk + JSON 文件存储 + tsx

> MVP 默认使用 Anthropic Claude，但从 Day 1 起即通过 `ProviderRegistry` 抽象支持切换到阿里云千问或 DeepSeek，仅需配置 API Key 和环境变量。

### 5.2 项目目录结构（完整版）

```
ai-agent/
├── package.json / tsconfig.json / .env
├── src/
│   ├── index.ts                    # CLI 入口
│   ├── core/                       # Agent 核心
│   │   ├── agent-loop.ts           # ReAct 循环
│   │   ├── stream-parser.ts        # 流式解析
│   │   └── types.ts                # 核心类型
│   ├── llm/                        # LLM 提供商抽象
│   │   ├── provider-registry.ts    # 多提供商注册表
│   │   ├── model-router.ts         # 模型路由（按任务类型选模型）
│   │   └── providers.json          # 提供商默认配置模板
│   ├── prompt/                     # 提示词系统
│   │   ├── builder.ts              # 3 层构建器
│   │   ├── environment.ts          # 环境信息
│   │   └── templates/              # 模板文件（含 providers/ 子目录）
│   ├── context/                    # 上下文管理
│   │   ├── manager.ts              # 组装器
│   │   ├── token-budget.ts         # 预算管理
│   │   └── tool-results.ts         # Hot Tail
│   ├── tools/                      # 内建工具
│   │   ├── registry.ts / executor.ts
│   │   ├── read.ts / write.ts / edit.ts / bash.ts / glob.ts
│   ├── security/                   # 安全系统
│   │   ├── permission.ts / rules.ts
│   ├── memory/                     # 记忆系统
│   │   ├── session-store.ts / types.ts
│   ├── skills/                     # 技能系统 (P1)
│   │   ├── registry.ts / matcher.ts / loader.ts
│   │   └── builtin/  (15 个 .md 文件)
│   ├── mcp/                        # MCP 集成 (P1)
│   │   ├── manager.ts / client.ts / health.ts / config.ts
│   ├── plugins/                    # 插件系统 (P2)
│   │   ├── host.ts / loader.ts / context.ts
│   │   └── builtin/ (eslint/prettier/cost-tracker)
│   ├── automation/                 # 自动化 (P2)
│   │   ├── scheduler.ts / watcher.ts / runner.ts / webhook.ts / notify.ts
│   ├── search/                     # 搜索 (P1-P2)
│   │   ├── web-search.ts / web-fetch.ts / git-search.ts
│   │   ├── semantic-search.ts / dep-graph.ts / cache.ts
│   └── utils/                      # 工具函数
├── .agent/                         # Agent 配置
│   ├── providers.json              # LLM 提供商配置（API Key 引用环境变量）
│   ├── mcp.json / automation.yaml
│   ├── plugins/ / skills/ / reports/
├── data/sessions/                  # 运行时数据
└── tests/                          # 测试
```

### 5.3 逐日实施计划（Day 1-10 MVP）


| Day | 交付物                               | 验证标准                   |
| --- | --------------------------------- | ---------------------- |
| 1   | 项目骨架 + 核心类型 + ProviderRegistry      | `tsx src/index.ts` 可运行，可切换模型 |
| 2   | 3 层提示词构建器 + 模板 + 环境信息             | 打印完整系统提示词              |
| 3   | 流式 ReAct 循环引擎 + 流式解析器             | 基础对话正常                 |
| 4   | ToolRegistry + Read/Write/Glob 工具 | Agent 能读写文件            |
| 5   | Edit/Bash 工具 + 3 级权限 + 安全红线       | 完整代码修改+命令执行            |
| 6   | Token 预算管理 + Hot Tail 工具结果管理      | 10+ 轮不超出上下文            |
| 7   | Prompt Caching + 会话持久化            | 恢复会话继续工作               |
| 8   | CLI 交互优化 + 斜杠命令                   | 完整用户体验                 |
| 9   | 4 个集成测试 + Bug 修复                  | 全部通过                   |
| 10  | 文档 + 端到端验证                        | 真实项目 Bug 修复            |


### 5.4 后续路线图（5 阶段，共 10 周）

```
Phase 2（第 3-4 周）: 搜索 + 技能 + MCP + 安全强化
├── WebSearch / WebFetch / GitSearch 工具
├── 技能系统核心 + 5 个内建技能
├── MCP Manager + Client（单 Server）
├── 沙箱 + Policy Engine + 审批工作流
├── 自动压缩 + 8 段摘要 + MEMORY.md
├── 生命周期钩子（8 个）+ 多模型适配
└── Build→Verify→Fix 验证循环

Phase 3（第 5-6 周）: 多 Agent + 插件 + MCP 增强
├── Controller-Worker 多 Agent + 子 Agent 隔离
├── StuckDetector + 指数退避 + Circuit Breaker
├── 插件系统核心 + 3 个内建插件
├── MCP 多 Server 并行 + 健康管理 + 自动重连
├── 技能扩展到 15 个 + 事件触发
└── 语义搜索（Tree-sitter + 向量 + 混合检索）

Phase 4（第 7-8 周）: 上下文工程 + 自动化
├── 代码库索引（AST + 向量嵌入 + 增量更新）
├── 跨会话记忆检索
├── Scheduler（Cron）+ FileWatcher + TaskRunner
├── 依赖图搜索 + 搜索结果缓存
└── 任务历史 + 执行报告

Phase 5（第 9-10 周）: 生产优化
├── OpenTelemetry 可观测性
├── Webhook 接收器 + 多渠道通知
├── 插件沙箱隔离 + 远程技能安装
├── SWE-bench 基准测试 + 工具并行执行
└── 端到端自动化流程验证
```

### 5.5 成功标准


| 阶段  | 标准                   | 指标     |
| --- | -------------------- | ------ |
| MVP | 单文件 Bug 修复           | Day 5  |
| MVP | 安全红线零违反              | Day 5  |
| MVP | 10+ 轮对话不溢出           | Day 6  |
| MVP | Prompt Caching > 80% | Day 7  |
| MVP | 4 个集成测试通过            | Day 9  |
| P1  | Web 搜索首条相关率          | > 80%  |
| P1  | 自定义技能热加载             | < 5s   |
| P2  | 3 个 MCP Server 稳定并行  | 无冲突    |
| P2  | MCP 崩溃自动恢复率          | > 95%  |
| P2  | 插件不影响主循环性能           | < 50ms |
| P2  | Cron 任务准时执行偏差        | < 10s  |
| P3  | 语义搜索召回率              | > 70%  |
| P3  | 插件错误不崩主进程            | 100%   |
| 全局  | 新能力不破坏 MVP 功能        | 每阶段回归  |


### 5.6 风险与缓解


| 风险              | 缓解                            |
| --------------- | ----------------------------- |
| 流式解析复杂度超预期      | 使用 Vercel AI SDK 内建流式解析       |
| 单一模型提供商不可用     | ProviderRegistry 支持运行时切换到备用模型（千问/DeepSeek） |
| 工具结果溢出上下文       | Hot Tail 强制限制 + 截断            |
| 权限遗漏高风险操作       | 白名单策略（默认 deny）                |
| MCP Server 不稳定  | 心跳 + 指数退避重连 + Circuit Breaker |
| 插件崩溃影响主循环       | 插件沙箱隔离（P3 阶段）                 |
| 技能内容占用过多上下文     | 渐进式披露（描述~2%，内容按需加载/卸载）        |
| 定时任务耗尽 token 配额 | 独立 token 预算 + 独立会话隔离          |


