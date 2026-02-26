## Agent Skills 开放标准

2025 年 Anthropic 发布 MCP 协议时分享过 模型无关的AI集成革命：
MCP协议解读，MCP协议解读(https://mp.weixin.qq.com/s?__biz=MzA4Nzg2NTY2Mw==&mid=2247484968&idx=1&sn=30edee69f46c0cba1015a8c6579df9ee&scene=21#wechat_redirect)：
MCP-Server通信原理（SSE）(https://mp.weixin.qq.com/s?__biz=MzA4Nzg2NTY2Mw==&mid=2247485178&idx=1&sn=0c0ed6e7b5280f26c75f8a909bf480fa&scene=21#wechat_redirect)、
MCP协议解读：传输协议和消息格式(https://mp.weixin.qq.com/s?__biz=MzA4Nzg2NTY2Mw==&mid=2247484978&idx=1&sn=d490ed31b00ba58549f073871a4bf198&scene=21#wechat_redirect)，

如今 2026 年，有了新的话题 Agent Skills。

2025 年 12 月 18 日，Anthropic 将**Agent Skills**发布为开放标准（http://agentskills.io）。https://github.com/agentskills/agentskills
微软在 VS Code 和 GitHub 中集成了这套标准，Cursor、Goose、OpenCode 等主流编码 Agent 纷纷跟进。

Agent Skills 是一种轻量级的开放格式，可通过专业知识和工作流程扩展 AI Agent 的功能。


### 我对 obsidian skills 的理解
从名词上讲，prompt 类似 code snippet，skills 类似 spec coding 依赖的 specification，是完整的方法论。

1. skills 定义了 prompt 的编写标准，agent 加载 prompt 的标准，以渐进式披露（Progressive disclosure）实现了更准更省的调用 tool
2. skills 的能力覆盖 prompt，对用户是友好的，便于分享和传播的。
之前网上到处流传着各种咒语（提示词），awesome prompt，不同模型甚至还不一样。现在 prompt 未来都要升级为 skills 了。
比如 最近流行的 obsidian ceo kepano 开源的 obsidian skills，就是一个纯方法论的 skills，没有相关的工具和参考资源（ references、reference、assets）。

如下面的是 obsidian 里面关于如何创建和修改 白板（Canvas） 的 skills
```json
> Metadata（默认加载）：约100 token

---
name: json-canvas
description: Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian.
---

> Instruction（按需加载）：约2.9k tokens

# JSON Canvas Skill

This skill enables skills-compatible agents to create and edit valid JSON Canvas files (`.canvas`) used in Obsidian and other applications.

## Overview
## File Structure
## Nodes
## Edges
## Colors
## ID Generation
## Layout Guidelines
## Validation Rules
## Complete Examples
## References
……
```

有了这个 skill，就能让模型绘制出 obsidian 能正常解析的 canvas。

原理上，直接扔这个提示词在 user message 里面也是一样的效果，不过那是人工输入的。
而 skill 是启动时就提供所有 metadata 给 llm，让 llm 负责决策激活哪个 skill，再去加载 Instruction，更智能。

下面是 Agent Skills 的标准的具体定义，整理自官方文档，不包含个人观点。


### 目录结构
Skills 的核心是一个包含 SKILL.md 文件的文件夹。该文件包含元数据（至少包括 name 和 description ）以及指示 Agent 如何执行特定任务的指令。
Skills 还可以包含脚本、模板和参考资料。
```
my-skill/
├── SKILL.md    # [必需] 技能入口文件，包含元数据和指令
├── scripts/    # [可选] 可执行脚本
├── references/ # [可选] 参考文档（按需加载）
└── assets/     # [可选] 资产文件（用于输出）
```

### 渐进式披露
skill 应结构化，以便有效利用上下文：
- Metadata （约 100 个 token）：所有技能的 name 和 description 字段在启动时加载。
- Instructions （建议低于 5000 个 token）：技能激活时，完整的 SKILL.md 文件将被加载。
- Resources (按需加载): 文件（例如 scripts/ 、 references/ 或 assets/ 目录中的文件）仅在需要时加载。
主 SKILL.md 文件应控制在 500 行以内。详细的参考资料应移至单独的文件中。

### SKILL.md
SKILL.md 文件必须包含 YAML 前置元数据，后跟 Markdown 内容。
```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---

```
字段说明

|字段|必需|要求|
|--|--|--|
|name	|Yes|最多 64 个字符。仅限小写字母、数字和连字符。不得以连字符开头或结尾。|
|description	|Yes|最多 1024 个字符。非空。描述技能的效果以及何时使用。|
|license	|No|许可证名称或捆绑许可证文件的引用。|
|compatibility	|No|最多 500 个字符。说明环境要求（目标产品、系统软件包、网络访问等）。|
|metadata	|No|任意键值映射，用于添加元数据。|
|allowed-tools|	No |技能可使用的预先批准工具列表，以空格分隔。（实验性功能）


### scripts 目录
包含 agent 可以运行的代码。代码应：

- 要么是自包含的，要么清楚地记录依赖关系
- 包含有用的错误信息
- 优雅地处理极端情况
  支持的语言取决于 agent 的具体实现。常见的语言包括 Python、Bash 和 JavaScript。

### references 目录
包含 agent 在需要时可查阅的其他文档：

- REFERENCE.md：详细技术参考，包括 API 文档、库参考等。
- FORMS.md：表单模板或结构化数据格式，用于与用户交互。
- 特定领域文件（ finance.md 、 legal.md 等）：根据技能的特定领域，包含相关的参考材料。
保持各个 参考文件的 简洁性。agent 按需加载这些文件，因此文件越小，对上下文信息的依赖就越少。

### assets 目录
包含静态资源：

模板（文档模板、配置模板）
图片（图表、示例）
数据文件（ddl、dml）


### 文件引用
在技能中引用其他文件时，请使用相对于技能根目录的相对路径：

See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
文件引用应保持在 SKILL.md 的一级深度。避免使用深度嵌套的引用链。

### 验证
使用 skills-ref 参考库来验证 skill：
```bash
skills-ref validate ./my-skill
```
这会检查您的 SKILL.md 前置元数据是否有效并符合所有命名约定。

### 集成方法
skill 有 2 种集成方法：

1. Filesystem-based agents：在本地计算机环境（bash/unix）中运行。当模型发出类似 cat /path/to/my-skill/SKILL.md 的 shell 命令时，技能会被激活。捆绑的资源通过 shell 命令访问。
2. Tool-based agents：无需专用计算机环境即可运行。它们通过实现各种工具，使模型能够触发技能并访问关联的资源。具体的工具实现方式由开发者决定。

为了支持 skill，agent 需要
1. 在已配置的目录中发现skill
2. 启动时加载 skill 元数据 （name 和 description）
3. 将用户任务与相关 skill相匹配
4. 通过加载 Skill 完整说明激活 skill
5.根据需要执行skill 中的脚本或者访问 skill 中的资源

元数据加载示例
```xml
<available_skills>
<skill>
<name>pdf-processing</name>
<description>Extracts text and tables from PDF files, fills forms, merges documents.</description>
<location>/path/to/skills/pdf-processing/SKILL.md</location>
</skill>
</available_skills>
```

### 安全风险
skill 的脚本执行会带来安全风险。使用时考虑以下因素：

- **Sandboxing**: 在隔离的环境中运行脚本，防止恶意代码对主机系统造成损害。
- **Allowlisting**: 仅执行来自受信任 skill 的 script，避免执行未经验证的代码。
- **Confirmation**: 在执行潜在危险操作前，请征得用户同意。
- **Logging**: 记录所有 script 的执行情况以进行审计，方便排查问题。

### 参考
agent skill 开放标准:   https://agentskills.io/specification
Agent Skills 开放标准:  https://mp.weixin.qq.com/s/RWbA6dlNwNwVXwlaHw79mQ