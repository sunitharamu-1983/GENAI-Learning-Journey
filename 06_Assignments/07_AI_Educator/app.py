import os
import re
import time
import random
from datetime import datetime, timedelta, date
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from modules.claude_client import (
    ask_educator, generate_diagram_code, chat_with_educator,
    stream_educator, stream_chat,
)
from modules.diagram_generator import render_mermaid_to_png
from modules.login_tracker import record_login, get_dashboard_data
from modules.pdf_exporter import export_to_pdf
from modules.md_exporter import export_to_md

load_dotenv()


_STOP = {
    "what", "is", "are", "was", "were", "a", "an", "the", "how", "why",
    "do", "does", "did", "can", "could", "would", "should", "will",
    "i", "me", "my", "you", "your", "in", "on", "at", "to", "for",
    "of", "and", "or", "with", "about", "by", "be", "been",
}

def _slugify(text: str, max_words: int = 3, max_len: int = 30) -> str:
    """Keep the first few meaningful words from a question as a short slug."""
    words  = re.sub(r"[^\w\s]", "", text.lower()).split()
    kept   = [w for w in words if w not in _STOP] or words
    slug   = "_".join(kept[:max_words])
    return (slug[:max_len].rstrip("_")) or "ai_educator"


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Educator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Typography ── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
                     'Helvetica Neue', Arial, sans-serif !important;
    }
    h1 { color: #1e3a5f !important; font-weight: 700 !important;
         letter-spacing: -0.02em !important; }
    h2 { color: #1e3a5f !important; font-weight: 600 !important; }
    h3 { color: #2d4a7a !important; font-weight: 600 !important; }

    /* ── Metric cards ── */
    .metric-card {
        background: #ffffff;
        border: 1px solid #dde3ef;
        border-radius: 14px;
        padding: 22px 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(30,58,95,0.07);
        transition: box-shadow 0.2s ease, transform 0.15s ease;
    }
    .metric-card:hover {
        box-shadow: 0 8px 24px rgba(30,58,95,0.13);
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a5f;
        letter-spacing: -0.03em;
        line-height: 1.15;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-top: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.09em;
    }

    /* ── Answer box ── */
    .answer-box {
        background: #ffffff;
        border-left: 3px solid #c8a96e;
        border-radius: 0 10px 10px 0;
        padding: 22px 26px;
        margin-top: 10px;
        box-shadow: 0 2px 10px rgba(30,58,95,0.06);
        line-height: 1.78;
        color: #1a202c;
        font-size: 0.96rem;
    }

    /* ── Mode badge ── */
    .mode-badge {
        display: inline-block;
        background: #edf1f7;
        color: #1e3a5f;
        border-radius: 30px;
        padding: 4px 16px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        border: 1px solid #c5d0e4;
    }

    /* ── Dividers ── */
    hr { border-color: #e4e9f2 !important; opacity: 1 !important; }

    /* ── Streamlit message overrides (no jarring red/orange) ── */
    .stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "session_started" not in st.session_state:
    record_login()
    st.session_state.session_started = True

_defaults = {
    "response_text":       "",
    "diagram_code":        "",
    "diagram_bytes":       None,
    "diagram_path":        "",
    "last_question":       "",
    "last_mode":           "",
    "pdf_bytes":           None,
    "pdf_filename":        "",
    "pdf_save_path":       "",
    "md_bytes":            None,
    "md_filename":         "",
    "md_save_path":        "",
    "chat_history":        [],
    "chat_mode":           "",
    "chat_human_context":  "",
    "question_input_key":  0,
    "_gen_pdf":            False,
    "_gen_md":             False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 AI Educator")
    st.markdown(f"*{datetime.now().strftime('%A, %d %B %Y')}*")
    st.markdown("---")
    page = st.radio("", ["🏠  Dashboard", "📚  AI Educator"], label_visibility="collapsed")
    st.markdown("---")

    # ── Export — always visible ───────────────────────────────────────────────
    st.markdown("**Export Session**")
    st.caption("Full Q&A + all follow-ups included.")

    # ── PDF ───────────────────────────────────────────────────────────────────
    # Run export when flag is set (separate from button click to avoid
    # st.download_button state conflicts on repeat clicks)
    if st.session_state._gen_pdf:
        st.session_state._gen_pdf = False
        prog = st.progress(0, text="Preparing…")
        try:
            prog.progress(30, text="Formatting content…")
            time.sleep(0.25)
            slug = _slugify(st.session_state.last_question)
            pdf_path = export_to_pdf(
                mode=st.session_state.last_mode,
                chat_history=st.session_state.chat_history,
                image_path=st.session_state.diagram_path or None,
                filename=f"{slug}.pdf",
            )
            prog.progress(75, text="Saving to Downloads…")
            time.sleep(0.25)
            with open(pdf_path, "rb") as f:
                st.session_state.pdf_bytes    = f.read()
            st.session_state.pdf_filename  = Path(pdf_path).name
            st.session_state.pdf_save_path = pdf_path
            prog.progress(100, text="Done!")
            time.sleep(0.4)
            prog.empty()
            st.success("PDF saved to Downloads ✓")
        except Exception as e:
            prog.empty()
            st.error(str(e))

    if st.button("Generate PDF 📄", use_container_width=True, key="sb_gen_pdf"):
        if not st.session_state.chat_history:
            st.info("Ask a question first — nothing to export yet.")
        else:
            st.session_state._gen_pdf = True
            st.rerun()

    if st.session_state.pdf_save_path:
        st.caption(f"📁 Downloads → `{st.session_state.pdf_filename}`")
        col_dl, col_open = st.columns(2)
        with col_dl:
            st.download_button(
                label="⬇️ Download",
                data=st.session_state.pdf_bytes,
                file_name=st.session_state.pdf_filename,
                mime="application/pdf",
                use_container_width=True,
                key="sb_dl_pdf",
            )
        with col_open:
            if st.button("📂 Open", use_container_width=True, key="sb_open_pdf"):
                os.startfile(st.session_state.pdf_save_path)

    st.markdown("")

    # ── Markdown ──────────────────────────────────────────────────────────────
    if st.session_state._gen_md:
        st.session_state._gen_md = False
        prog = st.progress(0, text="Preparing…")
        try:
            prog.progress(30, text="Formatting content…")
            time.sleep(0.25)
            slug = _slugify(st.session_state.last_question)
            md_path, md_content = export_to_md(
                mode=st.session_state.last_mode,
                chat_history=st.session_state.chat_history,
                image_path=st.session_state.diagram_path or None,
                filename=f"{slug}.md",
            )
            prog.progress(75, text="Saving to Downloads…")
            time.sleep(0.25)
            st.session_state.md_bytes    = md_content
            st.session_state.md_filename = Path(md_path).name
            st.session_state.md_save_path = md_path
            prog.progress(100, text="Done!")
            time.sleep(0.4)
            prog.empty()
            st.success("Markdown saved to Downloads ✓")
        except Exception as e:
            prog.empty()
            st.error(str(e))

    if st.button("Generate MD 📝", use_container_width=True, key="sb_gen_md"):
        if not st.session_state.chat_history:
            st.info("Ask a question first — nothing to export yet.")
        else:
            st.session_state._gen_md = True
            st.rerun()

    if st.session_state.md_save_path:
        st.caption(f"📁 Downloads → `{st.session_state.md_filename}`")
        col_dl, col_open = st.columns(2)
        with col_dl:
            st.download_button(
                label="⬇️ Download",
                data=st.session_state.md_bytes,
                file_name=st.session_state.md_filename,
                mime="text/plain",
                use_container_width=True,
                key="sb_dl_md",
            )
        with col_open:
            if st.button("📂 Open", use_container_width=True, key="sb_open_md"):
                os.startfile(st.session_state.md_save_path)

    st.markdown("---")

    st.caption("Powered by Claude · Built for lifelong learners")


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ══════════════════════════════════════════════════════════════════════════════
def _heatmap(login_dates: set, days: int = 91) -> go.Figure:
    today = date.today()
    start = today - timedelta(days=days - 1)
    all_dates = [start + timedelta(days=i) for i in range(days)]

    num_weeks = (days + 6) // 7 + 1
    z    = [[None] * num_weeks for _ in range(7)]
    text = [[""]   * num_weeks for _ in range(7)]

    for d in all_dates:
        offset = (d - start).days
        week, day = offset // 7, d.weekday()
        if week < num_weeks:
            z[day][week]    = 1 if d.strftime("%Y-%m-%d") in login_dates else 0
            text[day][week] = d.strftime("%b %d, %Y")

    fig = go.Figure(go.Heatmap(
        z=z, text=text,
        hovertemplate="%{text}<extra></extra>",
        colorscale=[[0, "#ebedf0"], [1, "#40c463"]],
        showscale=False,
        xgap=3, ygap=3,
        zmin=0, zmax=1,
    ))
    fig.update_layout(
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(7)),
            ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        ),
        xaxis=dict(showticklabels=False),
        height=220,
        margin=dict(t=10, b=10, l=55, r=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig


def show_dashboard():
    st.title("Learning Dashboard")
    st.markdown("Track your AI learning journey — every day counts!")
    st.markdown("---")

    data = get_dashboard_data()

    # ── Metric cards ──────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)

    def _card(col, value, label, icon=""):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                      <div class="metric-value">{icon}{value}</div>
                      <div class="metric-label">{label}</div>
                    </div>""",
                unsafe_allow_html=True,
            )

    _card(c1, data["total_sessions"],  "Total Sessions",       "📅 ")
    _card(c2, data["total_days"],      "Days Studied",         "📖 ")
    _card(c3, f"{data['current_streak']}d", "Current Streak",  "🔥 ")
    _card(c4, f"{data['longest_streak']}d", "Longest Streak",  "🏆 ")
    _card(c5, data["missed_last_30"],  "Missed (Last 30 Days)","❌ ")

    st.markdown("---")

    # ── Heatmap ───────────────────────────────────────────────────────────────
    st.subheader("Activity Calendar — Last 13 Weeks")
    st.markdown(
        "<span style='color:#ebedf0;font-size:1.2rem;'>■</span> No session &nbsp;&nbsp;"
        "<span style='color:#40c463;font-size:1.2rem;'>■</span> Logged in",
        unsafe_allow_html=True,
    )
    st.plotly_chart(_heatmap(data["login_dates"]), use_container_width=True)

    st.markdown("---")

    # ── Tables ────────────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Days Missed (Last 30 Days)")
        if data["missed_dates"]:
            missed_df = pd.DataFrame({"Date": sorted(data["missed_dates"], reverse=True)})
            missed_df["Day"] = pd.to_datetime(missed_df["Date"]).dt.strftime("%A")
            st.dataframe(missed_df, use_container_width=True, hide_index=True)
        else:
            st.success("Perfect attendance in the last 30 days! Keep it up!")

    with col_b:
        st.subheader("Recent Sessions")
        if data["all_logins"]:
            recent = sorted(data["all_logins"], key=lambda x: x["datetime"], reverse=True)[:15]
            recent_df = pd.DataFrame([{"Date": s["date"], "Time": s["time"]} for s in recent])
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
        else:
            st.info("No sessions recorded yet.")


# ── Welcome messages ──────────────────────────────────────────────────────────
_WITTY = [
    "Ready to make AI a little less mysterious today?",
    "Another day, another algorithm to conquer!",
    "The best time to learn AI was yesterday. The second best time is right now.",
    "Fun fact: you're already surrounded by AI — time to truly understand it.",
    "Curiosity is the mother of all breakthroughs. Let's begin.",
    "GPT doesn't stand for 'Getting Pretty Tired' — though some days it feels close!",
    "Today's confusion is tomorrow's expertise. Let's get beautifully confused.",
    "Even the smartest models started with a single training step. So do we.",
    "Behind every great AI is a human who asked great questions. Like you.",
    "Neural networks, transformers, RAG — let's make them all click today.",
    "The robots aren't taking over. They're waiting for you to understand them.",
    "Every expert was once a beginner who refused to give up. Welcome back.",
]


def _welcome_card():
    name  = os.getenv("USER_NAME", "there")
    quote = random.choice(_WITTY)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5082 100%);
        border-radius: 10px;
        padding: 13px 22px;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(30,58,95,0.14);
    ">
        <div style="white-space: nowrap;">
            <span style="color:#c8a96e; font-size:0.62rem; font-weight:700;
                         letter-spacing:0.12em; text-transform:uppercase;">
                Welcome back &nbsp;·&nbsp;
            </span>
            <span style="color:#ffffff; font-size:0.97rem; font-weight:600;">
                {name} 👋
            </span>
        </div>
        <div style="color:#8ab0cc; font-size:0.8rem; font-style:italic;
                    line-height:1.45; text-align:right; padding-left:24px;">
            &ldquo;{quote}&rdquo;
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# AI EDUCATOR PAGE
# ══════════════════════════════════════════════════════════════════════════════
def show_educator():
    _welcome_card()
    st.markdown("Ask me anything about AI. Choose how you'd like me to explain it.")
    st.markdown("---")

    # ── Mode selector ─────────────────────────────────────────────────────────
    mode = st.radio(
        "**Explanation Mode**",
        ["Technical", "Simple", "Flow Diagram", "Blog"],
        horizontal=True,
        help=(
            "Technical: deep dive with full terminology  |  "
            "Simple: plain English, optionally tailored to your background  |  "
            "Flow Diagram: visual flowchart + explanation  |  "
            "Blog: ready-to-publish blog post"
        ),
    )

    human_context = ""
    if mode == "Simple":
        st.markdown("""
        <div style="background:#f4f6fb; border-left:3px solid #c8a96e;
                    border-radius:0 8px 8px 0; padding:11px 16px; margin:6px 0 10px 0;
                    font-size:0.85rem; color:#334155; line-height:1.55;">
            <strong>Plain English</strong> — no jargon, everyday analogies, easy to follow.<br>
            <span style="color:#64748b;">Add your background below and Coco will use examples
            from <em>your</em> world. Leave it blank for general simple English.</span>
        </div>
        """, unsafe_allow_html=True)

        human_context = st.text_input(
            "Your background (optional)",
            placeholder="e.g.  I am a nurse  ·  I am a school teacher  ·  I am a chef  ·  I am a software developer",
            help="Blank = plain everyday English for anyone.  Filled = analogies drawn from your specific field.",
            key=f"human_context_{st.session_state.question_input_key}",
        )

    # ── Question input ────────────────────────────────────────────────────────
    question = st.text_area(
        "**Your question about AI:**",
        placeholder=(
            "e.g.  What is a neural network?\n"
            "      How does backpropagation work?\n"
            "      What is Retrieval-Augmented Generation (RAG)?"
        ),
        height=120,
        key=f"question_input_{st.session_state.question_input_key}",
    )

    col_ask, col_clear, _ = st.columns([1, 1, 5])
    with col_ask:
        ask_clicked = st.button("Ask Coco 🎓", type="primary", use_container_width=True)
    with col_clear:
        if st.button("New Question", type="secondary", use_container_width=True):
            for k in ["response_text", "diagram_code", "diagram_bytes",
                      "diagram_path", "last_question", "last_mode",
                      "pdf_bytes", "pdf_filename", "pdf_save_path",
                      "md_bytes", "md_filename", "md_save_path",
                      "chat_mode", "chat_human_context"]:
                st.session_state[k] = "" if k not in ("diagram_bytes", "pdf_bytes", "md_bytes") else None
            st.session_state.chat_history = []
            st.session_state.question_input_key += 1
            st.rerun()

    # ── Ask logic ─────────────────────────────────────────────────────────────
    if ask_clicked:
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            # Reset previous state
            st.session_state.pdf_bytes     = None
            st.session_state.pdf_filename  = ""
            st.session_state.pdf_save_path = ""
            st.session_state.md_bytes      = None
            st.session_state.md_filename   = ""
            st.session_state.md_save_path  = ""
            st.session_state.chat_history  = []

            try:
                stream_box = st.empty()

                if mode == "Flow Diagram":
                    # Stream the explanation first so the user sees output immediately
                    with stream_box.container():
                        explanation = st.write_stream(
                            stream_educator(question, "Technical")
                        )
                    # Then generate the diagram (non-streaming)
                    with st.spinner("Rendering flow diagram..."):
                        mermaid_code = generate_diagram_code(question)
                        img_bytes, img_path = render_mermaid_to_png(mermaid_code)

                    st.session_state.response_text = explanation
                    st.session_state.diagram_code  = mermaid_code
                    st.session_state.diagram_bytes = img_bytes
                    st.session_state.diagram_path  = img_path
                else:
                    with stream_box.container():
                        explanation = st.write_stream(
                            stream_educator(question, mode, human_context)
                        )
                    st.session_state.response_text = explanation
                    st.session_state.diagram_code  = ""
                    st.session_state.diagram_bytes = None
                    st.session_state.diagram_path  = ""

                st.session_state.last_question      = question
                st.session_state.last_mode          = mode
                st.session_state.chat_mode          = mode
                st.session_state.chat_human_context = human_context
                st.session_state.chat_history = [
                    {"role": "user",      "content": question},
                    {"role": "assistant", "content": st.session_state.response_text},
                ]
                stream_box.empty()   # clear raw stream; formatted answer renders below

            except ValueError as e:
                st.error(f"Configuration error: {e}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    # ── Display results ───────────────────────────────────────────────────────
    if st.session_state.response_text:
        st.markdown("---")
        st.markdown(
            f"<span class='mode-badge'>{st.session_state.last_mode}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(f"> **Q:** {st.session_state.last_question}")

        # ── Answer display ────────────────────────────────────────────────────
        if st.session_state.last_mode == "Flow Diagram":
            col_exp, col_dia = st.columns([1, 1])

            with col_exp:
                st.subheader("Explanation")
                st.markdown(
                    f"<div class='answer-box'>{st.session_state.response_text}</div>",
                    unsafe_allow_html=True,
                )

            with col_dia:
                st.subheader("Flow Diagram")
                if st.session_state.diagram_bytes:
                    st.image(st.session_state.diagram_bytes, use_container_width=True)
                    st.download_button(
                        label="⬇️  Download PNG",
                        data=st.session_state.diagram_bytes,
                        file_name=Path(st.session_state.diagram_path).name
                                  if st.session_state.diagram_path else "diagram.png",
                        mime="image/png",
                        use_container_width=True,
                    )
                else:
                    st.code(st.session_state.diagram_code, language="text")
        else:
            st.subheader("Answer")
            if st.session_state.last_mode == "Blog":
                st.markdown(st.session_state.response_text)
            else:
                st.markdown(
                    f"<div class='answer-box'>{st.session_state.response_text}</div>",
                    unsafe_allow_html=True,
                )

        # ── Contextual chat ───────────────────────────────────────────────────
        if st.session_state.chat_history:
            st.markdown("---")
            st.subheader("💬 Continue the Conversation")
            st.caption("Ask Coco anything about this topic — the full context is remembered.")

            # Show follow-up exchanges (skip first 2 = the initial Q&A already shown above)
            for msg in st.session_state.chat_history[2:]:
                avatar = "🧑" if msg["role"] == "user" else "🎓"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

            # Inline input row — always visible
            st.markdown("**Your follow-up:**")
            col_inp, col_send = st.columns([5, 1])
            with col_inp:
                follow_up = st.text_input(
                    label="follow_up_input",
                    label_visibility="collapsed",
                    placeholder="e.g.  Can you give me a real-world example?",
                    key=f"followup_{len(st.session_state.chat_history)}",
                )
            with col_send:
                send_clicked = st.button("Send ➤", type="primary", use_container_width=True)

            if send_clicked and follow_up.strip():
                st.session_state.chat_history.append(
                    {"role": "user", "content": follow_up.strip()}
                )
                try:
                    with st.chat_message("assistant", avatar="🎓"):
                        reply = st.write_stream(
                            stream_chat(
                                messages=st.session_state.chat_history,
                                mode=st.session_state.chat_mode,
                                human_context=st.session_state.chat_human_context,
                            )
                        )
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": reply}
                    )
                except Exception as e:
                    st.error(f"Chat error: {e}")
                st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────
if "Dashboard" in page:
    show_dashboard()
else:
    show_educator()
