## RoxyBrowser
RoxyBrowser 是 OpenClaw 的浏览器 MCP 工具，用于安全隔离的网页自动化；OpenClaw 还内置托管浏览器（openclaw 配置文件），二者均可实现页面操控、填表、下载等自动化任务。以下是从安装、配置到实战的完整教程，优先推荐托管浏览器（更安全、无需扩展）。
## 一、前置准备
安装 Node.js ≥22.x（验证：node -v）与 npm/pnpm。
安装并初始化 OpenClaw：
bash
运行
```shell
npm install -g openclaw@latest
openclaw onboard --install-daemon  # 按向导配置模型与网关
```
启动网关（默认端口 18789）：
bash
运行
```shell
openclaw gateway --port 18789
```
## 二、方案 A：OpenClaw 托管浏览器（推荐）
无需额外安装 RoxyBrowser，使用隔离的 Chromium 配置文件，安全可控。
### 1. 安装浏览器依赖
bash
运行
```shell
# 安装 Playwright Chromium（用于托管浏览器）
npx playwright-core install chromium
```
### 2. 启用并设为默认
编辑配置文件 ~/.openclaw/openclaw.json，设置：
```json
{
  "browser": {
    "defaultProfile": "openclaw",  // 默认为托管模式
    "profiles": {
      "openclaw": {
        "driver": "managed"
      }
    }
  }
}
```
重启网关：openclaw gateway restart。

### 3. 核心操作流程（CLI）
表格
|步骤|命令|说明|
|--|--|--|
|启动浏览器|openclaw browser start|启动托管浏览器（橙色主题）|
|打开网页|openclaw browser open https://baidu.com|打开指定 URL|
|获取元素引用|openclaw browser snapshot --interactive --labels|生成带 ref（如 e12）的交互快照，含截图标签|
|点击元素|openclaw browser click e12|用角色 ref 点击（推荐）|
|输入文本|openclaw browser type e23 "搜索关键词" --submit|输入并提交|
|等待加载|openclaw browser wait --load networkidle --url "**/result"|等待网络空闲且 URL 匹配|
|截图 / 导出 PDF|openclaw browser screenshot --full-page
openclaw browser pdf|全页截图或导出当前页为 PDF|
|下载文件|openclaw browser download e45 /tmp/report.pdf|下载元素 e45 指向的文件到 /tmp/report.pdf|
|等待下载完成|openclaw browser waitfordownload /tmp/report.pdf|触发下载并等待完成|

## 三、方案 B：RoxyBrowser MCP（兼容模式）
通过 MCP 连接 RoxyBrowser，适合需特定浏览器环境的场景。
### 1. 安装 RoxyBrowser 与 MCP 管理工具
下载 RoxyBrowser：https://roxybrowser.com/zh，安装并登录。
安装 mcporter（MCP 端口管理）：
bash
运行
```shell
npm install -g mcporter
```
### 2. 获取 RoxyBrowser API 信息
打开 RoxyBrowser → 左下角设置 → API 设置，复制 API Key 与 API Host（默认：http://127.0.0.1:端口）。

### 3. 配置 MCP 连接
bash
运行
```shell
# 添加 RoxyBrowser MCP 配置
mcporter add roxy --url <API Host> --token <API Key>
# 验证连接
mcporter list
```
### 4. 在 OpenClaw 中使用
bash
运行
```shell
# 切换到 RoxyBrowser 配置
openclaw browser --browser-profile roxy open https://example.com
# 后续操作同方案A（snapshot → click/type 等）
```
## 四、实战案例：自动搜索并导出结果
bash
运行
```shell
# 1. 启动托管浏览器并打开百度
openclaw browser start
openclaw browser open https://baidu.com

# 2. 快照获取搜索框 ref（假设为 e18）
openclaw browser snapshot --interactive

# 3. 输入并提交搜索
openclaw browser type e18 "2026 人工智能发展趋势" --submit

# 4. 等待结果页加载
openclaw browser wait --load networkidle --url "**/s?wd=*"

# 5. 全页截图并导出 PDF
openclaw browser screenshot --full-page --output ./trends.png
openclaw browser pdf --output ./trends.pdf

# 6. 关闭浏览器
openclaw browser close
```
## 五、关键技巧与排错
1. 元素定位：优先使用 snapshot --interactive --labels 获取角色 ref（eXX），数字 ref（12）在导航后会失效。
2. 等待策略：避免固定延时，使用 wait --load networkidle、wait --url "**/path" 或 wait --fn "window.ready===true"。
3. 调试工具：
   - 高亮元素：openclaw browser highlight e12
   - 查看错误：openclaw browser errors
   - 录制轨迹：openclaw browser trace start → 操作 → trace stop（生成调试报告）。
4. 常见问题：
   - 提示 “Browser disabled”：检查配置文件是否启用 browser，并重启网关。
   - 操作失败（not visible）：用 snapshot 重新获取 ref，或调整页面大小（resize 1280 720）。
   - 依赖缺失：重新执行 npx playwright-core install chromium。
## 六、安全注意事项
1. 不建议在公共网络或共享设备上使用 RoxyBrowser MCP。
2. 托管浏览器与个人浏览器完全隔离，不会泄露隐私数据。
3. 自动化操作前，确保目标网站允许爬虫 / 自动化（遵守 robots.txt 与用户协议）。
4. 敏感操作（如登录、支付）建议在本地环境执行，避免使用公共网络。
