"""VinUni Lab 03 — Streamlit Research Agent UI.

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

st.set_page_config(
    page_title="Research Agent | VinUni Lab 03",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_PROVIDER = "gemini"
DEFAULT_MODELS = {
    "gemini": "gemini-3.5-flash-lite",
    "openrouter": "openrouter/auto",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "ollama": "llama3.1",
}
MODEL_SUGGESTIONS = {
    "gemini": ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"],
    "openrouter": ["openrouter/auto"],
    "openai": ["gpt-4o-mini"],
    "anthropic": ["claude-3-5-haiku-latest"],
    "ollama": ["llama3.1", "qwen2.5"],
}
PROVIDERS = list(DEFAULT_MODELS)


def initialize_state() -> None:
    """Set defaults once; Streamlit reruns must not clear conversation state."""
    ss = st.session_state
    defaults: dict[str, Any] = {
        "provider_choice": DEFAULT_PROVIDER,
        "model_choice": DEFAULT_MODELS[DEFAULT_PROVIDER],
        "last_provider_choice": DEFAULT_PROVIDER,
        "agent_version": "v0",
        "history_window": 5,
        "max_rounds": 4,
        "history": [],
        "display_messages": [],
        "transcript": None,
        "transcript_path": None,
        "turn_in_progress": False,
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


def new_conversation() -> None:
    """Only this explicit action resets conversation and transcript."""
    ss = st.session_state
    ss.history = []
    ss.display_messages = []
    ss.transcript = None
    ss.transcript_path = None


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
        "provider": provider,  # provider used for the first turn
        "model": model or None,  # model used for the first turn
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
    with st.expander(f"🔧 Chi tiết {len(events)} lượt thực thi tool", expanded=False):
        for i, item in enumerate(events, 1):
            st.markdown(f"**{i}. `{item.get('tool', 'unknown')}`**")
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
        return True, "Ollama cần máy chủ model có thể truy cập được."
    return bool(os.environ.get(key)), f"Biến môi trường: {key}"


initialize_state()

with st.sidebar:
    st.title("🔎 Research Agent")
    st.caption("VinUni AI20K · Day 03 · Tool Calling")
    st.text_input("Phiên bản prompt/tools", key="agent_version", help="Ví dụ: v0, v1, v2, v3. Đổi phiên bản áp dụng từ lượt chat tiếp theo.")
    st.slider("Số cặp chat giữ làm ngữ cảnh", 1, 10, key="history_window")
    st.slider("Số vòng gọi tool tối đa", 1, 8, key="max_rounds")
    if st.button("➕ Hội thoại mới", type="secondary", use_container_width=True):
        new_conversation()
        st.rerun()
    st.caption("Lịch sử không bị xóa khi bạn đổi provider/model. Chỉ nút Hội thoại mới mới xóa.")
    st.info("Tool `send` bị loại khỏi danh sách cho UI để tránh gửi Telegram ngoài ý muốn.")

st.title("AI Research Agent")
st.caption("Tìm kiếm, nghiên cứu và quan sát cách AI gọi công cụ")

# The controls are in the main conversation area, just above the chat input.
with st.container(border=True):
    col_provider, col_model = st.columns([1, 2], gap="medium")
    with col_provider:
        st.selectbox(
            "Provider",
            PROVIDERS,
            key="provider_choice",
            on_change=on_provider_change,
            help="Có thể đổi ngay khi đang chat; lịch sử được giữ nguyên.",
        )
    with col_model:
        st.text_input(
            "Model",
            key="model_choice",
            help="Nhập model ID của provider. Đổi provider sẽ tự đặt model mặc định phù hợp.",
        )
    provider_name = st.session_state.provider_choice
    model_name = st.session_state.model_choice.strip() or DEFAULT_MODELS[provider_name]
    key_ok, key_hint = provider_key_status(provider_name)
    if not key_ok:
        st.warning(f"Chưa thấy API key cho {provider_name}. {key_hint}. Cấu hình ở Streamlit Secrets.")
    elif provider_name == "ollama":
        st.caption(key_hint)
    else:
        st.caption(f"Đang chọn: **{provider_name}** · `{model_name}` · Có thể đổi ở lượt tiếp theo")

# This displays transcript turns (and tool details) after each Streamlit rerun.
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("provider"):
            st.caption(f"{msg['provider']} · {msg.get('model', '(mặc định)')}")
        show_tool_events(msg.get("tool_events", []))

user_text = st.chat_input("Nhập câu hỏi nghiên cứu...", disabled=st.session_state.turn_in_progress)
if user_text and user_text.strip():
    user_text = user_text.strip()
    version = st.session_state.agent_version.strip() or "v0"
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
    with st.chat_message("assistant"):
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
            with st.spinner("Agent đang suy nghĩ và gọi công cụ..."):
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=tools,
                    model=model_name,
                    max_tool_rounds=max_rounds,
                )
            turn_record.update(result)
            answer = result.get("assistant_text") or "(Agent không trả về văn bản.)"
            st.markdown(answer)
            st.caption(f"{provider_name} · {model_name}")
            events = result.get("tool_events", [])
            show_tool_events(events)
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
                st.info("Agent đang chờ bạn bổ sung thông tin trong ô chat.")
        except Exception as exc:
            # Avoid exposing secrets in the UI or exported transcript.
            message = f"{type(exc).__name__}: {exc}"
            for env_name in ("GEMINI_API_KEY", "OPENROUTER_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "TAVILY_API_KEY", "FIRECRAWL_API_KEY", "RAPIDAPI_KEY"):
                secret_value = os.environ.get(env_name)
                if secret_value:
                    message = message.replace(secret_value, "[REDACTED]")
            turn_record.update({"status": "provider_error", "error": message})
            st.error(f"Không thể chạy Agent: {message}")
            st.session_state.display_messages.append(
                {"role": "assistant", "content": f"⚠️ Không thể chạy Agent: {message}", "provider": provider_name, "model": model_name}
            )
        finally:
            st.session_state.turn_in_progress = False
            turn_record["ended_at"] = now_iso()
            st.session_state.transcript["turns"].append(turn_record)
            st.session_state.transcript["updated_at"] = now_iso()
            try:
                write_transcript(st.session_state.transcript_path, st.session_state.transcript)
            except OSError:
                # Some hosts have read-only / ephemeral disks. Download still works.
                pass

with st.sidebar:
    st.divider()
    count = len(st.session_state.transcript["turns"]) if st.session_state.transcript else 0
    st.caption(f"Đã ghi {count} lượt vào transcript JSON.")
    if count:
        st.download_button(
            "⬇️ Tải transcript JSON",
            data=download_transcript(),
            file_name=st.session_state.transcript_path.name,
            mime="application/json",
            use_container_width=True,
        )
