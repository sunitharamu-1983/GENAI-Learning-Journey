import os
from typing import Generator
import anthropic
from modules.prompts import get_system_prompt, DIAGRAM_PROMPT
from modules.diagram_generator import extract_mermaid_code

MODEL = "claude-sonnet-4-6"


def _client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key or api_key == "your_anthropic_api_key_here":
        raise ValueError(
            "ANTHROPIC_API_KEY is not set. "
            "Open the .env file and paste your key."
        )
    return anthropic.Anthropic(api_key=api_key)


def ask_educator(question: str, mode: str, human_context: str = "") -> str:
    """Ask Claude to explain an AI concept in the requested mode."""
    system = get_system_prompt(mode, human_context)
    msg = _client().messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    return msg.content[0].text


def generate_diagram_code(question: str) -> str:
    """Ask Claude to produce Mermaid.js code for the given topic."""
    msg = _client().messages.create(
        model=MODEL,
        max_tokens=2048,
        system=DIAGRAM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Create a Mermaid flowchart diagram that explains: {question}",
        }],
    )
    return extract_mermaid_code(msg.content[0].text)


def chat_with_educator(messages: list[dict], mode: str, human_context: str = "") -> str:
    """Continue a multi-turn conversation, keeping full history as context."""
    system = get_system_prompt(mode, human_context)
    msg = _client().messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system,
        messages=messages,
    )
    return msg.content[0].text


def stream_educator(question: str, mode: str, human_context: str = "") -> Generator[str, None, None]:
    """Stream the educator response token-by-token."""
    system = get_system_prompt(mode, human_context)
    with _client().messages.stream(
        model=MODEL,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": question}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def stream_chat(messages: list[dict], mode: str, human_context: str = "") -> Generator[str, None, None]:
    """Stream a chat follow-up response token-by-token."""
    system = get_system_prompt(mode, human_context)
    with _client().messages.stream(
        model=MODEL,
        max_tokens=2048,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
