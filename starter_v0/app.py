"""VinUni Lab 03 — Streamlit Research Agent UI (Minimalist ChatGPT-style layout).

Run from starter_v0::

    python -m streamlit run app.py

The application reuses the real Research Agent tool loop from chat.py.
Secrets are supplied through environment variables or Streamlit Cloud Secrets.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

import streamlit as st

from chat import now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
TRANSCRIPTS = ROOT / "transcripts"
load_lab_env(ROOT)

# Sidebar Panel Toggle SVG icon (monochrome window panel icon)
_SIDEBAR_PANEL_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none">'
    '<path fill="#5d5d5d" d="M3 6C3 4.34315 4.34315 3 6 3H18C19.6569 3 21 4.34315 21 6V18'
    "C21 19.6569 19.6569 21 18 21H6C4.34315 21 3 19.6569 3 18V6ZM9 5H6C5.44772 5 5 5.44772 5 6"
    "V18C5 18.5523 5.44772 19 6 19H9V5ZM11 5V19H18C18.5523 19 19 18.5523 19 18V6"
    'C19 5.44772 18.5523 5 18 5H11Z"/></svg>'
)
SIDEBAR_PANEL_ICON_URI = f"data:image/svg+xml;utf8,{quote(_SIDEBAR_PANEL_SVG)}"

st.set_page_config(
    page_title="Research Agent",
    page_icon=":material/search:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Authentic CSS & Typography (Inter Font + Composer Model Pill) ----------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Apply crisp Inter typography without breaking Material Symbols icon font */
    html, body, p, h1, h2, h3, h4, h5, h6, li, label, input, textarea,
    [data-testid="stMarkdownContainer"],
    [data-testid="stText"],
    [data-testid="stCaptionContainer"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        color: #0d0d0d;
    }}

    /* Hide Streamlit default chrome */
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    [data-testid="stDecoration"] {{display: none !important;}}
    [data-testid="stHeaderActionElements"] {{display: none !important;}}
    .stAppDeployButton {{display: none !important;}}

    /* Transparent top header for sidebar expand icon */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        height: 3.25rem !important;
        pointer-events: none !important;
    }}
    header[data-testid="stHeader"] button {{
        pointer-events: auto !important;
    }}

    /* Main centered chat container (48rem / 768px max-width) */
    .block-container {{
        max-width: 48rem !important;
        padding-top: 2rem !important;
        padding-bottom: 7.5rem !important;
        margin: 0 auto !important;
    }}

    /* =========================================================================
       SIDEBAR SLIDE ANIMATION (cubic-bezier(0.4, 0, 0.2, 1)) & PANEL TOGGLE ICON
       ========================================================================= */
    section[data-testid="stSidebar"] {{
        background-color: #f9f9f9 !important;
        border-right: 1px solid rgba(0, 0, 0, 0.06) !important;
        transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                    min-width 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                    max-width 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                    width 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    section[data-testid="stSidebar"][aria-expanded="true"] {{
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
        transform: translateX(0) !important;
    }}
    section[data-testid="stSidebar"][aria-expanded="false"] {{
        width: 0px !important;
        min-width: 0px !important;
        max-width: 0px !important;
        transform: translateX(-260px) !important;
    }}

    /* Lock sidebar width to 260px */
    [data-testid="stSidebarResizeHandle"] {{
        display: none !important;
    }}

    /* Sidebar top header bar */
    [data-testid="stSidebarHeader"] {{
        padding: 0.65rem 0.65rem 0.25rem 0.65rem !important;
        margin-bottom: 0.15rem !important;
        height: 3rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
    }}
    [data-testid="stSidebarCollapseButton"] {{
        visibility: visible !important;
        opacity: 1 !important;
        display: inline-flex !important;
    }}

    /* Replace default << / >> arrows with clean Sidebar Panel SVG icon */
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stExpandSidebarButton"] {{
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        padding: 0 !important;
        border-radius: 8px !important;
        border: none !important;
        background-color: transparent !important;
        background-image: url("{SIDEBAR_PANEL_ICON_URI}") !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-size: 20px 20px !important;
        transition: background-color 0.15s ease !important;
    }}
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stExpandSidebarButton"]:hover {{
        background-color: rgba(0, 0, 0, 0.06) !important;
    }}
    [data-testid="stSidebarCollapseButton"] button > *,
    [data-testid="stExpandSidebarButton"] > * {{
        display: none !important;
    }}

    /* Sidebar inner alignment — strictly left-aligned buttons & labels */
    [data-testid="stSidebarContent"] {{
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
    }}
    [data-testid="stSidebarUserContent"] {{
        padding-top: 0.1rem !important;
    }}
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stDownloadButton > button,
    section[data-testid="stSidebar"] button[data-testid="stPopoverButton"] {{
        background-color: transparent !important;
        color: #0d0d0d !important;
        border: none !important;
        border-radius: 0.5rem !important;
        box-shadow: none !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        text-align: left !important;
        width: 100% !important;
        padding: 0.5rem 0.65rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        min-height: 2.4rem !important;
        transition: background-color 0.12s ease !important;
    }}
    section[data-testid="stSidebar"] .stButton > button > div,
    section[data-testid="stSidebar"] .stDownloadButton > button > div,
    section[data-testid="stSidebar"] button[data-testid="stPopoverButton"] > div {{
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        text-align: left !important;
        width: 100% !important;
        margin: 0 !important;
    }}
    section[data-testid="stSidebar"] .stButton > button p,
    section[data-testid="stSidebar"] .stDownloadButton > button p,
    section[data-testid="stSidebar"] button[data-testid="stPopoverButton"] p {{
        text-align: left !important;
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        color: #0d0d0d !important;
        margin: 0 !important;
    }}
    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stDownloadButton > button:hover,
    section[data-testid="stSidebar"] button[data-testid="stPopoverButton"]:hover {{
        background-color: rgba(0, 0, 0, 0.06) !important;
    }}

    /* Sidebar section label ("Hôm nay") */
    .sidebar-section-label {{
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #676767;
        padding: 0.9rem 0.65rem 0.35rem 0.65rem;
        letter-spacing: 0.01em;
    }}
    .sidebar-empty-note {{
        font-family: 'Inter', sans-serif;
        font-size: 0.8125rem;
        color: #8e8e8e;
        padding: 0.25rem 0.65rem;
    }}

    /* Active conversation pill in sidebar */
    .sidebar-active-chat {{
        background-color: rgba(0, 0, 0, 0.06);
        border-radius: 0.5rem;
        padding: 0.5rem 0.65rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: #0d0d0d;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 0.15rem;
    }}

    /* =========================================================================
       EMPTY STATE ("Tôi có thể giúp gì cho bạn?") & 2-LINE STARTER CARDS
       ========================================================================= */
    .chatgpt-empty-hero {{
        text-align: center;
        margin-top: 17vh;
        margin-bottom: 2.25rem;
    }}
    .chatgpt-empty-hero h1 {{
        font-family: 'Inter', sans-serif !important;
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        color: #0d0d0d !important;
        letter-spacing: -0.025em !important;
        margin: 0 !important;
    }}

    /* Starter prompt cards: strictly uniform height & alignment across all 4 cards */
    div[data-testid="stMainBlockContainer"] div[data-testid="stHorizontalBlock"] .stButton > button {{
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 0, 0, 0.09) !important;
        border-radius: 0.9rem !important;
        padding: 0.9rem 1.15rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        align-items: center !important;
        height: 4.9rem !important;
        min-height: 4.9rem !important;
        max-height: 4.9rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        transition: background-color 0.15s ease, border-color 0.15s ease !important;
    }}
    div[data-testid="stMainBlockContainer"] div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
        background-color: #f9f9f9 !important;
        border-color: rgba(0, 0, 0, 0.15) !important;
    }}
    div[data-testid="stMainBlockContainer"] div[data-testid="stHorizontalBlock"] .stButton > button > div {{
        width: 100% !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
    }}
    div[data-testid="stMainBlockContainer"] div[data-testid="stHorizontalBlock"] .stButton > button [data-testid="stMarkdownContainer"] {{
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        justify-content: center !important;
        text-align: left !important;
        width: 100% !important;
        gap: 0.22rem !important;
        white-space: normal !important;
    }}
    div[data-testid="stMainBlockContainer"] div[data-testid="stHorizontalBlock"] .stButton > button [data-testid="stMarkdownContainer"] p {{
        margin: 0 !important;
        white-space: normal !important;
        overflow: hidden !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 2 !important;
        -webkit-box-orient: vertical !important;
        line-height: 1.35 !important;
    }}
    div[data-testid="stMainBlockContainer"] div[data-testid="stHorizontalBlock"] .stButton > button [data-testid="stMarkdownContainer"] p:first-child {{
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #0d0d0d !important;
        -webkit-line-clamp: 1 !important;
    }}
    div[data-testid="stMainBlockContainer"] div[data-testid="stHorizontalBlock"] .stButton > button [data-testid="stMarkdownContainer"] p:last-child {{
        font-size: 0.8125rem !important;
        font-weight: 400 !important;
        color: #676767 !important;
    }}

    /* =========================================================================
       CHAT MESSAGES (Right-aligned #f4f4f4 User Pill & Clean Assistant Message)
       ========================================================================= */
    [data-testid="stChatMessage"] {{
        padding: 0.85rem 0 !important;
        background: transparent !important;
        border: none !important;
        gap: 0.9rem !important;
    }}

    /* User message: right-aligned rounded #f4f4f4 pill, no avatar */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        flex-direction: row-reverse !important;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageAvatarUser"] {{
        display: none !important;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {{
        background-color: #f4f4f4 !important;
        color: #0d0d0d !important;
        padding: 0.7rem 1.15rem !important;
        border-radius: 1.5rem !important;
        max-width: 75% !important;
        margin-left: auto !important;
        flex-grow: 0 !important;
        width: fit-content !important;
    }}

    /* Assistant avatar: clean neutral circle with dark icon */
    [data-testid="stChatMessageAvatarCustom"],
    [data-testid="stChatMessageAvatarAssistant"] {{
        background-color: #f4f4f4 !important;
        color: #0d0d0d !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 50% !important;
        width: 28px !important;
        height: 28px !important;
    }}

    /* Minimal tool trace expander */
    [data-testid="stChatMessage"] [data-testid="stExpander"] {{
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        margin-bottom: 0.35rem !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stExpander"] details {{
        border: none !important;
        background: transparent !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stExpander"] summary {{
        padding: 0.2rem 0 !important;
        color: #676767 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }}
    [data-testid="stChatMessage"] [data-testid="stExpander"] summary:hover {{
        color: #0d0d0d !important;
    }}

    /* =========================================================================
       BOTTOM COMPOSER + INTEGRATED RIGHT-SIDE MODEL SELECTOR PILL
       ========================================================================= */
    [data-testid="stBottom"] > div {{
        background: linear-gradient(180deg, rgba(255,255,255,0) 0%, #ffffff 35%) !important;
    }}
    [data-testid="stBottomBlockContainer"] {{
        max-width: 48rem !important;
        width: 100% !important;
        margin: 0 auto !important;
        padding: 0.25rem 1rem 1.15rem 1rem !important;
        position: relative !important;
    }}
    [data-testid="stBottomBlockContainer"] > [data-testid="stVerticalBlock"] {{
        position: relative !important;
        gap: 0 !important;
    }}

    /* Outer wrapper must stay transparent with NO border */
    [data-testid="stChatInput"] {{
        max-width: 48rem !important;
        width: 100% !important;
        margin: 0 auto !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }}
    /* Inner container is the single rounded #f4f4f4 composer box */
    [data-testid="stChatInput"] > div {{
        background-color: #f4f4f4 !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 1.75rem !important;
        padding: 0.45rem 0.6rem 0.45rem 1.15rem !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }}
    [data-testid="stChatInput"] > div:focus-within {{
        border-color: rgba(0, 0, 0, 0.18) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06) !important;
    }}
    /* Leave room on the right inside composer so typed text never collides with model selector pill */
    [data-testid="stChatInputTextArea"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        color: #0d0d0d !important;
        padding-right: 13.5rem !important;
    }}
    [data-testid="stChatInputSubmitButton"] {{
        background-color: #0d0d0d !important;
        color: #ffffff !important;
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        min-height: 32px !important;
    }}
    [data-testid="stChatInputSubmitButton"]:disabled {{
        background-color: #d7d7d7 !important;
        color: #f4f4f4 !important;
    }}

    /* Position the "Research Agent · model ▾" popover INSIDE the chat input pill (left of Send button) */
    [data-testid="stBottomBlockContainer"] [data-testid="stVerticalBlock"] > *:has([data-testid="stPopover"]) {{
        position: absolute !important;
        right: 3.35rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: auto !important;
        height: auto !important;
        z-index: 30 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    [data-testid="stBottomBlockContainer"] [data-testid="stPopover"],
    [data-testid="stBottomBlockContainer"] [data-testid="stPopover"] > div,
    [data-testid="stBottomBlockContainer"] [data-testid="stPopover"] > div > div {{
        width: auto !important;
        display: inline-flex !important;
        align-items: center !important;
    }}
    [data-testid="stBottomBlockContainer"] button[data-testid="stPopoverButton"] {{
        background-color: transparent !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.25rem 0.55rem !important;
        min-height: 2rem !important;
        height: 2rem !important;
        width: auto !important;
        color: #676767 !important;
        box-shadow: none !important;
        transition: background-color 0.15s ease, color 0.15s ease !important;
    }}
    [data-testid="stBottomBlockContainer"] button[data-testid="stPopoverButton"] p {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        color: inherit !important;
        margin: 0 !important;
        white-space: nowrap !important;
    }}
    [data-testid="stBottomBlockContainer"] button[data-testid="stPopoverButton"] [data-testid="stIconMaterial"] {{
        font-family: 'Material Symbols Rounded' !important;
        font-size: 1.1rem !important;
        color: inherit !important;
    }}
    [data-testid="stBottomBlockContainer"] button[data-testid="stPopoverButton"]:hover {{
        background-color: rgba(0, 0, 0, 0.05) !important;
        color: #0d0d0d !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

DEFAULT_MODELS = {
    "openrouter": "openai/gpt-4o-mini",
    "gemini": "gemini-3.5-flash-lite",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "ollama": "qwen2.5:7b",
}
PROVIDERS = list(DEFAULT_MODELS)

STARTER_PROMPTS = [
    (
        "Tin tức AI mới nhất",
        "Tổng hợp các diễn biến nổi bật hôm nay",
        "Tin tức AI hôm nay có gì nổi bật?",
    ),
    (
        "Theo dõi mạng xã hội",
        "Xem 5 bài đăng mới nhất từ Sam Altman",
        "Lấy 5 tweet mới nhất của Sam Altman",
    ),
    (
        "Trích xuất từ khóa",
        "Phân tích thuật ngữ cốt lõi từ văn bản",
        "Trích xuất 3 từ khóa quan trọng trong đoạn này: AI agents can help researchers organize papers. AI agents also support literature review.",
    ),
    (
        "Tìm bài báo khoa học",
        "Tra cứu nghiên cứu trên arXiv về RAG",
        "Tìm tối đa 3 bài báo khoa học trên arXiv về retrieval-augmented generation.",
    ),
]


def detect_default_provider() -> str:
    if os.environ.get("OPENROUTER_API_KEY"):
        return "openrouter"
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    return "openrouter"


def initialize_state() -> None:
    """Set defaults once; Streamlit reruns must not clear conversation state."""
    ss = st.session_state
    default_prov = detect_default_provider()
    defaults: dict[str, Any] = {
        "provider_choice": default_prov,
        "model_choice": DEFAULT_MODELS[default_prov],
        "last_provider_choice": default_prov,
        "agent_version": "v3",
        "history_window": 5,
        "max_rounds": 4,
        "history": [],
        "display_messages": [],
        "transcript": None,
        "transcript_path": None,
        "turn_in_progress": False,
        "queued_prompt": None,
        "saved_sessions": [],
        "active_session_idx": None,
    }
    for name, value in defaults.items():
        if name not in ss:
            ss[name] = value


def on_provider_change() -> None:
    """Switch to a sensible model for a newly selected provider, preserving chat."""
    ss = st.session_state
    provider = ss.provider_choice
    if provider != ss.last_provider_choice:
        ss.model_choice = DEFAULT_MODELS[provider]
        ss.last_provider_choice = provider


def _archive_current_session() -> None:
    """Save current non-empty conversation into saved_sessions list."""
    ss = st.session_state
    if not ss.display_messages:
        return
    first_user_msg = next(
        (m["content"] for m in ss.display_messages if m.get("role") == "user"),
        "Cuộc trò chuyện",
    )
    title = first_user_msg[:30] + ("…" if len(first_user_msg) > 30 else "")
    snapshot = {
        "title": title,
        "history": list(ss.history),
        "display_messages": list(ss.display_messages),
        "transcript": ss.transcript,
        "transcript_path": ss.transcript_path,
    }
    if ss.active_session_idx is not None and 0 <= ss.active_session_idx < len(ss.saved_sessions):
        ss.saved_sessions[ss.active_session_idx] = snapshot
    else:
        ss.saved_sessions.insert(0, snapshot)


def new_conversation() -> None:
    """Archive current chat (if any) and start a fresh conversation."""
    _archive_current_session()
    ss = st.session_state
    ss.history = []
    ss.display_messages = []
    ss.transcript = None
    ss.transcript_path = None
    ss.queued_prompt = None
    ss.active_session_idx = None


def load_saved_session(idx: int) -> None:
    """Switch to a previously saved session from the sidebar list."""
    _archive_current_session()
    ss = st.session_state
    if 0 <= idx < len(ss.saved_sessions):
        target = ss.saved_sessions[idx]
        ss.history = list(target["history"])
        ss.display_messages = list(target["display_messages"])
        ss.transcript = target["transcript"]
        ss.transcript_path = target["transcript_path"]
        ss.active_session_idx = idx


def new_transcript(version: str, provider: str, model: str, window: int, rounds: int) -> None:
    """Create a transcript after the first message to record actual settings."""
    prompt_file = ARTIFACTS / "system_prompt.md"
    tools_file = ARTIFACTS / "tools.yaml"
    build = build_artifact_version(version, prompt_file, tools_file)
    ident = "_".join(
        (
            safe_slug(version),
            safe_slug(provider),
            datetime.now().strftime("%Y%m%dT%H%M%S%f"),
        )
    )
    st.session_state.transcript_path = TRANSCRIPTS / f"{ident}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": ident,
        **artifact_version_dict(build),
        "provider": provider,
        "model": model or None,
        "system_prompt": str(prompt_file),
        "tools": str(tools_file),
        "history_window": window,
        "max_tool_rounds": rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


def download_transcript() -> bytes:
    """Use in-memory transcript to work on local and hosted deployments."""
    return json.dumps(
        st.session_state.transcript,
        ensure_ascii=False,
        indent=2,
        default=str,
    ).encode("utf-8")


def show_tool_events(events: list[dict[str, Any]]) -> None:
    if not events:
        return
    tool_names = ", ".join(e.get("tool", "unknown") for e in events)
    label = f"Đã tra cứu {len(events)} bước ({tool_names})"
    with st.expander(label, expanded=False, icon=":material/travel_explore:"):
        for i, item in enumerate(events, 1):
            st.markdown(f"**Bước {i} · `{item.get('tool', 'unknown')}`**")
            st.json({"arguments": item.get("args", {}), "result": item.get("result", {})})


def provider_key_status(provider: str) -> tuple[bool, str]:
    """Show only presence of keys, never their values."""
    env_names = {
        "gemini": "GEMINI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    key = env_names.get(provider)
    if key is None:
        return True, "Ollama local server (http://localhost:11434/v1)"
    return bool(os.environ.get(key)), f"Biến môi trường: {key}"


initialize_state()

provider_name = st.session_state.provider_choice
model_name = st.session_state.model_choice.strip() or DEFAULT_MODELS[provider_name]
version_label = st.session_state.agent_version.strip() or "v3"
short_model = model_name.split("/")[-1]

# ---------------- 1. Left Sidebar (Navigation & History) ----------------
with st.sidebar:
    if st.button(
        "Cuộc trò chuyện mới",
        icon=":material/edit_square:",
        use_container_width=True,
        key="sidebar_new_chat",
    ):
        new_conversation()
        st.rerun()

    st.markdown('<div class="sidebar-section-label">Hôm nay</div>', unsafe_allow_html=True)

    # Current active session indicator
    if st.session_state.display_messages and st.session_state.active_session_idx is None:
        first_q = next(
            (m["content"] for m in st.session_state.display_messages if m.get("role") == "user"),
            "Cuộc trò chuyện mới",
        )
        short_q = first_q[:28] + ("…" if len(first_q) > 28 else "")
        st.markdown(f'<div class="sidebar-active-chat">{short_q}</div>', unsafe_allow_html=True)
    elif not st.session_state.display_messages and not st.session_state.saved_sessions:
        st.markdown(
            '<div class="sidebar-empty-note">Chưa có cuộc trò chuyện nào.</div>',
            unsafe_allow_html=True,
        )

    # Saved sessions list in "Hôm nay"
    for idx, sess in enumerate(st.session_state.saved_sessions):
        is_current = st.session_state.active_session_idx == idx
        if is_current:
            st.markdown(
                f'<div class="sidebar-active-chat">{sess["title"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            if st.button(
                sess["title"],
                icon=":material/chat_bubble_outline:",
                key=f"saved_sess_{idx}",
                use_container_width=True,
            ):
                load_saved_session(idx)
                st.rerun()

    st.divider()

    # Sidebar Footer: Settings Popover & Transcript Download
    with st.popover("Tùy chỉnh tham số", icon=":material/tune:", use_container_width=True):
        st.text_input(
            "Phiên bản prompt/tools",
            key="agent_version",
            help="Nhãn phiên bản ghi vào transcript (mặc định: v3).",
        )
        st.slider("Số cặp chat giữ làm ngữ cảnh", 1, 10, key="history_window")
        st.slider("Số vòng gọi tool tối đa", 1, 8, key="max_rounds")
        st.caption("Tool `send` được khóa trên giao diện web để tránh gửi Telegram ngoài ý muốn.")

    turn_count = len(st.session_state.transcript["turns"]) if st.session_state.transcript else 0
    if turn_count:
        st.download_button(
            f"Xuất bản ghi ({turn_count} lượt)",
            data=download_transcript(),
            file_name=st.session_state.transcript_path.name,
            mime="application/json",
            icon=":material/download:",
            use_container_width=True,
        )

# ---------------- 2. Empty State ("Tôi có thể giúp gì cho bạn?") ----------------
if not st.session_state.display_messages:
    st.markdown(
        """
        <div class="chatgpt-empty-hero">
            <h1>Tôi có thể giúp gì cho bạn?</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    row1_col1, row1_col2 = st.columns(2, gap="small")
    row2_col1, row2_col2 = st.columns(2, gap="small")
    grid_cols = [row1_col1, row1_col2, row2_col1, row2_col2]
    for col, (title, subtitle, sample_prompt) in zip(grid_cols, STARTER_PROMPTS):
        with col:
            if st.button(
                f"{title}\n\n{subtitle}",
                key=f"starter_{title}",
                use_container_width=True,
                wrap=True,
            ):
                st.session_state.queued_prompt = sample_prompt
                st.rerun()

# ---------------- 3. Conversation Message Stream ----------------
for msg in st.session_state.display_messages:
    avatar = ":material/auto_awesome:" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        if msg["role"] == "assistant":
            show_tool_events(msg.get("tool_events", []))
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("provider"):
            st.caption(f"{version_label} · {msg['provider']} · {msg.get('model', '(mặc định)')}")

# ---------------- 4. Bottom Composer with Right-Side Model Selector Pill ----------------
with st.bottom:
    chat_bar_text = st.chat_input(
        "Hỏi bất kỳ điều gì...",
        disabled=st.session_state.turn_in_progress,
    )
    with st.popover(f"Research Agent · {short_model}"):
        st.selectbox(
            "Provider",
            PROVIDERS,
            key="provider_choice",
            on_change=on_provider_change,
            help="Đổi provider ngay trong cuộc hội thoại; lịch sử chat được giữ nguyên.",
        )
        st.text_input(
            "Model ID",
            key="model_choice",
            help="Nhập model ID của provider đang chọn.",
        )
        key_ok, key_hint = provider_key_status(st.session_state.provider_choice)
        if key_ok:
            st.caption(f"Trạng thái: Đã cấu hình ({key_hint}) · Phiên bản `{version_label}`")
        else:
            st.warning(f"Chưa tìm thấy API key ({key_hint}).")

user_text = chat_bar_text or st.session_state.queued_prompt
if st.session_state.queued_prompt:
    st.session_state.queued_prompt = None

if user_text and user_text.strip():
    user_text = user_text.strip()
    version = st.session_state.agent_version.strip() or "v3"
    window = st.session_state.history_window
    max_rounds = st.session_state.max_rounds
    provider_name = st.session_state.provider_choice
    model_name = st.session_state.model_choice.strip() or DEFAULT_MODELS[provider_name]

    if st.session_state.transcript is None:
        new_transcript(version, provider_name, model_name, window, max_rounds)

    st.session_state.display_messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    turn_record: dict[str, Any] = {
        "turn_index": len(st.session_state.transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "provider": provider_name,
        "model": model_name,
        "version": version,
        "history_window": window,
        "max_tool_rounds": max_rounds,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    st.session_state.turn_in_progress = True
    with st.chat_message("assistant", avatar=":material/auto_awesome:"):
        try:
            prompt = (ARTIFACTS / "system_prompt.md").read_text(encoding="utf-8")
            declared = load_tool_declarations(ARTIFACTS / "tools.yaml")
            safe_declarations = [item for item in declared if item["name"] != "send"]
            tools = to_openai_tools(safe_declarations)
            provider = make_provider(provider_name)
            messages = [
                {"role": "system", "content": prompt},
                *trim_history(st.session_state.history, window),
                {"role": "user", "content": user_text},
            ]
            with st.spinner("Đang suy nghĩ..."):
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=tools,
                    model=model_name,
                    max_tool_rounds=max_rounds,
                )
            turn_record.update(result)
            events = result.get("tool_events", [])
            show_tool_events(events)
            answer = result.get("assistant_text") or "(Agent không trả về văn bản.)"
            st.markdown(answer)
            st.caption(f"{version} · {provider_name} · {model_name}")
            st.session_state.display_messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "provider": provider_name,
                    "model": model_name,
                    "tool_events": events,
                }
            )
            st.session_state.history.extend(
                [
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": answer},
                ]
            )
            if result.get("status") == "waiting_for_user":
                st.caption("Agent đang chờ bạn cung cấp thêm thông tin ở khung nhập bên dưới.")
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            for env_name in (
                "GEMINI_API_KEY",
                "OPENROUTER_API_KEY",
                "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY",
                "TAVILY_API_KEY",
                "FIRECRAWL_API_KEY",
                "RAPIDAPI_KEY",
            ):
                secret_value = os.environ.get(env_name)
                if secret_value:
                    message = message.replace(secret_value, "[REDACTED]")
            turn_record.update({"status": "provider_error", "error": message})
            st.error(f"Không thể chạy Agent: {message}")
            st.session_state.display_messages.append(
                {
                    "role": "assistant",
                    "content": f"Không thể chạy Agent: {message}",
                    "provider": provider_name,
                    "model": model_name,
                }
            )
        finally:
            st.session_state.turn_in_progress = False
            turn_record["ended_at"] = now_iso()
            st.session_state.transcript["turns"].append(turn_record)
            st.session_state.transcript["updated_at"] = now_iso()
            try:
                write_transcript(st.session_state.transcript_path, st.session_state.transcript)
            except OSError:
                pass
