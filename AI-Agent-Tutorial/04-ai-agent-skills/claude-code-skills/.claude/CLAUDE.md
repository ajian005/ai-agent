# AI指南

## 项目概述
AI商业内容生成引擎是一个基于FastAPI、Python和阿里云通义千问系列模型构建的内容生成平台，专注于为企业提供高质量、高效率的自动化内容生成服务，支持文案、图像、视频、音频、文档等多模态内容创作。

## 技术栈
### 后端技术栈
- **Python 3.9+** - 主要开发语言
- **FastAPI** - 高性能Web框架，支持自动API文档生成
- **Pydantic v2** - 数据验证与序列化框架
- **AsyncIO** - 异步编程模型，支持高并发
### AI/ML 技术栈
- **阿里云通义千问系列模型** - 包括qwen-turbo、qwen-max、wanx-v1等
- **DashScope SDK** - 阿里云AI服务SDK
- **LangGraph** - AI工作流编排与状态管理
- **LangChain Core** - LLM应用开发框架
### 基础设施技术栈
- **RocketMQ** - 消息队列系统
- **阿里云OSS** - 对象存储服务
- **YAML/Python-dotenv** - 配置与环境变量管理
## 项目架构
采用 **领域驱动设计(DDD) + 微服务架构** 模式，业务逻辑按领域垂直切分。
```
ai_business_content_generation/
├── core/                           # 核心基础设施
│   ├── config/                     # 配置管理
│   ├── infrastructure/             # 基础设施适配器
│   ├── models/                     # 通用数据模型
│   └── utils/                      # 通用工具
│
├── modules/                        # 业务模块
│   ├── content_generation/         # 内容生成模块
│   │   ├── api/                    # API路由
│   │   ├── services/               # 业务服务
│   │   ├── workflows/              # AI工作流
│   │   └── models/                 # 模块模型
│   └── multimodal/                 # 多模态处理模块
│
├── test/                           # 测试目录
├── config/                         # 环境配置
└── main.py                         # 应用入口
```

## 开发规范

### Python 编码规范
- 遵循 PEP 8 规范
- 必须使用类型提示
- 使用Pydantic进行数据验证
- 采用异步编程处理I/O操作
- 命名规范：snake_case（变量/函数）、PascalCase（类名）、UPPER_SNAKE_CASE（常量）

### 架构设计原则
- 单一职责原则
- 依赖注入模式
- 工厂模式管理客户端创建
- 服务层封装业务逻辑

### 错误处理与日志
- 自定义异常体系
- 结构化日志记录（包含request_id、timestamp）
- 标准化HTTP响应格式



## 性能优化

### AI模型调用优化
- 智能模型选择
- 批量处理支持
- 结果缓存机制
- 并发控制

### 系统性能优化
- 数据库连接池优化
- 响应压缩（GZIP）
- 异步处理长耗时任务

## 安全实践

### 认证与授权
- JWT Token认证
- RBAC权限控制
- API密钥安全管理
- 请求限流机制

### 数据安全
- 敏感数据加密
- 输入验证防注入
- 审计日志记录

## 监控与运维

### 系统监控
- Prometheus指标收集
- 分布式链路追踪
- Grafana监控面板
- 智能告警机制

### 日志管理
- JSON格式结构化日志
- 分级日志策略
- 日志轮转管理


## 环境配置与部署
### 本地开发环境
```bash
# 启动开发服务器
python main.py --env local
```
