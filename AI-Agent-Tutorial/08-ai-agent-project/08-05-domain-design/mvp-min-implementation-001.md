# 通用 AI Agent MVP-MIN 技术落地方案

> 从 11 个限界上下文中精确裁剪出**最小可运行子集**，以最少代码量实现一个端到端可工作的 CLI 编码 Agent。
>
> 来源：[领域设计](domain-design.md) | [架构方案](../08-04-system-architecture/ai-agent-general-design-v0.3.md)

---

## 目录

- [1. MVP-MIN 范围裁剪](#1-mvp-min-范围裁剪)
- [2. 限界上下文裁剪表](#2-限界上下文裁剪表)
- [3. 技术栈与依赖](#3-技术栈与依赖)
- [4. 目录结构](#4-目录结构)
- [5. 核心实现方案（逐文件）](#5-核心实现方案逐文件)
- [6. 提示词模板](#6-提示词模板)
- [7. 逐日交付计划（5 天）](#7-逐日交付计划5-天)
- [8. 验收标准](#8-验收标准)
- [9. MVP-MIN 之后的增量路径](#9-mvp-min-之后的增量路径)

---

## 1. MVP-MIN 范围裁剪

### 1.1 裁剪原则

```
MVP-MIN = 能完成"读取代码 → 理解 → 修改 → 验证"端到端闭环的最小实现

裁剪标准：
├── 保留：没有它 Agent 无法完成一次代码修改
├── 简化：用硬编码/内联代替独立模块
└── 排除：完全不影响核心循环的功能
```

### 1.2 功能裁剪对照


| 功能        | 完整版                      | MVP-MIN                     | 裁剪方式                        |
| --------- | ------------------------ | --------------------------- | --------------------------- |
| Agent 循环  | 流式 ReAct + 多模式           | 流式 ReAct（仅 build 模式）        | 去掉 plan/debug 模式            |
| LLM 调用    | ProviderRegistry 多提供商    | 单 Provider 直调               | 硬编码一个 provider，用环境变量切换      |
| 工具        | 6 个内建 + MCP + 搜索         | **3 个**：Read + Write + Bash | 去掉 Edit/Glob/Grep，用 Bash 替代 |
| 提示词       | 3 层构建器 + 缓存              | 单文件模板 + 环境变量拼接              | 不分层，不做缓存                    |
| 上下文       | Token 预算 + Hot Tail + 压缩 | 简单截断（保留最近 N 条消息）            | 无 Token 计数，无压缩              |
| 权限        | 策略引擎 + 沙箱 + 审批           | Bash 工具需用户确认（Y/n）           | 硬编码，Read/Write 自动允许         |
| 安全        | 安全红线规则库                  | 3 条硬编码规则                    | 内联在 Bash 执行前                |
| 会话        | JSON 持久化 + 恢复            | 无持久化（内存中）                   | 去掉会话持久化                     |
| 记忆        | MEMORY.md + 语义检索         | 无                           | 完全排除                        |
| 技能/MCP/插件 | 完整子系统                    | 无                           | 完全排除                        |
| 钩子/自动化    | 8 事件 + Cron              | 无                           | 完全排除                        |
| 多 Agent   | Controller-Worker        | 无                           | 完全排除                        |
| 错误恢复      | StuckDetector            | 无（循环超 20 轮自动停止）             | 硬编码轮次上限                     |


### 1.3 保留的限界上下文

```
完整版 11 个 BC:               MVP-MIN 保留 4 个（简化版）:

BC-1  Agent Core        →  ✅ 保留（简化为单文件）
BC-2  Tool              →  ✅ 保留（仅 3 个工具，无 Registry 抽象）
BC-3  Context            →  ✅ 保留（简化为消息截断）
BC-4  Security           →  ✅ 保留（简化为内联 3 条规则）
BC-5  Memory             →  ❌ 排除
BC-6  Coordination       →  ❌ 排除
BC-7  Skill              →  ❌ 排除
BC-8  MCP                →  ❌ 排除
BC-9  Plugin             →  ❌ 排除
BC-10 Automation         →  ❌ 排除
BC-11 LLM Provider       →  ✅ 简化为环境变量切换
```

---

## 2. 限界上下文裁剪表

### BC-1 Agent Core（MVP-MIN 版）

```
完整版:                              MVP-MIN:
聚合根 AgentLoop                     → agent() 异步生成器函数
├── Session 实体                     → 去掉（无持久化）
├── Turn 实体                        → 内联为循环变量
├── Message 值对象                   → Vercel AI SDK 内建 Message 类型
├── ToolCall / ToolResult            → AI SDK 内建类型
├── WorkMode                         → 去掉（固定 build）
├── Checkpoint                       → 去掉（不支持中断恢复）
└── StreamEvent                      → 简化为 console 直接输出

领域事件: 全部去掉（无事件总线）
```

### BC-2 Tool（MVP-MIN 版）

```
完整版:                              MVP-MIN:
聚合根 ToolRegistry                  → tools 对象字面量（3 个工具直接注册）
├── Tool 实体                        → Vercel AI SDK tool() 函数
├── ToolSchema (Zod)                → 保留（AI SDK 要求）
├── RiskLevel                        → 内联为 'safe' | 'dangerous'
├── ToolHealth                       → 去掉
├── ToolSource                       → 去掉
└── ToolExecutor 服务                → AI SDK 自动执行

仅实现 3 个工具:
├── read_file:  读取文件内容（safe，自动允许）
├── write_file: 写入文件（safe，自动允许）
└── run_command: 执行 Shell 命令（dangerous，需确认）
```

### BC-3 Context（MVP-MIN 版）

```
完整版:                              MVP-MIN:
聚合根 ContextManager               → 内联为消息数组管理
├── PromptBuilder (3层)             → 单个模板字符串
├── TokenBudgetManager              → 去掉（靠截断兜底）
├── Compactor                       → 去掉
└── ToolResultManager (Hot Tail)    → 保留最近 30 条消息（硬编码截断）
```

### BC-4 Security（MVP-MIN 版）

```
完整版:                              MVP-MIN:
聚合根 PolicyEngine                  → if/else 内联检查
├── PolicyRule                       → 3 条硬编码规则
├── Sandbox                          → 去掉（依赖 OS 权限）
└── ApprovalRecord                   → readline Y/n 确认

3 条安全规则:
1. run_command 执行前必须用户确认
2. 禁止执行包含 rm -rf 的命令
3. 禁止读写 .env 文件
```

### BC-11 LLM Provider（MVP-MIN 版）

```
完整版:                              MVP-MIN:
聚合根 ProviderRegistry              → 环境变量 + 条件判断
├── ProviderInstance                 → createAnthropic() 或 createOpenAICompatible()
├── ModelRouter                      → 去掉
└── ProviderConfig                   → .env 文件中的 3 个变量

环境变量:
AGENT_PROVIDER=qwen           # 或 qwen / deepseek /anthropic
AGENT_MODEL=qwen  # 模型 ID  claude-sonnet-4-20250514
AGENT_API_KEY=   # API Key
# 千问专用:
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

---

## 3. 技术栈与依赖

### 3.1 package.json

```json
{
  "name": "ai-agent-mvp-min",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "start": "tsx src/index.ts",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "ai": "^4.3",
    "@ai-sdk/anthropic": "^1.2",
    "@ai-sdk/openai-compatible": "^0.2",
    "zod": "^3.24",
    "chalk": "^5.4",
    "dotenv": "^16.4"
  },
  "devDependencies": {
    "tsx": "^4.19",
    "typescript": "^5.7",
    "@types/node": "^22"
  }
}
```

> 总计 6 个运行时依赖，零框架。

### 3.2 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true
  },
  "include": ["src"]
}
```

---

## 4. 目录结构

```
ai-agent-mvp-min/
├── package.json
├── tsconfig.json
├── .env                        # API Key 配置（不入 Git）
├── .env.example                # 配置模板
│
├── src/
│   ├── index.ts                # 入口：CLI 交互循环（~60 行）
│   ├── agent.ts                # 核心：流式 ReAct 循环（~80 行）
│   ├── provider.ts             # LLM：Provider 创建（~40 行）
│   ├── tools.ts                # 工具：3 个工具定义（~100 行）
│   ├── prompt.ts               # 提示词：系统提示模板（~30 行）
│   └── security.ts             # 安全：确认 + 规则检查（~40 行）
│
└── .env.example
```

**总计 6 个源文件，预估 ~350 行 TypeScript 代码。**

---

## 5. 核心实现方案（逐文件）

### 5.1 `src/provider.ts` — LLM Provider 创建

```typescript
// 根据环境变量创建 LLM Provider，支持 Anthropic / 千问 / DeepSeek / OpenAI 兼容
import { createAnthropic } from '@ai-sdk/anthropic';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

export function createProvider() {
  const provider = process.env.AGENT_PROVIDER || 'anthropic';
  const apiKey = process.env.AGENT_API_KEY;

  if (!apiKey) {
    throw new Error('AGENT_API_KEY 环境变量未设置');
  }

  switch (provider) {
    case 'anthropic':
      return createAnthropic({ apiKey });

    case 'qwen':
      return createOpenAICompatible({
        name: 'qwen',
        apiKey,
        baseURL: process.env.DASHSCOPE_BASE_URL
          || 'https://dashscope.aliyuncs.com/compatible-mode/v1',
      });

    case 'deepseek':
      return createOpenAICompatible({
        name: 'deepseek',
        apiKey,
        baseURL: 'https://api.deepseek.com/v1',
      });

    default:
      // 通用 OpenAI 兼容（自定义 baseURL）
      return createOpenAICompatible({
        name: provider,
        apiKey,
        baseURL: process.env.AGENT_BASE_URL || 'https://api.openai.com/v1',
      });
  }
}

export function getModelId(): string {
  return process.env.AGENT_MODEL || 'claude-sonnet-4-20250514';
}
```

### 5.2 `src/tools.ts` — 3 个核心工具

```typescript
import { tool } from 'ai';
import { z } from 'zod';
import { readFile, writeFile, mkdir } from 'fs/promises';
import { execSync } from 'child_process';
import { dirname } from 'path';
import { checkSecurity, confirmExecution } from './security.js';

export const agentTools = {
  read_file: tool({
    description: '读取文件内容。必须在修改文件之前先读取。',
    parameters: z.object({
      path: z.string().describe('文件路径（相对于工作目录）'),
    }),
    execute: async ({ path }) => {
      const content = await readFile(path, 'utf-8');
      return content;
    },
  }),

  write_file: tool({
    description: '将内容写入文件。自动创建不存在的目录。',
    parameters: z.object({
      path: z.string().describe('文件路径'),
      content: z.string().describe('文件完整内容'),
    }),
    execute: async ({ path, content }) => {
      await mkdir(dirname(path), { recursive: true });
      await writeFile(path, content, 'utf-8');
      return `文件已写入: ${path}`;
    },
  }),

  run_command: tool({
    description: '在 Shell 中执行命令。用于运行测试、安装依赖、Git 操作等。',
    parameters: z.object({
      command: z.string().describe('要执行的 Shell 命令'),
    }),
    execute: async ({ command }) => {
      // 安全检查
      const violation = checkSecurity(command);
      if (violation) return `[安全阻止] ${violation}`;

      // 用户确认
      const confirmed = await confirmExecution(command);
      if (!confirmed) return '[用户取消] 命令未执行';

      try {
        const output = execSync(command, {
          encoding: 'utf-8',
          timeout: 30_000,
          cwd: process.cwd(),
        });
        return output || '(命令执行成功，无输出)';
      } catch (err: any) {
        return `[执行错误] ${err.stderr || err.message}`;
      }
    },
  }),
};
```

### 5.3 `src/security.ts` — 安全检查与用户确认

```typescript
import * as readline from 'readline';
import chalk from 'chalk';

const BLOCKED_PATTERNS = [
  /rm\s+(-rf|-fr)\s+[\/~]/,     // rm -rf / 或 ~
  />(>)?\s*\/etc\//,             // 写入 /etc
  /\.env\b/,                     // 涉及 .env 文件
];

export function checkSecurity(command: string): string | null {
  for (const pattern of BLOCKED_PATTERNS) {
    if (pattern.test(command)) {
      return `命令匹配安全规则被阻止: ${pattern}`;
    }
  }
  return null;
}

export function confirmExecution(command: string): Promise<boolean> {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    rl.question(
      chalk.yellow(`\n  执行命令: ${chalk.bold(command)}\n  确认? (Y/n): `),
      (answer) => {
        rl.close();
        resolve(answer.trim().toLowerCase() !== 'n');
      }
    );
  });
}
```

### 5.4 `src/prompt.ts` — 系统提示词

```typescript
import { execSync } from 'child_process';
import { platform } from 'os';

export function buildSystemPrompt(): string {
  const cwd = process.cwd();
  const os = platform();
  const date = new Date().toISOString().split('T')[0];

  let gitBranch = '';
  try {
    gitBranch = execSync('git branch --show-current', { encoding: 'utf-8' }).trim();
  } catch {}

  return `You are a coding agent. You help users read, understand, and modify code.

## Rules
1. ALWAYS read a file before modifying it.
2. NEVER execute destructive commands (rm -rf /, drop database, etc.) without explicit user request.
3. NEVER read or expose .env files or credentials.
4. Be concise. Show file paths when referencing code.
5. After making changes, suggest running tests to verify.

## Environment
- OS: ${os}
- Working Directory: ${cwd}
- Date: ${date}
${gitBranch ? `- Git Branch: ${gitBranch}` : ''}

## Available Tools
- read_file: Read file content. Always read before modifying.
- write_file: Write content to a file.
- run_command: Execute a shell command (requires user confirmation).
`;
}
```

### 5.5 `src/agent.ts` — 流式 ReAct 循环

```typescript
import { streamText, type CoreMessage } from 'ai';
import chalk from 'chalk';
import { createProvider, getModelId } from './provider.js';
import { agentTools } from './tools.js';
import { buildSystemPrompt } from './prompt.js';

const MAX_TURNS = 20;
const MAX_MESSAGES = 30;

export async function runAgent(userMessage: string, history: CoreMessage[]) {
  const provider = createProvider();
  const modelId = getModelId();
  const model = provider(modelId);

  history.push({ role: 'user', content: userMessage });

  // 简单截断：保留最近 MAX_MESSAGES 条
  if (history.length > MAX_MESSAGES) {
    history.splice(0, history.length - MAX_MESSAGES);
  }

  const result = streamText({
    model,
    system: buildSystemPrompt(),
    messages: history,
    tools: agentTools,
    maxSteps: MAX_TURNS,
    onStepFinish: ({ stepType, text, toolCalls, toolResults }) => {
      if (stepType === 'tool-result' && toolCalls) {
        for (const tc of toolCalls) {
          console.log(chalk.cyan(`\n  [工具] ${tc.toolName}`));
          const result = toolResults?.find(r => r.toolCallId === tc.toolCallId);
          if (result) {
            const output = String(result.result);
            const truncated = output.length > 500
              ? output.slice(0, 500) + '...(截断)'
              : output;
            console.log(chalk.dim(`  ${truncated.split('\n').join('\n  ')}`));
          }
        }
      }
    },
  });

  let fullResponse = '';
  process.stdout.write(chalk.green('\nAgent: '));

  for await (const chunk of result.textStream) {
    process.stdout.write(chunk);
    fullResponse += chunk;
  }
  console.log();

  history.push({ role: 'assistant', content: fullResponse });
  return history;
}
```

### 5.6 `src/index.ts` — CLI 入口

```typescript
import 'dotenv/config';
import * as readline from 'readline';
import chalk from 'chalk';
import type { CoreMessage } from 'ai';
import { runAgent } from './agent.js';

async function main() {
  console.log(chalk.bold('\n  AI Agent MVP-MIN'));
  console.log(chalk.dim('  输入需求开始工作，输入 /exit 退出\n'));

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  let history: CoreMessage[] = [];

  const prompt = () => {
    rl.question(chalk.blue('You: '), async (input) => {
      const trimmed = input.trim();

      if (!trimmed) return prompt();
      if (trimmed === '/exit') {
        console.log(chalk.dim('  再见！'));
        rl.close();
        return;
      }
      if (trimmed === '/clear') {
        history = [];
        console.log(chalk.dim('  对话已清空'));
        return prompt();
      }

      try {
        history = await runAgent(trimmed, history);
      } catch (err: any) {
        console.error(chalk.red(`\n  错误: ${err.message}`));
      }

      prompt();
    });
  };

  prompt();
}

main();
```

### 5.7 `.env.example` — 配置模板

```bash
# === LLM Provider 配置 ===
# 可选值: anthropic | qwen | deepseek | openai | 自定义名称
AGENT_PROVIDER=anthropic

# 模型 ID（根据 Provider 不同而变化）
# Anthropic: claude-sonnet-4-20250514
# 千问: qwen-max / qwen-turbo / qwen-plus
# DeepSeek: deepseek-chat / deepseek-reasoner
AGENT_MODEL=claude-sonnet-4-20250514

# API Key
AGENT_API_KEY=sk-your-api-key-here

# === 千问专用（可选）===
# DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# === 自定义 Provider 专用（可选）===
# AGENT_BASE_URL=https://api.example.com/v1
```

---

## 6. 提示词模板

MVP-MIN 使用内联模板（`src/prompt.ts`），未来可拆分为文件。核心提示词结构：

```
身份（1 行）:   "You are a coding agent."
规则（5 条）:   先读后改 / 禁止破坏性命令 / 禁止读 .env / 简洁回复 / 建议测试
环境（4 行）:   OS / CWD / Date / Git Branch
工具说明（3 项）: read_file / write_file / run_command
```

**总大小**：~300 tokens，远低于完整版 6K-16K tokens。

---

## 7. 逐日交付计划（5 天）


| Day       | 交付物                                  | 代码量    | 验证标准                         |
| --------- | ------------------------------------ | ------ | ---------------------------- |
| **Day 1** | 项目初始化 + provider.ts + prompt.ts      | ~80 行  | `tsx src/index.ts` 可运行，打印提示词 |
| **Day 2** | tools.ts (3 个工具) + security.ts       | ~140 行 | 工具可独立调用测试                    |
| **Day 3** | agent.ts (ReAct 循环) + index.ts (CLI) | ~140 行 | 端到端对话 + 工具调用可工作              |
| **Day 4** | 联调 + Bug 修复 + 千问/DeepSeek 切换验证       | ~0 行   | 三个 Provider 均可工作             |
| **Day 5** | README + .env.example + 端到端验证        | ~0 行   | 在真实项目上完成一个代码修改               |


**总工作量**：~350 行代码，5 个工作日。

### Day 1 详细步骤

```
1. mkdir ai-agent-mvp-min && cd ai-agent-mvp-min
2. pnpm init
3. pnpm add ai @ai-sdk/anthropic @ai-sdk/openai-compatible zod chalk dotenv
4. pnpm add -D tsx typescript @types/node
5. 创建 tsconfig.json
6. 创建 .env（填入 API Key）
7. 实现 src/provider.ts
8. 实现 src/prompt.ts
9. 创建临时 src/index.ts 验证 Provider 创建和提示词构建
10. 运行: pnpm tsx src/index.ts → 确认可连接 LLM
```

### Day 3 关键验证

```
测试场景 1: 基础对话
> 你好，介绍一下你自己
→ Agent 回复文本（无工具调用）

测试场景 2: 读取文件
> 读取 package.json 的内容
→ Agent 调用 read_file → 返回文件内容

测试场景 3: 修改文件
> 在 package.json 的 scripts 中添加 "build": "tsc"
→ Agent 调用 read_file → 分析 → 调用 write_file

测试场景 4: 执行命令
> 运行 npm test
→ Agent 调用 run_command → 用户确认 → 返回结果

测试场景 5: 安全阻止
> 执行 rm -rf /
→ Agent 调用 run_command → 安全规则阻止
```

---

## 8. 验收标准


| #   | 标准               | 验证方法                            | Day |
| --- | ---------------- | ------------------------------- | --- |
| 1   | Agent 能进行多轮对话    | 连续 3+ 轮对话正常                     | 3   |
| 2   | Agent 能读取文件      | 请求读取 package.json 后返回正确内容       | 3   |
| 3   | Agent 能写入文件      | 请求创建新文件后文件确实生成                  | 3   |
| 4   | Agent 能执行命令（带确认） | 请求运行命令时弹出 Y/n 确认                | 3   |
| 5   | 安全规则阻止危险命令       | 请求 rm -rf / 时被阻止                | 3   |
| 6   | 支持切换到千问模型        | 改 .env 后 Agent 使用千问正常工作         | 4   |
| 7   | 支持切换到 DeepSeek   | 改 .env 后 Agent 使用 DeepSeek 正常工作 | 4   |
| 8   | 20+ 轮对话不崩溃       | 消息截断正常，无 OOM 或 token 溢出         | 4   |
| 9   | 端到端代码修改          | 在真实项目上完成一个简单修改                  | 5   |


---

## 9. MVP-MIN 之后的增量路径

每一步增量都是在 MVP-MIN 基础上**添加一个独立功能**，不需要重写核心代码：

```
MVP-MIN (Day 1-5)
  │  ~350 行, 6 个文件, 3 个工具
  │
  ├─ +1: 添加 Edit 工具（精确替换而非全文重写）
  │  └── 新增 src/tools/edit.ts (~50 行)
  │
  ├─ +2: 添加 Glob + Grep 工具
  │  └── 新增 2 个文件 (~80 行)
  │
  ├─ +3: 提取 ToolRegistry 抽象
  │  └── 重构 tools.ts → tools/registry.ts + tools/*.ts
  │
  ├─ +4: 添加 Token 预算 + Hot Tail
  │  └── 新增 src/context/ (~100 行)
  │
  ├─ +5: 3 层提示词 + Prompt Caching
  │  └── 重构 prompt.ts → prompt/builder.ts + templates/
  │
  ├─ +6: 会话持久化（JSON 文件）
  │  └── 新增 src/memory/session-store.ts (~80 行)
  │
  ├─ +7: 提取 ProviderRegistry
  │  └── 重构 provider.ts → llm/provider-registry.ts
  │
  ├─ +8: 添加 WebSearch + WebFetch 工具
  │  └── 新增 src/search/ (~120 行)
  │
  → 此时达到 V0.3 设计文档中的 MVP（Day 10）水平
  │  约 1000-1200 行代码
  │
  ├─ +9: 技能系统
  ├─ +10: MCP 集成
  ├─ +11: 插件系统
  └─ +12: 自动化
```

### 增量规则

```
每次增量的约束:
├── 只添加/修改，不重写已有代码
├── 新功能用接口抽象，不硬编码
├── 每次增量后原有测试场景仍通过
└── 每次增量控制在 50-120 行新代码
```

### MVP-MIN → MVP 完整版的代码量预估


| 阶段                | 累计代码行     | 累计文件数   | 新增能力                  |
| ----------------- | --------- | ------- | --------------------- |
| MVP-MIN           | ~350      | 6       | 3 工具 + 对话 + 安全        |
| +Edit/Glob/Grep   | ~480      | 9       | 6 工具                  |
| +Token/HotTail    | ~580      | 11      | 上下文管理                 |
| +Prompt 3 层       | ~680      | 14      | 提示词系统                 |
| +会话持久化            | ~760      | 15      | 会话恢复                  |
| +ProviderRegistry | ~820      | 16      | 多 Provider 抽象         |
| +Search 工具        | ~940      | 18      | Web 搜索                |
| +CLI 优化           | ~1050     | 19      | 斜杠命令 + 交互优化           |
| **MVP 完整版**       | **~1100** | **~20** | **对标 V0.3 Day 10 交付** |


