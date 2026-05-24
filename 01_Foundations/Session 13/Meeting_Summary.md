# Meeting Summary — GitHub, Open Source Contribution & Distil Project Setup
**Date:** May 16, 2026
**Sessions:** 3 (split due to technical issues)
- Session 1: 8:03 AM – 8:39 AM (36 minutes)
- Session 2: 8:41 AM – 11:41 AM (160 minutes)
- Session 3: 11:41 AM – 12:16 PM (35 minutes)

**Total Duration:** ~231 minutes (~3 hrs 51 mins)
**Platform:** Microsoft Teams
**Instructor:** Laxmi Narayen (Applied Research Scientist, OpenStream.ai)
**Co-instructor / Repo Owner:** Mohamed Noordeen

---

## Participants

**Session 1:** Ashika Farzana, Bhagya Ganisetti, Chandrakumar L, Devi Narayanan, Dinesh Balaraman, Jeganathan K, Laxmi Narayen, Manoj PS, Parthasarathi, Pon Ezhil, Sathiyarajan Mariyappan, Sirajuddeen G, Sri Ranjith, Sundar B, Suresh Soundararajan

**Session 2:** Afsar Ali, Akash Balmiki, Asha Ponraj, Bhagya Ganisetti, Bineetha Gooinathan, Damodaran Selvaraj, Dinesh Balaraman, Kannabiran G, Laxmi Narayen, Manoj PS, Mohamed Noordeen, Muniappan Mohanraj, Naveen Kumar, Navyatha Mattupali, neelsvel1, Parthasarathi, Pon Ezhil, Rajkannu, Ramachandran Kothandan, Sabarinathan J, Sathiyarajan Mariyappan, Sirajuddeen G, Sundar B, Sunitha Ramu, Vijayarajan Packrisamy

**Session 3:** Asha Ponraj, Bineetha Gooinathan, Damodaran Selvaraj, Dinesh Balaraman, Laxmi Narayen, neelsvel1, Nitish Jha, Parthasarathi, Pon Ezhil, Sathiyarajan Mariyappan, Sirajuddeen G, Sunitha Ramu, Vijayarajan Packrisamy

---

## Session Overview

This was a full-day hands-on lab session covering three interconnected topics:
1. **Laxmi Narayen's introduction** as the substitute instructor for Mohamed Noordeen's sessions going forward
2. **GitHub workflow** — forking, cloning, branching, committing, pushing, pull requests, conflict resolution, and badges
3. **Distil project setup** — running the AI classroom assessment tool locally using LM Studio or Olama
4. **Feature addition demo** — how to add a new feature (PDF support) using Claude Code and raise a PR

The session had recurring Microsoft Teams screen-sharing issues throughout, which caused multiple interruptions.

---

## Part 1 — Instructor Introduction & Session Recap (Session 1: 00:00 – ~23:00)

### Laxmi Narayen — Self Introduction

Laxmi Narayen introduced herself as the substitute trainer for the next few sessions, replacing Mohamed Noordeen. Key points:
- **Role:** Applied Research Scientist at **OpenStream.ai**
- **Background:** 8–9 years as a trainer at Inceptez
- **Research:** Invents new ML algorithms and publishes them. Publications include generative AI algorithms — one for 3D facial expression generation and another for 2D facial expression generation
- **Active research paper:** *"Invisible Biases and Filters"* — published at AIES (AI Ethics and Society), studying cultural bias in LLMs used for hiring

### Recap of Previous Session

Laxmi summarised what had been done in prior sessions:
- **Local LLMs:** Explored running quantized LLM versions locally — floating point weights, quantized weights, double quantized weights
- **Tools used:** Olama and LM Studio — both zero-cost local API options
- **Project built:** **Distil** — an AI Classroom Assessment Tool

**What Distil does:**
- Accepts uploaded transcripts or meeting/lecture recordings
- Generates structured session summaries
- Has a "Teach-it-Back" voice system using ASR (Automatic Speech Recognition) and STT/TTS (Speech-to-Text / Text-to-Speech)
- Generates interactive quizzes and concept maps
- Is a fully documented open source repository

**Tech stack of Distil:**
- Frontend: Node.js
- Backend: Python
- LLM Server: LM Studio or Olama + Whisper for STT

---

### Why Open Source and Prior Work Matters — Real World Analogy

Laxmi used an example from her own domain (AI for media/movies) to explain the value of building on existing open source projects:

**Example:** Shipping a Bollywood blockbuster (Bahubali) to China, where there are multiple dialects. You would want AI-driven lip dubbing — where the video's lip movements match a different audio track. This is done by a system called **Diff2Lip**. If you are an ML engineer at a company like Cube Cinemas and need to productionise this:

1. **First thing you check:** The GitHub repository's **License** — is it non-commercial? Can you build a derived product from it?
2. **Second thing:** The **README** — how detailed is the setup, what are GPU/system requirements, what are the parameters?
3. **Then:** You build on top of it rather than starting from scratch.

**Key insight:** In research and industry, building on existing open source work is the norm. Projects like NumPy, scikit-learn cannot exist without open source contributors. Python's biggest advantage is its large, active open source community.

---

### Agenda for the Day

1. Set up the Distil project from GitHub (fork → clone → run)
2. Make a small contribution (documentation fix)
3. Raise a pull request
4. Understand conflict resolution
5. Become open source contributors

---

## Part 2 — GitHub Workflow (Session 1: ~24:00 – End; Session 2: 00:00 – ~01:58)

### Two Ways to Contribute to a Repository

**Way 1 — Direct collaborator access:**
- If you are assigned as a collaborator or co-owner of the project, you clone the repo directly and push with write access. No fork needed.

**Way 2 — Open source contribution (forking):**
- If you are NOT a collaborator, you fork the repository first. Fork creates your own copy of the repository. You work on your copy, make changes, and raise a pull request to the main repo.

**Key rule:** Clone your fork — NOT the original repo. If you clone the original, you cannot push your changes (you don't have write access).

---

### Step-by-Step GitHub Workflow Demonstrated Live

Laxmi demonstrated the complete workflow with the Distil repo (owned by Mohamed Noordeen / NoorNas):

#### Step 1 — Fork
- Go to the main Distil repository on GitHub
- Click **Fork** → select your account → click **Create Fork**
- This creates `YourUsername/distil` as a copy of `NoorNas/distil`

#### Step 2 — Clone
- Copy the HTTPS URL of your fork
- Open VS Code terminal
- Create a folder (e.g., `my-project-contributions`)
- Run: `git clone <your-fork-url>`
- This downloads the project into your local folder

#### Step 3 — Check Status and Sync
```bash
git status               # Check current branch and changes
git checkout main        # Make sure you're on main
git pull upstream main   # Pull latest from original repo to stay in sync
```

To set the upstream (original repo) if not already set:
```bash
git remote add upstream <original-repo-url>
```

#### Step 4 — Create a New Branch
**Golden rule of pull requests:** Never commit directly to main. Always create a new branch.

Branch naming conventions:
- Documentation changes: `docs/fix-readme` or `docs-fix-more-text-rules`
- Bug fixes: `bug-fix/description`
- New features: `feature/feature-name`

These are unwritten community rules of open source contribution.

```bash
git checkout -b docs/fix-readme-something
```

#### Step 5 — Make Changes
- Edit the README or any file
- Example: Laxmi added lines about branch naming conventions and healthy community push rules

#### Step 6 — Stage, Commit, Push
```bash
git add .                              # Stage all changes
git commit -m "docs: added branch naming rules"   # Commit with descriptive message
git push -u origin docs/fix-readme-something      # Push to your fork
```
**Important:** Never do a "blind push" without a commit message. The message helps reviewers understand what changed.

#### Step 7 — Raise a Pull Request (PR)
- Go to the original Noor Nas / Distil repository on GitHub
- GitHub automatically shows a yellow banner: *"You have recent pushes in branch X. Compare and pull request."*
- Click **Compare and pull request**
- Add a title and description
- Select reviewers and assignees if needed
- Click **Create pull request**

#### Step 8 — Conflict Resolution (from collaborator's perspective)
When multiple people push changes to the same file, merge conflicts arise. As a collaborator:
1. Assign the conflict resolution to yourself
2. Click **Resolve conflicts**
3. GitHub shows the conflicting sections — incoming change vs current change
4. Choose: accept incoming, keep current, or accept both
5. Mark conflict as resolved
6. Commit the merge

**Example shown:** A conflict in README.md where one change said "test comment from Raj" — Laxmi accepted both changes and marked resolved.

#### Step 9 — Merge Types
Three merge options are available in GitHub:
- **Squash and merge** — combines all commits into one
- **Create a merge commit** — merges all commits with a merge commit
- **Rebase and merge** — replays commits on top of the base branch

Laxmi let participants explore the differences.

#### Step 10 — GitHub Achievement Badges
After a merge is accepted, GitHub awards badges:
- **YOLO badge** — given when a merge is done without review (sarcastically named)
- **Pull Shark badge** — earned when pull requests you opened are merged

**Note from Asha Ponraj:** She could not see her badge initially. The reason was that the username in VS Code was different from her GitHub profile username (her son had used her laptop). After changing the username and doing a second commit, the badge appeared. This is a common issue to watch out for.

---

### Individual Troubleshooting — Key Issues and Resolutions

**Sunitha Ramu — Wrong repository origin issue:**
Sunitha's push was failing because her local folder was nested inside another folder that already had a Git initialisation (pointing to a different repository). Fix: Move outside the nested Git repo — clone in a clean folder with no parent Git connection. Then fork already existed, so she only needed to sync the fork (96 commits behind) and re-clone.

**Damodaran Selvaraj — Inside wrong repository:**
Damodaran had cloned from a different repo (zero-to-engineer repository, not distil). Fix: Re-fork and re-clone from the correct distil repository link. He also had a "distil inside distil" folder issue from nested cloning — resolved by navigating to the correct inner distil folder.

**Kannabiran G — Authentication failure:**
Repeated "invalid username or token" when pushing. Fix: Generate a **Personal Access Token (PAT)** from GitHub Settings → Developer Settings → Personal Access Tokens → Generate new token (Classic) → select all relevant scopes (repo, workflow, write packages, admin). When prompted for a password during git push, paste the PAT instead of the account password.

**Vijayarajan Packrisamy — Setting upstream URL changed origin:**
After setting the upstream URL, his origin changed automatically. He faced the same "permission denied" push issue. Same fix: use PAT.

**Manoj PS — Conflict on every push:**
When pushing README changes, a conflict would appear. Fix: Pull upstream before every push to ensure your branch is in sync with the latest main. Then re-push. This is a safe mechanism — it ensures your changes don't overwrite others' work.

**Navyatha Mattupali — GitHub CLI authentication (Mac):**
She was logging into GitHub via Google account and couldn't provide a password. Fix: Used GitHub CLI (`brew install gh` on Mac) to authenticate globally. This sets system-wide GitHub credentials so you don't need to provide a password on every push.

**Three authentication methods identified:**
1. Personal Access Token (PAT) — paste as password
2. Email + password login (if password auth is enabled)
3. GitHub CLI (`gh auth login`) — sets global authentication; easiest long-term solution

---

### Repository Statistics at End of Session

By the end of the hands-on session, the Distil repository had:
- **~40–42 contributors** (from the batch of students)
- **63 forks**
- **146 commits**

Laxmi celebrated this milestone — students went from not knowing GitHub to becoming open source contributors in a single session.

---

## Part 3 — Setting Up Distil Locally (Session 2: ~01:58 – 02:38; Session 3: 00:00 – ~22:00)

### Project: Distil — AI Classroom Assessment Tool

**What Distil does:**
- Turns any Teams/Zoom meeting into a complete learning assessment
- Analyses transcripts
- Draws concept maps
- Extracts key concepts and confusion zones
- Builds structured session summaries
- Generates interactive quizzes (Q&A system)
- Creates relationship mappings between topics

**Repository structure:**
```
distil/
├── README.md
├── Makefile
├── backend/
│   ├── requirements.txt
│   ├── main.py (app entry point)
│   ├── analyzer/
│   ├── assessor/
│   ├── evaluator/
│   ├── storage/
│   └── config.yaml (DO NOT push this — contains API keys)
├── frontend/
│   └── (Node.js / React)
├── prompts/
├── data/
└── tests/
```

**Important:** `config.yaml` contains API keys. Never push it to a public repository.

---

### Setup Method 1 — Using LM Studio

1. Download **LM Studio** from lmstudio.ai
   - DMG for Mac, EXE for Windows
2. Open LM Studio → go to **Discover** tab
3. Search for model: **Qwen3-4B-2507** (or similar)
4. Select the **GGUF 8-bit** version (as specified in instructions)
5. Download the model
6. Load the model — it will host automatically on the **default port**

*Note: Laxmi mentioned the Qwen 32K context model would not load even on her MacBook Air due to RAM constraints. Stick to smaller models for local setups.*

---

### Setup Method 2 — Using Olama

1. Install Olama from olama.com
2. Pull the model:
   ```bash
   ollama pull qwen2
   ```
3. In `backend/config.yaml`, change the model reference to `ollama/qwen2.0`
4. Save config

---

### Setup Method 3 — Using Cloud LLM (Gemini or Claude)

If LM Studio and Olama both fail (RAM constraints, model loading issues), use a cloud LLM like Gemini or Claude. Update the config accordingly.

---

### Backend Setup

```bash
# Navigate to backend
cd backend

# Copy example config (DO NOT push config.yaml)
cp config.example.yaml config.yaml

# Install dependencies (recommended: use base Python, not conda, due to Whisper dependency issues)
/usr/local/bin/python3 -m pip install -r requirements.txt

# Run backend
python -m uvicorn main:app --reload
```

*The project was built targeting Python 3.10. Later versions should work with minor installation adjustments.*

*Whisper (STT model) has known compatibility issues with conda environments. Run pip install directly on base Python to avoid this.*

---

### Frontend Setup

```bash
# In a separate terminal
cd frontend

# Install Node.js dependencies
npm install

# Run frontend
npm run dev
```

*If npm is not installed: Install Node.js first from nodejs.org (or use `winget install openjs.nodejs.lts` on Windows).*

*Both backend and frontend must run simultaneously in separate terminals.*

---

### Running the App

1. Open browser → go to `localhost:8000` (or the port shown in the terminal)
2. Enter your name
3. Upload a transcript file (`.txt`, `.vtt`, `.docx` — and PDF if the PDF feature is added)
4. Click **Analyse**
5. The app will:
   - Summarise different blocks of the transcript
   - Extract key concepts
   - Merge summaries
   - Build a structured session summary
   - Create a concept map
   - List confusion zones
   - Generate Q&A / assessment questions

**Supported file formats (base):** `.txt`, `.vtt`, `.docx`

---

## Part 4 — Feature Addition Demo (Session 3: ~03:00 – 27:00)

### Live Feature Demo: Adding PDF Support

Laxmi demonstrated adding PDF upload support to Distil — a feature that was not in the original repository.

**What the original supported:** `.txt`, `.vtt`, `.docx`
**Feature added:** `.pdf`

She used the same meeting document that was shared in WhatsApp, converted it to PDF, and uploaded it through Distil to show it working.

**How she added it:**
- Used **Claude Code** (Anthropic's agentic coding tool) to modify the existing codebase
- Prompted Claude Code: *"Add PDF support to the upload pipeline"*
- Claude Code automatically modified `config.py`, `analyzer.py`, and other relevant files
- She tested it locally, confirmed PDF analysis worked end-to-end
- Then pushed it as a new feature PR

---

### Two Ways to Push a Feature

**Manual way (what the class learned):**
```bash
git checkout main
git pull upstream main
git checkout -b feature/add-pdf-support
# make changes
git add .
git commit -m "feature: added PDF upload and pipeline support"
git push -u origin feature/add-pdf-support
# then go to GitHub and raise a PR manually
```

**Assisted way using Claude Code + GitHub CLI:**
- Prompt Claude Code: *"Please create a PR for this into the main repository. This is a feature. List all changes. Add documentation for this PR."*
- Claude Code:
  - Ran `git status` automatically
  - Created a new feature branch
  - Added only the changed files (not a blanket `git add .`)
  - Committed with full documentation
  - Pushed the branch
  - Used GitHub CLI (`gh`) to automatically raise the PR request

The PR created by Claude Code included:
- Feature name: "PDF Upload and Pipeline Fixes"
- Files changed
- Bug fixes included (OpenAI API key was silently ignored from config — now fixed; SQLite issue fixed; error message fixed)
- Testing plan for reviewers
- Co-authored-by note: "Co-authored by Claude Sonnet and Laxmi Narayen"

---

### PR Review Process (Collaborator's Perspective)

Once a PR is raised:
1. The PR appears in the repository's pull requests tab
2. Reviewer (in this case Laxmi as collaborator, or Noordeen as owner) receives the request
3. Reviewer goes to **Files Changed** tab — reviews all modifications
4. Reviewer can:
   - Add comments
   - Request changes
   - Assign it to another reviewer
   - Add labels (e.g., milestone, feature type)
5. Once satisfied: click **Merge pull request** → **Confirm merge**
6. The feature is now in the main repository — all forks can sync it

**Note:** When adding features, PR descriptions should be detailed — list all changes, fixes, and a testing plan. This is what real production PRs look like.

---

### Bug Found During Session

**neelsvel1** found a bug: When typing text directly into the transcript box (instead of uploading a file) and clicking Analyse, the backend returns a `JSON parse failed` error.

**Root cause:** The system only accepts file uploads in the four supported formats. Direct text pasting was not designed as an input method — the backend tries to parse the text as a file and fails.

**Laxmi's response:** This is a valid bug. Ideally, if a user pastes text directly, the system should still process it. This is exactly the kind of bug fix that can be contributed as a PR.

**Additional issue (neelsvel1):** The Qwen model with 32,768 context length would not load on a 16GB RAM system. Workaround: use a smaller model, or switch to a cloud LLM (Gemini/Claude).

**Missing config.yaml:** neelsvel1 had not created the `config.yaml` file. Solution: download `config.example.yaml` from the repository (in the zero-to-engineer resources folder shared by the instructor) and rename it to `config.yaml`. Never push `config.yaml` — it contains API keys.

---

## Part 5 — Assignment (Session 3: ~11:00 – 14:00)

### Assignment Details

Laxmi gave a team-based open source contribution assignment:

**Team:** Form a team of **maximum 4 people**

**Task:**
1. **Step 1:** Set up Distil locally and run it yourself — upload a document and verify the analysis works
2. **Step 2:** Think of a feature or bug fix to contribute
3. **Step 3:** Implement it, test it locally, and raise a pull request
4. **Step 4:** Fill in the Google Sheets tracker with: team member names, feature description, and the pull request link

**Deadline:** **Next Sunday**

**Feature ideas suggested:**
- Multilingual support — automatically detect language of the transcript (Tamil, Hindi, etc.)
- UI improvements — the current UI is basic; improve it
- Allow pasting transcript text directly (instead of only file upload) — this is also the bug fix neelsvel1 found
- Any other add-on that makes Distil better

**Laxmi's suggestion:** Ask Claude or any LLM — *"Tell me interesting features to add to Distil to make it better"* — and use that list as inspiration.

**Laxmi's note:** Documentation fixes were the first level of open source contribution. Feature additions are the next level. The goal is for students to understand the full loop — ideate, implement, test, push, review, merge.

---

## Technical Issues Log

Throughout all three sessions, Microsoft Teams screen sharing repeatedly disconnected. Key incidents:

- **Session 1:** Screen sharing was not working for the first 26 minutes — participants could not see Laxmi's screen. Parthasarathi mentioned that Mohamed Noordeen had solved this previously by changing settings.
- **Fix suggested by Sirajuddeen G:** Connecting via the Teams app (not browser) resolves screen sharing stability. Laxmi was initially on the browser.
- **Session 2:** After reconnecting via the Teams app, screen sharing was more stable but still dropped multiple times. Fix implemented mid-session: Teams Settings → General → Screen Sharing → switch from "Use Teams Content Sharing" to **"Use Mac OS Content Sharing"**.
- **Session 3:** Screen sharing issues continued but were less disruptive.

---

## Key Concepts — Quick Reference

| Concept | Definition |
|---------|-----------|
| Fork | A personal copy of someone else's repository on your GitHub account |
| Clone | Downloading a repository (your fork) to your local machine |
| Branch | An isolated version of the code where you make changes without affecting main |
| git add . | Stage all changed files for committing |
| git commit -m "message" | Save staged changes with a description |
| git push origin branch-name | Upload your branch to your fork on GitHub |
| Pull Request (PR) | A request to merge your changes into the original repository |
| Upstream | The original repository you forked from |
| git pull upstream main | Sync your local main with the latest from the original repo |
| Merge conflict | When two people change the same line — must be manually resolved |
| PAT | Personal Access Token — used instead of password for GitHub authentication |
| GitHub CLI (gh) | Command-line tool for GitHub — enables authentication and PR creation from terminal |
| YOLO badge | GitHub badge for merging without review |
| Pull Shark badge | GitHub badge for having merged pull requests |

---

## Git Commands Reference (as shared during session)

```bash
# Check status
git status

# Switch to main branch
git checkout main

# Sync with original repo
git pull upstream main

# Or add upstream first if not set
git remote add upstream <original-repo-url>

# Create and switch to new branch
git checkout -b docs/your-branch-name     # for documentation
git checkout -b feature/your-feature      # for features
git checkout -b bug-fix/description       # for bug fixes

# Stage changes
git add .

# Commit changes
git commit -m "your descriptive message here"

# Push to your fork
git push -u origin your-branch-name

# View commit history
history    # or git log
```

---

## Final Notes from Laxmi

- Students went from zero GitHub knowledge to being official open source contributors in one session. At peak, the Distil repo had 40+ contributors, 63 forks, 146 commits — all within the class day.
- Open source contribution is a fantastic way to learn and build a public portfolio.
- Always test locally before raising a PR. Never push untested code.
- Never push `config.yaml` or any file containing API keys.
- The class still has three more sessions — Laxmi will continue tomorrow and next week.

---

## Closing

Sunitha Ramu thanked Laxmi on behalf of several participants for her patience in walking through Git step-by-step for those who were completely new to it. Laxmi acknowledged the thanks gracefully and said she would continue coming for all remaining sessions.

Sathiyarajan Mariyappan raised a final issue — NPM was not installed on his Windows machine, causing `npm install` to fail. Resolution: Install Node.js from nodejs.org or via `winget install openjs.nodejs.lts`, which installs both Node.js and NPM together.

---

*Summary prepared from three meeting transcripts dated May 16, 2026 (Sessions 1, 2, and 3).*
