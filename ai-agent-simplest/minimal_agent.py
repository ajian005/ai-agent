#!/usr/bin/env python3
"""
最小 AI Agent 示例：人机对话外层循环 + 工具内层循环 + LLM 调用。
依赖：pip install -r requirements.txt
配置：复制 .env.example 为 .env 并填写 ANTHROPIC_API_KEY（或兼容代理的 ANTHROPIC_AUTH_TOKEN）。
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple

import anthropic
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------------
# 工具：尽量保持极少，演示「模型 → tool: 协议 → 执行 → tool_result」即可
# -----------------------------------------------------------------------------


def get_time_tool() -> Dict[str, Any]:
    """Return current local time as ISO-8601 string."""
    return {"now": datetime.now().isoformat(timespec="seconds")}


def add_tool(a: float, b: float) -> Dict[str, Any]:
    """Return the sum of two numbers."""
    return {"sum": a + b}


TOOL_REGISTRY: Dict[str, Callable[..., Any]] = {
    "get_time": get_time_tool,
    "add": add_tool,
}

SYSTEM_PROMPT = """You are a helpful assistant with tools.
Tools:
- get_time() — no arguments
- add — JSON keys: "a", "b" (numbers)

To call a tool, output exactly one line and nothing else:
tool: NAME({JSON_ARGS})

Examples:
tool: get_time({})
tool: add({"a": 1, "b": 2})

After a line tool_result(...), continue until you can answer the user in plain text without tools.
"""


def extract_tool_invocations(text: str) -> List[Tuple[str, Dict[str, Any]]]:
    out: List[Tuple[str, Dict[str, Any]]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("tool:"):
            continue
        try:
            after = line[len("tool:") :].strip()
            name, rest = after.split("(", 1)
            name = name.strip()
            if not rest.endswith(")"):
                continue
            args = json.loads(rest[:-1].strip())
            out.append((name, args))
        except Exception:
            continue
    return out


def make_client() -> anthropic.Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if not key:
        print("Set ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN in .env", file=sys.stderr)
        sys.exit(1)
    base = os.environ.get("ANTHROPIC_BASE_URL")
    if os.environ.get("ANTHROPIC_API_KEY"):
        kw: Dict[str, Any] = {"api_key": key}
    else:
        kw = {"auth_token": key}
    if base:
        kw["base_url"] = base
    return anthropic.Anthropic(**kw)


def run_llm(client: anthropic.Anthropic, model: str, conversation: List[Dict[str, str]]) -> str:
    system = ""
    messages: List[Dict[str, str]] = []
    for m in conversation:
        if m["role"] == "system":
            system = m["content"]
        else:
            messages.append(m)
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=messages,
    )
    return resp.content[0].text


def dispatch_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if name not in TOOL_REGISTRY:
        return {"error": f"unknown tool: {name}"}
    fn = TOOL_REGISTRY[name]
    if name == "get_time":
        return fn()
    if name == "add":
        try:
            return fn(float(args["a"]), float(args["b"]))
        except KeyError:
            return {"error": 'add requires numeric "a" and "b"'}
    return fn(**args)


def main() -> None:
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    client = make_client()
    conversation: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Minimal agent. Ctrl+D / Ctrl+C to exit.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            continue
        conversation.append({"role": "user", "content": user})
        while True:
            text = run_llm(client, model, conversation)
            invocations = extract_tool_invocations(text)
            if not invocations:
                print(f"Assistant: {text}\n")
                conversation.append({"role": "assistant", "content": text})
                break
            for name, args in invocations:
                result = dispatch_tool(name, args)
                conversation.append(
                    {"role": "user", "content": f"tool_result({json.dumps(result, ensure_ascii=False)})"}
                )


if __name__ == "__main__":
    main()
