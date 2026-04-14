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
from langchain_core.tools import tool
# Import the new create_agent from langchain.agents
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
try:
    load_dotenv()
except Exception:
    pass

# Configuration
# Using the same configuration as the original script
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "sk-") 
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://www.dmxapi.cn")
MODEL_NAME = "claude-sonnet-4-20250514" 

# Terminal Colors
YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

def resolve_abs_path(path_str: str) -> Path:
    """
    file.py -> /Users/you/project/file.py
    """
    path = Path(path_str).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path

@tool
def read_file_tool(filename: str) -> Dict[str, Any]:
    """
    Gets the full content of a file provided by the user.
    """
    full_path = resolve_abs_path(filename)
    # print(f"Reading file: {full_path}")
    try:
        with open(str(full_path), "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "file_path": str(full_path),
            "content": content
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def list_files_tool(path: str) -> Dict[str, Any]:
    """
    Lists the files in a directory provided by the user.
    """
    full_path = resolve_abs_path(path)
    all_files = []
    try:
        if not full_path.exists():
             return {"error": f"Path {full_path} does not exist"}
             
        for item in full_path.iterdir():
            all_files.append({
                "filename": item.name,
                "type": "file" if item.is_file() else "dir"
            })
        return {
            "path": str(full_path),
            "files": all_files
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def edit_file_tool(path: str, old_str: str, new_str: str) -> Dict[str, Any]:
    """
    Replaces first occurrence of old_str with new_str in file. If old_str is empty,
    create/overwrite file with new_str.
    """
    full_path = resolve_abs_path(path)
    try:
        if old_str == "":
            full_path.write_text(new_str, encoding="utf-8")
            return {
                "path": str(full_path),
                "action": "created_file"
            }
        
        if not full_path.exists():
             return {
                "path": str(full_path),
                "action": "file not found"
            }

        original = full_path.read_text(encoding="utf-8")
        if original.find(old_str) == -1:
            return {
                "path": str(full_path),
                "action": "old_str not found"
            }
        edited = original.replace(old_str, new_str, 1)
        full_path.write_text(edited, encoding="utf-8")
        return {
            "path": str(full_path),
            "action": "edited"
        }
    except Exception as e:
        return {"error": str(e)}

def run_agent():
    print(f"Initializing LangChain Agent (create_agent) with model: {MODEL_NAME} at {BASE_URL}...")
    
    # Initialize the model
    llm = ChatAnthropic(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0,
        max_tokens=2000
    )

    tools = [read_file_tool, list_files_tool, edit_file_tool]

    # System prompt
    system_prompt = "You are a coding assistant whose goal it is to help us solve coding tasks. You have access to a series of tools you can execute. When asked to edit files, use the edit_file_tool. Always verify file content before editing if unsure."
    
    # Create the agent using the new create_agent API
    # This returns a CompiledStateGraph
    agent = create_agent(
        model=llm, 
        tools=tools, 
        system_prompt=system_prompt
    )

    if False :
        # Print and save workflow
        print("\n--- Agent Workflow (Mermaid) ---")
        try:
            mermaid_graph = agent.get_graph().draw_mermaid()
            print(mermaid_graph)
            graph_image_data = agent.get_graph().draw_mermaid_png()
            with open("multimodal_workflow.png", "wb") as f:
                f.write(graph_image_data)
            print("Workflow graph saved as 'multimodal_workflow.png'")
            
            # Save to file
            workflow_path = Path("agent_workflow.mermaid")
            workflow_path.write_text(mermaid_graph, encoding="utf-8")
            print(f"\nWorkflow saved to: {workflow_path.absolute()}")
        except Exception as e:
            print(f"Could not draw/save mermaid graph: {e}")
        print("--------------------------------\n")

    # Interactive Loop
    print("LangChain Agent Started. Type 'exit' or 'quit' to end.")
    
    # Initialize history
    # Note: create_agent manages state internally when invoked with messages, 
    # but since it's a StateGraph, we need to maintain the conversation state or pass the accumulated messages.
    # The standard way with StateGraph is to pass the full list of messages.
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
            # response_state["messages"] contains the full list of messages
            chat_history = response_state["messages"]
            
            # The last message is the AI's final response
            final_response = chat_history[-1].content
            print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {final_response}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    run_agent()
