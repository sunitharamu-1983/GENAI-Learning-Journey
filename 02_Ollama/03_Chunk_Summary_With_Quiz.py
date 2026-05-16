import os
import ollama
import json
from typing import List, Dict

# -------------------------------
# Configuration (same as earlier)
# -------------------------------
MODEL_NAME = "llama3.1"          # or "mistral", "gemma:2b"
TEMPERATURE = 0.3

# -------------------------------
# 1. Generate multiple-choice questions from transcript
# -------------------------------
def generate_quiz(transcript_text: str, num_questions: int = 5) -> List[Dict]:
    """
    Sends the transcript to Ollama and asks for a JSON list of MCQs.
    Each question dict has: question, options (list of 4), answer (0-indexed).
    """
    prompt = f"""You are an AI that creates multiple‑choice quizzes from meeting transcripts.
Based on the transcript below, generate exactly {num_questions} multiple‑choice questions.
Each question must test understanding of key points, decisions, or action items.

Return ONLY valid JSON in the following format (no extra text):

[
  {{
    "question": "What was the main decision about X?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0
  }},
  ...
]

The "answer" field is the index (0‑based) of the correct option.
Transcript:
\"\"\"
{transcript_text [:12000]}   # limit to avoid context overflow
\"\"\"
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": TEMPERATURE, "format": "json"}
        )
        raw = response["message"]["content"].strip()
        # Sometimes the model wraps JSON in ```json ... ``` – clean it
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.endswith("```"):
            raw = raw[:-3]
        questions = json.loads(raw)
        return questions[:num_questions]   # ensure we have exactly the requested number
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return []

# -------------------------------
# 2. Run the quiz interactively and score
# -------------------------------
def run_quiz(questions: List[Dict]) -> None:
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

        # Get user input with validation
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

# -------------------------------
# 3. Main (add quiz option to the earlier pipeline)
# -------------------------------
if __name__ == "__main__":
    # Same file loading as before
    input_file = "D:\\Sunitha - Learning\\GENAI\\02 Assignment\\02_Ollama\\meeting_transcript.txt"
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
    else:
        with open(input_file, "r", encoding="utf-8") as f:
            transcript = f.read()

        # Optional: first generate and save summary (if you still want that)
        # final_summary = process_transcript(transcript)   # from previous code
        # print("\n--- FINAL SUMMARY ---\n", final_summary)

        # Now generate the quiz
        print("\n🧠 Generating multiple‑choice questions from the transcript...")
        quiz_questions = generate_quiz(transcript, num_questions=5)

        if quiz_questions:
            run_quiz(quiz_questions)
        else:
            print("Could not generate quiz. Check your Ollama connection and model.")