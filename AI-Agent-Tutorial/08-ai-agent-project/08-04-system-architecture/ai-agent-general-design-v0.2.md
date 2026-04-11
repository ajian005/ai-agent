# 通用 AI Agent 设计方案 V0.2：扩展能力体系

> 在 V0.1（需求、架构、领域设计、MVP）基础上，补充 **技能系统、MCP 集成、插件体系、自动化任务、搜索能力** 五大扩展模块，形成完整的 V0.2 设计方案。
>
> 前置文档：[V0.1 设计方案](ai-agent-general-design.md)

---

## 目录

- [第六章：技能系统（Skills）](#第六章技能系统skills)
- [第七章：MCP 集成](#第七章mcp-集成)
- [第八章：插件系统（Plugin）](#第八章插件系统plugin)
- [第九章：自动化与定时任务](#第九章自动化与定时任务)
- [第十章：搜索能力体系](#第十章搜索能力体系)
- [第十一章：V0.2 架构更新](#第十一章v02-架构更新)
- [第十二章：V0.2 领域模型增量](#第十二章v02-领域模型增量)
- [第十三章：V0.2 路线图](#第十三章v02-路线图)

---

## 第六章：技能系统（Skills）

### 6.1 技能 vs 工具 的本质区别

```
工具（Tool）= 原子能力                技能（Skill）= 编排智慧
"能做什么"                            "何时做、怎么组合做"

┌──────────────┐                     ┌──────────────────────────┐
│ bash          │                     │ deploy-to-production     │
│ ├ 输入: 命令  │                     │ ├ 前置: 运行测试套件      │
│ └ 输出: 结果  │                     │ ├ 检查: CI 状态为绿色     │
│               │                     │ ├ 执行: git tag + push    │
│ file_write    │                     │ ├ 等待: CI/CD 管线完成    │
│ ├ 输入: 路径  │                     │ └ 验证: 健康检查通过      │
│ └ 输出: 确认  │                     │                          │
└──────────────┘                     │ 引用工具: bash, read,     │
                                     │ web_fetch, git            │
                                     └──────────────────────────┘

工具 = 无状态的原子操作
技能 = 有领域知识的多步骤编排指导
```

### 6.2 技能架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                     技能系统架构                                  │
│                                                                 │
│  ┌─ 技能注册表（SkillRegistry）─────────────────────────────┐   │
│  │                                                           │   │
│  │  发现机制:                                                │   │
│  │  ├── 内建技能: src/skills/ 目录自动扫描                   │   │
│  │  ├── 项目技能: .agent/skills/ 目录自动加载                │   │
│  │  ├── 全局技能: ~/.agent/skills/ 用户级技能                │   │
│  │  └── 远程技能: npm 包 / Git 仓库安装                     │   │
│  │                                                           │   │
│  │  技能索引:                                                │   │
│  │  ├── 名称 + 一行描述（始终在系统提示词中，轻量）          │   │
│  │  └── 完整指导内容（仅在 Agent 决定使用时加载）            │   │
│  │                                                           │   │
│  │  上下文成本: 所有技能描述总计仅占 ~2% 上下文窗口          │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─ 技能文件格式（Markdown + YAML Frontmatter）──────────────┐  │
│  │                                                           │  │
│  │  ---                                                      │  │
│  │  name: code-review                                        │  │
│  │  description: "审查代码变更，检测安全问题和最佳实践"       │  │
│  │  version: 1.0.0                                           │  │
│  │  triggers:                                                │  │
│  │    - pattern: "review|审查|检查代码"                       │  │
│  │    - event: PostToolUse                                   │  │
│  │      tool: git_diff                                       │  │
│  │  requires_tools: [read, grep, bash]                       │  │
│  │  requires_permissions: [safe]                             │  │
│  │  model_preference: "高能力模型"                            │  │
│  │  ---                                                      │  │
│  │                                                           │  │
│  │  # Code Review 技能                                       │  │
│  │  ## 执行步骤                                              │  │
│  │  1. 获取变更文件列表（git diff --name-only）              │  │
│  │  2. 逐文件审查...                                         │  │
│  │  ## 检查清单                                              │  │
│  │  - [ ] 安全漏洞（SQL注入、XSS...）                        │  │
│  │  - [ ] 错误处理                                           │  │
│  │  ...                                                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ 技能执行引擎 ────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │  触发方式:                                                │  │
│  │  ├── 显式触发: 用户输入匹配 triggers.pattern              │  │
│  │  ├── 事件触发: 生命周期钩子匹配 triggers.event            │  │
│  │  ├── Agent 自主选择: 模型判断任务适合某技能               │  │
│  │  └── 命令触发: /skill <name> 斜杠命令                    │  │
│  │                                                           │  │
│  │  执行流程:                                                │  │
│  │  1. 检查 requires_tools 是否都可用                        │  │
│  │  2. 检查 requires_permissions 是否满足                    │  │
│  │  3. 将技能完整内容注入当前上下文（按需加载）              │  │
│  │  4. Agent 按技能指导执行多步骤操作                        │  │
│  │  5. 技能完成后从上下文中移除完整内容（仅保留摘要）        │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 内建技能目录（首批 15 个）

| 分类 | 技能名 | 描述 | 引用工具 |
|------|--------|------|---------|
| **代码质量** | code-review | 审查代码变更，检测安全和最佳实践 | read, grep, bash |
| **代码质量** | refactor | 重构代码（提取函数、消除重复等）| read, edit, bash |
| **代码质量** | add-tests | 为指定代码生成单元测试 | read, write, bash |
| **Git 工作流** | git-commit | 分析变更生成规范化提交信息 | bash, read |
| **Git 工作流** | create-pr | 创建 PR 并生成描述 | bash, read, web_fetch |
| **Git 工作流** | resolve-conflict | 分析并解决 Git 合并冲突 | read, edit, bash |
| **项目管理** | init-project | 初始化项目（依赖、配置、CI）| write, bash |
| **项目管理** | update-deps | 安全地更新项目依赖 | bash, read, edit |
| **文档** | generate-docs | 为代码生成 API 文档/README | read, write, grep |
| **文档** | explain-codebase | 分析并解释代码库架构 | read, glob, grep |
| **调试** | debug-error | 系统化调试错误（日志分析→定位→修复）| read, bash, grep |
| **调试** | performance-profile | 性能分析和优化建议 | bash, read |
| **安全** | security-audit | 扫描常见安全漏洞 | grep, read, bash |
| **部署** | deploy | 执行部署流程（测试→构建→发布→验证）| bash, web_fetch |
| **搜索** | deep-research | 深度调研技术方案（搜索→分析→总结）| web_search, read, write |

### 6.4 技能接口定义

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
}

type SkillTrigger =
  | { type: 'pattern'; pattern: string | RegExp }
  | { type: 'event'; event: HookEvent; tool?: string }
  | { type: 'command'; command: string };

interface SkillRegistry {
  register(skill: Skill): void;
  unregister(name: string): void;
  discover(directories: string[]): Promise<Skill[]>;
  match(input: string): Skill | null;
  matchEvent(event: HookEvent, data: HookData): Skill | null;
  getDescriptors(): SkillDescriptor[];
  getFullContent(name: string): string;
  install(source: string): Promise<Skill>;
}

interface SkillDescriptor {
  name: string;
  description: string;
  triggers: string[];
}
```

---

## 第七章：MCP 集成

### 7.1 MCP 在 Agent 中的定位

```
┌─────────────────────────────────────────────────────────────────┐
│               MCP（Model Context Protocol）定位                  │
│                                                                 │
│  Agent 核心引擎                                                  │
│  ├── 内建工具（编译时确定，直接调用，零协议开销）                │
│  │   └── Read, Write, Edit, Bash, Glob, Grep                   │
│  │                                                              │
│  └── MCP 工具（运行时发现，通过协议中转）                        │
│      ├── 数据库查询: @mcp/postgres, @mcp/redis                 │
│      ├── 云服务: @mcp/aws, @mcp/gcloud, @mcp/azure             │
│      ├── API 集成: @mcp/github, @mcp/jira, @mcp/slack          │
│      ├── 浏览器: @mcp/playwright, @mcp/puppeteer               │
│      └── 自定义: 用户开发的 MCP Server                          │
│                                                                 │
│  价值: 无需修改 Agent 核心，通过 MCP 无限扩展能力               │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 MCP 集成架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP 集成架构                                   │
│                                                                 │
│  ┌─ MCPManager（MCP 管理器）──────────────────────────────┐     │
│  │                                                         │     │
│  │  配置加载:                                               │     │
│  │  ├── .agent/mcp.json（项目级 MCP 配置）                 │     │
│  │  ├── ~/.agent/mcp.json（全局 MCP 配置）                 │     │
│  │  └── 环境变量覆盖                                       │     │
│  │                                                         │     │
│  │  配置示例:                                               │     │
│  │  {                                                      │     │
│  │    "servers": {                                         │     │
│  │      "postgres": {                                      │     │
│  │        "command": "npx",                                │     │
│  │        "args": ["@mcp/postgres"],                       │     │
│  │        "env": { "DATABASE_URL": "${DB_URL}" },          │     │
│  │        "permission": "ask_user",                        │     │
│  │        "timeout": 30000                                 │     │
│  │      },                                                 │     │
│  │      "github": {                                        │     │
│  │        "command": "npx",                                │     │
│  │        "args": ["@mcp/github"],                         │     │
│  │        "env": { "GITHUB_TOKEN": "${GH_TOKEN}" },        │     │
│  │        "permission": "allow"                            │     │
│  │      }                                                  │     │
│  │    }                                                    │     │
│  │  }                                                      │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌─ MCPClient（MCP 客户端）───────────────────────────────┐     │
│  │                                                         │     │
│  │  生命周期:                                               │     │
│  │  1. 启动: 根据配置 spawn MCP Server 子进程              │     │
│  │  2. 握手: 通过 stdio/SSE 完成 MCP 初始化协商            │     │
│  │  3. 发现: 获取 Server 暴露的工具列表（tools/list）       │     │
│  │  4. 注册: 将 MCP 工具注册到 ToolRegistry                │     │
│  │  5. 调用: Agent 调用工具时通过 MCP 协议中转              │     │
│  │  6. 关闭: 会话结束时优雅关闭 Server 进程                │     │
│  │                                                         │     │
│  │  传输方式:                                               │     │
│  │  ├── stdio（默认）: JSON-RPC over stdin/stdout          │     │
│  │  └── SSE: HTTP Server-Sent Events（远程 Server）        │     │
│  │                                                         │     │
│  │  健康管理:                                               │     │
│  │  ├── 心跳检测: 定期 ping MCP Server                     │     │
│  │  ├── 自动重连: Server 崩溃后指数退避重启                │     │
│  │  └── 超时保护: 单次工具调用超时 → 终止并报错            │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌─ MCP 工具权限 ─────────────────────────────────────────┐     │
│  │                                                         │     │
│  │  独立于内建工具的权限策略:                                │     │
│  │  ├── 配置级: mcp.json 中 per-server 权限                │     │
│  │  ├── 策略引擎: PolicyEngine 评估 MCP 工具调用            │     │
│  │  └── 动态策略: 本地 Server → ALLOW，远程 Server → ASK   │     │
│  │                                                         │     │
│  └─────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 MCP 接口定义

```typescript
interface MCPManager {
  loadConfig(paths: string[]): Promise<MCPConfig>;
  startServer(name: string): Promise<MCPClient>;
  startAll(): Promise<Map<string, MCPClient>>;
  stopServer(name: string): Promise<void>;
  stopAll(): Promise<void>;
  getClient(name: string): MCPClient | undefined;
  listServers(): MCPServerStatus[];
}

interface MCPClient {
  readonly serverName: string;
  readonly status: 'starting' | 'ready' | 'error' | 'closed';

  initialize(): Promise<void>;
  listTools(): Promise<MCPToolDescriptor[]>;
  callTool(name: string, args: unknown): Promise<MCPToolResult>;
  close(): Promise<void>;

  onHealthChange(cb: (status: MCPServerStatus) => void): void;
}

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

## 第八章：插件系统（Plugin）

### 8.1 插件体系定位

```
技能(Skill)、MCP、插件(Plugin) 的关系:

┌──────────────────────────────────────────────────────────┐
│                                                          │
│  技能 = Markdown 指导文件                                │
│  └── 教 Agent "何时做、怎么做"（纯提示词注入）           │
│                                                          │
│  MCP = 标准化外部工具协议                                │
│  └── 给 Agent 新的"手脚"（新工具能力）                   │
│                                                          │
│  插件 = 深度修改 Agent 行为的代码扩展                    │
│  └── 改变 Agent 的"大脑回路"（拦截/修改/增强核心流程）   │
│                                                          │
│  对比:                                                   │
│  ├── 技能: 无代码，纯 Markdown → 最易创建               │
│  ├── MCP: 独立进程，标准协议 → 中等复杂度               │
│  └── 插件: TypeScript 代码，深度集成 → 最强大但最复杂    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 8.2 插件架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      插件系统架构                                 │
│                                                                 │
│  ┌─ PluginHost（插件宿主）───────────────────────────────┐      │
│  │                                                        │      │
│  │  插件发现:                                              │      │
│  │  ├── 内建插件: @agent/plugin-* 包                      │      │
│  │  ├── 项目插件: .agent/plugins/ 目录                    │      │
│  │  ├── npm 插件: package.json 的 agentPlugins 字段       │      │
│  │  └── 全局插件: ~/.agent/plugins/                       │      │
│  │                                                        │      │
│  │  生命周期:                                              │      │
│  │  1. discover() → 扫描所有插件来源                      │      │
│  │  2. validate() → 校验插件 manifest                     │      │
│  │  3. load() → 动态 import 插件模块                      │      │
│  │  4. activate() → 调用插件 activate 函数                │      │
│  │  5. deactivate() → 会话结束时调用 deactivate           │      │
│  └────────────────────────────────────────────────────────┘      │
│                                                                 │
│  ┌─ Plugin API（插件可访问的接口）──────────────────────┐        │
│  │                                                      │        │
│  │  上下文修改:                                          │        │
│  │  ├── onSystemPromptBuild → 修改系统提示词             │        │
│  │  ├── onContextAssemble → 修改上下文组装结果           │        │
│  │  └── onCompact → 在压缩前注入保留指令                 │        │
│  │                                                      │        │
│  │  工具扩展:                                            │        │
│  │  ├── registerTool → 注册新工具                        │        │
│  │  └── wrapTool → 包装现有工具（前置/后置处理）         │        │
│  │                                                      │        │
│  │  行为拦截:                                            │        │
│  │  ├── onPreToolUse → 工具执行前拦截/修改               │        │
│  │  ├── onPostToolUse → 工具执行后处理                   │        │
│  │  ├── onAgentResponse → Agent 响应后处理               │        │
│  │  └── onError → 错误处理增强                           │        │
│  │                                                      │        │
│  │  数据访问:                                            │        │
│  │  ├── getSession → 访问当前会话                        │        │
│  │  ├── getMemory → 访问记忆系统                         │        │
│  │  └── getConfig → 访问配置                             │        │
│  │                                                      │        │
│  └──────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─ 插件 Manifest 格式 ──────────────────────────────────┐      │
│  │                                                        │      │
│  │  // .agent/plugins/my-plugin/manifest.json             │      │
│  │  {                                                     │      │
│  │    "name": "@agent/plugin-eslint",                     │      │
│  │    "version": "1.0.0",                                 │      │
│  │    "description": "代码修改后自动运行 ESLint",          │      │
│  │    "entry": "./index.ts",                              │      │
│  │    "hooks": ["PostToolUse"],                           │      │
│  │    "permissions": ["safe"],                            │      │
│  │    "config": {                                         │      │
│  │      "autoFix": true,                                  │      │
│  │      "rules": "project"                                │      │
│  │    }                                                   │      │
│  │  }                                                     │      │
│  └────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### 8.3 内建插件示例

| 插件名 | 功能 | 钩子 |
|--------|------|------|
| **plugin-eslint** | 代码修改后自动运行 ESLint + 自动修复 | PostToolUse(write/edit) |
| **plugin-prettier** | 代码写入后自动格式化 | PostToolUse(write/edit) |
| **plugin-git-guard** | 阻止在 main/master 上直接提交 | PreToolUse(bash) |
| **plugin-cost-tracker** | 追踪每次请求的 token 成本 | AgentResponse |
| **plugin-changelog** | 自动维护 CHANGELOG.md | PostToolUse(git_commit) |
| **plugin-notify** | 长任务完成后发送通知（Slack/邮件）| SessionEnd |
| **plugin-telemetry** | OpenTelemetry 追踪集成 | 全部钩子 |
| **plugin-i18n** | Agent 响应自动翻译 | AgentResponse |

### 8.4 插件接口定义

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
}

type PluginSource =
  | { type: 'directory'; path: string }
  | { type: 'npm'; package: string }
  | { type: 'builtin' };
```

---

## 第九章：自动化与定时任务

### 9.1 自动化场景

```
┌─────────────────────────────────────────────────────────────────┐
│                    自动化任务场景                                 │
│                                                                 │
│  定时任务（Cron-like）:                                          │
│  ├── 每日代码库健康检查（Lint 违规、废弃 API 使用、依赖漏洞）   │
│  ├── 每周技术债务报告                                           │
│  ├── 每日自动更新 CHANGELOG                                     │
│  └── 定时备份记忆和会话数据                                     │
│                                                                 │
│  事件驱动任务:                                                   │
│  ├── Git push → 自动代码审查                                    │
│  ├── PR 创建 → 自动生成 PR 描述                                 │
│  ├── CI 失败 → 自动分析失败原因并尝试修复                       │
│  ├── 文件变更 → 自动更新相关文档                                │
│  └── 依赖更新通知 → 自动评估兼容性                              │
│                                                                 │
│  守护进程任务:                                                   │
│  ├── 后台监听文件变更 → 增量索引更新                            │
│  ├── 后台记忆整理 → 异步蒸馏知识                                │
│  └── 后台健康监控 → MCP Server 状态检查                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 自动化架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    自动化系统架构                                 │
│                                                                 │
│  ┌─ Scheduler（调度器）──────────────────────────────────┐      │
│  │                                                        │      │
│  │  任务定义（.agent/automation.yaml）:                    │      │
│  │                                                        │      │
│  │  schedules:                                            │      │
│  │    - name: daily-health-check                          │      │
│  │      cron: "0 9 * * 1-5"      # 工作日每天 9 点       │      │
│  │      task: |                                           │      │
│  │        运行 lint 和测试，生成健康报告到                 │      │
│  │        .agent/reports/health-{date}.md                 │      │
│  │      skill: security-audit                             │      │
│  │      timeout: 300                                      │      │
│  │      notify: slack                                     │      │
│  │                                                        │      │
│  │    - name: dep-update-check                            │      │
│  │      cron: "0 10 * * 1"       # 每周一 10 点          │      │
│  │      task: "检查并报告可更新的依赖"                     │      │
│  │      skill: update-deps                                │      │
│  │      mode: dry-run            # 仅报告不执行           │      │
│  │                                                        │      │
│  │  watchers:                                             │      │
│  │    - name: auto-lint                                   │      │
│  │      watch: "src/**/*.ts"                              │      │
│  │      event: change                                     │      │
│  │      debounce: 5000           # 5 秒防抖              │      │
│  │      task: "对变更的文件运行 lint 检查"                 │      │
│  │                                                        │      │
│  │    - name: doc-sync                                    │      │
│  │      watch: "src/api/**/*.ts"                          │      │
│  │      event: change                                     │      │
│  │      task: "更新对应的 API 文档"                        │      │
│  │      skill: generate-docs                              │      │
│  │                                                        │      │
│  │  hooks:                                                │      │
│  │    - name: pr-auto-review                              │      │
│  │      trigger: github.pull_request.opened               │      │
│  │      task: "审查 PR 变更并提交评论"                     │      │
│  │      skill: code-review                                │      │
│  │                                                        │      │
│  └────────────────────────────────────────────────────────┘      │
│                                                                 │
│  ┌─ TaskRunner（任务执行器）──────────────────────────────┐      │
│  │                                                        │      │
│  │  执行模式:                                              │      │
│  │  ├── foreground: 在当前会话中执行（用户可见）           │      │
│  │  ├── background: 独立会话执行（不影响当前工作）         │      │
│  │  └── dry-run: 仅生成计划不实际执行                     │      │
│  │                                                        │      │
│  │  隔离机制:                                              │      │
│  │  ├── 每个定时任务在独立 Session 中执行                 │      │
│  │  ├── 独立 token 预算（防止定时任务耗尽配额）           │      │
│  │  └── 独立权限上下文（定时任务默认更严格的权限）         │      │
│  │                                                        │      │
│  │  通知机制:                                              │      │
│  │  ├── 终端通知（完成/失败 bell）                        │      │
│  │  ├── 文件报告（写入 .agent/reports/）                  │      │
│  │  ├── Slack/Discord/邮件（通过 MCP Server）             │      │
│  │  └── Webhook（HTTP POST 回调）                        │      │
│  │                                                        │      │
│  └────────────────────────────────────────────────────────┘      │
│                                                                 │
│  ┌─ FileWatcher（文件监听器）──────────────────────────────┐     │
│  │  基于 chokidar 的文件系统监听                           │     │
│  │  ├── glob 模式匹配                                     │     │
│  │  ├── 防抖处理（debounce）                              │     │
│  │  ├── 变更聚合（多个文件变更合并为一次触发）             │     │
│  │  └── .gitignore 尊重（忽略 node_modules 等）           │     │
│  └────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### 9.3 自动化接口定义

```typescript
interface Scheduler {
  loadConfig(path: string): Promise<AutomationConfig>;
  scheduleTask(task: ScheduledTask): string;
  cancelTask(taskId: string): void;
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
```

---

## 第十章：搜索能力体系

### 10.1 搜索能力全景

```
┌─────────────────────────────────────────────────────────────────┐
│                    搜索能力体系                                   │
│                                                                 │
│  ┌─ 本地搜索（零网络，低延迟）────────────────────────────┐     │
│  │                                                         │     │
│  │  文件搜索（Glob）:                                      │     │
│  │  ├── 递归模式匹配 (**/*.ts)                             │     │
│  │  ├── .gitignore 尊重                                    │     │
│  │  └── 按修改时间排序                                     │     │
│  │                                                         │     │
│  │  文本搜索（Grep / Ripgrep）:                            │     │
│  │  ├── 正则表达式匹配                                     │     │
│  │  ├── 文件类型过滤                                       │     │
│  │  ├── 上下文行（-A/-B/-C）                              │     │
│  │  └── 匹配计数模式                                       │     │
│  │                                                         │     │
│  │  语义搜索（P2，需代码索引）:                            │     │
│  │  ├── 自然语言 → 相关代码（"认证逻辑在哪里？"）         │     │
│  │  ├── Tree-sitter AST 语义代码块                        │     │
│  │  ├── 向量嵌入 + ANN 近似搜索                           │     │
│  │  ├── BM25 关键词精确搜索                               │     │
│  │  └── 混合排序（语义 0.4 + 关键词 0.3 + 新近度 0.3）   │     │
│  │                                                         │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌─ 网络搜索（需网络权限）─────────────────────────────────┐    │
│  │                                                          │    │
│  │  Web 搜索:                                               │    │
│  │  ├── 通用搜索（Google/Bing/DuckDuckGo API）             │    │
│  │  ├── 结果摘要（返回精简摘要而非完整网页）               │    │
│  │  ├── 相关链接提取                                       │    │
│  │  └── 搜索结果缓存（相同查询 5 分钟内复用）             │    │
│  │                                                          │    │
│  │  网页抓取:                                               │    │
│  │  ├── URL 内容获取 → Markdown 转换                       │    │
│  │  ├── 自动截断（最大 token 限制）                        │    │
│  │  ├── 缓存机制（避免重复抓取）                           │    │
│  │  └── robots.txt 尊重                                    │    │
│  │                                                          │    │
│  │  文档搜索:                                               │    │
│  │  ├── 官方文档检索（MDN, npm docs, crates.io docs）      │    │
│  │  ├── Stack Overflow / GitHub Issues 搜索                │    │
│  │  └── API 参考查询                                       │    │
│  │                                                          │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─ 项目上下文搜索 ────────────────────────────────────────┐    │
│  │                                                          │    │
│  │  依赖图搜索:                                              │    │
│  │  ├── "谁调用了这个函数？"（调用者追踪）                 │    │
│  │  ├── "这个模块的依赖是什么？"（导入分析）               │    │
│  │  └── "修改这个文件会影响哪些测试？"（影响分析）         │    │
│  │                                                          │    │
│  │  Git 历史搜索:                                           │    │
│  │  ├── "这段代码是谁在什么时候改的？"（git blame）         │    │
│  │  ├── "最近改过这个文件的提交"（git log）                │    │
│  │  └── "这个 Bug 是从哪个提交引入的？"（git bisect）      │    │
│  │                                                          │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 搜索工具清单

| 工具名 | 类别 | 描述 | 风险级别 | 优先级 |
|--------|------|------|---------|--------|
| `glob` | 本地 | 文件模式匹配搜索 | safe | P0 |
| `grep` | 本地 | 正则文本搜索（基于 ripgrep）| safe | P0 |
| `semantic_search` | 本地 | 自然语言代码语义搜索 | safe | P2 |
| `web_search` | 网络 | 通用 Web 搜索 | medium | P1 |
| `web_fetch` | 网络 | URL 内容获取（→ Markdown）| medium | P1 |
| `doc_search` | 网络 | 技术文档专项搜索 | medium | P2 |
| `git_search` | 本地 | Git 历史和 blame 搜索 | safe | P1 |
| `dep_graph` | 本地 | 依赖图查询（调用者/导入）| safe | P2 |

### 10.3 搜索接口定义

```typescript
interface WebSearchTool extends Tool {
  name: 'web_search';
  execute(input: {
    query: string;
    maxResults?: number;
    language?: string;
  }, ctx: ExecutionContext): Promise<ToolResult>;
}

interface WebFetchTool extends Tool {
  name: 'web_fetch';
  execute(input: {
    url: string;
    maxTokens?: number;
    selector?: string;
  }, ctx: ExecutionContext): Promise<ToolResult>;
}

interface SemanticSearchTool extends Tool {
  name: 'semantic_search';
  execute(input: {
    query: string;
    targetDirectory?: string;
    maxResults?: number;
    fileType?: string;
  }, ctx: ExecutionContext): Promise<ToolResult>;
}

interface SearchResultCache {
  get(query: string): CachedResult | null;
  set(query: string, result: SearchResult, ttl: number): void;
  invalidate(pattern?: string): void;
}
```

---

## 第十一章：V0.2 架构更新

### 11.1 更新后的分层架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                    V0.2 分层架构（新增部分以 ★ 标记）                 │
│                                                                     │
│  ┌─ Layer 1: 客户端层 ──────────────────────────────────────────┐  │
│  │  CLI │ Web UI │ IDE │ CI/CD │ API │ ★ Webhook 入口           │  │
│  └──────────────────────────────┬────────────────────────────────┘  │
│                                 │                                   │
│  ┌─ Layer 2: 协议层 ────────────┴───────────────────────────────┐  │
│  │  JSON-RPC 2.0 │ SSE │ ★ Webhook Handler                      │  │
│  └──────────────────────────────┬────────────────────────────────┘  │
│                                 │                                   │
│  ┌─ Layer 3: 核心引擎层 ────────┴───────────────────────────────┐  │
│  │  Agent 循环 │ 提示词构建 │ 上下文管理 │ 工具注册 │ 策略引擎   │  │
│  │  错误恢复 │ 生命周期钩子 │ Agent 协调                        │  │
│  │  ★ 技能引擎(SkillEngine) │ ★ 插件宿主(PluginHost)           │  │
│  └──────────────────────────────┬────────────────────────────────┘  │
│                                 │                                   │
│  ┌─ Layer 4: 工具层 ────────────┴───────────────────────────────┐  │
│  │  内建工具(Read/Write/Edit/Bash/Glob/Grep)                    │  │
│  │  ★ 搜索工具(WebSearch/WebFetch/SemanticSearch/GitSearch)     │  │
│  │  ★ MCP 动态工具(MCPManager → MCPClient → MCP Server)        │  │
│  │  子 Agent 工具(Task/Explore/General)                         │  │
│  └──────────────────────────────┬────────────────────────────────┘  │
│                                 │                                   │
│  ┌─ Layer 5: 数据层 ────────────┴───────────────────────────────┐  │
│  │  向量索引 │ 记忆存储 │ 会话存储 │ ★ 搜索缓存 │ ★ 任务历史   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                 │                                   │
│  ┌─ Layer 6: ★ 自动化层 ────────┴───────────────────────────────┐  │
│  │  Scheduler(Cron) │ FileWatcher │ WebhookReceiver │ TaskRunner │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 11.2 V0.2 新增模块依赖

```
V0.1 模块:                     V0.2 新增模块:
@agent/core                    ★ @agent/skills      ← 技能系统
@agent/tools                   ★ @agent/mcp         ← MCP 集成
@agent/context                 ★ @agent/plugins     ← 插件系统
@agent/security                ★ @agent/automation  ← 自动化/定时任务
@agent/memory                  ★ @agent/search      ← 搜索能力
@agent/coord
@agent/protocol
@agent/cli
@agent/shared

依赖关系:
@agent/skills   → @agent/core, @agent/tools, @agent/shared
@agent/mcp      → @agent/tools, @agent/security, @agent/shared
@agent/plugins  → @agent/core, @agent/tools, @agent/memory, @agent/shared
@agent/automation → @agent/core, @agent/skills, @agent/shared
@agent/search   → @agent/tools, @agent/shared
```

---

## 第十二章：V0.2 领域模型增量

### 12.1 新增限界上下文

在 V0.1 的 6 个限界上下文基础上，新增 **4 个**：

```
V0.1（6个）:                      V0.2 新增（4个）:
├── Agent Core                    ★ BC-7: 技能上下文 (Skill)
├── Tool                          ★ BC-8: MCP 上下文
├── Context Management            ★ BC-9: 插件上下文 (Plugin)
├── Security                      ★ BC-10: 自动化上下文 (Automation)
├── Memory
└── Coordination
```

#### BC-7: 技能上下文

```
聚合根: SkillRegistry
├── 实体: Skill
│   ├── 值对象: SkillTrigger
│   ├── 值对象: SkillRequirement
│   └── 值对象: SkillContent
├── 服务: SkillMatcher（触发匹配引擎）
└── 服务: SkillInstaller（远程技能安装）

领域事件:
├── SkillRegistered / SkillUnregistered
├── SkillTriggered（技能被激活）
├── SkillContentInjected（技能内容注入上下文）
├── SkillContentEvicted（技能内容从上下文移除）
└── SkillInstalled / SkillUpdated
```

#### BC-8: MCP 上下文

```
聚合根: MCPManager
├── 实体: MCPConnection
│   ├── 值对象: MCPServerConfig
│   ├── 值对象: MCPServerStatus
│   └── 值对象: MCPTransport (stdio | sse)
├── 服务: MCPClient（协议通信）
└── 服务: MCPHealthMonitor（健康检查）

领域事件:
├── MCPServerStarted / MCPServerStopped
├── MCPToolDiscovered（发现新工具）
├── MCPToolCallForwarded（工具调用转发）
├── MCPServerHealthChanged
└── MCPServerCrashed / MCPServerRestarted
```

#### BC-9: 插件上下文

```
聚合根: PluginHost
├── 实体: PluginInstance
│   ├── 值对象: PluginManifest
│   ├── 值对象: PluginStatus (discovered | loaded | active | error)
│   └── 值对象: PluginConfig
├── 服务: PluginLoader（动态加载）
└── 服务: PluginSandbox（插件隔离运行）

领域事件:
├── PluginDiscovered / PluginLoaded
├── PluginActivated / PluginDeactivated
├── PluginError（插件运行错误，不影响主循环）
└── PluginHookFired（插件钩子触发）
```

#### BC-10: 自动化上下文

```
聚合根: Scheduler
├── 实体: ScheduledTask
│   ├── 值对象: CronExpression / WatchPattern / WebhookTrigger
│   ├── 值对象: TaskConfig (timeout, notify, permissions, budget)
│   └── 值对象: TaskStatus (scheduled | running | completed | failed)
├── 实体: TaskExecution（单次执行记录）
│   ├── 值对象: ExecutionResult
│   └── 值对象: ExecutionReport
├── 服务: TaskRunner（独立会话执行）
├── 服务: FileWatcher（文件变更监听）
└── 服务: NotificationService（通知发送）

领域事件:
├── TaskScheduled / TaskCancelled
├── TaskExecutionStarted / TaskExecutionCompleted / TaskExecutionFailed
├── FileChangeDetected
├── WebhookReceived
└── NotificationSent
```

---

## 第十三章：V0.2 路线图

### 13.1 更新后的优先级矩阵

```
┌─────────────────────────────────────────────────────────────────────┐
│  V0.2 优先级矩阵（★ 标记本次新增）                                  │
│                                                                     │
│  P0（MVP, 第 1-2 周）        │  P1（第 3-4 周）                     │
│  [与 V0.1 相同，不变]         │  [V0.1 内容] +                      │
│                               │  ★ WebSearch / WebFetch 工具         │
│                               │  ★ GitSearch 工具                    │
│                               │  ★ 技能系统核心 + 5 个内建技能       │
│                               │  ★ MCP 管理器 + 配置加载             │
│                               │  ★ MCP 单 Server 连接                │
├───────────────────────────────┼──────────────────────────────────────┤
│  P2（第 5-8 周）              │  P3（第 9-12+ 周）                   │
│  [V0.1 内容] +                │  [V0.1 内容] +                       │
│  ★ 完整 MCP 多 Server 支持    │  ★ 远程技能市场/安装                 │
│  ★ MCP 健康管理 + 自动重连    │  ★ 插件沙箱隔离                      │
│  ★ 插件系统核心 + 3 个内建    │  ★ 守护进程模式（Daemon）            │
│  ★ 搜索结果缓存              │  ★ Webhook 接收器                    │
│  ★ 语义搜索（向量索引）       │  ★ 多渠道通知（Slack/Discord/邮件）  │
│  ★ 依赖图搜索                │  ★ 插件市场                          │
│  ★ 文件监听器（FileWatcher）  │  ★ 定时任务可视化面板                │
│  ★ 基础定时任务（Cron）       │  ★ 浏览器自动化（MCP Playwright）    │
│  ★ 技能扩展到 15 个           │  ★ 跨项目知识共享                    │
│  ★ 技能事件触发               │                                      │
└───────────────────────────────┴──────────────────────────────────────┘
```

### 13.2 V0.2 实施路线图

```
Phase 2 扩展（第 3-4 周）: 搜索 + 技能 + MCP 基础
├── Week 3:
│   ├── 实现 WebSearch 工具（调用搜索 API + 结果摘要）
│   ├── 实现 WebFetch 工具（URL → Markdown + 截断）
│   ├── 实现 GitSearch 工具（git log/blame/diff 封装）
│   ├── 实现技能系统核心（SkillRegistry + 发现 + 加载 + 匹配）
│   └── 编写 5 个内建技能（code-review, git-commit, debug-error,
│       explain-codebase, deep-research）
│
├── Week 4:
│   ├── 实现 MCP Manager（配置加载 + Server 启动/关闭）
│   ├── 实现 MCP Client（stdio 传输 + 工具发现 + 调用转发）
│   ├── MCP 工具注册到 ToolRegistry + 权限集成
│   ├── 搜索结果缓存机制
│   └── 集成测试（搜索 + 技能 + MCP 联合验证）

Phase 3 增强（第 5-6 周）: 安全 + 多 Agent + 插件
├── [V0.1 Phase 3 内容: 沙箱/策略引擎/多 Agent/错误恢复]
├── 实现插件系统核心（PluginHost + 发现 + 加载 + 激活）
├── 实现 3 个内建插件（eslint, prettier, cost-tracker）
├── MCP 多 Server 并行 + 健康管理 + 自动重连
├── 技能扩展到 15 个 + 事件触发机制
└── 语义搜索（Tree-sitter + 向量嵌入 + 混合检索）

Phase 4 自动化（第 7-8 周）: 上下文工程 + 定时任务
├── [V0.1 Phase 4 内容: 代码索引/压缩/记忆]
├── 实现 Scheduler（Cron 表达式解析 + 任务调度）
├── 实现 FileWatcher（chokidar 文件监听 + 防抖）
├── 实现 TaskRunner（独立会话执行 + 隔离）
├── 依赖图搜索（调用者追踪/导入分析）
└── 任务历史记录 + 执行报告

Phase 5 生产化（第 9-10 周）: 验证闭环 + 生产优化
├── [V0.1 Phase 5 内容: Build-Verify-Fix/可观测性/多模型]
├── Webhook 接收器（GitHub/GitLab 事件驱动）
├── 多渠道通知（通过 MCP Server 发送 Slack/邮件）
├── 插件沙箱隔离（防止插件崩溃影响主循环）
├── 远程技能安装（npm/git 安装技能包）
└── 端到端自动化流程验证
```

### 13.3 V0.2 新增目录结构

```
ai-agent/
├── [V0.1 全部结构不变]
│
├── src/
│   ├── [V0.1 目录不变]
│   │
│   ├── skills/                    # ★ 技能系统
│   │   ├── registry.ts            # 技能注册表
│   │   ├── matcher.ts             # 触发匹配引擎
│   │   ├── loader.ts              # 技能文件加载器
│   │   └── builtin/               # 内建技能
│   │       ├── code-review.md
│   │       ├── git-commit.md
│   │       ├── debug-error.md
│   │       ├── explain-codebase.md
│   │       └── deep-research.md
│   │
│   ├── mcp/                       # ★ MCP 集成
│   │   ├── manager.ts             # MCP 管理器
│   │   ├── client.ts              # MCP 客户端
│   │   ├── health.ts              # 健康监控
│   │   └── config.ts              # 配置加载
│   │
│   ├── plugins/                   # ★ 插件系统
│   │   ├── host.ts                # 插件宿主
│   │   ├── loader.ts              # 动态加载器
│   │   ├── context.ts             # 插件上下文 API
│   │   └── builtin/               # 内建插件
│   │       ├── eslint/
│   │       ├── prettier/
│   │       └── cost-tracker/
│   │
│   ├── automation/                # ★ 自动化系统
│   │   ├── scheduler.ts           # 调度器（Cron）
│   │   ├── watcher.ts             # 文件监听器
│   │   ├── runner.ts              # 任务执行器
│   │   ├── webhook.ts             # Webhook 接收器
│   │   └── notify.ts              # 通知服务
│   │
│   └── search/                    # ★ 搜索能力
│       ├── web-search.ts          # Web 搜索工具
│       ├── web-fetch.ts           # URL 抓取工具
│       ├── semantic-search.ts     # 语义搜索工具
│       ├── git-search.ts          # Git 历史搜索
│       ├── dep-graph.ts           # 依赖图搜索
│       └── cache.ts               # 搜索结果缓存
│
├── skills/                        # 项目级自定义技能
│   └── .gitkeep
│
└── .agent/                        # Agent 配置目录
    ├── mcp.json                   # MCP Server 配置
    ├── automation.yaml            # 自动化任务配置
    ├── plugins/                   # 项目级插件
    ├── skills/                    # 项目级技能
    └── reports/                   # 自动化任务报告
```

### 13.4 V0.2 成功标准（增量）

| 能力 | 指标 | 目标 | 阶段 |
|------|------|------|------|
| **搜索** | Web 搜索返回相关结果 | 首条结果相关率 >80% | Phase 2 |
| **搜索** | 语义搜索在 1000+ 文件仓库中命中 | 召回率 >70% | Phase 3 |
| **技能** | 内建技能可正确执行 | 15 个技能全部端到端通过 | Phase 3 |
| **技能** | 自定义技能热加载 | 放入目录后 <5 秒可用 | Phase 2 |
| **MCP** | 至少 3 个 MCP Server 并行运行 | 无冲突稳定运行 | Phase 3 |
| **MCP** | MCP Server 崩溃自动恢复 | 恢复成功率 >95% | Phase 3 |
| **插件** | 内建插件不影响主循环性能 | 延迟增加 <50ms | Phase 3 |
| **插件** | 插件错误不崩溃主进程 | 隔离率 100% | Phase 5 |
| **自动化** | Cron 任务准时执行 | 偏差 <10 秒 | Phase 4 |
| **自动化** | 文件监听触发响应时间 | <5 秒（含防抖后）| Phase 4 |
| **整体** | 新能力接入不影响 MVP 功能 | 全部 V0.1 测试仍通过 | 每阶段 |
