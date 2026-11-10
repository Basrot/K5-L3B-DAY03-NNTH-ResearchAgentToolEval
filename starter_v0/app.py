"""VinUni Lab 03 — Streamlit UI for the existing multi-round Research Agent.

Run from starter_v0: python -m streamlit run app.py
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from chat import (
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
TRANSCRIPTS = ROOT / "transcripts"
load_lab_env(ROOT)

st.set_page_config(page_title="Research Agent | VinUni Lab 03", page_icon="🔎", layout="wide")


def start_session(provider_name: str, version: str, model_name: str, history_window: int, max_rounds: int):
    prompt_file = ARTIFACTS / "system_prompt.md"
    tools_file = ARTIFACTS / "tools.yaml"
    build = build_artifact_version(version, prompt_file, tools_file)
    ident = "_".join((safe_slug(version), safe_slug(provider_name), datetime.now().strftime("%Y%m%dT%H%M%S%f")))
    st.session_state.transcript_path = TRANSCRIPTS / f"{ident}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": ident,
        **artifact_version_dict(build),
        "provider": provider_name,
        "model": model_name or None,
        "system_prompt": str(prompt_file),
        "tools": str(tools_file),
        "history_window": history_window,
        "max_tool_rounds": max_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    st.session_state.history = []
    st.session_state.display_messages = []
    st.session_state.session_settings = (provider_name, version, model_name, history_window, max_rounds)


with st.sidebar:
    st.title("🔎 Research Agent")
    st.caption("VinUni AI20K · Day 03 · Tool Calling")
    provider_name = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini", "ollama"])
    version = st.text_input("Phiên bản", value="v0", help="Chọn đúng phiên bản prompt/tools đang sử dụng")
    model_name = st.text_input("Model (để trống dùng mặc định)", value="")
    history_window = st.slider("Số cặp chat giữ làm ngữ cảnh", 1, 10, 5)
    max_rounds = st.slider("Số vòng gọi tool tối đa", 1, 8, 4)
    st.caption("Dùng cùng backend với chat.py; tool calls và transcript đều là kết quả thực.")
    st.info("Tool `send` bị ẩn trong UI để tránh gửi Telegram ngoài ý muốn. Dùng chat.py và bước xác nhận riêng để kiểm thử tác vụ gửi.")
    if st.button("🗑️ Hội thoại mới", use_container_width=True):
        start_session(provider_name, version, model_name, history_window, max_rounds)
        st.rerun()

current_settings = (provider_name, version, model_name, history_window, max_rounds)
if "transcript" not in st.session_state:
    start_session(*current_settings)

st.title("AI Research Agent")
st.caption("Tìm kiếm, nghiên cứu và quan sát cách AI gọi công cụ")
if st.session_state.session_settings != current_settings:
    st.warning("Các cài đặt ở thanh bên đã thay đổi. Bấm **Hội thoại mới** để áp dụng. Cuộc chat hiện tại vẫn giữ cấu hình cũ.")

for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("tool_events"):
            with st.expander(f"🔧 Chi tiết {len(msg['tool_events'])} lượt thực thi tool"):
                for item in msg["tool_events"]:
                    st.markdown(f"**{item.get('tool', 'unknown')}**")
                    st.json({"arguments": item.get("args", {}), "result": item.get("result", {})})

user_text = st.chat_input("Nhập câu hỏi nghiên cứu...")
if user_text and user_text.strip():
    user_text = user_text.strip()
    active_provider, active_version, active_model, active_window, active_rounds = st.session_state.session_settings
    st.session_state.display_messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    turn_record = {
        "turn_index": len(st.session_state.transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    with st.chat_message("assistant"):
        try:
            prompt = (ARTIFACTS / "system_prompt.md").read_text(encoding="utf-8")
            declared = load_tool_declarations(ARTIFACTS / "tools.yaml")
            # A UI chat message is never authorization to publish to Telegram.
            safe_declarations = [tool for tool in declared if tool["name"] != "send"]
            tools = to_openai_tools(safe_declarations)
            provider = make_provider(active_provider)
            messages = [
                {"role": "system", "content": prompt},
                *trim_history(st.session_state.history, active_window),
                {"role": "user", "content": user_text},
            ]
            with st.spinner("Agent đang suy nghĩ và gọi công cụ..."):
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=tools,
                    model=active_model or None,
                    max_tool_rounds=active_rounds,
                )
            turn_record.update(result)
            answer = result.get("assistant_text") or "(Agent không trả về văn bản.)"
            st.markdown(answer)
            events = result.get("tool_events", [])
            if events:
                with st.expander(f"🔧 Chi tiết {len(events)} lượt thực thi tool"):
                    for item in events:
                        st.markdown(f"**{item.get('tool', 'unknown')}**")
                        st.json({"arguments": item.get("args", {}), "result": item.get("result", {})})
            st.session_state.display_messages.append({"role": "assistant", "content": answer, "tool_events": events})
            st.session_state.history.extend([
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": answer},
            ])
            if result.get("status") == "waiting_for_user":
                st.info("Agent đang chờ bạn bổ sung thông tin trong ô chat.")
        except Exception as exc:
            turn_record.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
            st.error(f"Không thể chạy Agent: {type(exc).__name__}: {exc}")
    turn_record["ended_at"] = now_iso()
    st.session_state.transcript["turns"].append(turn_record)
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)

with st.sidebar:
    st.divider()
    st.caption(f"Đã ghi {len(st.session_state.transcript['turns'])} lượt vào transcript JSON.")
    if st.session_state.transcript["turns"]:
        st.download_button(
            "⬇️ Tải transcript JSON",
            data=st.session_state.transcript_path.read_bytes(),
            file_name=st.session_state.transcript_path.name,
            mime="application/json",
            use_container_width=True,
        )
