# 🔮 DVYRA // UNIVERSAL LLM GATEWAY

**DVYRA** is a high-performance, unified API Gateway that aggregates multiple AI providers (Google Gemini, Groq/Llama, DeepSeek, OpenAI) under a **Single Master API Key**. 

It features an "Unkillable" routing system with smart fallbacks (e.g., if Gemini fails, it auto-switches to Llama 70B) and a futuristic, glassmorphism-styled Command Center UI.

---

## ⚡ Key Features

* **🛡️ One Key to Rule Them All:** Use a single `sk-master-key` to access 10+ models.
* **🔄 Unkillable Fallbacks:** Automatically reroutes traffic if a provider hits Rate Limits (429) or goes down.
    * *Route:* `Gemini Flash` → `Llama 3 70B` → `DeepSeek V3`.
* **🖥️ Cyberpunk Command Center:** A stunning Streamlit UI with:
    * Real-time Latency Monitoring.
    * Live Terminal Logs (simulating handshake & data packets).
    * Toast Notifications & Token Usage tracking.
* **🔐 Enterprise Security:** All keys managed via `.env`; no hardcoded secrets.
* **🔔 Slack/Discord Alerts:** Real-time webhooks trigger when a fallback event occurs.

---

## 📂 Project Structure

```text
DVYRA/
├── config.yaml               # 🧠 Brain: Defines models & fallback logic
├── main.py                   # ⚙️ Core: The LiteLLM Proxy Server
├── ui.py                     # 🎨 Frontend: The Streamlit Command Center
├── error_alert_callback.py   # 🚨 Alerting: Handles Slack/Discord webhooks
├── testslack.py              # 🧪 Test: Script to verify webhook connections
├── .env                      # 🔐 Secrets: API Keys (Not uploaded to GitHub)
├── Dockerfile                # 🐳 Deploy: Docker configuration
└── requirements.txt          # 📦 Deps: Python dependencies