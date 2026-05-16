import os
import re
import json
import requests
import ollama
from typing import List, Dict

# ======================
# CONFIGURATION
# ======================
MODEL_NAME = "qwen2:1.5b"          # Use a fast, capable model
TEMPERATURE = 0.3                   # Lower = more deterministic
CHUNK_SIZE = 2000                   # Characters per chunk (adjust based on context)
CHUNK_OVERLAP = 200                 # Overlap to preserve continuity

# ======================
# HELPER FUNCTIONS
# ======================
def load_transcript_from_url(url: str) -> str:
    """
    Download the meeting transcript from a GitHub raw URL.
    Convert a standard GitHub blob URL to its raw equivalent.
    """
    if "github.com" in url and "/blob/" in url:
        raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    else:
        raw_url = url
    response = requests.get(raw_url)
    response.raise_for_status()
    return response.text

def split_text_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split long text into overlapping chunks, preferring sentence boundaries."""
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        if end < text_length:
            boundary = max(text.rfind('. ', start, end),
                           text.rfind('! ', start, end),
                           text.rfind('? ', start, end),
                           text.rfind('\n\n', start, end))
            if boundary != -1 and boundary > start + chunk_size * 0.8:
                end = boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end < text_length:
            start = end - overlap
        else:
            break
    return chunks

def summarize_chunk(chunk: str, chunk_index: int, total_chunks: int) -> str:
    """Summarize a single chunk using Ollama."""
    prompt = f"""You are an AI assistant summarizing a meeting transcript.
Summarize the following part (chunk {chunk_index+1} of {total_chunks}) concisely.
Focus on: key decisions, action items, important discussions, and conclusions.

Transcript chunk:
\"\"\"
{chunk}
\"\"\"

Provide a short, bullet‑point summary.
"""
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": TEMPERATURE}
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Error summarizing chunk {chunk_index+1}: {e}")
        return f"[Failed to summarize chunk {chunk_index+1}]"

def combine_summaries(summaries: List[str]) -> str:
    """Merge chunk summaries into a single final summary."""
    combined = "\n\n---\n\n".join(summaries)
    prompt = f"""You are given several summaries of different parts of a meeting.
Combine them into one coherent, concise final summary of the entire meeting.
Highlight key decisions, action items, and main conclusions.

Chunk summaries:
\"\"\"
{combined}
\"\"\"

Write the final meeting summary.
"""
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": TEMPERATURE}
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Error during final combination: {e}")
        return "Failed to produce final summary."

def generate_quiz(transcript_text: str, num_questions: int = 5) -> List[Dict]:
    """
    Generate multiple‑choice questions from the transcript.
    Uses a clean JSON output prompt and robust parsing.
    """
    max_chars = 8000
    if len(transcript_text) > max_chars:
        transcript_text = transcript_text[:max_chars] + "\n...[truncated]"

    prompt = f"""You are an AI that creates multiple‑choice quizzes from meeting transcripts.
Based on the transcript below, generate exactly {num_questions} multiple‑choice questions.
Each question must test understanding of key points, decisions, or action items.

Return ONLY valid JSON. Do not include any extra text before or after the JSON.
Use this exact format:

[
  {{
    "question": "What was the main decision about X?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0
  }}
]

The "answer" field is the 0‑based index of the correct option.

Transcript:
\"\"\"
{transcript_text}
\"\"\"
"""
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": TEMPERATURE}
        )
        raw = response["message"]["content"].strip()

        # Extract JSON using regex (handles extra text)
        json_match = re.search(r'\[\s*\{.*\}\s*\]', raw, re.DOTALL)
        if json_match:
            raw = json_match.group(0)
        elif raw.startswith('{'):
            raw = '[' + raw + ']'
        else:
            raise ValueError("No valid JSON array found in response")

        questions = json.loads(raw)
        # Ensure answer is integer
        for q in questions:
            if 'answer' in q and isinstance(q['answer'], str):
                q['answer'] = int(q['answer'])
        return questions[:num_questions]
    except Exception as e:
        print(f"Error generating quiz: {e}")
        print("Raw response from model:")
        print(raw[:500] if 'raw' in locals() else "No response")
        return []

def run_quiz(questions: List[Dict]) -> None:
    """Run the quiz interactively."""
    if not questions:
        print("No questions generated. Cannot run quiz.")
        return

    print("\n" + "="*50)
    print("📝 QUIZ TIME! Answer the following multiple‑choice questions.")
    print("Enter the letter of your answer (A, B, C, or D).")
    print("="*50 + "\n")

    score = 0
    for i, q in enumerate(questions, start=1):
        print(f"Question {i}: {q['question']}")
        for idx, opt in enumerate(q['options']):
            print(f"   {chr(65+idx)}. {opt}")

        while True:
            answer_letter = input("\nYour answer (A/B/C/D): ").strip().upper()
            if answer_letter in ['A','B','C','D']:
                break
            print("Please enter A, B, C, or D.")

        correct_index = q['answer']
        correct_letter = chr(65 + correct_index)
        if answer_letter == correct_letter:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. The correct answer was {correct_letter}. {q['options'][correct_index]}\n")

    print("="*50)
    print(f"🎯 Your final score: {score} / {len(questions)} ({score/len(questions)*100:.1f}%)")
    if score == len(questions):
        print("Perfect! You really understood the meeting.")
    elif score >= len(questions)*0.7:
        print("Good job! You have a solid grasp.")
    else:
        print("You might want to review the transcript again.")
    print("="*50)

# ======================
# MAIN PIPELINE
# ======================
def main():
    # URL of the meeting summary (raw content)
    meeting_url = "https://raw.githubusercontent.com/sunitharamu-1983/GENAI-Learning-Journey/main/01_Foundations/Session%2011/Meeting_Summary.md"
    print("📥 Downloading meeting transcript...")
    transcript = load_transcript_from_url(meeting_url)
    print(f"✅ Loaded {len(transcript)} characters.\n")

    # Step 1: Summarize the transcript (optional, but useful)
    print("🔄 Splitting transcript into chunks...")
    chunks = split_text_into_chunks(transcript, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"   Created {len(chunks)} chunk(s).")

    chunk_summaries = []
    for idx, chunk in enumerate(chunks):
        print(f"   Summarizing chunk {idx+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk, idx, len(chunks))
        chunk_summaries.append(summary)

    print("🔗 Combining chunks into final summary...")
    final_summary = combine_summaries(chunk_summaries)

    # Save the summary
    with open("meeting_summary.txt", "w", encoding="utf-8") as f:
        f.write(final_summary)
    print("✅ Final summary saved to meeting_summary.txt\n")

    # Step 2: Generate quiz
    print("🧠 Generating multiple‑choice questions from the transcript...")
    quiz_questions = generate_quiz(transcript, num_questions=5)

    # Run quiz if questions were generated
    if quiz_questions:
        run_quiz(quiz_questions)
    else:
        print("⚠️ Could not generate quiz. Try a different model (e.g., 'llama3.2:3b' or 'mistral').")

if __name__ == "__main__":
    main()