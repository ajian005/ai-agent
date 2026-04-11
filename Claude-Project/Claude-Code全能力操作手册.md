# Claude Code 全能力操作手册

> 生成时间：2026-04-10 | 版本：v2.0
> 覆盖：官方原生能力 + 自定义 Skills/Workflows/Plugins/Hooks/MCP/Agents/Commands

---

## 目录

- [Part A：Claude Code 官方原生能力](#part-aclaude-code-官方原生能力)
  - [A1. 内置斜杠命令（50+）](#a1-内置斜杠命令)
  - [A2. 内置工具（30+）](#a2-内置工具)
  - [A3. 键盘快捷键](#a3-键盘快捷键)
  - [A4. CLI 命令行参数](#a4-cli-命令行参数)
  - [A5. 配置系统（settings.json / CLAUDE.md）](#a5-配置系统)
  - [A6. 权限模式](#a6-权限模式)
  - [A7. 内存系统](#a7-内存系统)
  - [A8. Hook 生命周期（官方26+事件）](#a8-hook-生命周期)
- [Part B：项目自定义能力](#part-b项目自定义能力)
  - [B1. 项目级 Workflows（17个）](#b1-项目级-workflows)
  - [B2. 全局 Skills + gstack（44个）](#b2-全局-skills--gstack)
  - [B3. Plugin Skills（~40个）](#b3-plugin-skills)
  - [B4. GSD 命令集（32个）](#b4-gsd-命令集)
  - [B5. MCP 工具（5组）](#b5-mcp-工具)
  - [B6. 自定义 Hooks（6个）](#b6-自定义-hooks)
  - [B7. Agents（16个）](#b7-agents)
  - [B8. Contexts 工作模式（4个）](#b8-contexts-工作模式)
- [Part C：按场景速查索引](#part-c按场景速查索引)

---

# Part A：Claude Code 官方原生能力

## A1. 内置斜杠命令

> 在对话中直接输入 `/命令名` 使用

### 会话管理

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/clear` | 清空当前对话，从头开始（别名：`/reset`、`/new`） | `/clear` |
| `/compact [提示]` | 压缩上下文窗口，释放空间保留要点 | `/compact "保留：当前任务目标和接口契约"` |
| `/resume` | 恢复上一次会话（别名：`/continue`） | `/resume` |
| `/rewind` | 撤销上一轮 AI 回复，回到之前的状态 | `/rewind` |
| `/rename` | 重命名当前对话 | `/rename 用户模块开发` |
| `/fork-session` | 从现有会话分叉一个新会话 | — |

### 模式与模型

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/fast` | 切换快速模式（同模型，减少思考，更快输出） | `/fast` |
| `/effort <级别>` | 设置思考深度：low / medium / high | `/effort high` |
| `/model` | 显示当前模型信息（不能切换，需 CLI 参数） | `/model` |
| `/plan` | 进入计划模式（只分析不执行） | `/plan` |
| `/ultraplan` | 高级计划模式 | `/ultraplan` |

### 状态查看

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/context` | 显示当前上下文窗口使用百分比 | `/context` |
| `/cost` | 显示当前会话费用 | `/cost` |
| `/usage` | 显示使用统计 | `/usage` |
| `/extra-usage` | 显示额外用量信息 | `/extra-usage` |
| `/stats` | 显示会话统计 | `/stats` |
| `/status` | 显示当前状态 | `/status` |
| `/diff` | 显示本次会话中的所有文件变更 | `/diff` |
| `/tasks` | 查看后台运行的任务 | `/tasks` |

### 项目与配置

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/init` | 为当前项目初始化 CLAUDE.md | `/init` |
| `/config` | 查看和编辑配置 | `/config` |
| `/permissions` | 查看和管理权限规则 | `/permissions` |
| `/memory` | 查看和管理内存/规则 | `/memory` |
| `/add-dir` | 添加工作目录到当前会话 | `/add-dir ../other-project` |
| `/branch` | 创建或切换 git 分支 | `/branch feat/user-auth` |

### 工具与集成

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/mcp` | 管理 MCP 服务器 | `/mcp` |
| `/plugin` | 管理插件 | `/plugin` |
| `/skills` | 管理 Skills | `/skills` |
| `/hooks` | 管理 Hooks | `/hooks` |
| `/agents` | 管理 Agents 和 Agent 团队 | `/agents` |
| `/chrome` | 打开 Chrome DevTools 集成 | `/chrome` |
| `/ide` | IDE 集成管理 | `/ide` |
| `/desktop` | 打开 Claude 桌面应用集成 | `/desktop` |
| `/sandbox` | 配置沙箱设置 | `/sandbox` |

### 输出与导出

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/copy` | 复制对话内容到剪贴板 | `/copy` |
| `/export` | 导出对话到文件 | `/export` |
| `/insights` | 生成会话洞察报告 | `/insights` |
| `/color` | 切换彩色输出 | `/color` |
| `/theme` | 切换主题 | `/theme` |

### 账户与系统

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/login` | 登录 Anthropic 账户 | `/login` |
| `/logout` | 登出 | `/logout` |
| `/upgrade` | 升级 Claude Code 到最新版本 | `/upgrade` |
| `/release-notes` | 查看发布说明 | `/release-notes` |
| `/doctor` | 运行诊断检查 Claude Code 健康状态 | `/doctor` |
| `/feedback` | 向 Anthropic 提交反馈 | `/feedback` |
| `/help` | 显示帮助信息 | `/help` |
| `/exit` | 退出 Claude Code（别名：`/quit`） | `/exit` |
| `/voice` | 切换语音输入 | `/voice` |
| `/keybindings` | 查看或自定义快捷键 | `/keybindings` |

### 安全与部署

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/security-review` | 对当前变更运行安全审查 | `/security-review` |
| `/autofix-pr` | 自动修复 PR 中的问题 | `/autofix-pr` |
| `/setup-bedrock` | 设置 Amazon Bedrock 集成 | `/setup-bedrock` |
| `/install-github-app` | 安装 Claude Code GitHub App | `/install-github-app` |
| `/install-slack-app` | 安装 Claude Code Slack App | `/install-slack-app` |

### 其他

| 命令 | 用途 | 使用示例 |
|------|------|----------|
| `/btw` | 问一个旁路问题，不打断主任务 | `/btw 这个变量是什么意思？` |
| `/schedule` | 安排定时任务 | `/schedule` |
| `/passes` | 配置编辑器 passes | `/passes` |
| `/powerup` | Power-up 管理 | `/powerup` |
| `/reload-plugins` | 重新加载所有插件 | `/reload-plugins` |
| `/privacy-settings` | 配置隐私设置 | `/privacy-settings` |
| `/remote-env` | 配置远程环境 | `/remote-env` |
| `/remote-control` | 远程控制管理 | `/remote-control` |
| `/teleport` | 传送到远程环境 | `/teleport` |
| `/terminal-setup` | 配置终端设置 | `/terminal-setup` |
| `/web-setup` | Web 开发设置 | `/web-setup` |
| `/statusline` | 配置状态栏 UI | `/statusline` |

### 快速前缀（非 / 命令）

| 前缀 | 用途 | 示例 |
|------|------|------|
| `!` | 直接执行 Bash 命令（不经过 AI） | `!ls -la` |
| `@` | 引用文件（将文件内容注入上下文） | `@src/App.vue 看看这个组件` |
| `Shift+Tab` | 循环切换权限模式 | — |
| `Option+P` | 切换模型 | — |
| `Option+T` | 切换扩展思考 | — |
| `Option+O` | 切换快速模式 | — |

---

## A2. 内置工具

> AI 自动调用，用户无需手动触发，但了解其能力有助于正确描述需求

### 文件操作

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| **Read** | 读取文件内容（支持图片、PDF、Jupyter笔记本） | "看看 src/App.vue 的内容" |
| **Write** | 创建新文件或完全覆盖文件 | "创建一个新组件 Button.vue" |
| **Edit** | 精确搜索替换文件中的特定字符串 | "把第42行的 foo 改成 bar" |
| **Glob** | 按模式搜索文件名（如 `**/*.tsx`） | "找一下所有 Vue 组件" |
| **Grep** | 搜索文件内容（基于 ripgrep，支持正则） | "搜索所有使用了 useState 的文件" |
| **NotebookEdit** | 编辑 Jupyter Notebook 单元格 | "修改 notebook 的第三个 cell" |

### 执行与分析

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| **Bash** | 执行 Shell 命令（独立进程，cwd 持久） | "运行 npm run build" |
| **LSP** | 语言服务器协议（定义跳转/引用/悬停/类型错误） | "找一下这个函数的所有调用方" |
| **WebSearch** | 搜索互联网获取最新信息 | "搜索 Vue 3.5 的新特性" |
| **WebFetch** | 抓取 URL 内容 | — |

### 交互与规划

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| **AskUserQuestion** | 向用户提问（最多4个问题，支持选项和预览） | AI 需要澄清需求时自动触发 |
| **EnterPlanMode** | 进入计划模式（先分析后执行） | 复杂任务前 AI 先规划 |
| **ExitPlanMode** | 退出计划模式，等待用户批准 | — |
| **TodoWrite** | 管理任务列表（追踪进度） | AI 自动创建待办列表 |

### Agent 与任务

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| **Agent** | 生成子代理执行委派任务（支持多种类型） | AI 自动调度子任务 |
| **EnterWorktree** | 创建隔离的 Git 工作树 | "在一个 worktree 里开发" |
| **ExitWorktree** | 退出工作树 | — |

### 定时任务

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| **CronCreate** | 创建定时任务（支持 cron 表达式） | "每5分钟检查一次部署状态" |
| **CronDelete** | 删除定时任务 | — |
| **CronList** | 列出所有定时任务 | — |

### 技能

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| **Skill** | 加载并执行一个 Skill | `/commit`、`/gsd:progress` 等斜杠命令的底层机制 |

---

## A3. 键盘快捷键

### 基本控制

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 取消当前操作 / 清空输入 |
| `Ctrl+D` | 退出 Claude Code |
| `Ctrl+L` | 清空输入行 |
| `Ctrl+G` | 打开外部编辑器 |
| `Ctrl+O` | 打开对话查看器 |
| `Ctrl+R` | 反向搜索历史 |
| `Ctrl+V` | 从剪贴板粘贴图片 |
| `Ctrl+B` | 查看后台任务 |
| `Ctrl+T` | 切换任务列表 |
| `Esc Esc` | 撤销上一轮回复（同 /rewind） |
| `Shift+Tab` | 循环切换权限模式 |
| `Option+P / Alt+P` | 切换模型 |
| `Option+T / Alt+T` | 切换扩展思考 |
| `Option+O / Alt+O` | 切换快速模式 |
| `Up/Down` | 浏览历史/建议列表 |
| `Ctrl+X Ctrl+K` | 终止所有运行中的 agents |

### 多行输入

| 快捷键 | 功能 |
|--------|------|
| `\ + Enter` | 插入新行 |
| `Option + Enter` | 插入新行 |
| `Shift + Enter` | 插入新行 |
| `Ctrl+J` | 插入新行 |

### 文本编辑（Emacs 风格）

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+K` | 剪切到行尾 |
| `Ctrl+U` | 剪切到行首 |
| `Ctrl+Y` | 粘贴 |
| `Alt+B` | 向前移一个单词 |
| `Alt+F` | 向后移一个单词 |

### Vim 模式

通过 `/terminal-setup` 或 `~/.claude.json` 的 `editorMode: "vim"` 启用。支持完整 Vim 操作：
- 移动：`h/j/k/l`、`w/b/e`、`0/$`、`gg/G`
- 编辑：`i/a/I/A/o/O`、`x/r/s`、`dd/dw/d$`、`cc/cw`、`yy/p`
- 文本对象：`diw`、`ci"`、`da(`
- 可视模式：`v/V/Ctrl+V`
- 搜索：`/`、`?`、`n/N`
- 撤销：`u`、`Ctrl+R`

### 语音输入

| 操作 | 功能 |
|------|------|
| `按住 Space` | 按住说话（Push-to-talk） |

---

## A4. CLI 命令行参数

> 在终端中通过 `claude` 命令启动时使用

### 基本用法

```bash
claude                        # 交互模式
claude -p "你的提示"           # 非交互模式，输出到 stdout
claude update                 # 更新 Claude Code
```

### 会话管理

| 参数 | 用途 | 示例 |
|------|------|------|
| `--resume` / `-r` | 恢复最近会话 | `claude -r` |
| `--continue` / `-c` | 继续最近对话 | `claude -c` |
| `--name` / `-n` | 命名会话 | `claude -n "用户模块开发"` |
| `--fork-session` | 从现有会话分叉 | — |
| `--from-pr` | 从 PR 加载上下文 | `claude --from-pr 123` |

### 模型与行为

| 参数 | 用途 | 示例 |
|------|------|------|
| `--model` | 指定模型 | `claude --model opus` |
| `--effort` | 设置思考深度 | `claude --effort high` |
| `--permission-mode` | 设置权限模式 | `claude --permission-mode plan` |
| `--dangerously-skip-permissions` | 跳过所有权限提示 | ⚠️ 谨慎使用 |
| `--max-turns` | 限制对话轮数 | `claude -p "fix bug" --max-turns 5` |
| `--max-budget-usd` | 设置最大花费预算 | `claude --max-budget-usd 5` |

### 系统提示

| 参数 | 用途 | 示例 |
|------|------|------|
| `--system-prompt` | 替换默认系统提示 | — |
| `--system-prompt-file` | 从文件加载系统提示 | — |
| `--append-system-prompt` | 追加到系统提示 | — |
| `--append-system-prompt-file` | 从文件追加 | — |

### 工具与 MCP

| 参数 | 用途 | 示例 |
|------|------|------|
| `--tools` | 指定可用工具 | — |
| `--allowedTools` | 白名单工具 | — |
| `--disallowedTools` | 黑名单工具 | — |
| `--mcp-config` | MCP 配置文件路径 | — |

### 输出格式

| 参数 | 用途 | 示例 |
|------|------|------|
| `--output-format` | 输出格式（text/json/stream-json） | `claude -p "..." --output-format json` |
| `--verbose` | 详细输出 | — |
| `--debug` | 调试模式 | — |
| `--bare` | 最简 UI 模式 | — |

### 其他

| 参数 | 用途 | 示例 |
|------|------|------|
| `--worktree` / `-w` | 创建/使用 git worktree | `claude -w` |
| `--add-dir` | 添加工作目录 | `claude --add-dir ../backend` |
| `--settings` | 指定 settings 文件 | — |

### 子命令

```bash
claude auth login             # 登录
claude auth logout            # 登出
claude auth status            # 查看认证状态
claude mcp                    # 管理 MCP 服务器
claude plugin                 # 管理插件
claude agents                 # 管理 Agents
```

---

## A5. 配置系统

### 配置文件层级（优先级从高到低）

| 层级 | 文件 | 说明 |
|------|------|------|
| 1. 企业管理 | `managed-settings.json` | IT 管理员设置，最高优先级 |
| 2. 命令行参数 | `claude --model opus` 等 | 覆盖以下所有层级 |
| 3. 项目本地 | `.claude/settings.local.json` | 每个项目，gitignored，个人偏好 |
| 4. 项目共享 | `.claude/settings.json` | 每个项目，提交到 git，团队共享 |
| 5. 用户全局 | `~/.claude/settings.json` | 全局用户设置，最低优先级 |

### settings.json 主要字段

```jsonc
{
  "model": "sonnet",              // 默认模型
  "effortLevel": "high",          // 思考深度 low/medium/high
  "env": {},                      // 环境变量
  "permissions": {
    "allow": ["Bash(*)", "Read(*)"],    // 允许的工具
    "deny": ["Bash(git push *)"]        // 拒绝的工具
  },
  "hooks": {},                    // Hook 配置
  "enabledPlugins": {},           // 启用的插件
  "sandbox": {},                  // 沙箱配置
  "autoUpdatesChannel": "stable"  // 更新通道 stable/beta/canary
}
```

### 权限规则语法

```
工具名(匹配模式)
```

- 评估顺序：**deny > ask > allow**（先拒绝，再询问，最后允许）
- 支持 Glob 模式

| 示例规则 | 含义 |
|----------|------|
| `Bash(*)` | 允许所有 Bash 命令 |
| `Bash(git push *)` | 匹配 git push 命令 |
| `Read(**/.env)` | 读取 .env 文件 |
| `Write(**/*.key)` | 写入 .key 文件 |
| `mcp__server__tool_name` | 特定 MCP 工具 |

### CLAUDE.md 层级（指令加载顺序）

| 层级 | 文件 | 说明 |
|------|------|------|
| 1. 全局 | `~/.claude/CLAUDE.md` | 所有项目生效 |
| 2. 项目根 | `<项目>/.claude/CLAUDE.md` | 提交到 git，团队共享 |
| 3. 项目本地 | `<项目>/.claude/CLAUDE.local.md` | gitignored，个人偏好 |
| 4. 子目录 | `<项目>/<子目录>/.claude/CLAUDE.md` | 目录级规则 |
| 5. 父目录 | 逐级向上查找 `.claude/CLAUDE.md` | — |

### ~/.claude.json 全局配置

```jsonc
{
  "autoConnectIde": true,            // 自动连接 IDE
  "autoInstallIdeExtension": true,   // 自动安装 IDE 扩展
  "editorMode": "default",           // 编辑器模式 default/vim
  "showTurnDuration": true,          // 显示轮次耗时
  "theme": "dark",                   // 主题
  "notifications": {},               // 通知设置
  "mcpServers": {}                   // MCP 服务器配置
}
```

---

## A6. 权限模式

> 通过 `Shift+Tab` 循环切换 或 `--permission-mode` 指定

| 模式 | 说明 | 适合场景 |
|------|------|----------|
| **Default** | 文件写入和 Shell 命令需确认 | 日常开发（默认） |
| **acceptEdits** | 自动接受文件编辑，Shell 命令需确认 | 大量文件修改 |
| **plan** | 只规划不执行（只读模式） | 需求分析、架构设计 |
| **auto** | 自动接受一切 | CI/CD、自动化脚本 |
| **dontAsk** | 跳过所有提示，使用默认决策 | 批量处理 |
| **bypassPermissions** | 完全跳过权限系统 | ⚠️ 仅限受信环境 |

### 交互式权限应答

当 AI 请求权限时，可以选择：
- **Allow once** — 本次允许
- **Allow always** — 永久允许（写入 settings.json）
- **Deny** — 拒绝

---

## A7. 内存系统

### 三层记忆架构

| 层级 | 机制 | 生命周期 | 用途 |
|------|------|----------|------|
| **CLAUDE.md 规则** | 文件加载 | 永久（随文件） | 项目约定、编码规范 |
| **自动记忆** | `/memory` 管理 | 跨会话 | 用户偏好、项目状态 |
| **会话上下文** | 对话历史 | 单次会话 | 当前任务上下文 |

### 自动记忆操作

| 操作 | 方法 | 示例 |
|------|------|------|
| 让 AI 记住某事 | 直接说"记住..." | "记住我喜欢用 TDD" |
| 查看记忆 | `/memory` | — |
| 删除记忆 | "忘记..." | "忘记之前关于 X 的记忆" |

### 上下文压缩（Context Compaction）

| 操作 | 用法 | 说明 |
|------|------|------|
| 手动压缩 | `/compact "保留要点"` | 压缩并保留指定内容 |
| 自动压缩 | — | 上下文快满时自动触发 |
| 恢复锚点 | 项目使用 `cat .claude/compact-anchor.txt` | 压缩后恢复核心约束 |

### 会话持久化

| 操作 | 方法 | 说明 |
|------|------|------|
| 恢复上次会话 | `/resume` 或 `claude -r` | 恢复完整对话历史 |
| 继续上次对话 | `/continue` 或 `claude -c` | 继续最近的对话 |
| 文件记忆（本项目） | `task_plan.md` + `progress.md` + `findings.md` | planning-with-files Skill |

---

## A8. Hook 生命周期

> Hook 是在特定事件触发时自动执行的脚本/HTTP请求/AI判断

### 官方支持的 26+ 事件

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| **SessionStart** | 会话开始 | 环境检查、加载配置 |
| **SessionEnd** | 会话结束 | 清理、统计 |
| **InstructionsLoaded** | 指令加载完成后 | 注入额外上下文 |
| **UserPromptSubmit** | 用户提交提示后 | 输入验证、预处理 |
| **Notification** | 通知事件 | 桌面通知、状态更新 |
| **PreToolUse** | 工具执行前 | 安全拦截、参数修改 |
| **PostToolUse** | 工具成功执行后 | 后处理、日志、验证 |
| **PostToolUseFailure** | 工具执行失败后 | 错误处理、告警 |
| **PermissionRequest** | 权限请求时 | 自定义权限逻辑 |
| **PermissionDenied** | 权限被拒绝后 | 日志记录 |
| **SubagentStart** | 子代理启动时 | — |
| **SubagentStop** | 子代理完成时 | — |
| **TaskCreated** | 任务创建时 | — |
| **TaskCompleted** | 任务完成时 | — |
| **Stop** | Agent 正常停止时 | — |
| **StopFailure** | Agent 异常停止时 | — |
| **ConfigChange** | 配置变更时 | — |
| **CwdChanged** | 工作目录变更时 | — |
| **FileChanged** | 文件变更时 | — |
| **WorktreeCreate** | Worktree 创建时 | — |
| **WorktreeRemove** | Worktree 移除时 | — |
| **PreCompact** | 压缩前 | 保存关键上下文 |
| **PostCompact** | 压缩后 | 恢复锚点 |
| **Elicitation** | MCP 求解事件 | — |
| **ElicitationResult** | MCP 求解结果 | — |
| **TeammateIdle** | 团队成员空闲时 | — |

### Hook 处理器类型

| 类型 | 说明 | 适合场景 |
|------|------|----------|
| `command` | 执行 Shell 命令 | 验证、日志、预处理 |
| `http` | 发送 HTTP POST | 远程通知、CI 触发 |
| `prompt` | LLM 评估 | 动态决策、内容分析 |
| `agent` | 带 tools 的子代理 | 复杂工作流 |

### Hook 退出码

| 码 | 含义 |
|----|------|
| `0` | 成功 / 允许 |
| `2` | 阻断错误（停止操作） |
| 其他 | 非阻断错误（警告日志，操作继续） |

### Hook 输出格式

```json
{
  "decision": "allow|deny|ask|defer",
  "additionalContext": "补充给 AI 的上下文",
  "updatedInput": {}  // PreToolUse 可修改工具参数
}
```

---

# Part B：项目自定义能力

## B1. 项目级 Workflows

> 存放：`.agents/workflows/` | 调用：自然语言触发 或 `/命令名`

### 开发核心流程

| 命令 | 触发语 | 用途 | 使用方法 |
|------|--------|------|----------|
| `/requirement-parse` | "解析需求"、"分析原型" | 从 prototype 设计稿解析出规范化需求文档 | 1. 确认 `prototype/` 有设计稿<br>2. 说"解析需求"或直接 `/requirement-parse`<br>3. 自动六维度提取<br>4. 输出到 `ai-doc/需求解析/` |
| `/requirement-audit` | "审计需求"、"检查需求" | 六维度需求审计 | 1. 确认 `ai-doc/需求解析/` 有文档<br>2. 说"审计需求"<br>3. 发现必须修改项则阻断开发 |
| `/module-dev` | "开发模块"、"实现功能" | 单模块标准开发循环 | 1. 说"开发 XX 模块"<br>2. 自动：设计→开发→审计→自测<br>3. 最多5轮修复循环 |
| `/new-feature` | "新增功能"、"开发新功能" | 新功能完整生命周期 | 1. 说"新增 XX 功能"<br>2. 自动：业务价值验证→技术设计→执行→验证 |
| `/bugfix` | "有bug"、"报错了"、"功能异常" | 强制四步调试协议 | 1. 说"有 bug" + 描述现象<br>2. 自动：收集症状→假设→验证→最小修复 |
| `/qa-cycle` | "质检"、"全面测试" | 对抗性 QA 循环 | 1. 说"质检"<br>2. Critic 找问题 → Fixer 修复 → 再审<br>3. 最多5轮 |

### 架构与协调

| 命令 | 触发语 | 用途 | 使用方法 |
|------|--------|------|----------|
| `/conductor` | "生成执行计划"、"跨端协调" | 跨端协调执行计划 | 1. 说"生成执行计划"<br>2. 自动分析模块依赖<br>3. 产出分阶段执行计划到 `final_doc/plans/` |
| `/linear-walkthrough` | "走读代码"、"了解模块" | 结构化代码走读（只读） | 1. 说"走读 XX 模块的代码"<br>2. 按层扫描输出走读报告 |
| `/project-rules` | "加载项目规则" | 加载项目开发契约 | 直接 `/project-rules` |

### 安全变更

| 命令 | 触发语 | 用途 | 使用方法 |
|------|--------|------|----------|
| `/api-change` | "修改接口"、"接口变更" | 接口变更安全检查 | 1. 说"修改 XX 接口" + 描述变更<br>2. 自动影响分析<br>3. 等待你确认后执行 |
| `/db-migration` | "数据库变更"、"修改表结构" | 安全数据库迁移 | 1. 说"修改 XX 表"<br>2. 自动生成前进+回滚 SQL<br>3. 等待你确认后执行 |

### IDE 协作

| 命令 | 触发语 | 用途 | 使用方法 |
|------|--------|------|----------|
| `/handoff` | "生成交接卡"、"切换IDE" | CC ↔ AG 交接 | 1. 准备切换 IDE 前说"生成交接卡"<br>2. 自动产出交接卡到 `final_doc/plans/handoffs/` |

### 非编码业务

| 命令 | 触发语 | 输出目录 |
|------|--------|----------|
| `/market-analysis` "市场分析" | PEST + 竞争矩阵 + TAM/SAM/SOM + SWOT | `ai-doc/市场分析/` |
| `/growth-ops` "增长策略" | AARRR 漏斗 + 渠道评估 + 增长实验 | `ai-doc/运营方案/` |
| `/legal-compliance` "法律合规" | PIPL/GDPR + 知识产权 + 经营合规 | `ai-doc/合规评估/` |
| `/security-audit` "安全审计" | OWASP Top10 + 代码级扫描 + 权限审查 | `ai-doc/安全审计/` |
| `/devops-ops` "部署方案" | CI/CD + 容器化 + 监控 + 容灾 | `ai-doc/运维方案/` |

---

## B2. 全局 Skills + gstack

> 存放：`~/.claude/skills/` | gstack 版本：1.1.0

### 核心流程 Skill

| Skill | 触发语 | 用途 | 使用方法 |
|-------|--------|------|----------|
| **planning-with-files** | "开始任务"、"继续上次" | 跨 session 三文件记忆 | 自动维护 `task_plan.md` + `progress.md` + `findings.md`。说"开始任务"创建，说"继续上次"恢复 |
| **systematic-debugging** | "有bug"、"报错了" | 四步调试协议 | 说"有 bug"+ 描述症状。禁止猜测，强制按协议：复现→假设→验证→迭代 |
| **verification-before-completion** | 说"完成了"时自动触发 | 完成前五维验证 | AI 准备声称完成时自动检查：三文件/功能/代码质量/集成/安全 |

### gstack 浏览器 QA 工具箱（34 子能力）

> 入口：输入 `/子命令` 或自然语言触发

#### QA 测试

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/browse` | 无头浏览器：截图/交互/验证 | `/browse https://localhost:3000 截图首页` |
| `/qa` | 系统化 QA + 自动修复 | `/qa 测试登录功能` |
| `/qa-only` | 仅报告模式（不修复） | `/qa-only 检查首页布局` |
| `/benchmark` | 性能回归检测 | `/benchmark 测量首页加载时间` |
| `/canary` | 发布后金丝雀监控 | `/canary 监控生产环境` |
| `/webapp-testing` | 本地 Web 应用测试 | `/webapp-testing 测试 localhost:5173` |

#### 代码审查

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/review` | PR 审查 | `/review` 或 `/review PR #123` |
| `/design-review` | 设计还原 QA | `/design-review 对比设计稿和实现` |

#### 设计

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/design-consultation` | 设计系统咨询 | `/design-consultation 设计一套按钮组件` |
| `/design-html` | 生成生产 HTML/CSS | `/design-html 从 mockup 生成代码` |
| `/design-shotgun` | 多设计变体对比 | `/design-shotgun 生成3种首页布局` |

#### 计划评审

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/plan-ceo-review` | CEO 视角评审 | `/plan-ceo-review 评审当前计划` |
| `/plan-design-review` | 设计师视角评审 | `/plan-design-review` |
| `/plan-eng-review` | 工程经理视角评审 | `/plan-eng-review 评审技术方案` |
| `/autoplan` | 自动串行评审 | `/autoplan` |

#### 业务验证

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/office-hours` | YC Office Hours 模式 | `/office-hours 验证这个功能值不值得做` |
| `/checkpoint` | 保存/恢复状态 | `/checkpoint save` / `/checkpoint restore` |
| `/retro` | 周工程回顾 | `/retro` |
| `/learn` | 经验教训管理 | `/learn review` / `/learn search "登录"` |

#### 部署

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/ship` | 发布流程 | `/ship` |
| `/land-and-deploy` | 合并+部署+验证 | `/land-and-deploy PR #45` |
| `/setup-deploy` | 配置部署目标 | `/setup-deploy` |
| `/document-release` | 发布后文档更新 | `/document-release` |

#### 安全防护

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/careful` | 破坏性命令拦截 | `/careful` 激活 |
| `/freeze` | 限制编辑到指定目录 | `/freeze src/components/` |
| `/guard` | 完全安全模式 | `/guard` |
| `/unfreeze` | 解除编辑限制 | `/unfreeze` |
| `/health` | 代码质量仪表盘(0-10) | `/health` |

#### 调试与安全

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/investigate` | 系统化根因调查 | `/investigate 为什么首页加载慢` |
| `/cso` | 首席安全官模式 | `/cso 审查认证模块` |

#### 工具

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/connect-chrome` | 启动真实 Chrome | `/connect-chrome` |
| `/codex` | OpenAI Codex CLI | `/codex review` |
| `/gstack-upgrade` | 升级 gstack | `/gstack-upgrade` |
| `/setup-browser-cookies` | 导入浏览器 cookies | `/setup-browser-cookies` |

### 技能库（_library）

| Skill | 触发方式 | 用途 | 使用方法 |
|-------|----------|------|----------|
| **code-reader** (v2.0) | 自动（doc-auditor 调用） | 防幻觉代码读取 | 无需手动调用，其他 Skill 自动使用 |
| **doc-auditor** (v1.0) | `/requirement-audit` | 文档-代码一致性审计 | 通常通过 `/requirement-audit` 间接触发 |
| **sync-docs** (v1.0) | `@sync-docs` | 代码-文档同步 | 输入 `@sync-docs` |
| **github-kb** | "github"、"repo" | 本地仓库管理 | "克隆 XX 仓库"、"搜索 XX 项目" |
| **prompt-os** (v1.0) | `@PROMPT-OS` | Prompt 优化系统 | 输入 `@PROMPT-OS + 你的需求` |

---

## B3. Plugin Skills

> 调用：`/插件名:技能名` 或自然语言触发

### superpowers 插件（v5.0.7）

| 技能 | 用途 | 使用方法 |
|------|------|----------|
| **brainstorming** | 创意工作前的头脑风暴 | `/superpowers:brainstorming` 或描述你想创建的功能 |
| **writing-plans** | 多步骤任务的计划编写 | `/superpowers:writing-plans` + 需求描述 |
| **executing-plans** | 执行已有计划 | `/superpowers:executing-plans` |
| **dispatching-parallel-agents** | 并行处理2+个独立任务 | `/superpowers:dispatching-parallel-agents` |
| **subagent-driven-development** | 子代理驱动开发 | `/superpowers:subagent-driven-development` |
| **test-driven-development** | TDD：先写测试再写代码 | `/superpowers:test-driven-development` + 功能描述 |
| **systematic-debugging** | 系统化调试 | `/superpowers:systematic-debugging` |
| **verification-before-completion** | 完成前验证 | `/superpowers:verification-before-completion` |
| **using-git-worktrees** | 隔离的功能开发 | `/superpowers:using-git-worktrees` |
| **requesting-code-review** | 请求代码审查 | `/superpowers:requesting-code-review` |
| **receiving-code-review** | 处理审查反馈 | `/superpowers:receiving-code-review` |
| **finishing-a-development-branch** | 完成开发分支 | `/superpowers:finishing-a-development-branch` |
| **writing-skills** | 创建/编辑 Skills | `/superpowers:writing-skills` |

### feature-dev 插件

| 技能 | 用途 | 使用方法 |
|------|------|----------|
| **feature-dev** | 引导式功能开发 | `/feature-dev:feature-dev` + 功能描述 |

### code-review 插件

| 技能 | 用途 | 使用方法 |
|------|------|----------|
| **code-review** | PR 代码审查 | `/code-review:code-review` |

### frontend-design 插件

| 技能 | 用途 | 使用方法 |
|------|------|----------|
| **frontend-design** | 创建生产级前端界面 | `/frontend-design:frontend-design` + 界面描述 |

### figma 插件（v2.0.2）

| 技能 | 用途 | 使用方法 |
|------|------|----------|
| **figma-use** | Figma 基础（必须最先调用） | `/figma:figma-use` |
| **figma-implement-design** | Figma 设计转代码 | 先 figma-use，再 `/figma:figma-implement-design` |
| **figma-generate-design** | 从 Figma 生成 UI | 先 figma-use，再 `/figma:figma-generate-design` |
| **figma-generate-library** | 构建设计系统库 | `/figma:figma-generate-library` |
| **figma-create-design-system-rules** | 生成设计系统规则 | `/figma:figma-create-design-system-rules` |
| **figma-code-connect-components** | 连接 Figma 到代码组件 | `/figma:figma-code-connect-components` |

> 首次使用需 OAuth 认证，AI 会自动引导。

### example-skills 插件

| 技能 | 用途 | 使用方法 |
|------|------|----------|
| **pdf** | PDF 处理 | `/example-skills:pdf` + "创建一份报告 PDF" |
| **docx** | Word 文档 | `/example-skills:docx` + "写一份需求文档" |
| **pptx** | PPT 演示 | `/example-skills:pptx` + "做10页产品介绍" |
| **xlsx** | Excel 表格 | `/example-skills:xlsx` + "创建预算表" |
| **canvas-design** | p5.js 算法艺术 | `/example-skills:canvas-design` |
| **mcp-builder** | 创建 MCP 服务器 | `/example-skills:mcp-builder` |
| **skill-creator** | 创建/修改 Skills | `/example-skills:skill-creator` |
| **claude-api** | Claude API 应用 | `/example-skills:claude-api` |
| **doc-coauthoring** | 文档协作 | `/example-skills:doc-coauthoring` |
| **internal-comms** | 内部沟通文档 | `/example-skills:internal-comms` |
| **web-artifacts-builder** | Web 作品集 | `/example-skills:web-artifacts-builder` |
| **slack-gif-creator** | Slack 动图 | `/example-skills:slack-gif-creator` |
| **theme-factory** | 主题样式 | `/example-skills:theme-factory` |
| **brand-guidelines** | Anthropic 品牌风格 | `/example-skills:brand-guidelines` |
| **algorithmic-art** | 种子随机艺术 | `/example-skills:algorithmic-art` |
| **webapp-testing** | Web 应用测试 | `/example-skills:webapp-testing` |

### 其他插件（自动工作）

| 插件 | 用途 | 说明 |
|------|------|------|
| **context7** | 获取最新库文档 | AI 需要查库文档时自动调用 |
| **jdtls-lsp** (v1.0) | Java LSP 代码智能 | Java 文件中自动提供跳转/补全 |
| **typescript-lsp** (v1.0) | TypeScript LSP | TS/JS 文件中自动提供跳转/补全 |
| **security-guidance** | 安全指导 | AI 编码时自动参考安全最佳实践 |

---

## B4. GSD 命令集

> 调用：`/gsd:命令名` | 完整的项目管理生命周期

### 项目初始化与规划

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/gsd:new-project` | 初始化新项目 | `/gsd:new-project` → 自动收集上下文并创建 PROJECT.md |
| `/gsd:new-milestone` | 开始新里程碑 | `/gsd:new-milestone` → 更新 PROJECT.md |
| `/gsd:add-phase` | 添加阶段到当前里程碑 | `/gsd:add-phase` |
| `/gsd:insert-phase` | 插入紧急小数阶段 | `/gsd:insert-phase 72.1 紧急修复` |
| `/gsd:remove-phase` | 移除未来阶段 | `/gsd:remove-phase 3` |
| `/gsd:plan-phase` | 创建阶段详细计划 | `/gsd:plan-phase` → 产出 PLAN.md |
| `/gsd:research-phase` | 研究阶段实现方式 | `/gsd:research-phase` |
| `/gsd:discuss-phase` | 规划前收集上下文 | `/gsd:discuss-phase` → 通过问答澄清需求 |

### 执行与验证

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/gsd:execute-phase` | 执行阶段计划 | `/gsd:execute-phase` → 波次并行执行 |
| `/gsd:verify-work` | UAT 验证 | `/gsd:verify-work` → 对话式用户验收测试 |
| `/gsd:add-tests` | 生成测试 | `/gsd:add-tests` → 基于 UAT 标准生成 |
| `/gsd:validate-phase` | 回溯审计验证 | `/gsd:validate-phase` |

### 进度管理

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/gsd:progress` | 查看项目进度 | `/gsd:progress` |
| `/gsd:pause-work` | 暂停并交接 | `/gsd:pause-work` |
| `/gsd:resume-work` | 恢复上次工作 | `/gsd:resume-work` |
| `/gsd:checkpoint` | 保存当前状态 | `/gsd:checkpoint` |

### 里程碑管理

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/gsd:audit-milestone` | 里程碑审计 | `/gsd:audit-milestone` |
| `/gsd:complete-milestone` | 归档完成里程碑 | `/gsd:complete-milestone` |
| `/gsd:plan-milestone-gaps` | 填补审计缺口 | `/gsd:plan-milestone-gaps` |
| `/gsd:cleanup` | 归档旧目录 | `/gsd:cleanup` |

### 辅助工具

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/gsd:map-codebase` | 分析代码库 | `/gsd:map-codebase` → 并行 mapper agents |
| `/gsd:debug` | 系统化调试 | `/gsd:debug` |
| `/gsd:quick` | 快速任务 | `/gsd:quick 实现登录表单` |
| `/gsd:add-todo` | 捕获想法 | `/gsd:add-todo 需要优化查询性能` |
| `/gsd:check-todos` | 查看待办 | `/gsd:check-todos` |
| `/gsd:list-phase-assumptions` | 列出假设 | `/gsd:list-phase-assumptions` |
| `/gsd:health` | 诊断规划目录 | `/gsd:health` |

### 配置与维护

| 命令 | 用途 | 使用方法 |
|------|------|----------|
| `/gsd:settings` | 配置工作流开关 | `/gsd:settings` |
| `/gsd:set-profile` | 切换模型配置 | `/gsd:set-profile quality` / `balanced` / `budget` |
| `/gsd:update` | 更新 GSD | `/gsd:update` |
| `/gsd:reapply-patches` | 更新后重新应用修改 | `/gsd:reapply-patches` |
| `/gsd:help` | 帮助 | `/gsd:help` |

---

## B5. MCP 工具

> AI 自动调用，了解其能力有助于正确描述需求

### Context7（库文档查询）

| 工具 | 用途 | 如何触发 |
|------|------|----------|
| `resolve-library-id` | 解析库名 | — |
| `query-docs` | 查询最新文档 | 说"Vue 3 的 Composition API 怎么用？" 或 "查一下 Spring Boot 的最新配置方式" |

### Chrome DevTools（浏览器自动化）

> 25 个工具，`mcp__chrome-devtools__*` 命名空间

| 工具类别 | 能力 | 如何触发 |
|----------|------|----------|
| 页面导航 | navigate, screenshot, click, fill | "打开 localhost:3000 并截图"、"点击登录按钮" |
| 脚本执行 | evaluate_script | "在页面上执行一段 JS" |
| 性能分析 | lighthouse_audit, performance tracing | "跑一次 Lighthouse 审计" |
| 内存分析 | memory snapshots | "检查内存泄漏" |

### Web Reader

| 工具 | 用途 | 如何触发 |
|------|------|----------|
| `webReader` | 抓取 URL 转为 Markdown | "读取这个网页的内容：https://..." |

### Image Analysis

| 工具 | 用途 | 如何触发 |
|------|------|----------|
| `analyze_image` | 分析远程图片（仅 URL） | "分析这张图片：https://...png" |

### IDE 集成

| 工具 | 用途 | 如何触发 |
|------|------|----------|
| `executeCode` | 在 Jupyter 中执行 Python | — |
| `getDiagnostics` | 获取 VS Code 诊断 | — |

### Figma（需 OAuth）

| 工具 | 用途 | 如何触发 |
|------|------|----------|
| `authenticate` | OAuth 认证 | 首次使用 Figma 技能时自动引导 |

---

## B6. 自定义 Hooks

> 脚本：`~/.claude/hooks/` | 自动触发，无需手动调用

| Hook | 触发事件 | 脚本 | 行为 |
|------|----------|------|------|
| **通知+检查** | Notification | `notify-and-check.sh` | macOS 通知 + 检查三文件是否过期(>15min) |
| **状态栏** | Notification | `gsd-statusline.js` | 显示模型/任务/目录/上下文使用率 |
| **Bash 安全** | PreToolUse(Bash) | `pre-bash-check.sh` | 阻断 DROP TABLE/rm -rf/force-push；警告 --force/--skip-tests |
| **Write 校验** | PostToolUse(Write) | `post-write-check.sh` | 自动语法检查：Python/JSON/YAML/Vue/TypeScript |
| **上下文监控** | PostToolUse | `gsd-context-monitor.js` | ≤35% 警告，≤25% 严重告警 |
| **GSD 更新** | SessionStart | `gsd-check-update.js` | 后台检查 GSD 框架更新 |

---

## B7. Agents

> AI 按需调度，无需手动调用

### 项目级

| Agent | 角色 | 用途 | 如何触发 |
|-------|------|------|----------|
| **qa-reviewer** | 只读 Critic | 代码审查 | `/qa-cycle` 或 `/review` 时自动调度 |
| **qa-fixer** | 可写 Fixer | 修复 qa-reviewer 报告的问题 | QA 循环中自动调度 |
| **perf-reviewer** | 只读 | N+1/SELECT */缺分页等性能问题 | 说"性能检查"或"慢查询" |
| **cross-end-coordinator** | 只读 | 前后端接口契约一致性 | 说"联调"或"跨端检查" |

### GSD 系统

| Agent | 用途 |
|-------|------|
| gsd-codebase-mapper | 代码库结构分析 |
| gsd-debugger | 持久化调试会话 |
| gsd-executor | 原子提交执行器 |
| gsd-integration-checker | 跨阶段集成验证 |
| gsd-nyquist-auditor | 验证缺口填充 |
| gsd-phase-researcher | 阶段实现研究 |
| gsd-plan-checker | 计划质量验证 |
| gsd-planner | 阶段计划创建 |
| gsd-project-researcher | 项目域研究 |
| gsd-research-synthesizer | 研究结果综合 |
| gsd-roadmapper | 项目路线图 |
| gsd-verifier | 阶段目标验证 |

### 插件 Agent

| Agent | 来源 | 用途 |
|-------|------|------|
| feature-dev:code-architect | feature-dev | 功能架构蓝图 |
| feature-dev:code-explorer | feature-dev | 代码功能深度分析 |
| feature-dev:code-reviewer | feature-dev | 置信度代码审查 |
| superpowers:code-reviewer | superpowers | 对照计划的代码审查 |
| Explore | 内置 | 快速代码库探索 |
| Plan | 内置 | 实现方案设计 |

---

## B8. Contexts 工作模式

> 路径：`~/.claude/contexts/` | 切换：`/context 模式名`

| 模式 | 用途 | 特点 | 使用方法 |
|------|------|------|----------|
| **dev** | 完整开发模式 | 全部约定生效，含文件修改红线 | `/context dev`（默认） |
| **research** | 研究模式 | 只读，子 Agent 并行，结论附证据 | `/context research` |
| **review** | 审查模式 | 只读，安全/正确性/性能/风格检查 | `/context review` |
| **walkthrough** | 走读模式 | 严格只读，bash 提取代码 | `/context walkthrough` |

---

# Part C：按场景速查索引

### 需求 → 设计 → 开发 → 测试 → 部署 完整流程

```
prototype/
   ↓
/requirement-parse    → ai-doc/需求解析/
   ↓
/requirement-audit    → ai-doc/需求审计/（阻断项必须修复）
   ↓
人工确认
   ↓
/new-feature 或 /module-dev 循环
   ↓
/qa-cycle → /review → verification-before-completion
   ↓
commit → /ship 或 /land-and-deploy
```

### 需求阶段

| 场景 | 命令 |
|------|------|
| 从原型解析需求 | `/requirement-parse` |
| 审计需求质量 | `/requirement-audit` |
| 业务价值验证 | `/office-hours` |

### 开发阶段

| 场景 | 命令 |
|------|------|
| 新功能 | `/new-feature` → `/module-dev` |
| TDD | `/superpowers:test-driven-development` |
| 跨端协调 | `/conductor` |
| 数据库变更 | `/db-migration` |
| 接口变更 | `/api-change` |
| 代码走读 | `/linear-walkthrough` |
| 功能开发引导 | `/feature-dev:feature-dev` |

### 质量保证

| 场景 | 命令 |
|------|------|
| 全面 QA | `/qa-cycle` |
| 前端 QA | `/qa` 或 `/qa-only` |
| PR 审查 | `/review` 或 `/code-review:code-review` |
| 安全审计 | `/security-audit` |
| 性能审查 | 说"性能检查" |
| 完成前验证 | 自动触发 |

### 调试

| 场景 | 命令 |
|------|------|
| 修 Bug | `/bugfix` |
| 根因调查 | `/investigate` |
| GSD 调试 | `/gsd:debug` |

### 设计

| 场景 | 命令 |
|------|------|
| 前端界面 | `/frontend-design:frontend-design` |
| Figma 转代码 | `/figma:figma-use` → `/figma:figma-implement-design` |
| 设计系统 | `/figma:figma-generate-library` |
| 设计评审 | `/design-review` |

### 项目管理

| 场景 | 命令 |
|------|------|
| 新项目 | `/gsd:new-project` |
| 查看进度 | `/gsd:progress` |
| 暂停/恢复 | `/gsd:pause-work` / `/gsd:resume-work` |
| 执行阶段 | `/gsd:execute-phase` |

### 文档处理

| 场景 | 命令 |
|------|------|
| PDF | `/example-skills:pdf` |
| Word | `/example-skills:docx` |
| PPT | `/example-skills:pptx` |
| Excel | `/example-skills:xlsx` |

### 会话管理

| 场景 | 命令 |
|------|------|
| 上下文快满了 | `/compact "保留：任务目标+已完成+接口契约+下一步"` |
| 压缩后恢复 | `cat .claude/compact-anchor.txt` |
| 恢复上次会话 | `/resume` 或 `claude -r` |
| 查看变更 | `/diff` |
| 查看上下文用量 | `/context` |

### IDE 切换

```
Claude Code → /handoff → 切换 Antigravity → 继续工作
Antigravity → 交接卡 → 切换 Claude Code → /gsd:resume-work
```

---

> 文档来源：Claude Code 官方文档 (code.claude.com) + 项目自定义配置
