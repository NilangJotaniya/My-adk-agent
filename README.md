# 🌟 ADK Multi-Tool Agent — Day 1 & Day 2 (5-Day AI Agents Intensive)

This repository demonstrates my Day-1 and Day-2 work from the *5-Day AI Agents Intensive*:
- Day 1: Quickstart with Google ADK + a Time Agent
- Day 2: Building and using **custom tools** and a **specialist calculation agent**

The project uses **Google ADK**, **Gemini** (Gemini API), and small custom tools to show how to extend LLMs into useful agents.

---

## 🔥 Live locally (what I have running)
- ADK Web UI running at `http://localhost:8000` (select `root_agent`)
- `root_agent` supports:
  - Time queries (`get_current_time`)
  - Currency conversions with accurate delegated calculations (via `enhanced_currency_agent`)

---

## 📁 Repo structure
```
my-adk-agent/
├─ my_agent/
│  ├─ agent.py                
│  └─ __init__.py
├─ screenshots/
│  ├─ day1-adk-ui.png         
│  └─ day2-currency-agent.png 
├─ .env.template
├─ requirements.txt
├─ .gitignore
├─ README.md
```

---

## ⚙️ Quickstart — run locally

1. Clone the repo:
```bash
git clone https://github.com/<NilangJotaniya>/<repo>.git
cd <repo>
```

2. Create & activate a virtual environment:
```bash
python -m venv venv
# Windows (PowerShell)
.env\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Add your Gemini API key (local only):
```text
# copy .env.template -> my_agent/.env and edit the value
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

5. Run ADK (CLI) or the Web UI:
```bash
# CLI
adk run my_agent

# Web UI (recommended)
adk web --port 8000
# Then open: http://localhost:8000 and select "root_agent"
```

---

## 🧠 What I built

### Day 1 — Time Agent
- `get_current_time(city)` (tool)
- Accepts timezone strings (`Europe/Paris`) and common city names (via a small mapping)
- Uses `worldtimeapi.org` as a fallback and `pytz` to format output

### Day 2 — Tools & Specialist Agent
- `get_fee_for_payment_method(method)` — function tool (mocked fee lookup)
- `get_exchange_rate(base, target)` — function tool (mocked rates)
- `calculation_agent` — specialist agent that **only** returns Python code and uses `BuiltInCodeExecutor` to run calculations reliably
- `enhanced_currency_agent` — delegates arithmetic to `calculation_agent` and provides a clear breakdown of conversions

All these are composed under a `root_agent` so a user can ask either time or conversion questions in one place.

---

## 🧪 Example prompts to test

- `what time is it in Paris?`
- `what time is it in Asia/Kolkata?`
- `Convert 500 USD to EUR using my Platinum Credit Card.`
- `Convert 1250 USD to INR using a Bank Transfer. Show the calculation breakdown.`

---

## 📸 Proof / Screenshots

- **Day 1:** ADK Web UI — Time agent responding  
  `screenshots/day1-adk-ui.png`

- **Day 2:** ADK Web UI — Currency agent & calculation trace  
  `screenshots/day2-currency-agent.png`

(Displayed inline in this README.)

---

## 🛡 Security & Notes
- **Do not commit** `my_agent/.env` or any keys.
- If a secret is accidentally pushed, rotate it immediately from Google AI Studio.
- This repo uses mock data for currency rates and fees — replace with real APIs for production.

---

## 🚀 Next steps / Roadmap
- Expand `CITY_MAP` or use geocoding to accept casual city names (e.g., “Paris”) robustly
- Replace mock exchange rates with a live provider (e.g., exchangerate.host or another reliable API)
- Add automated tests and a GitHub Actions check for `pip install -r requirements.txt`
- Deploy a small frontend demo that calls `adk` endpoints (if you decide to expose via a backend)

---

## ✍️ Author
**Nilang Jotaniya**  
GitHub: https://github.com/NilangJotaniya
LinkedIn: https://www.linkedin.com/in/NilangJotaniya

---

## 📄 License
MIT — see `LICENSE` (optional).
