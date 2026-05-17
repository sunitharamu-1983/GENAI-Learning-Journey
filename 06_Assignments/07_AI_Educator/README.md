# 🎓 AI Educator — Coco

> *Your personal AI learning companion — powered by Claude, built for curious minds.*

A Windows desktop app (and browser app) that explains any AI concept exactly the way *you* need it —
technical deep-dives, plain-English summaries, visual flowcharts, field-tailored explanations,
and publish-ready blog posts. Every session is tracked so your learning journey is always visible.

---

## ✨ What Can It Do?

| Mode | What you get |
|---|---|
| **Technical** | Full-depth explanation with precise terminology, architecture details, and structured headings |
| **Simple** | Plain English with everyday analogies — optionally tailored to *your* profession or background |
| **Flow Diagram** | A written explanation *and* an auto-generated visual flowchart rendered as a PNG |
| **Blog** | A complete, publish-ready blog post — title, sections, key takeaways, and conclusion |
| **Follow-up Chat** | After any answer, keep the conversation going — Coco remembers the full context |
| **Streaming** | Answers appear token by token, just like ChatGPT — no waiting for a full response |
| **PDF Export** | The full Q&A (including all follow-ups) exported as a formatted PDF to your Downloads folder |
| **Markdown Export** | Same content as a clean `.md` file — great for notes, GitHub, or Obsidian |
| **PNG Download** | Flow diagrams saved as PNG images |
| **Learning Dashboard** | GitHub-style activity heatmap, streaks, missed days, and session history |

---

## 🖥️ App Screens

### AI Educator — Ask Mode
```
┌─────────────────────────────────────────────────────────────────────┐
│  Welcome back · Sunitha 👋   "Ready to make AI less mysterious?"    │  ← Personalised banner
├──────────────────────────────────────────────────────────────────────┤
│  Explanation Mode:  ● Technical  ○ Simple  ○ Flow Diagram  ○ Blog   │
│                                                                      │
│  Your question about AI:                                             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ What is Retrieval-Augmented Generation (RAG)?                │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  [ Ask Coco 🎓 ]  [ New Question ]                                  │
│                                                                      │
│  ── Answer ──────────────────────────────────────────────────────── │
│  │ RAG is an architecture that combines a retrieval system with  │   │
│  │ a generative language model...  ← streams in live             │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ── 💬 Continue the Conversation ──────────────────────────────── │
│  Your follow-up: [________________________]  [ Send ➤ ]            │
└──────────────────────────────────────────────────────────────────────┘
```

### Flow Diagram Mode
```
┌────────────────────────────────┬───────────────────────────────────┐
│  Explanation                   │  Flow Diagram                     │
│  ─────────────────────────────  │  ────────────────────────────── │
│  RAG retrieves relevant        │         ┌──────────────┐          │
│  documents from a vector       │         │  User Query  │          │
│  store before generating...    │         └──────┬───────┘          │
│                                │                ▼                  │
│                                │      ┌─────────────────┐          │
│                                │      │  Embed & Search  │         │
│                                │      └────────┬────────┘          │
│                                │               ▼                   │
│                                │      ┌─────────────────┐          │
│                                │      │  Retrieve Docs  │          │
│                                │      └────────┬────────┘          │
│                                │               ▼                   │
│                                │      ┌─────────────────┐          │
│                                │      │  Generate Answer │         │
│                                │      └─────────────────┘          │
│                                │  [ ⬇️ Download PNG ]              │
└────────────────────────────────┴───────────────────────────────────┘
```

### Learning Dashboard
```
┌──────────┬──────────┬──────────┬──────────┬──────────────────────┐
│ 📅  42   │ 📖  28   │ 🔥  7d   │ 🏆  14d  │ ❌  3                │
│ Sessions │  Days    │  Streak  │  Longest │  Missed (30 days)    │
└──────────┴──────────┴──────────┴──────────┴──────────────────────┘

  Activity Calendar — Last 13 Weeks
  Mon  ░ ░ █ ░ █ █ ░ █ █ ░ ░ █ █
  Tue  █ ░ ░ █ █ ░ █ ░ █ █ ░ █ ░
  ...
  (█ = logged in   ░ = no session)
```

---

## 🗂️ Project Structure

```
07_AI_Educator/
│
├── app.py                        # Main Streamlit application
├── launcher.py                   # pywebview desktop launcher (Windows app)
├── Launch_AI_Educator.bat        # One-click shortcut to open the desktop app
│
├── modules/
│   ├── claude_client.py          # Anthropic API — streaming + non-streaming calls
│   ├── prompts.py                # System prompts for every explanation mode
│   ├── diagram_generator.py      # Mermaid code → PNG via mermaid.ink API
│   ├── pdf_exporter.py           # Formatted PDF export (navy/gold theme, fpdf2)
│   ├── md_exporter.py            # Markdown export with full Q&A history
│   └── login_tracker.py          # Login recording, streak calculation, dashboard data
│
├── data/
│   └── login_tracker.json        # Auto-created on first run (gitignored)
│
├── exports/
│   └── diagram_*.png             # Flow diagram PNGs saved here
│
├── .streamlit/
│   └── config.toml               # Navy/gold professional theme
│
├── .env                          # Your API key (gitignored — never commit)
├── .env.example                  # Template: shows required env variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Anthropic API key** — [Get one](https://console.anthropic.com/)
- **Internet connection** — Required for Claude API calls and diagram rendering

### 1. Navigate to the project folder

```bash
cd 06_Assignments/07_AI_Educator
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy `.env.example` to `.env` and fill in your key:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
USER_NAME=Your Name
```

> **Never commit `.env`** — it is already in `.gitignore`.

---

## ▶️ Running the App

### Option A — Browser (Streamlit)

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` in your default browser.

### Option B — Windows Desktop App

```bash
python launcher.py
```

Or double-click **`Launch_AI_Educator.bat`** — opens as a native Windows window
(powered by pywebview + WebView2). No browser tab needed.

---

## 📖 How to Use

### Step 1 — Pick an Explanation Mode

| Mode | Best for |
|---|---|
| **Technical** | Developers, researchers — full depth, precise terminology |
| **Simple** | Beginners, or anyone wanting the quick human-friendly version |
| **Simple + Your Background** | Fill in "I am a nurse / teacher / chef" and get analogies from *your* world |
| **Flow Diagram** | Visual learners — get a flowchart and explanation side by side |
| **Blog** | Content creators — get a ready-to-publish post in one click |

### Step 2 — Ask Your Question

Type anything AI-related in the text area and click **Ask Coco 🎓**.
The answer streams in live — you'll see it appear word by word.

### Step 3 — Follow Up

After any answer, a **"Continue the Conversation"** section appears.
Type a follow-up question and click **Send ➤**.
Coco remembers everything said so far — no need to repeat context.

### Step 4 — Export

Use the **Export Session** panel in the sidebar at any time:

- **Generate PDF 📄** — Full Q&A (initial answer + all follow-ups) as a formatted PDF,
  saved directly to your **Downloads** folder. Named after your question (e.g. `neural_network.pdf`).
- **Generate MD 📝** — Same content as a clean Markdown file in your **Downloads** folder.
- **⬇️ Download** — Trigger a browser/OS download of the last generated file.
- **📂 Open** — Open the saved file directly from within the app.

> Export works at any point — even after follow-up conversations. The PDF/MD always
> contains the complete session including every follow-up.

### Step 5 — Start Fresh

Click **New Question** to clear everything and start a new topic.
All fields reset, including the optional background input.

---

## ⚙️ How It Works Under the Hood

### Streaming Architecture

```
User clicks "Ask Coco"
        │
        ▼
stream_educator() → anthropic.messages.stream()
        │
        ▼
st.write_stream() → tokens arrive and render live in the browser
        │
        ▼
Full response stored in st.session_state
        │
        ▼
Formatted answer box renders (answer-box with gold left border)
```

### Flow Diagram Pipeline

```
Your question
      │
      ▼
Claude generates Mermaid.js code
      │
      ▼
Code is base64-encoded (URL-safe)
      │
      ▼
GET https://mermaid.ink/img/{base64}
      │
      ▼
PNG bytes returned
      │
      ├──▶  st.image()  →  shown inline in the app
      └──▶  exports/diagram_*.png  →  saved to disk
```

### Export Pipeline

```
"Generate PDF" button clicked
      │
      ▼
_gen_pdf flag set → st.rerun()
      │
      ▼
export_to_pdf(mode, chat_history, image_path)
      │  (progress bar: 0% → 30% → 75% → 100%)
      ▼
PDF written to  ~/Downloads/{question_slug}.pdf
      │
      ▼
"⬇️ Download" and "📂 Open" buttons appear
```

### Multi-turn Chat

```
Initial Q&A stored as:
  chat_history = [
      {"role": "user",      "content": "What is RAG?"},
      {"role": "assistant", "content": "RAG stands for..."},
  ]

Each follow-up appends to this list and the full history
is sent to Claude on every turn — maintaining full context.
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **AI Model** | [Anthropic Claude](https://www.anthropic.com) `claude-sonnet-4-6` |
| **UI Framework** | [Streamlit](https://streamlit.io) |
| **Desktop Wrapper** | [pywebview](https://pywebview.flowrl.com) + WebView2 |
| **Diagram Rendering** | [mermaid.ink](https://mermaid.ink) (free public API) |
| **PDF Generation** | [fpdf2](https://py-fpdf2.readthedocs.io) |
| **Charts** | [Plotly](https://plotly.com/python/) |
| **Data Handling** | [pandas](https://pandas.pydata.org/) |
| **Image Processing** | [Pillow](https://python-pillow.org/) |
| **Config** | [python-dotenv](https://pypi.org/project/python-dotenv/) |

---

## 🔧 Troubleshooting

**"ANTHROPIC_API_KEY is not set"**
Open `.env`, paste your key, and ensure there are no trailing spaces.

**Streamlit not found after install**
Run pip via the full venv path:
```bash
d:\path\to\project\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Flow diagram is blank or fails**
The [mermaid.ink](https://mermaid.ink) public API occasionally has brief downtime.
Try again in a moment. The raw Mermaid code is always shown as a fallback — paste it
into [mermaid.live](https://mermaid.live) to render it manually.

**PDF shows `?` instead of special characters**
The PDF uses built-in Latin-1 fonts. Smart quotes, em-dashes, and accented characters
are automatically converted to their nearest ASCII equivalents before rendering.

**Desktop app opens a blank window**
WebView2 (Edge runtime) must be installed on the machine. It ships with Windows 11
and modern Windows 10. If missing, the launcher falls back to the default browser.

**Export progress bar not visible for MD files**
MD generation is near-instantaneous. Small `time.sleep()` delays are inserted between
progress steps to ensure Streamlit has time to render the intermediate states.

---

## 📊 Learning Dashboard Details

Every time you open the app, a login timestamp is recorded to `data/login_tracker.json`.

The dashboard shows:

| Metric | How it's calculated |
|---|---|
| **Total Sessions** | Count of all records in the JSON file |
| **Days Studied** | Count of *unique* calendar dates (multiple logins on one day = 1 day) |
| **Current Streak** | Consecutive days ending today (or yesterday if today has no session yet) |
| **Longest Streak** | Best unbroken run of unique login days ever recorded |
| **Missed (Last 30 Days)** | Calendar days in the last 30 with no session |
| **Activity Calendar** | Last 13 weeks plotted as a GitHub-style Plotly heatmap |

---

## 🔒 Security Notes

- Your Anthropic API key lives only in `.env` and is never committed to version control.
- `.gitignore` excludes `.env`, `data/login_tracker.json`, `__pycache__/`, and `.venv/`.
- No user data leaves your machine except the API calls to Anthropic for AI responses.

---

## 👩‍💻 Author

Built by **Sunitha** as part of a personal GenAI Learning Journey.

*Powered by Claude · Streamlit · Python · Built with curiosity and a lot of follow-up questions.*
