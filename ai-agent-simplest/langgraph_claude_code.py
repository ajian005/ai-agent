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
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated

# Load environment variables
try:
    load_dotenv()
except Exception:
    pass

# Configuration
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "sk-") 
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://www.dmxapi.cn")
MODEL_NAME = "claude-sonnet-4-20250514" 

# Terminal Colors
YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

# --- Tools ---

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

# --- Graph Definition ---

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def run_agent():
    print(f"Initializing LangGraph StateGraph Agent with model: {MODEL_NAME} at {BASE_URL}...")
    
    # Initialize the model
    llm = ChatAnthropic(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0,
        max_tokens=2000
    )

    tools = [read_file_tool, list_files_tool, edit_file_tool]
    llm_with_tools = llm.bind_tools(tools)

    # Node: Agent (calls model)
    def agent_node(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # Node: Tools (executes tools)
    tool_node = ToolNode(tools)

    # Build the Graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    # Add edges
    workflow.add_edge(START, "agent")
    
    # Conditional edge: If tool calls, go to 'tools', else 'END'
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
    )
    
    # From tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile
    app = workflow.compile()

    # Print and save workflow
    print("\n--- LangGraph Workflow (Mermaid) ---")
    try:
        mermaid_graph = app.get_graph().draw_mermaid()
        
        # Save to file
        workflow_path = Path("langgraph_workflow.mermaid")
        workflow_path.write_text(mermaid_graph, encoding="utf-8")
        print(f"Workflow saved to: {workflow_path.absolute()}")
    except Exception as e:
        print(f"Could not draw/save mermaid graph: {e}")
    print("--------------------------------\n")

    # Interactive Loop
    print("LangGraph Agent Started. Type 'exit' or 'quit' to end.")
    
    chat_history = [] 
    # Add System Message
    chat_history.append(SystemMessage(content="You are a coding assistant. Use the provided tools to read, list, and edit files."))

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
            # Use streaming to get updates, or invoke for final result
            # Here we use invoke for simplicity matching previous scripts
            final_state = app.invoke({"messages": chat_history})
            
            # Update history
            chat_history = final_state["messages"]
            
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
