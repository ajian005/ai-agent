# 通用 AI Agent 设计方案：需求、架构、领域设计与 MVP

> 基于对 Claude Code、Cursor、OpenAI Codex CLI、Gemini CLI、OpenCode、OpenClaw/OpenHands 六大主流 Agent 的深度分析，综合提示词工程、上下文工程、Harness 工程三大领域研究成果，形成通用 AI Agent 的完整设计方案。

---

## 目录

- [第一章：跨领域分析总结](#第一章跨领域分析总结)
- [第二章：通用 AI Agent 需求方案](#第二章通用-ai-agent-需求方案)
- [第三章：通用 AI Agent 架构方案](#第三章通用-ai-agent-架构方案)
- [第四章：通用 AI Agent 领域设计](#第四章通用-ai-agent-领域设计)
- [第五章：通用 AI Agent MVP 方案](#第五章通用-ai-agent-mvp-方案)

---

## 第一章：跨领域分析总结

### 1.1 三大工程支柱核心发现

AI Agent 工程由三大支柱构成，各自解决不同层面的问题：

```
┌──────────────────────────────────────────────────────────────────┐
│                    AI Agent 工程三大支柱                          │
│                                                                  │
│  提示词工程              上下文工程              Harness 工程      │
│  (Prompt Engineering)   (Context Engineering)  (Harness Eng.)    │
│                                                                  │
│  "告诉模型怎么做"        "控制模型看到什么"       "围绕模型构建      │
│                                                 执行基础设施"      │
│                                                                  │
│  核心产出:               核心产出:               核心产出:          │
│  ├ 3层提示词架构         ├ 4层上下文管理          ├ 流式ReAct循环    │
│  ├ 多模型适配策略        ├ 3级压缩系统            ├ 工具注册与执行   │
│  ├ 安全红线设计          ├ 混合检索(RAG)管线      ├ 双层安全控制     │
│  └ 评测框架              ├ Token预算分配          ├ 多Agent协调      │
│                          └ 分层记忆系统           ├ 错误恢复与自愈   │
│                                                  └ 验证闭环         │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 六大 Agent 能力全景

| 能力维度 | Claude Code | Cursor | Codex CLI | Gemini CLI | OpenCode | OpenClaw |
|---------|------------|--------|-----------|------------|----------|----------|
| **提示词规模** | ~30K tokens | ~5-8K | ~3-5K | ~8-15K（动态）| ~1.2K 词 | 150KB+ |
| **上下文窗口** | ~200K | ~200K（实际70-120K）| ~200K | ~1M | ~200K | ~200K |
| **Agent 循环** | 流式 ReAct | IDE-ReAct | App Server | Core ReAct | 基础循环 | ACP 循环 |
| **工具系统** | 26+工具+MCP | IDE 原生+子 Agent | Shell+权限升级 | 注册+MCP | 基础+MCP | 工具+52 技能 |
| **权限控制** | 5 级+钩子 | Visual Diff | 沙箱+审批 | Policy Engine | 基础 | ACP 策略 |
| **多 Agent** | 子Agent+Teams | 子Agent+并行Tab | 子Agent+隔离 | 基础子Agent | 3种会话模式 | ACP+Cron |
| **生命周期钩子** | 12 事件 | 有限 | 6 事件 | 8 事件 | 插件钩子 | ContextEngine |
| **压缩系统** | 3 层压缩 | 内建 | 服务端自动 | ContextFlow | Compaction Agent | compact()钩子 |
| **记忆系统** | 5 层记忆 | 索引持久化 | 无 | 分层 GEMINI.md | 基本 | 4 层记忆栈 |
| **开源程度** | 半开源 | 闭源 | 部分开源 | 完全开源 | 完全开源 | 完全开源 |

### 1.3 提炼的统一设计原则

从六大 Agent 的分析中，提炼出 **12 条统一设计原则**：

| 编号 | 原则 | 说明 | 主要参考来源 |
|------|------|------|------------|
| P1 | **Agent = Model + Harness** | 模型提供智能，Harness 提供可靠性 | 全部 Agent |
| P2 | **安全是不可协商的基线** | 沙箱+策略引擎双层控制，安全红线不可被模型绕过 | Codex CLI |
| P3 | **流式优先** | 所有响应和工具执行都应该是流式的 | Claude Code |
| P4 | **引擎与表面解耦** | Agent 循环引擎独立于客户端（CLI/IDE/Web）| Codex App Server |
| P5 | **Token 即货币** | 每个进入上下文的 token 都有成本，必须证明其价值 | 全部 Agent |
| P6 | **零成本压缩优先** | 先用不需要 LLM 的策略（工具结果清理），再用 LLM 摘要 | Claude Code |
| P7 | **渐进式披露** | 预加载轻量描述，按需加载完整内容 | Cursor / Claude Code |
| P8 | **隔离防污染** | 子 Agent 独立上下文，防止噪音传播到主 Agent | 全部 Agent |
| P9 | **验证驱动** | 每次代码修改后自动验证（类型+Lint+构建+测试）| Gemini CLI |
| P10 | **失败即学习** | 每次错误都注入完整失败历史，避免重复犯错 | 自愈管线 |
| P11 | **钩子可扩展** | 所有关键决策点暴露钩子，允许外部逻辑介入 | Claude Code |
| P12 | **渐进式自动化** | 从"全部询问"到"全自动"，提供多级权限，用户可控 | Claude Code / Codex |

### 1.4 当前主流 Agent 的共同短板

| 短板 | 说明 | 影响 |
|------|------|------|
| **上下文腐蚀** | 所有模型的准确率都随上下文增长而下降，32K-64K 常出现性能悬崖 | 长会话质量不可靠 |
| **压缩信息丢失** | 压缩后用户指令、技术细节、调试历史容易丢失 | 重复犯错、重复提问 |
| **单模型锁定** | 多数 Agent 绑定单一模型提供商 | 无法利用不同模型的优势 |
| **评测不充分** | 多数依赖 SWE-bench，缺少上下文质量和 Harness 韧性评测 | 无法定向优化 |
| **成本不透明** | 缺少 token 消耗的细粒度可观测性 | 难以做成本优化 |

---

## 第二章：通用 AI Agent 需求方案

### 2.1 用户画像与使用场景

#### 画像一：个人开发者（日常编码）

```
角色: 全栈开发者
场景: 日常功能开发、Bug 修复、代码重构
交互方式: CLI 终端 或 IDE 集成
核心诉求:
├── 快速理解代码库并做出修改
├── 自动运行测试验证修改
├── 安全地执行 shell 命令
└── 在长会话中保持上下文连续性
```

#### 画像二：DevOps 工程师（CI/CD 集成）

```
角色: DevOps / 平台工程师
场景: 自动化代码审查、PR 处理、部署管线
交互方式: API / CI/CD 管线嵌入
核心诉求:
├── 无人值守自动执行
├── 严格的权限控制和沙箱隔离
├── 可编程的 Agent 工作流
└── 完善的日志和可追溯性
```

#### 画像三：技术团队（多 Agent 编排）

```
角色: 技术 Lead / 架构师
场景: 大型特性开发、跨模块重构
交互方式: 多 Agent 并行 + 协调器
核心诉求:
├── 将复杂任务分解到多个专业 Agent
├── 前端/后端/测试 Agent 并行工作
├── 结果聚合与冲突检测
└── 成本可控（按任务分配 token 预算）
```

### 2.2 功能需求

#### FR-1: Agent 循环引擎

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-1.1 | 流式 ReAct 循环（感知→推理→行动→观察→循环）| P0 |
| FR-1.2 | 流式中途检测 tool_use 块并即时执行 | P0 |
| FR-1.3 | 单次 API 调用支持多个 tool_use 块（顺序执行）| P1 |
| FR-1.4 | 循环终止条件：模型响应不含 tool_use 时终止 | P0 |
| FR-1.5 | 支持中断和恢复（Checkpoint 机制）| P2 |
| FR-1.6 | 支持 Plan / Build / Debug 多种工作模式 | P1 |

#### FR-2: 工具系统

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-2.1 | 内建核心工具：Read, Write, Edit, Bash, Glob, Grep | P0 |
| FR-2.2 | 工具 Schema 校验（JSON Schema / Zod）| P0 |
| FR-2.3 | 工具风险分级（safe / medium / high / forbidden）| P0 |
| FR-2.4 | MCP 协议动态工具注册 | P1 |
| FR-2.5 | 工具执行超时控制 | P1 |
| FR-2.6 | 工具健康检查和版本管理 | P2 |
| FR-2.7 | 工具并行执行（独立工具可并行）| P2 |

#### FR-3: 提示词系统

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-3.1 | 3 层提示词架构（核心层/场景层/动态层）| P0 |
| FR-3.2 | 静态/动态分离以支持 Prompt Caching | P0 |
| FR-3.3 | 多模型提供商适配（按模型 ID 选择提示词文件）| P1 |
| FR-3.4 | 用户自定义指令文件（AGENTS.md / CLAUDE.md）| P1 |
| FR-3.5 | 环境信息动态注入（OS、目录、时间、Git 状态）| P0 |

#### FR-4: 上下文管理

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-4.1 | Token 预算管理器（跟踪每个组件的 token 消耗）| P0 |
| FR-4.2 | 工具结果管理（Hot Tail 保留最近 N 个 + Cold Storage 卸载）| P0 |
| FR-4.3 | 自动压缩（上下文接近阈值时触发 LLM 摘要）| P1 |
| FR-4.4 | 手动压缩（/compact 命令 + 焦点提示）| P1 |
| FR-4.5 | 8 段结构化压缩摘要模板 | P1 |
| FR-4.6 | 代码库语义索引（Tree-sitter AST + 向量嵌入）| P2 |
| FR-4.7 | 混合检索（向量 ANN + BM25 关键词）| P2 |

#### FR-5: 权限与安全

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-5.1 | 工具级权限检查（allow / deny / ask）| P0 |
| FR-5.2 | 3 级权限模式（全询问 / 工作区写自动 / 全自动）| P0 |
| FR-5.3 | 安全红线规则（不可删除非工作区文件、不可提交 .env 等）| P0 |
| FR-5.4 | 沙箱隔离（文件系统+网络+进程限制）| P1 |
| FR-5.5 | 策略引擎（规则 + 优先级 + 决策）| P1 |
| FR-5.6 | 审批工作流（accept-once / accept-session / persist）| P1 |

#### FR-6: 多 Agent 协调

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-6.1 | Controller-Worker 模式（主 Agent 分配 + 子 Agent 执行）| P2 |
| FR-6.2 | 子 Agent 上下文隔离 | P2 |
| FR-6.3 | 子 Agent 结果摘要汇报（非完整输出）| P2 |
| FR-6.4 | 深度限制（默认 2 层，防递归失控）| P2 |
| FR-6.5 | Worker 独立 token 预算和超时控制 | P2 |

#### FR-7: 记忆系统

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-7.1 | 会话历史持久化（支持恢复/续接）| P0 |
| FR-7.2 | MEMORY.md 持久化记忆文件（<2K tokens）| P1 |
| FR-7.3 | 跨会话记忆检索（语义搜索）| P2 |
| FR-7.4 | 记忆类型区分（持久事实 / 执行状态 / 蒸馏知识）| P2 |

#### FR-8: 验证闭环

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-8.1 | 修改后自动 Lint 检查 | P1 |
| FR-8.2 | Build → Verify → Self-Fix 循环（最多 N 次）| P1 |
| FR-8.3 | 结构化错误上下文注入（失败历史+建议）| P1 |
| FR-8.4 | 自动运行测试并反馈结果 | P2 |

#### FR-9: 生命周期钩子

| 需求项 | 描述 | 优先级 |
|--------|------|--------|
| FR-9.1 | 最小钩子集（8个）：SessionStart/End, UserSubmit, PreToolUse, PostToolUse, PreCompact, AgentResponse, Error | P1 |
| FR-9.2 | 钩子类型支持 Shell 命令和 HTTP 端点 | P2 |
| FR-9.3 | 钩子控制机制（exit code 0=允许, 2=阻止）| P1 |

### 2.3 非功能需求

| 维度 | 指标 | 目标值 | 优先级 |
|------|------|--------|--------|
| **性能** | 首 token 延迟（TTFT）| < 2 秒 | P0 |
| **性能** | 工具执行响应 | < 5 秒（常规工具）| P0 |
| **安全** | 安全红线违反率 | 0% | P0 |
| **成本** | Prompt Caching 降本率 | > 80% | P1 |
| **成本** | 单次任务平均 token 消耗 | 可观测 + 持续优化 | P1 |
| **可靠性** | pass@5（5 次试验至少 1 次成功）| > 80%（SWE-bench 子集）| P1 |
| **可靠性** | 错误自动恢复率 | > 80% | P2 |
| **可扩展** | 新工具接入时间 | < 1 小时 | P1 |
| **可扩展** | 新模型提供商接入 | < 1 天 | P1 |
| **可观测** | token 消耗分布追踪 | 每次请求可查 | P1 |
| **可观测** | 工具调用链追踪 | OpenTelemetry span | P2 |

### 2.4 优先级矩阵

```
┌────────────────────────────────────────────────────────────────┐
│  P0（MVP 必须）           │  P1（第二轮迭代）                    │
│                           │                                    │
│  • 流式 ReAct 循环         │  • MCP 动态工具加载                 │
│  • 5 个核心工具            │  • 沙箱隔离 + 策略引擎              │
│  • 3 层提示词架构          │  • 自动压缩 + 结构化摘要            │
│  • Token 预算管理          │  • Plan/Build/Debug 工作模式        │
│  • 工具结果 Hot Tail       │  • 多模型适配                      │
│  • 3 级权限检查            │  • Build→Verify→Fix 循环           │
│  • 会话持久化              │  • 生命周期钩子（8 个）             │
│  • 安全红线                │  • MEMORY.md 持久化记忆             │
│  • Prompt Caching          │  • Prompt Caching 优化             │
│  • 环境信息注入            │  • 审批工作流                      │
├────────────────────────────┼────────────────────────────────────┤
│  P2（第三轮迭代）          │  P3（长期演进）                     │
│                           │                                    │
│  • Controller-Worker 多Agent│  • Agent Teams 对等协作             │
│  • 代码库语义索引（RAG）    │  • 知识图谱                        │
│  • 混合检索（向量+BM25）   │  • 自动化评测管线                   │
│  • 跨会话记忆检索          │  • 多租户部署                       │
│  • 工具并行执行            │  • Agent 市场/技能商店              │
│  • HTTP 钩子               │  • 语音交互                        │
│  • 可观测性(OpenTelemetry) │  • 浏览器自动化                     │
│  • 自动运行测试            │                                    │
└────────────────────────────┴────────────────────────────────────┘
```

---

## 第三章：通用 AI Agent 架构方案

### 3.1 总体分层架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                         分层架构总览                                 │
│                                                                     │
│  ┌─ Layer 1: 客户端层（多入口）──────────────────────────────────┐  │
│  │  CLI 终端 │ Web UI │ IDE 插件 │ CI/CD 管线 │ API 客户端       │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                             │                                       │
│  ┌─ Layer 2: 协议层 ────────┴───────────────────────────────────┐  │
│  │  JSON-RPC 2.0 (stdio / WebSocket)  │  SSE 流式响应            │  │
│  │  双向通信：客户端→引擎 + 引擎→客户端（审批请求）              │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                             │                                       │
│  ┌─ Layer 3: 核心引擎层 ────┴───────────────────────────────────┐  │
│  │                                                               │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐  │  │
│  │  │ Agent 循环引擎 │ │ 提示词构建器  │ │ 上下文管理器          │  │  │
│  │  │ (ReAct Loop) │ │ (3层架构)    │ │ (预算+压缩+检索)     │  │  │
│  │  └──────────────┘ └──────────────┘ └──────────────────────┘  │  │
│  │                                                               │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐  │  │
│  │  │ 工具注册器    │ │ 策略引擎      │ │ 错误恢复器            │  │  │
│  │  │ (Registry)   │ │ (Policy)     │ │ (StuckDetector)      │  │  │
│  │  └──────────────┘ └──────────────┘ └──────────────────────┘  │  │
│  │                                                               │  │
│  │  ┌──────────────┐ ┌──────────────┐                           │  │
│  │  │ 生命周期钩子  │ │ Agent 协调器  │                           │  │
│  │  │ (HookSystem) │ │ (Coordinator)│                           │  │
│  │  └──────────────┘ └──────────────┘                           │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                             │                                       │
│  ┌─ Layer 4: 工具层 ────────┴───────────────────────────────────┐  │
│  │  内建工具              MCP 动态工具          子 Agent 工具     │  │
│  │  Read/Write/Edit       DB Query/Deploy       Explore/General  │  │
│  │  Bash/Glob/Grep        Custom APIs           Background Task  │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                             │                                       │
│  ┌─ Layer 5: 数据层 ────────┴───────────────────────────────────┐  │
│  │  向量索引              记忆存储              会话存储          │  │
│  │  (pgvector/Qdrant)    (MEMORY.md/SQLite)   (JSON/SQLite)    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 核心数据流

```
用户输入
    │
    ▼
┌─ 1. 上下文组装 ──────────────────────────────────────────┐
│  提示词构建器:                                             │
│  ├── 核心层（身份+安全红线+核心行为）  ← 可缓存            │
│  ├── 场景层（工具指南+工作模式）       ← 按需加载          │
│  └── 动态层（环境+记忆+用户偏好）      ← 每次变化          │
│                                                           │
│  上下文管理器:                                             │
│  ├── Token 预算分配                                       │
│  ├── 对话历史（经 MicroCompaction 清理）                   │
│  ├── 检索的代码上下文（RAG，如已启用）                     │
│  └── 工具定义（JSON Schema）                              │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌─ 2. LLM 推理（流式）─────────────────────────────────────┐
│  API 调用 → Server-Sent Events 流式响应                   │
│  ├── 文本块 → 增量渲染到客户端                             │
│  └── tool_use 块 → 流式中途检测                           │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌─ 3. 工具执行管线 ─────────────────────────────────────────┐
│  3a. PreToolUse 钩子 → 可阻止                             │
│  3b. 策略引擎权限检查 → allow / deny / ask_user           │
│  3c. 执行工具逻辑                                         │
│  3d. PostToolUse 钩子                                     │
│  3e. 收集 tool_result                                     │
│  3f. 工具结果管理（Hot Tail / Cold Storage / 卸载大输出）  │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌─ 4. 循环决策 ─────────────────────────────────────────────┐
│  ├── 响应含 tool_use → 追加 tool_result，回到步骤 2       │
│  ├── 响应不含 tool_use → 进入步骤 5                       │
│  └── 错误恢复器检测:                                       │
│      ├── Repeater（重复）→ 注入提示                        │
│      ├── Wanderer（偏离）→ 重申目标                        │
│      └── Looper（循环）→ 中断+换策略                       │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌─ 5. 验证与输出 ───────────────────────────────────────────┐
│  5a. 如有代码修改 → Build→Verify→Self-Fix 循环            │
│  5b. 最终响应 → 流式输出到客户端                           │
│  5c. 会话持久化 + 记忆更新                                 │
└──────────────────────────────────────────────────────────┘
```

### 3.3 技术选型

| 层次 | 技术选择 | 选型理由 |
|------|---------|---------|
| **语言/运行时** | TypeScript + Node.js 20 LTS | 主流 Agent 均采用 TS（Claude Code 51万行 TS），生态最丰富 |
| **LLM 抽象** | Vercel AI SDK (`ai` 包) | 多提供商统一接口（Anthropic/OpenAI/Google/Groq），流式+工具调用+结构化输出 |
| **Schema 校验** | Zod | 运行时类型安全，与 Vercel AI SDK 深度集成 |
| **代码解析** | Tree-sitter (WASM) | 语义级代码块提取（函数/类/方法），不在函数中间截断 |
| **向量存储** | pgvector（MVP: 内存/SQLite）| 如已有 Postgres 则 pgvector；独立部署则 Qdrant |
| **通信协议** | JSON-RPC 2.0 (stdio) + SSE | 参考 Codex App Server 设计，双向通信支持审批请求 |
| **会话存储** | SQLite (better-sqlite3) | 零依赖本地存储，MVP 足够；可后续迁移 Postgres |
| **可观测性** | OpenTelemetry | 行业标准追踪框架，支持自建和商业后端 |
| **CLI 框架** | ink (React for CLI) | 丰富的终端 UI 组件，流式渲染友好 |
| **包管理** | pnpm + monorepo (turborepo) | 多包管理（core/cli/tools/sdk），构建高效 |

### 3.4 关键架构决策记录（ADR）

#### ADR-1: 引擎与客户端解耦

```
状态: 已采纳
背景: Agent 需要支持 CLI、IDE 插件、Web UI、CI/CD 等多种接入方式
决策: 采用 App Server 模式，核心引擎通过 JSON-RPC 2.0 协议暴露能力
参考: Codex App Server（统一 CLI/VS Code/Web/Desktop）
影响:
├── 正面: 一次实现多端接入，协议标准化
├── 正面: 双向通信支持 Agent 主动请求审批
└── 代价: 协议层增加开发复杂度
替代方案: 直接库调用（放弃多端支持）
```

#### ADR-2: 流式优先的 Agent 循环

```
状态: 已采纳
背景: Agent 执行可能耗时很长（分钟级），用户需要实时看到进展
决策: 所有 API 调用使用 SSE 流式响应，tool_use 块在流式中途检测
参考: Claude Code 流式 Agentic Loop
影响:
├── 正面: 用户体验显著提升，首 token 延迟感知低
├── 正面: 工具调用不需等待完整响应
└── 代价: 流式解析逻辑复杂度增加
```

#### ADR-3: 双层安全控制

```
状态: 已采纳
背景: Agent 可执行 shell 命令、读写文件，安全风险极高
决策: 采用沙箱（OS 级）+ 策略引擎（规则级）双层控制
  Layer A: 沙箱 — 文件系统仅工作区可写，网络默认禁用
  Layer B: 策略引擎 — 规则(condition+decision+priority)评估每次工具调用
参考: Codex CLI 双层安全 + Gemini CLI Policy Engine
影响:
├── 正面: 即使模型被诱导，OS 级沙箱仍能阻止越权操作
├── 正面: 策略引擎可以细粒度控制（正则匹配参数模式）
└── 代价: 配置复杂度增加
```

#### ADR-4: 多模型提供商适配

```
状态: 已采纳
背景: 不同模型有不同的能力特点和最佳提示方式
决策: 采用 Provider 文件机制，按模型 ID 选择对应的提示词文件
  Claude → prompts/anthropic.txt
  GPT → prompts/openai.txt
  Gemini → prompts/gemini.txt
参考: OpenCode 的 provider-specific prompt 设计
影响:
├── 正面: 可以针对每个模型的特点优化提示词
├── 正面: 切换模型时无需修改核心逻辑
└── 代价: 需要维护多份提示词文件
```

---

## 第四章：通用 AI Agent 领域设计

### 4.1 限界上下文总览

采用领域驱动设计（DDD）划分 **6 个限界上下文**：

```
┌─────────────────────────────────────────────────────────────────────┐
│                         限界上下文关系图                             │
│                                                                     │
│                    ┌────────────────────┐                           │
│                    │  Agent 核心上下文    │                          │
│                    │  (Agent Core)       │                          │
│                    └──────┬─────────────┘                           │
│                           │                                         │
│              ┌────────────┼────────────────────────┐                │
│              │            │            │           │                │
│        ┌─────▼────┐ ┌────▼─────┐ ┌────▼────┐ ┌───▼──────┐        │
│        │ 工具上下文 │ │上下文管理│ │安全上下文│ │记忆上下文 │        │
│        │ (Tool)    │ │(Context)│ │(Security)│ │(Memory) │        │
│        └──────────┘ └─────────┘ └─────────┘ └──────────┘        │
│                           │                                         │
│                    ┌──────▼─────────────┐                           │
│                    │  协调上下文          │                           │
│                    │  (Coordination)     │                           │
│                    └────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘

上下文间通信:
├── Agent Core → Tool: 直接调用（同步，工具执行在循环关键路径）
├── Agent Core → Context: 直接调用（同步，上下文组装在循环关键路径）
├── Agent Core → Security: 直接调用（同步，权限检查在工具执行前）
├── Agent Core → Memory: 异步事件（会话持久化不阻塞循环）
├── Agent Core → Coordination: 直接调用（子 Agent 生成）
└── Tool → Security: 直接调用（每次工具执行前检查权限）
```

### 4.2 限界上下文详细设计

#### BC-1: Agent 核心上下文（Agent Core）

**职责**：Agent 循环引擎的核心编排，管理 Turn/Message 的生命周期

```
聚合根: AgentLoop
├── 实体: Turn（一次完整的 Agent 工作单元）
│   ├── 值对象: Message（用户消息或 Agent 消息）
│   ├── 值对象: ToolCall（工具调用请求）
│   └── 值对象: ToolResult（工具执行结果）
├── 实体: Session（持久化会话容器）
│   ├── 值对象: SessionConfig（模型、权限模式等配置）
│   └── 值对象: Checkpoint（中断恢复点）
└── 值对象: WorkMode（plan | build | debug）

领域事件:
├── TurnStarted（轮次开始）
├── TurnCompleted（轮次完成）
├── ToolCallRequested（请求工具调用）
├── ToolResultReceived（收到工具结果）
├── SessionCreated / SessionResumed / SessionEnded
└── AgentStuck（检测到卡住状态）
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

interface Turn {
  readonly id: string;
  readonly messages: Message[];
  readonly toolCalls: ToolCall[];
  readonly startedAt: Date;
  completedAt?: Date;
}

interface Session {
  readonly id: string;
  readonly config: SessionConfig;
  readonly turns: Turn[];
  readonly createdAt: Date;
  checkpoint?: Checkpoint;
}
```

#### BC-2: 工具上下文（Tool Context）

**职责**：工具注册、Schema 校验、执行调度、MCP 集成

```
聚合根: ToolRegistry
├── 实体: Tool（注册的工具实例）
│   ├── 值对象: ToolSchema（JSON Schema 输入定义）
│   ├── 值对象: RiskLevel（safe | medium | high | forbidden）
│   └── 值对象: ToolHealth（healthy | degraded | unavailable）
├── 实体: MCPConnection（MCP 服务器连接）
└── 服务: ToolExecutor（工具执行调度器）

领域事件:
├── ToolRegistered / ToolUnregistered
├── ToolExecutionStarted / ToolExecutionCompleted / ToolExecutionFailed
├── MCPServerConnected / MCPServerDisconnected
└── ToolHealthChanged
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

interface ToolExecutor {
  execute(call: ToolCall, ctx: ExecutionContext): Promise<ToolResult>;
  executeParallel(calls: ToolCall[], ctx: ExecutionContext): Promise<ToolResult[]>;
}

interface ToolResult {
  readonly toolName: string;
  readonly callId: string;
  readonly output: string;
  readonly tokenCount: number;
  readonly durationMs: number;
  readonly error?: string;
}
```

#### BC-3: 上下文管理上下文（Context Management）

**职责**：提示词构建、Token 预算分配、上下文压缩、代码检索

```
聚合根: ContextManager
├── 实体: PromptBuilder（3 层提示词构建器）
│   ├── 值对象: CorePrompt（核心层，可缓存）
│   ├── 值对象: ScenarioPrompt（场景层，按需加载）
│   └── 值对象: DynamicPrompt（动态层，每次变化）
├── 实体: TokenBudgetManager（Token 预算管理器）
│   └── 值对象: TokenBudget（各组件的预算分配）
├── 实体: Compactor（压缩管理器）
│   ├── 值对象: CompactionStrategy（micro | auto | full）
│   └── 值对象: CompactionTemplate（8 段结构化摘要模板）
└── 实体: ToolResultManager（工具结果管理器）
    ├── 值对象: HotTail（最近 N 个活跃结果）
    └── 值对象: ColdReference（已卸载结果的引用）

领域事件:
├── ContextAssembled（上下文组装完成，含 token 分布）
├── CompactionTriggered / CompactionCompleted
├── TokenBudgetExceeded（预算超限警告）
└── ToolResultOffloaded（工具结果卸载到磁盘）
```

```typescript
interface ContextManager {
  bootstrap(config: ProjectConfig): Promise<void>;
  assemble(query: string, history: Message[]): Promise<AssembledContext>;
  compact(strategy: CompactionStrategy): Promise<void>;
  getTokenUsage(): TokenUsageReport;
}

interface AssembledContext {
  readonly systemPrompt: string;
  readonly tools: ToolDefinition[];
  readonly messages: Message[];
  readonly tokenUsage: TokenBudget;
  readonly cacheControl: CacheConfig;
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

interface ToolResultManager {
  readonly hotTailSize: number;
  readonly maxResultTokens: number;
  readonly offloadThreshold: number;

  add(result: ToolResult): void;
  getHotResults(): ToolResult[];
  getColdReferences(): ColdReference[];
  cleanup(): void;
}

interface CompactionTemplate {
  sections: readonly [
    'work_overview',
    'user_directives',
    'failed_approaches',
    'resolved_code',
    'how_things_work_now',
    'credentials_config',
    'pending_tasks',
    'current_work'
  ];
  preserveRules: string[];
}
```

#### BC-4: 安全上下文（Security Context）

**职责**：权限检查、策略引擎、沙箱管理、审批工作流

```
聚合根: PolicyEngine
├── 实体: PolicyRule（策略规则）
│   ├── 值对象: RuleCondition（匹配条件：工具名+参数模式+环境）
│   ├── 值对象: RuleDecision（allow | deny | ask_user）
│   └── 值对象: RulePriority（优先级数值）
├── 实体: ApprovalRecord（审批记录）
│   └── 值对象: ApprovalScope（once | session | persist）
├── 实体: Sandbox（沙箱配置）
│   ├── 值对象: FileSystemPolicy（工作区路径限制）
│   ├── 值对象: NetworkPolicy（网络访问规则）
│   └── 值对象: ProcessPolicy（进程限制）
└── 服务: PermissionChecker（权限检查器，组合策略引擎和沙箱）

领域事件:
├── PermissionGranted / PermissionDenied
├── ApprovalRequested / ApprovalReceived
├── PolicyRuleAdded / PolicyRuleRemoved
└── SecurityViolationAttempted（安全红线触发）
```

```typescript
interface PolicyEngine {
  addRule(rule: PolicyRule): void;
  removeRule(id: string): void;
  evaluate(toolCall: ToolCall, ctx: SecurityContext): Decision;
  recordApproval(toolCall: ToolCall, scope: ApprovalScope): void;
}

interface PolicyRule {
  readonly id: string;
  readonly condition: RuleCondition;
  readonly decision: 'allow' | 'deny' | 'ask_user';
  readonly priority: number;
  readonly reason?: string;
}

interface RuleCondition {
  tool?: string | RegExp;
  argsPattern?: Record<string, unknown>;
  environment?: string;
}

type Decision =
  | { type: 'allow' }
  | { type: 'deny'; reason: string }
  | { type: 'ask_user'; reason: string };

interface Sandbox {
  readonly fileSystemPolicy: FileSystemPolicy;
  readonly networkPolicy: NetworkPolicy;
  readonly processPolicy: ProcessPolicy;

  validateFileAccess(path: string, mode: 'read' | 'write' | 'delete'): boolean;
  validateNetworkAccess(url: string): boolean;
  validateProcessExecution(command: string): boolean;
}
```

#### BC-5: 记忆上下文（Memory Context）

**职责**：会话持久化、跨会话记忆、代码索引

```
聚合根: MemoryStore
├── 实体: SessionRecord（会话持久化记录）
│   ├── 值对象: SessionSummary（会话摘要）
│   └── 值对象: SessionMetadata（创建时间、模型、token 消耗等）
├── 实体: PersistentMemory（持久化记忆条目）
│   ├── 值对象: MemoryType（durable_fact | execution_state | distilled_knowledge）
│   └── 值对象: MemoryTTL（过期策略）
├── 实体: CodeIndex（代码库索引）（P2）
│   ├── 值对象: CodeChunk（语义代码块）
│   └── 值对象: Embedding（向量嵌入）
└── 服务: MemoryRetriever（记忆检索器）

领域事件:
├── SessionPersisted / SessionRestored
├── MemoryCreated / MemoryUpdated / MemoryExpired
├── CodeIndexUpdated
└── MemoryRetrievalCompleted
```

```typescript
interface MemoryStore {
  persistSession(session: Session): Promise<void>;
  restoreSession(sessionId: string): Promise<Session | null>;
  listSessions(limit: number): Promise<SessionSummary[]>;

  saveMemory(entry: MemoryEntry): Promise<void>;
  loadMemory(projectPath: string): Promise<MemoryEntry[]>;
  searchMemory(query: string, limit: number): Promise<MemoryEntry[]>;
}

interface MemoryEntry {
  readonly id: string;
  readonly type: MemoryType;
  readonly content: string;
  readonly projectPath: string;
  readonly createdAt: Date;
  readonly expiresAt?: Date;
  readonly metadata: Record<string, unknown>;
}

type MemoryType = 'durable_fact' | 'execution_state' | 'distilled_knowledge';
```

#### BC-6: 协调上下文（Coordination Context）

**职责**：多 Agent 协调、子 Agent 生命周期管理

```
聚合根: AgentCoordinator
├── 实体: WorkerAgent（子 Agent 实例）
│   ├── 值对象: WorkerConfig（模型、token 预算、超时、工具白名单）
│   ├── 值对象: WorkerStatus（pending | running | completed | failed | timeout）
│   └── 值对象: WorkerResult（摘要结果）
├── 值对象: TaskDescription（子任务描述）
└── 值对象: DepthLimit（递归深度限制）

领域事件:
├── WorkerSpawned / WorkerCompleted / WorkerFailed / WorkerTimedOut
├── TaskDelegated（任务被委派到子 Agent）
└── ResultAggregated（子 Agent 结果聚合）
```

```typescript
interface AgentCoordinator {
  spawnWorker(task: TaskDescription, config: WorkerConfig): Promise<WorkerHandle>;
  awaitWorker(handle: WorkerHandle): Promise<WorkerResult>;
  cancelWorker(handle: WorkerHandle): Promise<void>;
  getWorkerStatus(handle: WorkerHandle): WorkerStatus;
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

interface WorkerResult {
  readonly workerId: string;
  readonly status: 'completed' | 'failed' | 'timeout';
  readonly summary: string;
  readonly filesChanged: string[];
  readonly tokenUsed: number;
  readonly durationMs: number;
  readonly error?: string;
}
```

### 4.3 领域事件流

```
用户发送消息
    │
    ├─► TurnStarted
    │       │
    │       ├─► ContextAssembled { tokenUsage }
    │       │
    │       ├─► ToolCallRequested { toolName, input }
    │       │       │
    │       │       ├─► PermissionGranted | PermissionDenied | ApprovalRequested
    │       │       │
    │       │       ├─► ToolExecutionStarted
    │       │       │       │
    │       │       │       └─► ToolExecutionCompleted | ToolExecutionFailed
    │       │       │
    │       │       └─► ToolResultReceived { tokenCount }
    │       │               │
    │       │               └─► [如超限] ToolResultOffloaded
    │       │
    │       ├─► [如卡住] AgentStuck { failureMode }
    │       │
    │       ├─► [如需压缩] CompactionTriggered → CompactionCompleted
    │       │
    │       └─► TurnCompleted
    │
    ├─► SessionPersisted（异步）
    │
    └─► [如需记忆更新] MemoryCreated / MemoryUpdated（异步）
```

### 4.4 模块依赖关系

```
┌─────────────────────────────────────────────────────────────┐
│  依赖方向: 上层依赖下层，同层通过事件/接口通信               │
│                                                             │
│  @agent/core          ← 核心引擎，依赖所有下层               │
│    ├── @agent/tools   ← 工具系统                            │
│    ├── @agent/context ← 上下文管理                          │
│    ├── @agent/security← 安全系统                            │
│    ├── @agent/memory  ← 记忆系统                            │
│    └── @agent/coord   ← 协调系统                            │
│                                                             │
│  @agent/protocol      ← 协议层（JSON-RPC / SSE）            │
│    └── @agent/core                                          │
│                                                             │
│  @agent/cli           ← CLI 客户端                          │
│    └── @agent/protocol                                      │
│                                                             │
│  @agent/shared        ← 共享类型定义（全部包依赖）           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第五章：通用 AI Agent MVP 方案

### 5.1 MVP 范围定义

**目标**：2 周（10 个工作日）构建一个可工作的 CLI 编码 Agent，能完成简单的单文件/多文件代码修改任务。

**MVP 功能边界**（仅 P0）：

```
MVP 包含:                           MVP 不包含:
├── 流式 ReAct 循环                  ├── MCP 动态工具
├── 5 个核心工具                     ├── 沙箱隔离
│   (Read, Write, Edit, Bash, Glob) ├── 策略引擎（用硬编码规则代替）
├── 3 层提示词架构                   ├── 多 Agent 协调
├── Token 预算管理器                 ├── 代码库索引（RAG）
├── 工具结果 Hot Tail                ├── 自动压缩
├── 3 级权限检查（硬编码）           ├── 生命周期钩子
├── Prompt Caching                   ├── 错误恢复（StuckDetector）
├── 单模型（Anthropic Claude）       ├── Build→Verify→Fix 循环
├── 基础会话持久化                   ├── 多模型适配
├── 安全红线（硬编码规则）           └── 可观测性
└── 环境信息动态注入
```

### 5.2 MVP 技术选型（精简版）

| 组件 | MVP 选择 | 理由 |
|------|---------|------|
| 运行时 | TypeScript + Node.js 20 | 与全量方案一致 |
| LLM SDK | Vercel AI SDK (`ai`) | 多提供商，但 MVP 仅用 Anthropic |
| CLI | readline + chalk | 最简 CLI，不引入 ink 框架 |
| Schema | Zod | 工具输入校验 |
| 存储 | 文件系统（JSON 文件）| MVP 不引入 SQLite |
| 构建 | tsx (直接运行 TS) | 零配置，开发效率最高 |

### 5.3 项目目录结构

```
ai-agent/
├── package.json
├── tsconfig.json
├── .env                          # API Key 配置
│
├── src/
│   ├── index.ts                  # CLI 入口
│   │
│   ├── core/                     # Agent 核心
│   │   ├── agent-loop.ts         # ReAct 循环引擎
│   │   ├── stream-parser.ts      # 流式响应解析器
│   │   └── types.ts              # 核心类型定义
│   │
│   ├── prompt/                   # 提示词系统
│   │   ├── builder.ts            # 3 层提示词构建器
│   │   ├── templates/
│   │   │   ├── core.txt          # 核心层（身份+安全+行为）
│   │   │   ├── tools.txt         # 工具使用指南
│   │   │   └── providers/
│   │   │       └── anthropic.txt # Anthropic 特化指令
│   │   └── environment.ts        # 环境信息收集器
│   │
│   ├── context/                  # 上下文管理
│   │   ├── manager.ts            # 上下文组装器
│   │   ├── token-budget.ts       # Token 预算管理
│   │   └── tool-results.ts       # 工具结果管理（Hot Tail）
│   │
│   ├── tools/                    # 工具实现
│   │   ├── registry.ts           # 工具注册器
│   │   ├── executor.ts           # 工具执行器
│   │   ├── read.ts               # 读取文件
│   │   ├── write.ts              # 写入文件
│   │   ├── edit.ts               # 编辑文件（精确替换）
│   │   ├── bash.ts               # 执行 Shell 命令
│   │   └── glob.ts               # 文件搜索
│   │
│   ├── security/                 # 安全系统
│   │   ├── permission.ts         # 权限检查器（3 级）
│   │   └── rules.ts              # 安全红线规则（硬编码）
│   │
│   ├── memory/                   # 记忆系统
│   │   ├── session-store.ts      # 会话持久化（JSON 文件）
│   │   └── types.ts              # 记忆类型定义
│   │
│   └── utils/                    # 工具函数
│       ├── token-counter.ts      # Token 计数
│       └── logger.ts             # 日志
│
├── prompts/                      # 提示词模板文件
│   ├── core.txt
│   ├── tools.txt
│   └── providers/
│       └── anthropic.txt
│
├── data/                         # 运行时数据（.gitignore）
│   └── sessions/                 # 会话存储
│
└── tests/                        # 测试
    ├── agent-loop.test.ts
    ├── tools/
    └── fixtures/
```

### 5.4 逐日实施计划

```
Day 1: 项目骨架 + 类型定义
├── 初始化项目（package.json, tsconfig.json, .env）
├── 安装依赖（ai, @ai-sdk/anthropic, zod, chalk）
├── 定义核心类型（StreamEvent, Tool, ToolResult, Message, Session 等）
└── 验证: tsx src/index.ts 可运行

Day 2: 提示词系统
├── 实现 3 层提示词构建器（PromptBuilder）
├── 编写核心提示词模板（core.txt）
│   ├── 身份定义（一句话）
│   ├── 安全红线（5 条绝对规则）
│   ├── 核心行为（先读后改、验证结果等）
│   └── 输出规范
├── 编写工具使用指南模板（tools.txt）
├── 实现环境信息收集器（OS, CWD, Date, Git branch）
└── 验证: 构建完整系统提示词并打印

Day 3: Agent 循环引擎（核心）
├── 实现流式 ReAct 循环（agent-loop.ts）
│   ├── 调用 Anthropic API（流式 SSE）
│   ├── 流式中途检测 tool_use 块
│   ├── 收集 tool_result 并追加到消息历史
│   └── 循环终止条件判断
├── 实现流式响应解析器（stream-parser.ts）
└── 验证: 能进行基础对话（无工具调用）

Day 4: 工具系统（Read + Write + Glob）
├── 实现工具注册器（ToolRegistry）
├── 实现工具执行器（ToolExecutor）
├── 实现 Read 工具（读取文件，支持行号范围）
├── 实现 Write 工具（写入文件，自动创建目录）
├── 实现 Glob 工具（文件搜索，递归匹配）
└── 验证: Agent 能读写文件

Day 5: 工具系统（Edit + Bash）+ 权限
├── 实现 Edit 工具（精确字符串替换）
├── 实现 Bash 工具（执行 Shell 命令，超时控制）
├── 实现 3 级权限检查器
│   ├── safe: Read, Glob → 自动允许
│   ├── medium: Write, Edit → 自动允许（工作区内）
│   └── high: Bash → 需用户确认
├── 实现安全红线规则（rm -rf 禁止、.env 读取禁止等）
└── 验证: Agent 能做完整的代码修改 + 执行命令

Day 6: Token 预算 + 工具结果管理
├── 实现 Token 计数器（基于 tiktoken 或字符估算）
├── 实现 Token 预算管理器
│   ├── 分配各组件预算
│   └── 超限警告
├── 实现工具结果管理器（Hot Tail）
│   ├── 保留最近 5 个工具结果
│   ├── 旧结果仅保留调用记录（无内容）
│   └── 超过 2K tokens 的结果截断
└── 验证: 长对话不超出上下文限制

Day 7: Prompt Caching + 会话持久化
├── 实现 Prompt Caching（静态/动态分离 + cache_control 标记）
├── 实现会话持久化（JSON 文件存储）
│   ├── 保存会话历史
│   ├── 恢复会话（--resume 参数）
│   └── 列出历史会话（--list 参数）
└── 验证: 关闭终端后能恢复会话继续工作

Day 8: CLI 交互优化
├── 实现完整的 CLI 交互循环
│   ├── 流式输出（逐字符渲染）
│   ├── 工具调用展示（工具名 + 参数 + 结果摘要）
│   ├── 权限确认交互（Y/n 提示）
│   └── 错误展示（红色高亮）
├── 实现 /exit, /clear, /compact, /session 斜杠命令
└── 验证: 完整的用户交互体验

Day 9: 集成测试 + Bug 修复
├── 编写核心集成测试
│   ├── 测试 1: 单文件 Bug 修复（读取→定位→修改→验证）
│   ├── 测试 2: 新功能添加（创建文件→写入代码→执行测试）
│   ├── 测试 3: 安全红线测试（拒绝删除工作区外文件）
│   └── 测试 4: 长对话测试（10+ 轮对话不丢失上下文）
├── 修复发现的问题
└── 验证: 4 个测试全部通过

Day 10: 文档 + 发布准备
├── 编写 README.md（安装、配置、使用指南）
├── 编写 AGENTS.md（项目约定 + 指令模板示例）
├── 代码清理和注释
├── 最终端到端验证
│   └── 在一个真实项目上完成一个简单 Bug 修复
└── 打包发布（npm publish 或 GitHub Release）
```

### 5.5 后续路线图（MVP 后 8 周）

```
Phase 2: 安全与权限强化（第 3-4 周）
├── 实现沙箱隔离（文件系统路径限制 + 网络禁用）
├── 实现 Policy Engine（规则 + 优先级 + 决策）
├── 实现审批工作流（accept-once / accept-session / persist）
├── 实现 MCP 协议动态工具加载
├── 实现基础生命周期钩子（8 个事件）
└── 安全红线专项测试

Phase 3: 多 Agent + 错误恢复（第 5-6 周）
├── 实现 Controller-Worker 多 Agent 协调
├── 实现子 Agent 上下文隔离
├── 实现 StuckDetector（Repeater / Wanderer / Looper 检测）
├── 实现指数退避重试 + Circuit Breaker
├── 实现上下文注入式错误恢复
├── 实现 Plan / Build / Debug 工作模式切换
└── 故障注入测试

Phase 4: 上下文工程（第 7-8 周）
├── 集成 Tree-sitter 进行 AST 解析
├── 实现语义代码块向量嵌入
├── 实现 BM25 + 向量混合检索
├── 实现自动压缩（8 段结构化摘要 + "记忆转移"哲学）
├── 实现 MEMORY.md 持久化记忆
├── 实现跨会话记忆检索
└── 建立 ContextBench 评测

Phase 5: 验证闭环 + 生产优化（第 9-10 周）
├── 实现 Build → Verify → Self-Fix 循环
├── 集成类型检查 / Linter / 构建 / 测试 自动验证
├── 实现 OpenTelemetry 可观测性
├── 实现多模型提供商适配（OpenAI, Gemini）
├── SWE-bench Verified 基准测试
├── 性能优化: 工具并行执行
└── 成本优化: Token 消耗分析 + 压缩策略调优
```

### 5.6 MVP 成功标准

| 标准 | 指标 | 目标 |
|------|------|------|
| **基本可用** | 能完成简单的单文件 Bug 修复 | Day 5 达成 |
| **工具完备** | 5 个核心工具全部可用 | Day 5 达成 |
| **安全基线** | 安全红线零违反（5 条规则）| Day 5 达成 |
| **上下文稳定** | 10+ 轮对话不超出上下文限制 | Day 6 达成 |
| **成本可控** | Prompt Caching 命中率 > 80% | Day 7 达成 |
| **会话连续** | 关闭终端后能恢复会话继续工作 | Day 7 达成 |
| **集成测试** | 4 个核心测试用例全部通过 | Day 9 达成 |
| **端到端验证** | 在真实项目上完成一个 Bug 修复 | Day 10 达成 |

### 5.7 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 流式解析复杂度超预期 | 中 | Day 3 延期 | 使用 Vercel AI SDK 内建流式解析 |
| 工具结果过大导致上下文溢出 | 高 | 长对话失败 | Hot Tail 强制限制 + 大输出截断 |
| 权限检查遗漏高风险操作 | 中 | 安全事故 | 白名单策略（默认 deny，显式 allow）|
| Prompt Caching 未命中 | 低 | 成本增加 | 严格的静态/动态分离 + 哈希监控 |
| 模型幻觉调用不存在的工具 | 中 | 循环中断 | Schema 校验 + 优雅错误处理 |
