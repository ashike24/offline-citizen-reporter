# Offline-First Citizen Reporter

Streamlit demo. Reports are queued while "offline"; on reconnect, Sarvam AI writes a safety advisory
in the reporter's language.

## Run locally
    pip install -r requirements.txt
    # put SARVAM_API_KEY=... in .env (no quotes)
    streamlit run app.py

## Deploy
share.streamlit.io, main file app.py, Secrets: SARVAM_API_KEY = "..."

Never commit your key. .env is git-ignored.