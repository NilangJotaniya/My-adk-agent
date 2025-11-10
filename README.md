# 🌟 AI Agent with Google ADK — Day 1 (5-Day AI Agents Intensive)

This repository contains my work from **Day 1** of the *5-Day AI Agents Intensive* — a hands-on challenge to build intelligent agents using **Google’s Agent Development Kit (ADK)** and the **Gemini API**.

> ✅ Successfully created and ran a custom AI agent (`root_agent`) that tells the current time in any specified city.

---

## 🧩 Project Overview

### 🎯 Goal
Set up the Google ADK (Agent Development Kit) in Python and create a simple **“Time Agent”** that can respond with the current time for a given city using the Gemini model.

### ⚙️ Features
- Built with **Google ADK** and **Gemini 2.5 Flash**
- Implements a tool function `get_current_time`
- Accepts city/timezone names (e.g., `Europe/Paris`, `Asia/Kolkata`)
- Runs via command line (`adk run my_agent`) or via the ADK Web UI
- Clean `.env` integration for secure API key management

---

## 🧠 Tech Stack
| Component | Technology |
|------------|-------------|
| Agent Framework | Google ADK |
| Language | Python 3.9 + |
| Model | Gemini 2.5 Flash |
| Libraries | `pytz`, `requests`, `python-dotenv` |
| Interface | CLI + Web UI (`adk web`) |

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/my-adk-agent.git
cd my-adk-agent
