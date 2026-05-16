#!/usr/bin/env python3
"""
Local Meeting Summarizer with Dynamic Model Selection & Auto‑Pull
Uses Ollama. Requires: pip install psutil ollama
"""

import os
import sys
import subprocess
import psutil
import ollama
from typing import List, Tuple

# ==========================================
# CONFIGURATION (tweak as needed)
# ==========================================
# Preferred models in order of quality (best last)
MODEL_PREFERENCE = [
    "qwen2:1.5b",      # fastest, good quality
    "llama3.2:3b",     # better quality, slightly slower
    "tinyllama:1.1b"   # fallback – low quality but very light
]

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
# DYNAMIC MODEL SELECTION & AUTO‑PULL
# ==========================================
def get_installed_models() -> List[str]:
    """Return list of model names already pulled in Ollama."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        models = []
        for line in lines[1:]:  # skip header
            if line.strip():
                models.append(line.split()[0])
        return models
    except Exception:
        return []

def get_recommended_model(installed: List[str]) -> Tuple[str, bool]:
    """
    Pick best model based on:
    1. Preference order
    2. Availability (already installed)
    3. RAM constraints
    Returns (model_name, needs_pull)
    """
    ram_gb = psutil.virtual_memory().total / (1024**3)
    
    # Filter models that can run on this RAM (rough estimate)
    # 1.5B ~2GB, 3B ~3.5GB, 1.1B ~1.5GB
    possible = []
    for m in MODEL_PREFERENCE:
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
    
    # Otherwise pick first possible that is not installed
    for m in possible:
        if m not in installed:
            return m, True
    
    # Last resort – try tinyllama even if not installed
    return "tinyllama:1.1b", True

def ensure_model(model: str):
    """Pull the model if not already present."""
    installed = get_installed_models()
    if model in installed:
        print(f"✅ Model '{model}' already available locally.")
        return
    print(f"📥 Model '{model}' not found. Pulling now (this may take a few minutes)...")
    subprocess.run(["ollama", "pull", model], check=True)
    print("✅ Pull complete.")

# ==========================================
# TEXT SPLITTING (dynamic chunk size)
# ==========================================
def get_chunk_size(total_chars: int) -> int:
    """Dynamically set chunk size based on total text length."""
    if total_chars < 50_000:
        return 3000
    elif total_chars < 200_000:
        return 5000
    else:
        return 8000

OVERLAP = 500   # keep context between chunks

def split_text_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        if end < length:
            # try to break at sentence boundary
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
# SUMMARIZATION CORE
# ==========================================
def summarize_chunk(chunk: str, idx: int, total: int, model: str) -> str:
    chunk_num = idx + 1   # compute outside the format string
    prompt = DETAILED_PROMPT.format(chunk_num=chunk_num, total=total, chunk=chunk)
    try:
        resp = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}],
                           options={"temperature": 0.2})
        return resp["message"]["content"].strip()
    except Exception as e:
        print(f"❌ Error on chunk {chunk_num}: {e}")
        return ""

def combine_summaries(summaries: List[str], model: str) -> str:
    combined = "\n\n---\n\n".join(summaries)
    prompt = COMBINE_PROMPT.format(summaries=combined)
    resp = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}],
                       options={"temperature": 0.2})
    return resp["message"]["content"].strip()

# ==========================================
# MAIN PIPELINE
# ==========================================
def main():
    # 1. Input file (you can change this path)
    input_file = "D:\\Sunitha - Learning\\GENAI\\02 Assignment\\02_Ollama\\meeting_transcript.txt"
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        print("Please place your meeting transcript file in the same folder, or update 'input_file'.")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    total_chars = len(text)
    print(f"📄 Loaded {total_chars:,} characters.")

    # 2. Model selection & pull
    installed = get_installed_models()
    print(f"📋 Already installed models: {installed if installed else 'none'}")
    model, needs_pull = get_recommended_model(installed)
    print(f"🎯 Chosen model: {model}")
    if needs_pull:
        ensure_model(model)
    
    # 3. Chunk size
    chunk_size = get_chunk_size(total_chars)
    print(f"✂️  Using chunk size: {chunk_size} characters (overlap: {OVERLAP})")
    
    # 4. Split
    chunks = split_text_into_chunks(text, chunk_size, OVERLAP)
    print(f"🔨 Split into {len(chunks)} chunk(s).")
    
    # 5. Summarize each chunk
    print("📝 Generating detailed summaries...")
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"   - Chunk {i+1}/{len(chunks)}")
        summary = summarize_chunk(chunk, i, len(chunks), model)
        if summary:
            chunk_summaries.append(summary)
    
    if not chunk_summaries:
        print("❌ No summaries generated. Aborting.")
        sys.exit(1)
    
    # 6. Combine into final summary
    print("🔗 Merging chunk summaries into final output...")
    final_summary = combine_summaries(chunk_summaries, model)
    
    # 7. Save
    out_file = "super_detailed_summary.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(final_summary)
    print(f"✅ Done! Summary saved to: {out_file}")

if __name__ == "__main__":
    main()