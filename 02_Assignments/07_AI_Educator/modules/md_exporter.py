from datetime import datetime
from pathlib import Path

SAVE_DIR = Path.home() / "Downloads"


def export_to_md(mode: str, chat_history: list[dict],
                 image_path: str = None, filename: str = None) -> tuple[str, str]:
    """Export the full conversation to a Markdown file and return (file_path, content)."""
    SAVE_DIR.mkdir(exist_ok=True)

    lines = [
        "# AI Educator — Learning Session",
        "",
        f"**Date:** {datetime.now().strftime('%B %d, %Y  %H:%M')}  ",
        f"**Mode:** {mode}  ",
        "",
        "---",
        "",
    ]

    # Iterate through conversation pairs
    i = 0
    exchange_num = 0
    while i < len(chat_history) - 1:
        if chat_history[i]["role"] == "user" and chat_history[i + 1]["role"] == "assistant":
            exchange_num += 1
            question = chat_history[i]["content"]
            answer   = chat_history[i + 1]["content"]

            heading = "## Question" if exchange_num == 1 else f"## Follow-up {exchange_num - 1}"
            lines.append(heading)
            lines.append("")
            lines.append(f"**You:** {question}")
            lines.append("")
            lines.append(f"**Coco:**")
            lines.append("")
            lines.append(answer)
            lines.append("")
            lines.append("---")
            lines.append("")
            i += 2
        else:
            i += 1

    if image_path:
        lines.append("## Flow Diagram")
        lines.append("")
        lines.append(f"*Diagram image saved at: `{image_path}`*")
        lines.append("")

    content = "\n".join(lines)
    if not filename:
        filename = f"ai_educator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    out_path = SAVE_DIR / filename
    out_path.write_text(content, encoding="utf-8")
    return str(out_path), content
