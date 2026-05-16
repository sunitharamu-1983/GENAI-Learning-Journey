import os
import ollama
from typing import List

# -------------------------------
# Configuration
# -------------------------------
MODEL_NAME = "tinyllama"           # Change to any model you have pulled (e.g., "mistral", "gemma:2b")
CHUNK_SIZE = 2000               # Approximate characters per chunk (adjust based on your model's context window)
CHUNK_OVERLAP = 200             # Overlap between chunks to preserve context
TEMPERATURE = 0.3               # Lower = more deterministic, higher = more creative

# -------------------------------
# Helper: split text into chunks with overlap
# -------------------------------
def split_text_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Splits a long text into overlapping chunks based on character count.
    Tries to break at sentence boundaries (., !, ?) when possible.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # If not at the end, try to find a sentence boundary within the last 10% of the chunk
        if end < text_length:
            boundary = max(text.rfind('. ', start, end),
                           text.rfind('! ', start, end),
                           text.rfind('? ', start, end),
                           text.rfind('\n\n', start, end))
            if boundary != -1 and boundary > start + chunk_size * 0.8:
                end = boundary + 1  # include the punctuation

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start; if we're not at the end, step back by overlap length
        if end < text_length:
            start = end - overlap
        else:
            break

    return chunks

# -------------------------------
# Function: summarize a single chunk
# -------------------------------
def summarize_chunk(chunk: str, chunk_index: int, total_chunks: int) -> str:
    """
    Sends a chunk to Ollama and returns its summary.
    """
    prompt = f"""You are an AI assistant that summarizes meeting transcripts concisely.

Please summarize the following part (chunk {chunk_index+1} of {total_chunks}) of a long meeting transcript. 
Focus on: key decisions, action items, important discussions, questions raised, and conclusions.

Transcript chunk:
\"\"\"
{chunk}
\"\"\"

Write a clear, bullet‑point summary (3-8 points). Keep only the most important information.
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": TEMPERATURE}
        )
        summary = response["message"]["content"].strip()
        return summary
    except Exception as e:
        print(f"Error summarizing chunk {chunk_index+1}: {e}")
        return f"[Failed to summarize chunk {chunk_index+1}]"

# -------------------------------
# Function: combine chunk summaries into final summary
# -------------------------------
def combine_summaries(summaries: List[str]) -> str:
    """
    Takes all chunk summaries and asks Ollama to produce one final, coherent summary.
    """
    combined_text = "\n\n---\n\n".join(summaries)
    prompt = f"""You are given several summaries of different parts of the same long meeting transcript.
Your task is to combine them into a single, coherent, and concise **final summary** of the entire meeting.

Follow these guidelines:
- Remove duplicate information.
- Organize by topic or chronological order.
- Highlight **key decisions**, **action items**, **open questions**, and **main conclusions**.
- Use plain language, bullet points, or short paragraphs as appropriate.

Here are the chunk summaries:
\"\"\"
{combined_text}
\"\"\"

Write the final meeting summary below.
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": TEMPERATURE}
        )
        final_summary = response["message"]["content"].strip()
        return final_summary
    except Exception as e:
        print(f"Error during final combination: {e}")
        return "Failed to produce final summary."

# -------------------------------
# Main processing pipeline
# -------------------------------
def process_transcript(transcript_text: str) -> str:
    """
    Main entry point: splits, summarizes chunks, then combines.
    """
    if not transcript_text.strip():
        return "Error: Empty transcript."

    print("Splitting transcript into chunks...")
    chunks = split_text_into_chunks(transcript_text, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Created {len(chunks)} chunk(s).")

    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk, i, len(chunks))
        chunk_summaries.append(summary)

    print("Combining chunk summaries into final summary...")
    final = combine_summaries(chunk_summaries)
    return final

# -------------------------------
# Example usage (read from a file)
# -------------------------------
if __name__ == "__main__":
    # Change this path to your transcript file
    input_file = "D:\\Sunitha - Learning\\GENAI\\02 Assignment\\02_Ollama\\meeting_transcript.txt"
    print(os.path)

    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        print("Please place your transcript file in the same directory or change the path.")
    else:
        with open(input_file, "r", encoding="utf-8") as f:
            transcript = f.read()

        print(f"Loaded {len(transcript)} characters.")
        final_summary = process_transcript(transcript)

        output_file = "final_meeting_summary.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_summary)

        print(f"\n✅ Final summary saved to {output_file}")
        print("\n--- FINAL SUMMARY ---\n")
        print(final_summary)