import os
import requests
from dotenv import load_dotenv

load_dotenv(encoding="utf-8-sig")
key = os.getenv("SARVAM_API_KEY", "").strip()
model = os.getenv("SARVAM_MODEL", "sarvam-105b-conversations")
if not key:
    raise SystemExit("SARVAM_API_KEY is empty. Put it in .env first.")

r = requests.post(
    "https://api.sarvam.ai/v1/chat/completions",
    headers={"api-subscription-key": key, "Content-Type": "application/json"},
    json={"model": model, "messages": [{"role": "user", "content": "Say hello in Hindi in one short sentence."}]},
    timeout=60,
)
print("HTTP", r.status_code)
print(r.text[:1500])