import asyncio
import os
# 假设 SDK 支持从环境变量或特定配置类读取
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    # --- 方法：在代码中直接设置环境变量 ---
    # os.environ["ANTHROPIC_API_KEY"] = "你的_API_KEY_放在这里"
    # 如果需要指定 API 代理地址，可以取消下面这行的注释
    # os.environ["ANTHROPIC_BASE_URL"] = "https://api.anthropic.com" 
    os.environ["ANTHROPIC_API_KEY"] = "sk-"
    os.environ["ANTHROPIC_BASE_URL"] = "https://www.dmxapi.cn" 

    try:
        async for message in query(
            prompt="Find and fix the bug in auth.py",
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Edit", "Bash"],
                # 注意：部分 SDK 版本允许在此处直接传入 api_key
                # api_key="你的_API_KEY_放在这里" 
            )
        ):
            print(message) 
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())