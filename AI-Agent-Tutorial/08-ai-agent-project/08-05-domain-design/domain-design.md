# 通用 AI Agent 领域设计方案

> 版本：V0.3 | 来源：[总体架构方案](../08-04-system-architecture/ai-agent-general-design-v0.3.md) | [需求规格](../08-03-requirement-analyse/requirement-specification.md)
>
> 采用领域驱动设计（DDD），将系统划分为 **10 个限界上下文**，定义聚合根、实体、值对象、领域事件和完整 TypeScript 接口。

---

## 目录

- [1. 战略设计：限界上下文地图](#1-战略设计限界上下文地图)
- [2. 限界上下文间通信契约](#2-限界上下文间通信契约)
- [3. BC-1 Agent Core（Agent 核心）](#3-bc-1-agent-coreagent-核心)
- [4. BC-2 Tool（工具）](#4-bc-2-tool工具)
- [5. BC-3 Context Management（上下文管理）](#5-bc-3-context-management上下文管理)
- [6. BC-4 Security（安全）](#6-bc-4-security安全)
- [7. BC-5 Memory（记忆）](#7-bc-5-memory记忆)
- [8. BC-6 Coordination（协调）](#8-bc-6-coordination协调)
- [9. BC-7 Skill（技能）](#9-bc-7-skill技能)
- [10. BC-8 MCP（模型上下文协议）](#10-bc-8-mcp模型上下文协议)
- [11. BC-9 Plugin（插件）](#11-bc-9-plugin插件)
- [12. BC-10 Automation（自动化）](#12-bc-10-automation自动化)
- [13. BC-11 LLM Provider（LLM 提供商）](#13-bc-11-llm-providerllm-提供商)
- [14. 领域事件全景流](#14-领域事件全景流)
- [15. 模块包结构与依赖关系](#15-模块包结构与依赖关系)

---

## 1. 战略设计：限界上下文地图

### 1.1 上下文划分

```
┌───────────────────────────────────────────────────────────────────────┐
│                       限界上下文关系地图                                │
│                                                                       │
│                      ┌─────────────────────┐                          │
│                      │   BC-1 Agent Core    │                         │
│                      │   (核心编排引擎)       │                         │
│                      └──────────┬──────────┘                          │
│                                 │                                      │
│        ┌──────────┬─────────────┼──────────────┬──────────┐           │
│        │          │             │              │          │           │
│   ┌────▼───┐ ┌───▼─────┐ ┌────▼────┐ ┌──────▼───┐ ┌───▼──────┐    │
│   │ BC-2   │ │ BC-3    │ │ BC-4    │ │ BC-5     │ │ BC-6     │    │
│   │ Tool   │ │ Context │ │Security │ │ Memory   │ │Coordinat.│    │
│   │ (工具)  │ │ (上下文) │ │ (安全)   │ │ (记忆)    │ │ (协调)    │    │
│   └───┬────┘ └────┬────┘ └─────────┘ └─────┬────┘ └──────────┘    │
│       │           │                         │                       │
│  ┌────▼───┐  ┌───▼────┐               ┌───▼──────┐                │
│  │ BC-7   │  │ BC-8   │               │ BC-10    │                │
│  │ Skill  │  │ MCP    │               │Automation│                │
│  │ (技能)  │  │        │               │ (自动化)  │                │
│  └────────┘  └───┬────┘               └──────────┘                │
│                  │                                                  │
│             ┌────▼───┐    ┌────────────┐                           │
│             │ BC-9   │    │ BC-11      │                           │
│             │ Plugin │    │ LLM        │                           │
│             │ (插件)  │    │ Provider   │                           │
│             └────────┘    │ (LLM提供商)│                           │
│                           └────────────┘                           │
└───────────────────────────────────────────────────────────────────────┘
```

### 1.2 上下文职责摘要

| BC | 名称 | 职责 | 聚合根 | 对应需求域 |
|----|------|------|--------|-----------|
| BC-1 | Agent Core | 循环引擎编排，Turn/Session 生命周期 | AgentLoop | FR-1 |
| BC-2 | Tool | 工具注册、Schema 校验、执行调度 | ToolRegistry | FR-2 |
| BC-3 | Context | 提示词构建、Token 预算、压缩、检索 | ContextManager | FR-3, FR-4 |
| BC-4 | Security | 权限检查、策略引擎、沙箱、审批 | PolicyEngine | FR-5 |
| BC-5 | Memory | 会话持久化、跨会话记忆、代码索引 | MemoryStore | FR-7 |
| BC-6 | Coordination | 多 Agent 编排、子 Agent 生命周期 | AgentCoordinator | FR-6 |
| BC-7 | Skill | 技能注册/发现/匹配/执行 | SkillRegistry | FR-10 |
| BC-8 | MCP | MCP Server 管理、工具发现/转发 | MCPManager | FR-11 |
| BC-9 | Plugin | 插件加载/激活/钩子回调 | PluginHost | FR-12 |
| BC-10 | Automation | 定时任务/文件监听/Webhook/通知 | Scheduler | FR-13 |
| BC-11 | LLM Provider | 多提供商注册/切换/模型路由 | ProviderRegistry | FR-3.3, NFR-5.2~3 |

---

## 2. 限界上下文间通信契约

### 2.1 通信模式

| 调用方 | 被调用方 | 模式 | 理由 |
|--------|---------|------|------|
| Core → Tool | Tool | 同步直调 | 工具执行在循环关键路径上 |
| Core → Context | Context | 同步直调 | 上下文组装在每轮推理前必须完成 |
| Core → Security | Security | 同步直调 | 权限检查必须在工具执行前完成 |
| Core → LLM Provider | LLM Provider | 同步直调 | LLM 调用在循环关键路径上 |
| Core → Coordination | Coordination | 同步直调 | 子 Agent 生成是同步操作 |
| Core ↔ Skill | Skill | 同步直调 | 技能内容注入/卸载在上下文组装时 |
| Core ↔ Plugin | Plugin | 钩子回调 | 插件通过生命周期钩子同步拦截 |
| Core → Memory | Memory | **异步事件** | 会话持久化不阻塞循环 |
| Core → Automation | Automation | **异步事件** | 自动化触发检查不阻塞循环 |
| Tool → MCP | MCP | 同步直调 | MCP 工具调用通过协议转发 |
| Tool → Security | Security | 同步直调 | 每次工具执行前检查权限 |

### 2.2 防腐层（Anti-Corruption Layer）

```
外部系统边界需要防腐层:

┌──────────────┐     ┌──────────┐     ┌──────────────┐
│ MCP Server   │ ←── │ ACL:     │ ←── │ BC-8 MCP     │
│ (外部进程)    │     │ MCPClient│     │              │
└──────────────┘     └──────────┘     └──────────────┘

┌──────────────┐     ┌──────────┐     ┌──────────────┐
│ LLM API      │ ←── │ ACL:     │ ←── │ BC-11 LLM    │
│ (Anthropic/  │     │ Vercel   │     │ Provider     │
│  Qwen/GPT)   │     │ AI SDK   │     │              │
└──────────────┘     └──────────┘     └──────────────┘

┌──────────────┐     ┌──────────┐     ┌──────────────┐
│ 文件系统/Git  │ ←── │ ACL:     │ ←── │ BC-2 Tool    │
│ (OS)         │     │ Sandbox  │     │              │
└──────────────┘     └──────────┘     └──────────────┘

防腐层职责：
├── 将外部系统的概念翻译为领域内概念
├── 隔离外部系统变化对领域模型的影响
└── 在边界处执行安全校验
```

---

## 3. BC-1 Agent Core（Agent 核心）

**职责**：Agent 循环引擎的核心编排，管理 Turn/Message 生命周期，驱动整个感知→推理→行动→观察循环。

### 3.1 领域模型

```
聚合根: AgentLoop
│
├── 实体: Session（持久化会话容器）
│   ├── 值对象: SessionId                   (string, UUID)
│   ├── 值对象: SessionConfig               (model, permissionMode, workMode)
│   ├── 值对象: Checkpoint                  (turnIndex, messageIndex, timestamp)
│   └── 集合: Turn[]
│
├── 实体: Turn（一次完整的 Agent 工作单元）
│   ├── 值对象: TurnId                      (string, UUID)
│   ├── 值对象: TurnTiming                  (startedAt, completedAt, durationMs)
│   ├── 集合: Message[]
│   ├── 集合: ToolCall[]
│   └── 集合: ToolResult[]
│
├── 值对象: Message                          (role, content, timestamp)
├── 值对象: ToolCall                         (id, toolName, input)
├── 值对象: ToolResult                       (callId, toolName, output, tokenCount, error?)
├── 值对象: WorkMode                         ('plan' | 'build' | 'debug')
└── 值对象: StreamEvent                      (text | tool_call | tool_result | approval_request | error | done)
```

### 3.2 领域事件

| 事件 | 载荷 | 触发时机 | 消费者 |
|------|------|---------|--------|
| `TurnStarted` | { turnId, sessionId, timestamp } | 新一轮循环开始 | Memory, Automation |
| `TurnCompleted` | { turnId, toolCallCount, durationMs } | 循环结束 | Memory, Plugin |
| `ToolCallRequested` | { turnId, toolName, input } | 模型请求工具调用 | Tool, Security, Plugin |
| `ToolResultReceived` | { turnId, toolName, tokenCount } | 工具执行完成 | Context(Hot Tail), Plugin |
| `SessionCreated` | { sessionId, config } | 新会话启动 | Memory |
| `SessionResumed` | { sessionId, checkpoint } | 会话恢复 | Memory |
| `SessionEnded` | { sessionId, totalTurns, totalTokens } | 会话结束 | Memory, Automation |
| `AgentStuck` | { turnId, failureMode, recentActions } | 检测到卡住 | Core(自恢复) |

### 3.3 TypeScript 接口

```typescript
// ─── 聚合根 ───
interface AgentLoop {
  readonly sessionId: string;
  readonly mode: WorkMode;
  readonly isRunning: boolean;

  run(input: UserInput): AsyncGenerator<StreamEvent>;
  interrupt(): void;
  resume(checkpoint: Checkpoint): AsyncGenerator<StreamEvent>;
  switchMode(mode: WorkMode): void;
  getSession(): Session;
}

// ─── 实体 ───
interface Session {
  readonly id: string;
  readonly config: SessionConfig;
  readonly turns: Turn[];
  readonly createdAt: Date;
  checkpoint?: Checkpoint;
  readonly totalTokensUsed: number;
}

interface Turn {
  readonly id: string;
  readonly messages: Message[];
  readonly toolCalls: ToolCall[];
  readonly toolResults: ToolResult[];
  readonly timing: TurnTiming;
}

// ─── 值对象 ───
type WorkMode = 'plan' | 'build' | 'debug';

interface SessionConfig {
  model: string;
  permissionMode: 'ask-all' | 'workspace-write' | 'full-auto';
  workMode: WorkMode;
  maxTurns?: number;
  tokenBudget?: number;
}

interface Message {
  readonly role: 'user' | 'assistant' | 'system';
  readonly content: string;
  readonly timestamp: Date;
}

interface ToolCall {
  readonly id: string;
  readonly toolName: string;
  readonly input: unknown;
}

interface ToolResult {
  readonly callId: string;
  readonly toolName: string;
  readonly output: string;
  readonly tokenCount: number;
  readonly durationMs: number;
  readonly error?: string;
}

interface Checkpoint {
  readonly turnIndex: number;
  readonly messageIndex: number;
  readonly timestamp: Date;
}

interface TurnTiming {
  readonly startedAt: Date;
  completedAt?: Date;
  readonly durationMs?: number;
}

type StreamEvent =
  | { type: 'text'; content: string }
  | { type: 'tool_call'; id: string; tool: string; input: unknown }
  | { type: 'tool_result'; id: string; tool: string; output: unknown }
  | { type: 'approval_request'; id: string; tool: string; reason: string }
  | { type: 'error'; error: AgentError }
  | { type: 'done'; summary: string };

interface AgentError {
  code: string;
  message: string;
  recoverable: boolean;
  context?: Record<string, unknown>;
}

// ─── 领域事件 ───
type AgentCoreEvent =
  | { type: 'TurnStarted'; turnId: string; sessionId: string; timestamp: Date }
  | { type: 'TurnCompleted'; turnId: string; toolCallCount: number; durationMs: number }
  | { type: 'ToolCallRequested'; turnId: string; toolName: string; input: unknown }
  | { type: 'ToolResultReceived'; turnId: string; toolName: string; tokenCount: number }
  | { type: 'SessionCreated'; sessionId: string; config: SessionConfig }
  | { type: 'SessionResumed'; sessionId: string; checkpoint: Checkpoint }
  | { type: 'SessionEnded'; sessionId: string; totalTurns: number; totalTokens: number }
  | { type: 'AgentStuck'; turnId: string; failureMode: FailureMode; recentActions: string[] };

type FailureMode = 'repeater' | 'wanderer' | 'looper';
```

---

## 4. BC-2 Tool（工具）

**职责**：工具注册、输入 Schema 校验、执行调度、超时控制、健康检查。

### 4.1 领域模型

```
聚合根: ToolRegistry
│
├── 实体: Tool（注册的工具实例）
│   ├── 值对象: ToolName                    (string)
│   ├── 值对象: ToolDescription             (string, 供 LLM 理解)
│   ├── 值对象: ToolSchema                  (ZodSchema, 输入校验)
│   ├── 值对象: RiskLevel                   ('safe'|'medium'|'high'|'forbidden')
│   ├── 值对象: ToolTimeout                 (number, ms)
│   ├── 值对象: ToolHealth                  ('healthy'|'degraded'|'unavailable')
│   └── 值对象: ToolSource                  ('builtin'|'mcp'|'plugin')
│
└── 服务: ToolExecutor（工具执行调度器）
    ├── 输入校验 → 权限检查 → 执行 → 结果收集
    └── 支持串行和并行执行
```

### 4.2 领域事件

| 事件 | 载荷 | 消费者 |
|------|------|--------|
| `ToolRegistered` | { name, source, riskLevel } | Context(更新工具定义) |
| `ToolUnregistered` | { name } | Context |
| `ToolExecutionStarted` | { callId, toolName, input } | Plugin(PreToolUse) |
| `ToolExecutionCompleted` | { callId, toolName, durationMs, tokenCount } | Context(Hot Tail), Plugin(PostToolUse) |
| `ToolExecutionFailed` | { callId, toolName, error } | Core(错误恢复), Plugin |
| `ToolHealthChanged` | { name, oldStatus, newStatus } | Core(降级处理) |

### 4.3 TypeScript 接口

```typescript
// ─── 聚合根 ───
interface ToolRegistry {
  register(tool: Tool): void;
  unregister(name: string): void;
  get(name: string): Tool | undefined;
  has(name: string): boolean;
  list(): ToolDescriptor[];
  listByRisk(level: RiskLevel): ToolDescriptor[];
  healthCheck(): Promise<Map<string, ToolHealth>>;
}

// ─── 实体 ───
interface Tool {
  readonly name: string;
  readonly description: string;
  readonly schema: ZodSchema;
  readonly riskLevel: RiskLevel;
  readonly timeout: number;
  readonly source: ToolSource;

  execute(input: unknown, ctx: ExecutionContext): Promise<ToolResult>;
}

// ─── 值对象 ───
type RiskLevel = 'safe' | 'medium' | 'high' | 'forbidden';
type ToolHealth = 'healthy' | 'degraded' | 'unavailable';
type ToolSource = 'builtin' | 'mcp' | 'plugin';

interface ToolDescriptor {
  name: string;
  description: string;
  riskLevel: RiskLevel;
  source: ToolSource;
  inputSchema: Record<string, unknown>;
}

interface ExecutionContext {
  sessionId: string;
  workspacePath: string;
  permissions: PermissionMode;
  abortSignal: AbortSignal;
}

// ─── 服务 ───
interface ToolExecutor {
  execute(call: ToolCall, ctx: ExecutionContext): Promise<ToolResult>;
  executeParallel(calls: ToolCall[], ctx: ExecutionContext): Promise<ToolResult[]>;
}
```

---

## 5. BC-3 Context Management（上下文管理）

**职责**：3 层提示词构建、Token 预算分配与监控、工具结果生命周期管理、上下文压缩。

### 5.1 领域模型

```
聚合根: ContextManager
│
├── 实体: PromptBuilder（3 层提示词构建器）
│   ├── 值对象: CorePrompt                  (身份+安全+行为，可缓存)
│   ├── 值对象: ScenarioPrompt              (工具指南+工作模式，按需加载)
│   └── 值对象: DynamicPrompt               (环境+记忆+用户偏好，每次变化)
│
├── 实体: TokenBudgetManager（Token 预算管理器）
│   └── 值对象: TokenBudget                 (各组件的预算分配)
│
├── 实体: Compactor（压缩管理器）
│   ├── 值对象: CompactionStrategy          ('micro'|'auto'|'full')
│   └── 值对象: CompactionTemplate          (8 段结构化摘要模板)
│
└── 实体: ToolResultManager（工具结果管理器）
    ├── 值对象: HotTail                     (最近 N 个活跃结果)
    └── 值对象: ColdReference               (已卸载结果的引用)
```

### 5.2 领域事件

| 事件 | 载荷 | 消费者 |
|------|------|--------|
| `ContextAssembled` | { tokenUsage: TokenBudget, cacheHit: boolean } | Core, Plugin(telemetry) |
| `CompactionTriggered` | { strategy, currentTokens, threshold } | Plugin(PreCompact) |
| `CompactionCompleted` | { tokensBefore, tokensAfter, sectionsPreserved } | Core |
| `TokenBudgetExceeded` | { component, allocated, actual } | Core(触发压缩) |
| `ToolResultOffloaded` | { callId, tokenCount, storagePath } | -- |

### 5.3 TypeScript 接口

```typescript
// ─── 聚合根 ───
interface ContextManager {
  bootstrap(config: ProjectConfig): Promise<void>;
  assemble(query: string, history: Message[]): Promise<AssembledContext>;
  compact(strategy: CompactionStrategy): Promise<CompactionResult>;
  getTokenUsage(): TokenUsageReport;
}

// ─── 实体/值对象 ───
interface AssembledContext {
  readonly systemPrompt: string;
  readonly tools: ToolDefinition[];
  readonly messages: Message[];
  readonly tokenUsage: TokenBudget;
  readonly cacheControl: CacheConfig;
  readonly skillDescriptors: SkillDescriptor[];
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
  available: number;
}

type CompactionStrategy = 'micro' | 'auto' | 'full';

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

interface CompactionResult {
  tokensBefore: number;
  tokensAfter: number;
  compressionRatio: number;
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

interface ColdReference {
  callId: string;
  toolName: string;
  timestamp: Date;
  storagePath?: string;
}

interface CacheConfig {
  staticPartHash: string;
  cacheControl: { type: 'ephemeral' };
}

interface TokenUsageReport {
  budget: TokenBudget;
  history: Array<{ timestamp: Date; usage: TokenBudget }>;
}
```

---

## 6. BC-4 Security（安全）

**职责**：工具级权限检查、规则化策略引擎、OS 级沙箱、人类审批工作流。

### 6.1 领域模型

```
聚合根: PolicyEngine
│
├── 实体: PolicyRule（策略规则）
│   ├── 值对象: RuleId                      (string, UUID)
│   ├── 值对象: RuleCondition               (tool?, argsPattern?, environment?)
│   ├── 值对象: RuleDecision                ('allow'|'deny'|'ask_user')
│   ├── 值对象: RulePriority                (number, 越高越优先)
│   └── 值对象: RuleReason                  (string, 人类可读说明)
│
├── 实体: ApprovalRecord（审批记录）
│   ├── 值对象: ApprovalScope               ('once'|'session'|'persist')
│   └── 值对象: ApprovalTimestamp            (Date)
│
├── 实体: Sandbox（沙箱配置）
│   ├── 值对象: FileSystemPolicy            (allowedPaths, deniedPaths)
│   ├── 值对象: NetworkPolicy               (allowedHosts, denyAll)
│   └── 值对象: ProcessPolicy               (allowedCommands, deniedPatterns)
│
└── 服务: PermissionChecker（组合策略引擎+沙箱+审批记录）
```

### 6.2 领域事件

| 事件 | 载荷 | 消费者 |
|------|------|--------|
| `PermissionGranted` | { toolName, ruleId? } | Tool(执行) |
| `PermissionDenied` | { toolName, reason } | Core(跳过此工具调用) |
| `ApprovalRequested` | { toolName, reason } | Core(向用户请求) |
| `ApprovalReceived` | { toolName, scope, approved } | PolicyEngine(记录) |
| `PolicyRuleAdded` | { ruleId, condition, decision } | -- |
| `SecurityViolationAttempted` | { toolName, violationType, details } | Plugin(notify), Memory(记录) |

### 6.3 TypeScript 接口

```typescript
// ─── 聚合根 ───
interface PolicyEngine {
  addRule(rule: PolicyRule): void;
  removeRule(id: string): void;
  getRules(): PolicyRule[];
  evaluate(toolCall: ToolCall, ctx: SecurityContext): Decision;
  recordApproval(toolCall: ToolCall, scope: ApprovalScope): void;
  hasApproval(toolCall: ToolCall): boolean;
}

// ─── 实体/值对象 ───
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

type ApprovalScope = 'once' | 'session' | 'persist';
type PermissionMode = 'ask-all' | 'workspace-write' | 'full-auto';

interface SecurityContext {
  sessionId: string;
  workspacePath: string;
  permissionMode: PermissionMode;
}

interface Sandbox {
  readonly fileSystemPolicy: FileSystemPolicy;
  readonly networkPolicy: NetworkPolicy;
  readonly processPolicy: ProcessPolicy;

  validateFileAccess(path: string, mode: 'read' | 'write' | 'delete'): boolean;
  validateNetworkAccess(url: string): boolean;
  validateProcessExecution(command: string): boolean;
}

interface FileSystemPolicy {
  allowedPaths: string[];
  deniedPaths: string[];
}

interface NetworkPolicy {
  denyAll: boolean;
  allowedHosts: string[];
}

interface ProcessPolicy {
  deniedPatterns: RegExp[];
}
```

---

## 7. BC-5 Memory（记忆）

**职责**：会话持久化/恢复、项目级持久化记忆、跨会话语义检索、代码索引。

### 7.1 领域模型

```
聚合根: MemoryStore
│
├── 实体: SessionRecord（会话持久化记录）
│   ├── 值对象: SessionSummary              (简短摘要)
│   └── 值对象: SessionMetadata             (创建时间, 模型, tokenUsed, turnCount)
│
├── 实体: PersistentMemory（持久化记忆条目）
│   ├── 值对象: MemoryId                    (string, UUID)
│   ├── 值对象: MemoryType                  ('durable_fact'|'execution_state'|'distilled_knowledge')
│   ├── 值对象: MemoryContent               (string)
│   ├── 值对象: MemoryTTL                   (expiresAt?)
│   └── 值对象: MemoryMetadata              (projectPath, tags, source)
│
├── 实体: CodeIndex（代码库索引，P2）
│   ├── 值对象: CodeChunk                   (filePath, startLine, endLine, content, symbolName)
│   └── 值对象: Embedding                   (vector: number[], model: string)
│
└── 服务: MemoryRetriever（记忆检索器，支持语义搜索）
```

### 7.2 领域事件

| 事件 | 载荷 | 消费者 |
|------|------|--------|
| `SessionPersisted` | { sessionId, path } | -- |
| `SessionRestored` | { sessionId, turnCount } | Core |
| `MemoryCreated` | { memoryId, type, content } | -- |
| `MemoryUpdated` | { memoryId, oldContent, newContent } | -- |
| `MemoryExpired` | { memoryId } | -- |
| `CodeIndexUpdated` | { filesIndexed, chunksCreated } | Context(检索可用) |

### 7.3 TypeScript 接口

```typescript
// ─── 聚合根 ───
interface MemoryStore {
  persistSession(session: Session): Promise<void>;
  restoreSession(sessionId: string): Promise<Session | null>;
  listSessions(limit: number): Promise<SessionSummary[]>;
  deleteSession(sessionId: string): Promise<void>;

  saveMemory(entry: MemoryEntry): Promise<void>;
  updateMemory(id: string, content: string): Promise<void>;
  deleteMemory(id: string): Promise<void>;
  loadMemory(projectPath: string): Promise<MemoryEntry[]>;
  searchMemory(query: string, limit: number): Promise<MemoryEntry[]>;
}

// ─── 实体/值对象 ───
interface MemoryEntry {
  readonly id: string;
  readonly type: MemoryType;
  readonly content: string;
  readonly projectPath: string;
  readonly createdAt: Date;
  readonly updatedAt: Date;
  readonly expiresAt?: Date;
  readonly metadata: MemoryMetadata;
}

type MemoryType = 'durable_fact' | 'execution_state' | 'distilled_knowledge';

interface MemoryMetadata {
  tags: string[];
  source: 'user' | 'agent' | 'system';
  relatedSessionId?: string;
}

interface SessionSummary {
  id: string;
  summary: string;
  createdAt: Date;
  turnCount: number;
  tokenUsed: number;
  model: string;
}

interface CodeChunk {
  filePath: string;
  startLine: number;
  endLine: number;
  content: string;
  symbolName?: string;
  symbolType?: 'function' | 'class' | 'method' | 'interface' | 'module';
}
```

---

## 8. BC-6 Coordination（协调）

**职责**：多 Agent 编排（Controller-Worker 模式）、子 Agent 生命周期管理、结果聚合。

### 8.1 领域模型

```
聚合根: AgentCoordinator
│
├── 实体: WorkerAgent（子 Agent 实例）
│   ├── 值对象: WorkerId                    (string, UUID)
│   ├── 值对象: WorkerConfig                (model, maxTokens, timeout, tools, depthLimit)
│   ├── 值对象: WorkerStatus                ('pending'|'running'|'completed'|'failed'|'timeout')
│   └── 值对象: WorkerResult                (summary, filesChanged, tokenUsed, durationMs)
│
├── 值对象: TaskDescription                  (prompt, context, constraints)
└── 值对象: DepthLimit                       (maxDepth: number, currentDepth: number)
```

### 8.2 TypeScript 接口

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

interface TaskDescription {
  prompt: string;
  context?: string;
  constraints?: string[];
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

type WorkerStatus = 'pending' | 'running' | 'completed' | 'failed' | 'timeout';
```

---

## 9. BC-7 Skill（技能）

**职责**：技能发现/注册/匹配/触发、内容按需加载与卸载、远程技能安装。

### 9.1 领域模型

```
聚合根: SkillRegistry
│
├── 实体: Skill
│   ├── 值对象: SkillName                   (string)
│   ├── 值对象: SkillDescription            (string, 一行描述，常驻上下文)
│   ├── 值对象: SkillVersion                (semver string)
│   ├── 值对象: SkillContent                (string, 完整 Markdown 指导内容)
│   ├── 值对象: SkillTrigger[]              (pattern | event | command)
│   ├── 值对象: SkillRequirement            (requiresTools, requiresPermissions)
│   ├── 值对象: SkillModelPreference        (string?)
│   └── 值对象: SkillSource                 ('builtin'|'project'|'global'|'remote')
│
├── 服务: SkillMatcher（匹配用户输入或事件到技能）
└── 服务: SkillInstaller（从 npm/git 安装远程技能）
```

### 9.2 TypeScript 接口

```typescript
interface Skill {
  readonly name: string;
  readonly description: string;
  readonly version: string;
  readonly triggers: SkillTrigger[];
  readonly requiresTools: string[];
  readonly requiresPermissions: RiskLevel[];
  readonly modelPreference?: string;
  readonly content: string;
  readonly source: SkillSource;
}

type SkillTrigger =
  | { type: 'pattern'; pattern: string | RegExp }
  | { type: 'event'; event: HookEvent; tool?: string }
  | { type: 'command'; command: string };

type SkillSource = 'builtin' | 'project' | 'global' | 'remote';

interface SkillRegistry {
  register(skill: Skill): void;
  unregister(name: string): void;
  discover(directories: string[]): Promise<Skill[]>;
  match(input: string): Skill | null;
  matchEvent(event: HookEvent, data: HookData): Skill | null;
  getDescriptors(): SkillDescriptor[];
  getFullContent(name: string): string;
  install(source: string): Promise<Skill>;
  list(): SkillInfo[];
}

interface SkillDescriptor {
  name: string;
  description: string;
  triggers: string[];
}

// 内建技能清单（15 个）
type BuiltinSkillName =
  | 'code-review' | 'refactor' | 'add-tests'
  | 'git-commit' | 'create-pr' | 'resolve-conflict'
  | 'init-project' | 'update-deps'
  | 'generate-docs' | 'explain-codebase'
  | 'debug-error' | 'performance-profile'
  | 'security-audit' | 'deploy' | 'deep-research';
```

---

## 10. BC-8 MCP（模型上下文协议）

**职责**：MCP Server 生命周期管理、工具发现与注册转发、健康监控与自动重连。

### 10.1 领域模型

```
聚合根: MCPManager
│
├── 实体: MCPConnection
│   ├── 值对象: MCPServerName               (string)
│   ├── 值对象: MCPServerConfig             (command, args, env, permission, timeout, transport)
│   ├── 值对象: MCPServerStatus             ('starting'|'ready'|'error'|'closed')
│   └── 值对象: MCPTransport               ('stdio'|'sse')
│
├── 服务: MCPClient（协议通信：初始化/工具发现/调用转发/关闭）
└── 服务: MCPHealthMonitor（心跳检测、崩溃重连）
```

### 10.2 TypeScript 接口

```typescript
interface MCPManager {
  loadConfig(paths: string[]): Promise<MCPConfig>;
  startServer(name: string): Promise<MCPClient>;
  startAll(): Promise<Map<string, MCPClient>>;
  stopServer(name: string): Promise<void>;
  stopAll(): Promise<void>;
  getClient(name: string): MCPClient | undefined;
  listServers(): MCPServerInfo[];
}

interface MCPClient {
  readonly serverName: string;
  readonly status: MCPServerStatus;

  initialize(): Promise<void>;
  listTools(): Promise<MCPToolDescriptor[]>;
  callTool(name: string, args: unknown): Promise<MCPToolResult>;
  close(): Promise<void>;
  onHealthChange(cb: (status: MCPServerStatus) => void): void;
}

type MCPServerStatus = 'starting' | 'ready' | 'error' | 'closed';

interface MCPConfig {
  servers: Record<string, MCPServerConfig>;
}

interface MCPServerConfig {
  command: string;
  args?: string[];
  env?: Record<string, string>;
  permission: 'allow' | 'ask_user' | 'deny';
  timeout?: number;
  transport?: 'stdio' | 'sse';
  url?: string;
}
```

---

## 11. BC-9 Plugin（插件）

**职责**：插件发现/加载/激活/停用、钩子回调、运行时行为拦截与增强。

### 11.1 领域模型

```
聚合根: PluginHost
│
├── 实体: PluginInstance
│   ├── 值对象: PluginManifest              (name, version, description, entry, hooks, permissions, config)
│   ├── 值对象: PluginStatus                ('discovered'|'loaded'|'active'|'error'|'deactivated')
│   └── 值对象: PluginConfig                (Record<string, unknown>)
│
├── 服务: PluginLoader（动态 import 加载模块）
└── 服务: PluginSandbox（插件隔离运行，错误不崩主循环）
```

### 11.2 TypeScript 接口

```typescript
interface Plugin {
  readonly name: string;
  readonly version: string;
  readonly description: string;

  activate(ctx: PluginContext): Promise<void>;
  deactivate?(): Promise<void>;
}

interface PluginContext {
  readonly config: Record<string, unknown>;
  readonly logger: Logger;

  hooks: HookSystem;
  tools: ToolRegistry;
  memory: MemoryStore;
  session: Session;

  onSystemPromptBuild(handler: (prompt: string) => string): void;
  onContextAssemble(handler: (ctx: AssembledContext) => AssembledContext): void;
}

interface PluginHost {
  discover(sources: PluginSource[]): Promise<PluginManifest[]>;
  load(manifest: PluginManifest): Promise<Plugin>;
  activate(plugin: Plugin): Promise<void>;
  deactivate(name: string): Promise<void>;
  listActive(): PluginInfo[];
  listAll(): PluginInfo[];
}

type PluginSource =
  | { type: 'directory'; path: string }
  | { type: 'npm'; package: string }
  | { type: 'builtin' };

interface PluginManifest {
  name: string;
  version: string;
  description: string;
  entry: string;
  hooks: HookEvent[];
  permissions: RiskLevel[];
  config?: Record<string, unknown>;
}

// 内建插件
type BuiltinPluginName =
  | 'eslint' | 'prettier' | 'git-guard' | 'cost-tracker'
  | 'changelog' | 'notify' | 'telemetry' | 'i18n';
```

---

## 12. BC-10 Automation（自动化）

**职责**：Cron 定时调度、文件变更监听、Webhook 事件接收、独立会话任务执行、多渠道通知。

### 12.1 领域模型

```
聚合根: Scheduler
│
├── 实体: ScheduledTask（计划任务）
│   ├── 值对象: TaskId                      (string, UUID)
│   ├── 值对象: TaskSchedule                (CronExpression | WatchPattern | WebhookTrigger)
│   ├── 值对象: TaskConfig                  (timeout, notify, permissions, tokenBudget, skill?)
│   ├── 值对象: TaskMode                    ('foreground'|'background'|'dry-run')
│   └── 值对象: TaskStatus                  ('scheduled'|'running'|'completed'|'failed'|'paused')
│
├── 实体: TaskExecution（单次执行记录）
│   ├── 值对象: ExecutionResult             (status, output, tokenUsed, durationMs)
│   └── 值对象: ExecutionReport             (reportPath)
│
├── 服务: TaskRunner（独立会话执行 + 隔离）
├── 服务: FileWatcher（chokidar 文件监听 + 防抖 + 聚合）
└── 服务: NotificationService（终端/文件/Slack/Webhook 通知）
```

### 12.2 TypeScript 接口

```typescript
interface Scheduler {
  loadConfig(path: string): Promise<AutomationConfig>;
  scheduleTask(task: ScheduledTask): string;
  cancelTask(taskId: string): void;
  pauseTask(taskId: string): void;
  resumeTask(taskId: string): void;
  listTasks(): TaskInfo[];
  getTaskHistory(taskId: string): TaskExecution[];
}

interface ScheduledTask {
  name: string;
  schedule: CronSchedule | WatcherConfig | WebhookConfig;
  task: string;
  skill?: string;
  mode: 'foreground' | 'background' | 'dry-run';
  timeout?: number;
  notify?: NotifyConfig;
  permissions?: RiskLevel;
  tokenBudget?: number;
}

type CronSchedule = { type: 'cron'; expression: string };
type WatcherConfig = { type: 'watcher'; pattern: string; event: string; debounce?: number };
type WebhookConfig = { type: 'webhook'; trigger: string };

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

interface NotifyConfig {
  channels: Array<'terminal' | 'file' | 'slack' | 'webhook'>;
  webhookUrl?: string;
  slackChannel?: string;
}
```

---

## 13. BC-11 LLM Provider（LLM 提供商）

**职责**：多 LLM 提供商注册/切换、模型路由策略、Provider 级提示词适配。

### 13.1 领域模型

```
聚合根: ProviderRegistry
│
├── 实体: ProviderInstance（提供商实例）
│   ├── 值对象: ProviderName                (string, 如 'anthropic', 'qwen', 'deepseek')
│   ├── 值对象: ProviderConfig              (package, apiKey, baseURL, promptFile, models)
│   ├── 值对象: ProviderStatus              ('ready'|'error'|'unconfigured')
│   └── 值对象: ProviderType                ('official'|'openai-compatible'|'custom')
│
├── 值对象: ModelId                          (string, 格式 'provider:model', 如 'qwen:qwen-max')
├── 值对象: DefaultModel                     (ModelId)
│
└── 服务: ModelRouter（按任务类型路由到最适合的模型）
    ├── 策略: 高质量编码 → claude-sonnet-4 / qwen-max
    ├── 策略: 快速搜索 → qwen-turbo / deepseek-chat
    ├── 策略: 长上下文 → gemini-2.5-pro
    └── 策略: 成本敏感 → qwen-turbo / deepseek-chat
```

### 13.2 领域事件

| 事件 | 载荷 | 消费者 |
|------|------|--------|
| `ProviderRegistered` | { name, type, models } | Context(更新可用模型列表) |
| `ProviderSwitched` | { oldModel, newModel, reason } | Context(重新构建提示词) |
| `ProviderError` | { name, error } | Core(降级到备用模型) |
| `ModelRouted` | { taskType, selectedModel, reason } | Plugin(telemetry) |

### 13.3 TypeScript 接口

```typescript
interface ProviderRegistry {
  register(name: string, config: ProviderConfig): void;
  unregister(name: string): void;
  get(modelId: string): LanguageModel;
  getDefault(): LanguageModel;
  setDefault(modelId: string): void;
  list(): ProviderInfo[];
  getPromptFile(providerName: string): string | undefined;
}

interface ProviderConfig {
  package: string;
  apiKey?: string;
  baseURL?: string;
  promptFile?: string;
  models?: Record<string, string>;
}

interface ProviderInfo {
  name: string;
  type: ProviderType;
  status: ProviderStatus;
  models: string[];
  defaultModel: string;
}

type ProviderType = 'official' | 'openai-compatible' | 'custom';
type ProviderStatus = 'ready' | 'error' | 'unconfigured';

interface ModelRouter {
  route(taskType: TaskType): ModelId;
  setStrategy(taskType: TaskType, modelId: ModelId): void;
  getStrategies(): Map<TaskType, ModelId>;
}

type TaskType = 'coding' | 'search' | 'reasoning' | 'long-context' | 'cost-sensitive';
type ModelId = string;
```

---

## 14. 领域事件全景流

```
用户发送消息
    │
    ├─► SessionCreated (如果新会话)
    │   └─► Memory: 创建会话记录
    │
    ├─► TurnStarted
    │       │
    │       ├─► ContextAssembled { tokenUsage, cacheHit }
    │       │   └─► Plugin(telemetry): 记录 token 分布
    │       │
    │       ├─► [如需切换模型] ProviderSwitched { oldModel, newModel }
    │       │   └─► Context: 切换 Provider 提示词文件
    │       │
    │       ├─► [如匹配技能] SkillTriggered → SkillContentInjected
    │       │
    │       ├─► ToolCallRequested { toolName, input }
    │       │       │
    │       │       ├─► Plugin(PreToolUse): 拦截/修改
    │       │       │
    │       │       ├─► Security: PermissionGranted | PermissionDenied | ApprovalRequested
    │       │       │
    │       │       ├─► ToolExecutionStarted
    │       │       │       │
    │       │       │       ├─► [如 MCP 工具] MCPToolCallForwarded
    │       │       │       │
    │       │       │       └─► ToolExecutionCompleted | ToolExecutionFailed
    │       │       │
    │       │       ├─► Plugin(PostToolUse): 后处理 (eslint/prettier)
    │       │       │
    │       │       └─► ToolResultReceived { tokenCount }
    │       │               │
    │       │               ├─► Context(HotTail): 管理工具结果
    │       │               └─► [如超限] ToolResultOffloaded
    │       │
    │       ├─► [如卡住] AgentStuck { failureMode }
    │       │
    │       ├─► [如超限] TokenBudgetExceeded → CompactionTriggered
    │       │       └─► CompactionCompleted { compressionRatio }
    │       │
    │       ├─► [如技能完成] SkillContentEvicted
    │       │
    │       └─► TurnCompleted { toolCallCount, durationMs }
    │               └─► Plugin(telemetry): 记录轮次指标
    │
    ├─► Memory: SessionPersisted（异步）
    │
    ├─► Memory: MemoryCreated / MemoryUpdated（异步，如需记忆更新）
    │
    └─► Automation: 检查是否触发定时任务/文件监听（异步）
```

---

## 15. 模块包结构与依赖关系

### 15.1 Monorepo 包结构

```
packages/
├── @agent/shared        ← 共享类型定义（全部包依赖，无外部依赖）
├── @agent/core          ← Agent 核心引擎（AgentLoop, StreamParser, StuckDetector）
├── @agent/tools         ← 工具系统（ToolRegistry, ToolExecutor, 内建工具）
├── @agent/context       ← 上下文管理（PromptBuilder, TokenBudget, Compactor, HotTail）
├── @agent/security      ← 安全系统（PolicyEngine, Sandbox, PermissionChecker）
├── @agent/memory        ← 记忆系统（MemoryStore, SessionStore, CodeIndex）
├── @agent/coord         ← 协调系统（AgentCoordinator, WorkerManager）
├── @agent/skills        ← 技能系统（SkillRegistry, SkillMatcher, SkillLoader）
├── @agent/mcp           ← MCP 集成（MCPManager, MCPClient, MCPHealthMonitor）
├── @agent/plugins       ← 插件系统（PluginHost, PluginLoader, PluginContext）
├── @agent/automation    ← 自动化（Scheduler, FileWatcher, TaskRunner, Notify）
├── @agent/search        ← 搜索能力（WebSearch, WebFetch, SemanticSearch, GitSearch）
├── @agent/llm           ← LLM 提供商抽象（ProviderRegistry, ModelRouter）
├── @agent/protocol      ← 协议层（JSON-RPC Server, SSE Stream）
└── @agent/cli           ← CLI 客户端（终端 UI, 交互循环, 斜杠命令）
```

### 15.2 依赖关系图

```
@agent/shared           ← 零依赖，被所有包引用
    ↑
@agent/llm              ← 依赖 shared + Vercel AI SDK
    ↑
@agent/security         ← 依赖 shared
    ↑
@agent/tools            ← 依赖 shared, security
    ↑
@agent/mcp              ← 依赖 shared, tools, security
    ↑
@agent/context          ← 依赖 shared, tools
    ↑
@agent/memory           ← 依赖 shared
    ↑
@agent/skills           ← 依赖 shared, tools
    ↑
@agent/plugins          ← 依赖 shared, tools, memory, context
    ↑
@agent/coord            ← 依赖 shared, tools
    ↑
@agent/core             ← 依赖以上全部
    ↑
@agent/search           ← 依赖 shared, tools
    ↑
@agent/automation       ← 依赖 shared, core, skills
    ↑
@agent/protocol         ← 依赖 core
    ↑
@agent/cli              ← 依赖 protocol

依赖规则:
├── 上层依赖下层，禁止反向依赖
├── 同层通过领域事件解耦
└── @agent/shared 被所有包依赖，不依赖任何包
```

### 15.3 限界上下文 → 模块包映射

| 限界上下文 | 主包 | 辅助包 |
|-----------|------|--------|
| BC-1 Agent Core | @agent/core | -- |
| BC-2 Tool | @agent/tools | @agent/search |
| BC-3 Context | @agent/context | -- |
| BC-4 Security | @agent/security | -- |
| BC-5 Memory | @agent/memory | -- |
| BC-6 Coordination | @agent/coord | -- |
| BC-7 Skill | @agent/skills | -- |
| BC-8 MCP | @agent/mcp | -- |
| BC-9 Plugin | @agent/plugins | -- |
| BC-10 Automation | @agent/automation | -- |
| BC-11 LLM Provider | @agent/llm | -- |
