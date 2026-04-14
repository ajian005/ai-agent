import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import traceback

# Ensure we can import dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    pass

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Import from deepagents
from deepagents.graph import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend

# Load environment variables
try:
    load_dotenv()
except Exception:
    pass

# Configuration
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "sk-fscWHsRNMSQHQv0yFynKJLlG4m6Y6ufbRCVZwLUTOmo7nNCm") 
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://www.dmxapi.cn")
MODEL_NAME = "claude-sonnet-4-20250514" 

# Terminal Colors
YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

def run_agent():
    print(f"Initializing Deep Agent with model: {MODEL_NAME} at {BASE_URL}...")
    
    # Initialize the model
    llm = ChatAnthropic(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0,
        max_tokens=2000
    )

    # Initialize Backend
    # Use FilesystemBackend to interact with local files
    # We use root_dir="." to allow access from current directory
    backend = FilesystemBackend(root_dir=".")

    # Create the agent
    # deepagents automatically adds tools for filesystem, todos, subagents
    # We pass the backend to allow filesystem operations
    agent = create_deep_agent(
        model=llm, 
        backend=backend,
        system_prompt="You are a coding assistant. Use the provided filesystem tools to read, list, and edit files. When editing files, ensure you read them first to get the correct content."
    )

    # Print and save workflow
    print("\n--- Deep Agent Workflow (Mermaid) ---")
    try:
        mermaid_graph = agent.get_graph().draw_mermaid()
        
        # Save to file
        workflow_path = Path("deep_agent_workflow.mermaid")
        workflow_path.write_text(mermaid_graph, encoding="utf-8")
        print(f"Workflow saved to: {workflow_path.absolute()}")
    except Exception as e:
        print(f"Could not draw/save mermaid graph: {e}")
    print("--------------------------------\n")

    # Interactive Loop
    print("Deep Agent Started. Type 'exit' or 'quit' to end.")
    
    # Initialize history
    chat_history = [] 

    while True:
        try:
            user_input = input(f"{YOU_COLOR}You:{RESET_COLOR}:")
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Append user message to history
            chat_history.append(HumanMessage(content=user_input))
            
            # Run the agent
            # invoke returns the final state, which includes the updated 'messages' list
            response_state = agent.invoke({"messages": chat_history})
            
            # Update history with the new messages from the state
            if "messages" in response_state:
                chat_history = response_state["messages"]
                # The last message is the AI's final response
                final_response = chat_history[-1].content
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {final_response}")
            else:
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: (No message in output state)")
                # print(response_state.keys())

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    run_agent()
