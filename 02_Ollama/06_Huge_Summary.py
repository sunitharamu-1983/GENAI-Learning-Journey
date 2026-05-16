#!/usr/bin/env python3
"""
Local Meeting Summarizer – Optimised for Large Files (450 KB+)
- Dynamic chunk size based on file length
- Auto model selection & pull (prefers long‑context models for big files)
- Detailed summary preserving all decisions, actions, questions
- Runs locally with Ollama (no API keys, no quotas)
"""

import os
import sys
import subprocess
import psutil
import ollama
from typing import List, Tuple

# ==========================================
# CONFIGURATION
# ==========================================
OVERLAP = 200  # smaller overlap to save tokens

# Model preference order (best last, but will be overridden for large files)
MODEL_PREFERENCE = [
    "qwen2:1.5b",      # fast, good quality, 32k context
    "llama3.2:3b",     # better quality, 128k context (preferred for large files)
    "tinyllama:1.1b"   # fallback – low quality
]

# Prompt for detailed chunk summary
DETAILED_PROMPT = """You are an expert meeting summarizer. Never lose important details.

Below is part {chunk_num} of {total} of a meeting transcript.
Produce a **detailed, bullet‑point summary** that captures:
- All key decisions (exactly what was decided, by whom, any votes)
- Every action item (who does what, by when)
- Unresolved questions or concerns raised
- Main arguments, data points, or external references mentioned
- The overall flow of the discussion

Do not omit anything that could be important later. Use your own words but stay faithful to the transcript.

Transcript chunk:
\"\"\"
{chunk}
\"\"\"

Detailed summary:"""

COMBINE_PROMPT = """You are a synthesis expert.
Below are detailed summaries of different parts of the same meeting.
Your job is to merge them into **one final, ultra‑detailed summary**.
Eliminate repetition but keep every unique decision, action item, and subtle point.
Organise by topic or time. Preserve the original nuance.

Partial summaries:
\"\"\"
{summaries}
\"\"\"

Final comprehensive summary:"""

# ==========================================
# DYNAMIC CHUNK SIZE (optimised for large files)
# ==========================================
def get_chunk_size(total_chars: int) -> int:
    """Return optimal chunk size based on total characters."""
    if total_chars < 50_000:
        return 3000
    elif total_chars < 200_000:
        return 5000
    elif total_chars < 1_000_000:
        # 450 KB → ~16k characters per chunk (approx 4000 tokens)
        return 16000
    else:
        return 20000

def split_text_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into overlapping chunks, respecting sentence boundaries."""
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        if end < length:
            boundary = max(text.rfind('. ', start, end),
                           text.rfind('! ', start, end),
                           text.rfind('? ', start, end),
                           text.rfind('\n\n', start, end))
            if boundary != -1 and boundary > start + chunk_size * 0.7:
                end = boundary + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap if end < length else length
    return chunks

# ==========================================
# MODEL SELECTION & AUTO‑PULL
# ==========================================
def get_installed_models() -> List[str]:
    """Return list of model names pulled in Ollama."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        models = []
        for line in lines[1:]:
            if line.strip():
                models.append(line.split()[0])
        return models
    except Exception:
        return []

def get_recommended_model(installed: List[str], total_chars: int) -> Tuple[str, bool]:
    """
    Choose best model based on:
    - Available RAM
    - File size (prefer long‑context models for large files)
    - Already installed models
    Returns (model_name, needs_pull)
    """
    ram_gb = psutil.virtual_memory().total / (1024**3)

    # For large files, prioritise models with longer context windows
    if total_chars > 200_000:
        priority = ["llama3.2:3b", "qwen2:1.5b", "tinyllama:1.1b"]
    else:
        priority = MODEL_PREFERENCE

    possible = []
    for m in priority:
        if "qwen" in m and ram_gb >= 2:
            possible.append(m)
        elif "llama3.2:3b" in m and ram_gb >= 4:
            possible.append(m)
        elif "tinyllama" in m and ram_gb >= 1.5:
            possible.append(m)

    # Prefer already installed
    for m in possible:
        if m in installed:
            return m, False
    # Otherwise pick first that is not installed
    for m in possible:
        if m not in installed:
            return m, True
    # Ultimate fallback
    return "tinyllama:1.1b", True

def ensure_model(model: str):
    """Pull the model if not already present."""
    installed = get_installed_models()
    if model in installed:
        print(f"✅ Model '{model}' already available.")
        return
    print(f"📥 Model '{model}' not found. Pulling (one‑time download)...")
    subprocess.run(["ollama", "pull", model], check=True)
    print("✅ Pull complete.")

# ==========================================
# SUMMARISATION FUNCTIONS
# ==========================================
def summarize_chunk(chunk: str, idx: int, total: int, model: str) -> str:
    """Summarise a single chunk using the selected model."""
    chunk_num = idx + 1
    prompt = DETAILED_PROMPT.format(chunk_num=chunk_num, total=total, chunk=chunk)
    try:
        resp = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2}
        )
        return resp["message"]["content"].strip()
    except Exception as e:
        print(f"❌ Error on chunk {chunk_num}: {e}")
        return ""

def combine_summaries(summaries: List[str], model: str) -> str:
    """Merge all chunk summaries into one final summary."""
    combined = "\n\n---\n\n".join(summaries)
    prompt = COMBINE_PROMPT.format(summaries=combined)
    resp = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2}
    )
    return resp["message"]["content"].strip()

# ==========================================
# MAIN PIPELINE
# ==========================================
def main():
    # --- Input file (change as needed) ---
    input_file = "D:\\Sunitha - Learning\\GENAI\\02 Assignment\\02_Ollama\\Meeting Transcription_0503.txt"
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        print("Please place your transcript file in the same folder.")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    total_chars = len(text)
    print(f"📄 Loaded {total_chars:,} characters.")

    # --- Model selection ---
    installed = get_installed_models()
    print(f"📋 Already installed: {installed if installed else 'none'}")
    model, need_pull = get_recommended_model(installed, total_chars)
    print(f"🎯 Selected model: {model}")
    if need_pull:
        ensure_model(model)

    # --- Chunking ---
    chunk_size = get_chunk_size(total_chars)
    print(f"✂️  Chunk size: {chunk_size} chars, overlap: {OVERLAP}")
    chunks = split_text_into_chunks(text, chunk_size, OVERLAP)
    print(f"🔨 Created {len(chunks)} chunk(s).")

    # --- Summarise each chunk ---
    print("📝 Generating detailed summaries...")
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"   - Chunk {i+1}/{len(chunks)}")
        summary = summarize_chunk(chunk, i, len(chunks), model)
        if summary:
            chunk_summaries.append(summary)
        else:
            print(f"      ⚠️  Chunk {i+1} produced empty summary.")

    if not chunk_summaries:
        print("❌ No summaries generated. Aborting.")
        sys.exit(1)

    # --- Combine ---
    print("🔗 Merging into final summary...")
    final_summary = combine_summaries(chunk_summaries, model)

    # --- Save output ---
    out_file = "super_detailed_summary.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(final_summary)
    print(f"✅ Done! Summary saved to: {out_file}")

if __name__ == "__main__":
    main()