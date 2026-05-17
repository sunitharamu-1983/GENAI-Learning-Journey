import base64
import requests
from datetime import datetime
from pathlib import Path

EXPORTS_DIR = Path(__file__).parent.parent / "exports"
MERMAID_INK_URL = "https://mermaid.ink/img/{encoded}"


def render_mermaid_to_png(mermaid_code: str, filename: str = None) -> tuple[bytes, str]:
    """Send Mermaid code to mermaid.ink and return (image_bytes, saved_file_path)."""
    encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
    url = MERMAID_INK_URL.format(encoded=encoded)

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    image_bytes = response.content

    EXPORTS_DIR.mkdir(exist_ok=True)
    if not filename:
        filename = f"diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    file_path = EXPORTS_DIR / filename

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return image_bytes, str(file_path)


def extract_mermaid_code(raw: str) -> str:
    """Pull the Mermaid code out of a fenced code block if present."""
    if "```mermaid" in raw:
        start = raw.find("```mermaid") + len("```mermaid")
        end = raw.find("```", start)
        return raw[start:end].strip()
    if "```" in raw:
        start = raw.find("```") + 3
        end = raw.find("```", start)
        return raw[start:end].strip()
    return raw.strip()
