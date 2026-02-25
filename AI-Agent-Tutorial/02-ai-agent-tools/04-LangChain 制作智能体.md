## LangChain 制作智能体
LangChain 是一个用于构建 LLM 应用的框架，可以把模型调用升级为可组合、可控制、可扩展的应用系统。
LangChain 解决的不是怎么调模型，而是：
- 多步骤推理如何组织
- 外部数据如何接入
- 工具如何被模型安全调用
- 上下文如何被长期管理
开源地址：https://github.com/langchain-ai/langchain。
```
想象一下，你正在建造一个智能机器人助手，这个助手需要能够理解你的问题、从各种资料中查找信息、进行逻辑推理，最后用自然语言回答你。单独使用像 GPT 这样的语言模型，就像只给机器人装了一个聪明的大脑，但它还缺少手和眼睛——它不知道如何获取外部数据、如何执行具体任务。
```


LangChain 就是这样一个框架，它充当了连接器和协调者的角色。

LangChain 将强大的语言模型（如 GPT-4、DeepSeek）与外部数据源、计算工具以及记忆系统巧妙地连接起来，构建出功能强大、可实际应用的 AI 应用程序。

简单来说，LangChain 的核心价值在于：让语言模型变得有用，解决了大语言模型（LLM）的几个关键限制：
1. 知识实时性：LLM 的训练数据有截止日期，无法获取最新信息。
2. 领域专精性：通用 LLM 缺乏特定行业或公司的私有知识。
3. 可操作性：LLM 本身无法执行如计算、查询数据库、调用 API 等动作。
4. 对话连贯性：在多轮对话中，LLM 需要记住之前的聊天历史。

LangChain 通过一系列标准化的链（Chains）和组件（Components）来组织这些功能，让开发者能够像搭积木一样，快速构建复杂的 AI 应用。

LangChain 模块总览：
- LLMs / ChatModels：模型接口
- Prompt Templates：Prompt 结构化
- Chains：流程编排
- Memory：上下文管理
- Retrievers / VectorStores：知识检索
- Agents & Tools：自动决策与执行


### 环境准备
使用国内镜像安装：
```
pip install langchain langchain-openai langchain-community python-dotenv -i https://mirrors.aliyun.com/pypi/simple/
```
如果你要 OpenAI 的可以，可以配置环境变量：
```
export OPENAI_API_KEY=你的key
```
然后使用以下代码测试：

实例
```python
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


resp = llm.invoke("用一句话解释什么是 LangChain")
print(resp.content)
```

国内我们可以采用 DeepSeek 大模型来测试，如果还没有需要先去 https://platform.deepseek.com/api_keys 创建一个 API key。

DeepSeek 的 API 文档参考：https://api-docs.deepseek.com/zh-cn/。

LLM 对第三方模型（包括 DeepSeek）底层必须通过 LiteLLM，使用前我们需要先安装：
```
pip install -U litellm
```
实例
```python
import os
from langchain_openai import ChatOpenAI

# 建议将 API Key 放在环境变量中，或者直接在此处赋值（生产环境请勿硬编码）
# os.environ["DEEPSEEK_API_KEY"] = "sk-你的DeepSeek密钥"

# 初始化模型
llm = ChatOpenAI(
    model="deepseek-chat",             # DeepSeek V3 模型名称
    openai_api_key="sk-你的Key",        # 填入你的 DeepSeek API Key
    openai_api_base="https://api.deepseek.com", # DeepSeek 的 API 地址
    temperature=0.7,
    max_tokens=1024
)

# 测试一下
response = llm.invoke("你好，DeepSeek！请做一个简短的自我介绍。")
print(response.content)
```
执行以上代码，就会输出内容：

你好！很高兴认识你！

我是DeepSeek，由深度求索公司创造的AI助手。我的特点包括：
。。。


###构建 LCEL 链 (LangChain Expression Language)
单纯调用模型不够强大，我们需要构建一个标准的处理流程：
```
Prompt -> LLM -> OutputParser
```
完整代码如下：

实例
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 1. 定义模型 (Model)
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key="你的_DEEPSEEK_API_KEY",
    openai_api_base="https://api.deepseek.com"
)

# 2. 定义提示词模板 (Prompt)
# system: 设定 AI 的角色
# user: 用户的具体输入
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深的技术专家，擅长用通俗易懂的'大白话'解释复杂的科技概念。你的解释应该包含一个生动的比喻。"),
    ("user", "{concept}")
])

# 3. 定义输出解析器 (Output Parser)
# 将模型的 Message 对象直接转为纯字符串
parser = StrOutputParser()

# 4. 构建链 (Chain) - 使用管道符 | 连接
# 流程：输入字典 -> 填充 Prompt -> 发给 LLM -> 解析输出
chain = prompt | llm | parser

# 5. 调用链
concept_to_explain = "量子纠缠"
print(f"正在解释概念：{concept_to_explain}...\n")

result = chain.invoke({"concept": concept_to_explain})

print("--- DeepSeek 回答 ---")
print(result)
```

### 流式输出 (Streaming)
在实际应用（如聊天机器人）中，我们需要像 ChatGPT 那样一个字一个字地吐出文字，而不是等生成完了才一次性显示。

LangChain 对此支持非常简单，使用 .stream() 替代 .invoke()：

实例
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 1. 定义模型 (Model)
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key="你的_DEEPSEEK_API_KEY",
    openai_api_base="https://api.deepseek.com"
)

# 2. 定义提示词模板 (Prompt)
# system: 设定 AI 的角色
# user: 用户的具体输入
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深的技术专家，擅长用通俗易懂的'大白话'解释复杂的科技概念。你的解释应该包含一个生动的比喻。"),
    ("user", "{concept}")
])

# 3. 定义输出解析器 (Output Parser)
# 将模型的 Message 对象直接转为纯字符串
parser = StrOutputParser()

# 4. 构建链 (Chain) - 使用管道符 | 连接
# 流程：输入字典 -> 填充 Prompt -> 发给 LLM -> 解析输出
chain = prompt | llm | parser

# 5. 调用链
concept_to_explain = "量子纠缠"
print(f"正在解释概念：{concept_to_explain} (流式输出)...\n")

# 这里的 chunk 是每次生成的片段
for chunk in chain.stream({"concept": "递归神经网络"}):
    print(chunk, end="", flush=True)
```

### 代码结构
#### Prompt
- ChatPromptTemplate 明确区分 system / user
- Prompt 是结构化输入函数，不是字符串
#### LLM
- ChatOpenAI 只是统一接口
- LangChain 不增强模型能力，只增强可控性
#### OutputParser
- 模型输出永远是 Message
- StrOutputParser 是显式类型转换
- 没有 Parser，工程不可控



### 核心组件详解
#### 1. 模型 (Models)
LangChain 提供了统一的抽象接口，现在主要推荐使用 Chat Models，因为目前的模型（如 DeepSeek, GPT-4）大多针对对话进行了优化。
- Chat Models: 输入和输出是结构化的消息。
- SystemMessage: 设定 AI 角色。
- HumanMessage: 用户发送的消息。
- AIMessage: AI 返回的消息。
#### 2. 提示词 (Prompts)
新版本中，推荐使用 ChatPromptTemplate 来构建对话式提示词，它更符合当前主流 LLM 的调用习惯。
```python
from langchain_core.prompts import ChatPromptTemplate

# 使用 from_messages 构建结构化模板
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一位专业的{role}。"),
    ("user", "{content}")
])

# 动态填充变量
prompt = prompt_template.invoke({"role": "美食评论家", "content": "评价一下这碗炸酱面"})
# 输出：包含 SystemMessage 和 HumanMessage 的列表
```

#### 3. 链 (Chains) & LCEL
重要更新： LLMChain 已被弃用。现在使用 LCEL (管道符 |) 语法。这种方式更灵活、支持异步和流式输出。
```python
# 现代写法：Prompt | Model | OutputParser
from langchain_core.output_parsers import StrOutputParser

# 这里的 llm 是 ChatOpenAI(model="deepseek-chat") 的实例
chain = prompt_template | llm | StrOutputParser()

# 调用链
result = chain.invoke({"role": "导游", "content": "介绍一下故宫"})
print(result) # 直接输出字符串
```

#### 4. 索引与检索 (Indexes & Retrieval)
这是 RAG (检索增强生成) 的核心。新版本强调了将文档转化为"检索器"的过程。

- 流程: DocumentLoaders (加载) -> TextSplitter (切片) -> Embeddings (向量化) -> VectorStore (存储)。
- Retriever: 不再仅仅是数据库搜索，它是一个可以集成在链中的组件。
```python
# 将向量库转为检索器
retriever = vectorstore.as_retriever()
# 在新版链中引用
# chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm
```

#### 5. 记忆 (Memory)
**重要更新：** 传统的 ConversationBufferMemory 在复杂的 LCEL 链中较难集成。最新推荐使用 ChatMessageHistory 配合 RunnableWithMessageHistory。

- 核心逻辑: 记忆不再是链的一个属性，而是一个独立的消息存储库，通过 session_id 区分不同用户。
- 持久化: 支持存入 Redis、PostgreSQL 或内存。

#### 6. 代理 (Agents)
代理是 LangChain 的高级应用。新版本推荐使用 LangGraph (LangChain 官方推出的新框架) 来构建更复杂的代理，但基础代理仍可使用 create_tool_calling_agent。

- 工具 (Tools): 使用 @tool 装饰器将任何 Python 函数转为模型可调用的工具。
- 代理执行器: LLM 观察任务 -> 决定调用工具 -> 观察工具结果 -> 给出最终答复。
```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
# 定义工具并创建代理
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

### 快速开始：构建你的第一个 LangChain 应用
让我们通过一个简单的例子，感受一下 LangChain 的便捷性。

实际的开发中，我们可以把 API 的相关信息保存在项目根目录的 .env 文件中，方便使用。
```
# .env 文件内容
DEEPSEEK_API_KEY = sk-xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```
#### 示例 1：基础问答链
实例
```python
import os
from dotenv import load_dotenv
# 正确的导入路径
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

llm = ChatOpenAI(
    model=os.getenv('DEEPSEEK_MODEL'),
    openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
    openai_api_base=os.getenv('DEEPSEEK_BASE_URL'),
)

# 创建提示词模板
template = """
你是一位友好的助手。
请回答以下问题：

问题：{question}
回答：
"""
prompt = PromptTemplate.from_template(template)

# 使用 LCEL 语法创建链 (推荐方式)
# 结构：Prompt -> LLM -> 解析为字符串
chain = prompt | llm | StrOutputParser()

# 运行链
question = "LangChain 是什么？它有什么主要用途？"

response = chain.invoke({"question": question})

print("问题：", question)
print("-" * 20)
print("回答：", response)
```

#### 示例 2：带记忆的对话链
让我们创建一个能记住对话历史的简单聊天机器人。

实例
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. 加载配置
load_dotenv()

# 2. 初始化 DeepSeek 模型
llm = ChatOpenAI(
    model=os.getenv('DEEPSEEK_MODEL', 'deepseek-chat'),
    openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
    openai_api_base=os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com'),
)

# 3. 定义提示词模板
# MessagesPlaceholder 会在运行时被对话历史填充
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个乐于助人的 AI 助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# 4. 构建链
chain = prompt | llm

# 5. 管理内存：创建一个字典来存储不同用户的历史记录
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 6. 使用 RunnableWithMessageHistory 包装我们的链
# 这样 LangChain 会自动处理历史记录的读取和更新
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 7. 进入对话循环
print("--- 已进入 DeepSeek 聊天模式 (输入 'exit' 退出) ---")
session_config = {"configurable": {"session_id": "user_001"}} # 区分不同会话的 ID

while True:
    user_input = input("你: ")
    if user_input.lower() in ["exit", "quit", "退出"]:
        break
       
    # 调用带记忆的链
    response = with_message_history.invoke(
        {"question": user_input},
        config=session_config
    )
   
    print(f"AI: {response.content}\n")

```


运行上述代码，你会看到：

--- 已进入 DeepSeek 聊天模式 (输入 'exit' 退出) ---
你: 你好
AI: 你好！很高兴见到你！ 有什么我可以帮助你的吗？无论是回答问题、聊天，还是协助解决问题，我都很乐意为你提供帮助！

你: 我叫小明
AI: 你好，小明！很高兴认识你！ 
如果你有任何问题、想法，或者需要帮助的地方，随时告诉我哦～

你: 我叫什么记得吗？
AI: 当然记得！你刚刚告诉我你叫**小明**～  
我会认真记住我们的对话内容，在之后的交流中尽量保持上下文连贯。不过如果对话过长或间隔太久，我可能需要你提醒一下哦～  
有什么想聊的或需要帮助的吗？ 