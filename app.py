import json
import os
import re
import time
import uuid
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv(encoding="utf-8-sig")

API_URL = "https://api.sarvam.ai/v1/chat/completions"
MODEL = os.getenv("SARVAM_MODEL", "sarvam-105b-conversations")
QUEUE_FILE = Path("queue.json")
LANGUAGES = ["Hindi", "Bengali", "Tamil", "Telugu", "Marathi", "Gujarati",
             "Kannada", "Malayalam", "Punjabi", "Odia", "English"]
CATEGORIES = ["Flood / water logging", "Fire", "Road accident", "Broken power line",
              "Health emergency", "Building damage", "Other hazard"]


def get_key():
    key = os.getenv("SARVAM_API_KEY", "").strip()
    if not key:
        try:
            key = str(st.secrets["SARVAM_API_KEY"]).strip()
        except Exception:
            key = ""
    return key


def load_queue():
    if QUEUE_FILE.exists():
        try:
            return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_queue(q):
    try:
        QUEUE_FILE.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def make_advisory(report, key):
    prompt = (
        "You are an emergency safety assistant for citizens in India. A citizen filed this hazard report "
        "while offline. Write a short, calm safety advisory (max 6 bullet points) for the reporter and "
        "people nearby, then one line on which local authority to contact. "
        f"Reply ONLY in {report['language']}.\n\n"
        f"Category: {report['category']}\n"
        f"Location: {report['location']}\n"
        f"Details: {report['description']}\n"
        f"Reported at: {report['created']}"
    )
    r = requests.post(
        API_URL,
        headers={"api-subscription-key": key, "Content-Type": "application/json"},
        json={"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3},
        timeout=90,
    )
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
    text = r.json()["choices"][0]["message"]["content"] or ""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
    return text


st.set_page_config(page_title="Offline-First Citizen Reporter", page_icon="!", layout="centered")

if "queue" not in st.session_state:
    st.session_state.queue = load_queue()

st.title("Offline-First Citizen Reporter")
st.caption("File hazard reports with no signal. They queue on the device and sync when you reconnect, "
           "with a safety advisory in your language.")

offline = st.toggle("Device is offline (simulated)", value=True)
st.write("Status: " + ("OFFLINE - reports will be queued" if offline else "ONLINE - you can sync the queue"))

st.subheader("New report")
with st.form("report", clear_on_submit=True):
    category = st.selectbox("What happened?", CATEGORIES)
    location = st.text_input("Location / landmark")
    description = st.text_area("Describe the situation")
    language = st.selectbox("Advisory language", LANGUAGES)
    submitted = st.form_submit_button("Queue report")

if submitted:
    if not location.strip() or not description.strip():
        st.error("Please fill in location and description.")
    else:
        st.session_state.queue.append({
            "id": uuid.uuid4().hex[:8],
            "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "location": location.strip(),
            "description": description.strip(),
            "language": language,
            "status": "queued",
            "advisory": "",
        })
        save_queue(st.session_state.queue)
        st.success("Saved on device. It will sync when you reconnect.")

queued = [r for r in st.session_state.queue if r["status"] == "queued"]
st.subheader(f"Queue ({len(queued)} waiting)")

if st.button("Reconnect and sync", disabled=offline or not queued, type="primary"):
    key = get_key()
    if not key:
        st.error("SARVAM_API_KEY is missing. Add it to .env (local) or Streamlit Secrets (cloud).")
    else:
        for rep in queued:
            with st.spinner(f"Syncing report {rep['id']}..."):
                try:
                    rep["advisory"] = make_advisory(rep, key)
                    rep["status"] = "synced"
                except Exception as e:
                    rep["status"] = "queued"
                    st.error(f"Report {rep['id']} failed: {e}")
        save_queue(st.session_state.queue)
        st.rerun()

for rep in reversed(st.session_state.queue):
    label = f"[{rep['status'].upper()}] {rep['category']} - {rep['location']} ({rep['created']})"
    with st.expander(label, expanded=(rep["status"] == "synced")):
        st.write(rep["description"])
        st.caption(f"Language: {rep['language']}  |  ID: {rep['id']}")
        if rep["advisory"]:
            st.markdown("**Safety advisory**")
            st.markdown(rep["advisory"])

if st.session_state.queue and st.button("Clear all reports"):
    st.session_state.queue = []
    save_queue([])
    st.rerun()