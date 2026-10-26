@'
# Offline-First Citizen Reporter

**Live demo:** https://offline-citizen-reporter-izl8dfbtjd5iqushsatgcm.streamlit.app

File hazard reports (floods, waterlogging, etc.) with no signal. Reports are saved on the device and queued. When connectivity returns, the app syncs them and generates a **safety advisory in the reporter's own language** using Sarvam AI.

## The problem
During floods and other local hazards, mobile networks are often the first thing to fail, and the people who most need safety guidance get it in a language they may not read comfortably. Reports and advice both break down exactly when they matter most.

## How it works
1. **Report offline.** Pick the hazard, add a location/landmark and a short description, and choose an advisory language.
2. **Queue on device.** The report is stored locally and shown in the queue (`[QUEUED]`).
3. **Reconnect and sync.** When the connection is back, the queued reports are sent to Sarvam AI (`sarvam-105b-conversations`).
4. **Get an advisory.** A short, practical safety advisory is generated in the chosen language and attached to the report.

## Features
- Offline queue that holds multiple reports
- Multilingual advisories (Hindi and other Indian languages)
- Simulated offline/online toggle so the flow can be demoed anywhere
- Clean model output (reasoning `<think>` blocks are stripped)
- API key kept in secrets, never in the repo

## Tech stack
Python, Streamlit, Sarvam AI API, Streamlit Community Cloud

## Run locally
```bash
pip install -r requirements.txt
# create a .env file containing: SARVAM_API_KEY=your_key (no quotes)
streamlit run app.py
```

## Deploy
On share.streamlit.io, set the main file to `app.py` and add this under Settings > Secrets:
```toml
SARVAM_API_KEY = "your_key"
```
Never commit your key. `.env` is git-ignored.

## Notes and limitations
- Offline mode is **simulated** with a toggle for demo purposes. A production version would use a PWA or mobile app with local storage and background sync.
- The queue resets when the Streamlit Cloud app restarts.

## Roadmap
- Voice advisories with Sarvam text-to-speech
- Photo attachments and GPS location
- Real offline storage with background sync
- Authority dashboard to view synced reports
'@ | Set-Content -Encoding utf8 README.md
git add README.md
git commit -m "Improve README"
git push
