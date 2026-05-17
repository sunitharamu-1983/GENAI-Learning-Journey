# Building a Personal AI Educator with Claude, Streamlit, and pywebview

## From API calls to a native Windows desktop app — architecture, challenges, and the decisions that mattered

---

The problem with learning AI in 2025 is not a lack of content. It is a lack of *personalisation*. A nurse trying to understand neural networks does not need the same explanation as a software engineer. A visual learner does not need a wall of text. A blogger does not need a textbook entry.

**Coco** is a personal AI Educator built to solve exactly that — a desktop app that explains any AI concept in the style that actually works for the person asking. This post covers how it was built, the architecture decisions behind it, and the non-obvious engineering challenges that came up along the way.

---

## What It Does

Four explanation modes, each backed by a purpose-built system prompt:

| Mode | Output |
|---|---|
| **Technical** | Full-depth explanation with precise terminology, architecture details, and structured headings |
| **Simple** | Plain English with everyday analogies — optionally personalised to the reader's profession |
| **Flow Diagram** | A written explanation alongside a Mermaid.js flowchart rendered as a PNG |
| **Blog** | A complete, publish-ready blog post with title, sections, takeaways, and conclusion |

Beyond the modes:

- **Streaming responses** — tokens render live via the Anthropic streaming API
- **Multi-turn contextual chat** — follow-up questions with the full conversation history sent on each turn
- **PDF and Markdown export** — the complete session (initial answer + all follow-ups) exported to the system Downloads folder, named from the question itself
- **Learning dashboard** — GitHub-style activity heatmap, streak tracking, and missed-day visibility
- **Native Windows desktop app** — the Streamlit UI wrapped in a pywebview window via WebView2

---

## Architecture

```
07_AI_Educator/
├── app.py                   ← Streamlit application (UI + orchestration)
├── launcher.py              ← pywebview desktop launcher
├── modules/
│   ├── claude_client.py     ← Anthropic API calls (streaming + non-streaming)
│   ├── prompts.py           ← System prompts for all modes
│   ├── diagram_generator.py ← Mermaid code → PNG via mermaid.ink
│   ├── pdf_exporter.py      ← Formatted PDF export (fpdf2)
│   ├── md_exporter.py       ← Markdown export
│   └── login_tracker.py     ← Login recording + streak calculation
├── data/
│   └── login_tracker.json   ← Auto-created, gitignored
└── exports/
    └── diagram_*.png
```

Clean module separation — each file has a single responsibility. `app.py` orchestrates; modules do the work.

---

## The Engineering Details

### 1. Streaming

The Anthropic Python SDK exposes a clean generator-based streaming interface:

```python
def stream_educator(question, mode, human_context=""):
    system = get_system_prompt(mode, human_context)
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": question}],
    ) as stream:
        for text in stream.text_stream:
            yield text
```

Streamlit's `st.write_stream()` consumes the generator and renders tokens incrementally. Crucially, it also returns the full accumulated string — which gets stored in `st.session_state` for formatted re-rendering on subsequent reruns:

```python
explanation = st.write_stream(stream_educator(question, mode, human_context))
st.session_state.response_text = explanation
```

Two functions. The app feels live.

---

### 2. Prompt Architecture — The Merged Simple Mode

The original design had three separate modes: Technical, Layman, and Human Context. Layman gave plain-English explanations with everyday analogies. Human Context let the user describe their background and receive field-specific examples.

The observation: these are the same mode. Layman is Human Context where the context is "anyone". Merging them into a single **Simple** mode with an optional background field simplifies both the UI and the prompt logic:

```python
def get_system_prompt(mode, human_context=""):
    if mode == "Simple":
        if human_context.strip():
            return HUMAN_CONTEXT_PROMPT_TEMPLATE.format(
                human_context=human_context.strip()
            )
        return LAYMAN_PROMPT
    return {
        "Technical":    TECHNICAL_PROMPT,
        "Blog":         BLOG_PROMPT,
        "Flow Diagram": TECHNICAL_PROMPT,
    }.get(mode, TECHNICAL_PROMPT)
```

Empty background → plain English for any reader. Filled background → analogies drawn entirely from the user's domain. One mode, two behaviours, zero UI friction.

---

### 3. The Diagram Pipeline

```
Question
   ↓
Claude generates Mermaid.js code
   ↓
base64.urlsafe_b64encode(code)
   ↓
GET https://mermaid.ink/img/{encoded}
   ↓
PNG bytes
   ↓
st.image()  +  saved to exports/
```

[mermaid.ink](https://mermaid.ink) is a free public rendering API — no key required. Encode Mermaid code as URL-safe base64, append to the endpoint, receive a PNG.

The prompt engineering here was critical. Claude generates valid Mermaid syntax reliably, but without constraints the diagrams become unrenderable — too many nodes, labels that are too long, or unsupported syntax variants. The system prompt enforces:

- `graph TD` for processes, `graph LR` for pipelines
- Node labels ≤ 5 words
- Maximum 15 nodes total
- **Return ONLY the code block** — no preamble, no explanation

That last constraint is the most important. Without it, Claude wraps the code in explanatory prose that breaks the parser.

---

### 4. Streamlit State Management — The Hard Part

Streamlit's execution model is: every interaction triggers a full script re-execution from top to bottom. This is simple and predictable for basic apps. For an app combining streaming, progress bars, download buttons, and multi-turn chat, it creates a set of non-obvious challenges.

**The streaming capture problem**

`st.write_stream()` consumes a generator — generators can only be iterated once. After streaming completes, the response needs to be preserved in session state before the next rerun clears it. The return value of `st.write_stream()` is the full accumulated text, captured immediately after the stream closes.

**The export re-trigger problem**

`st.download_button` uses a special response mechanism that can interfere with subsequent button click detection in the same widget tree. On the second click of "Generate PDF", nothing would happen.

The fix: separate the button click from the export execution using a session state flag and an explicit rerun:

```python
# Button click only sets a flag
if st.button("Generate PDF"):
    st.session_state._gen_pdf = True
    st.rerun()

# Export runs on the following rerun, cleanly isolated
if st.session_state._gen_pdf:
    st.session_state._gen_pdf = False
    # progress bar + export_to_pdf() + file read
```

The trigger fires in one rerun. The export executes in the next. No widget state conflict.

**The progress bar visibility problem**

Markdown export is pure string manipulation — near-instantaneous. `st.progress()` steps through 0% → 30% → 75% → 100% too fast for Streamlit to flush intermediate renders to the frontend. `time.sleep(0.25)` between steps gives the WebSocket time to push each state update before the next one overwrites it.

---

### 5. Native Desktop Packaging with pywebview

`streamlit run app.py` opens a browser tab. For a desktop app feel — its own window, its own title bar, no browser chrome — pywebview wraps the Streamlit server in a native WebView2 window.

`launcher.py` handles the full lifecycle:

```python
# 1. Start Streamlit as a hidden subprocess
proc = subprocess.Popen(
    ["streamlit", "run", "app.py"],
    creationflags=subprocess.CREATE_NO_WINDOW,
)

# 2. Poll until the server is ready
while True:
    try:
        requests.get("http://localhost:8501", timeout=1)
        break
    except:
        time.sleep(0.3)

# 3. Open as a native window
window = webview.create_window("AI Educator", "http://localhost:8501",
                                width=1280, height=860, resizable=True)
webview.start()
```

If WebView2 is not installed, the launcher falls back to `webbrowser.open()`. The app stays usable either way.

---

### 6. The Learning Dashboard

Each app launch appends a timestamp to `data/login_tracker.json`. The dashboard reads this file and computes:

- **Unique days studied** — multiple sessions on the same day count as one
- **Current streak** — consecutive calendar days with at least one session
- **Longest streak** — the best unbroken run ever recorded
- **Missed days** — calendar days in the last 30 with no session
- **Activity heatmap** — a Plotly heatmap laid out as a 7×N calendar grid (last 13 weeks)

The streak calculation handles the edge case where the user opens the app for the first time today but has not yet recorded yesterday — the streak does not break until the end of the day.

The heatmap is a `go.Heatmap` trace with a two-colour scale (`#ebedf0` for no session, `#40c463` for logged in), `xgap=3` and `ygap=3` for the grid appearance, and custom Y-axis tick labels for day names.

---

## What the Prompt Engineering Actually Looks Like

Each mode has a purpose-built system prompt. A few examples of constraints that made a real difference:

**Technical mode** — "Structure your response with clear headings using markdown. Include relevant mathematical concepts where appropriate." Without the heading instruction, Claude produces dense paragraphs. With it, responses are navigable.

**Blog mode** — "A catchy, SEO-friendly title (H1). A compelling introduction hook (2–3 sentences). 3–5 sections with H2 headings. 700–900 words." Word count constraints are surprisingly effective — they prevent both truncation and padding.

**Diagram mode** — "Return ONLY the Mermaid code block. No explanation text, no preamble, just the code." The word "CRITICAL" before this instruction was added after testing — Claude treats it as a stronger signal than plain instruction text.

**Simple mode with context** — "Connect AI concepts directly to their professional world and experiences. Show how AI concepts map to things they already know well." The framing "map to things they already know well" produces much better analogies than "use examples from their field".

---

## Lessons Worth Keeping

**The Anthropic SDK is well-designed.** The streaming interface, error types, and documentation are honest about model capabilities. Working API calls in minutes, not hours.

**Prompt engineering is product design.** The delta between a mediocre system prompt and an excellent one is often five well-chosen sentences. Small constraints — word limits, format instructions, output-only directives — have outsized impact on response quality.

**Streamlit's rerun model is the mental model.** Once it clicks, everything makes sense. Fighting it produces fragile code. Working with it — session state flags, explicit reruns, widget keys tied to state counters — produces reliable code.

**Accountability features change behaviour.** The learning dashboard was the last thing added and the first thing opened on each session. A streak counter backed by a JSON file and rendered as a heatmap is a remarkably effective forcing function.

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Anthropic Claude (`claude-sonnet-4-6`) |
| UI | Streamlit |
| Desktop Wrapper | pywebview + WebView2 |
| Diagram Rendering | mermaid.ink |
| PDF Generation | fpdf2 |
| Charts | Plotly |
| Data | pandas |
| Config | python-dotenv |

---

*The source code is structured as a reference implementation — modular, documented, and straightforward to extend. Each module is independently testable and the prompt definitions are cleanly separated from the API client logic.*
