# my_agent/agent.py
# Complete agent.py for Day 1 + Day 2 (time tool + currency tools + calc specialist)

from typing import Dict, Optional
import datetime
import pytz
import requests

# ADK imports
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor

# ---------------------------
#  -- Utility / helper map --
# ---------------------------
# Small map for casual city names -> tz database names (extend as needed)
CITY_MAP = {
    "paris": "Europe/Paris",
    "kolkata": "Asia/Kolkata",
    "mumbai": "Asia/Kolkata",
    "new york": "America/New_York",
    "nyc": "America/New_York",
    "london": "Europe/London",
    "tokyo": "Asia/Tokyo",
    "los angeles": "America/Los_Angeles",
    "sf": "America/Los_Angeles",
    "san francisco": "America/Los_Angeles",
}

# ---------------------------
#  -- Day 1: Time tool --
# ---------------------------
def get_current_time(city: str) -> Dict[str, str]:
    """
    Return current time for a city. Accepts casual names (e.g. 'Paris')
    or tz strings (e.g. 'Europe/Paris'). Tries:
      1) CITY_MAP lookup (casual names)
      2) If input contains '/', treat as tz string and use pytz
      3) If tz known, try worldtimeapi (no API key) to get precise time with offset
      4) Fallback to pytz.now if available
    Returns:
      {"status":"success","city":..., "time":"HH:MM AM/PM"}
      or {"status":"error", "message": "..."}
    """
    if not city or not city.strip():
        return {"status": "error", "message": "No city provided."}
    name = city.strip()
    name_lower = name.lower()

    # 1) map casual names
    tz_name: Optional[str] = CITY_MAP.get(name_lower)

    # 2) if user already provided tz string format
    if not tz_name and "/" in name:
        tz_name = name

    # 3) If we have a tz name, try worldtimeapi first (better offset handling)
    if tz_name:
        try:
            # worldtimeapi returns ISO datetime with offset
            resp = requests.get(f"https://worldtimeapi.org/api/timezone/{tz_name}", timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                dt_iso = data.get("datetime")
                if dt_iso:
                    # Parse ISO timestamp safely
                    dt = datetime.datetime.fromisoformat(dt_iso)
                    return {"status": "success", "city": name, "time": dt.strftime("%I:%M %p")}
            # fallback to pytz if worldtimeapi fails
        except Exception:
            pass

        # fallback: use pytz
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.datetime.now(tz)
            return {"status": "success", "city": name, "time": now.strftime("%I:%M %p")}
        except Exception as e:
            return {"status": "error", "message": f"Could not determine time for '{name}' ({e})"}

    # 4) Nothing found
    return {"status": "error", "message": f"Unknown city or timezone '{name}'. Try 'Paris' or 'Europe/Paris'."}


# ---------------------------
#  -- Day 2: Business Tools --
# ---------------------------
def get_fee_for_payment_method(method: str) -> Dict[str, object]:
    """
    Simulated fee lookup.
    Returns:
      {"status":"success", "fee_percentage": 0.02}
      or {"status":"error", "error_message": "..."}
    """
    if not method:
        return {"status": "error", "error_message": "No payment method provided."}
    fee_database = {
        "platinum credit card": 0.02,  # 2%
        "gold debit card": 0.035,      # 3.5%
        "bank transfer": 0.01,         # 1%
    }
    fee = fee_database.get(method.lower())
    if fee is not None:
        return {"status": "success", "fee_percentage": fee}
    return {"status": "error", "error_message": f"Payment method '{method}' not found"}


def get_exchange_rate(base_currency: str, target_currency: str) -> Dict[str, object]:
    """
    Simulated exchange rate lookup.
    Returns:
      {"status":"success", "rate": 0.93}
      or {"status":"error", "error_message": "..."}
    """
    if not base_currency or not target_currency:
        return {"status": "error", "error_message": "Please provide base and target currencies."}

    rate_database = {
        "usd": {
            "eur": 0.93,
            "jpy": 157.50,
            "inr": 83.58,
        },
        # extend as needed
    }
    base = base_currency.lower()
    target = target_currency.lower()
    rate = rate_database.get(base, {}).get(target)
    if rate is not None:
        return {"status": "success", "rate": rate}
    return {"status": "error", "error_message": f"Unsupported currency pair: {base_currency}/{target_currency}"}


# ---------------------------
#  -- Calculation Agent (specialist) --
# ---------------------------
calculation_agent = LlmAgent(
    name="calculation_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You are a specialized calculator that ONLY responds with valid Python code inside a single "
        "code block. Do not provide prose. The code must `print()` the final numeric result and any "
        "intermediate values needed for a readable breakdown. You are forbidden from writing any "
        "explanations outside the code block."
    ),
    code_executor=BuiltInCodeExecutor(),
)


# ---------------------------
#  -- Enhanced Currency Agent (delegates math) --
# ---------------------------
enhanced_currency_agent = LlmAgent(
    name="enhanced_currency_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction=(
        "You are a precise currency conversion assistant. For any conversion request, strictly do the following:\n"
        "1) Call get_fee_for_payment_method(payment_method) to find the fee percentage.\n"
        "2) Call get_exchange_rate(base_currency, target_currency) to get the conversion rate.\n"
        "3) Do NOT perform arithmetic yourself. Instead, generate Python code that computes:\n"
        "   - fee amount in original currency\n"
        "   - amount after fee\n"
        "   - final converted amount\n"
        "   Then call the calculation agent (provided as a tool) to execute the code and return results.\n"
        "4) Present a clear breakdown: original amount, fee%, fee amount, amount after fee, exchange rate, and final result.\n"
        "5) If any tool returns an error status, stop and explain the error."
    ),
    tools=[get_fee_for_payment_method, get_exchange_rate, AgentTool(agent=calculation_agent)],
)

# ---------------------------
#  -- Root agent (exposes time + currency capabilities) --
# ---------------------------
# root agent combines: get_current_time tool + enhanced currency agent as an AgentTool
root_agent = LlmAgent(
    name="root_agent",
    model=Gemini(model="gemini-2.5-flash"),
    instruction=(
        "You are a multi-tool assistant. You can:\n"
        " - Tell the current time for cities/timezones using get_current_time(city).\n"
        " - Perform currency conversions using the enhanced currency agent tool. "
        "When users ask about money conversion, call the enhanced currency agent (it's available as a tool). "
        "When users ask about time, call the get_current_time function.\n"
        "Decide which tool to call based on the user's request and return helpful, structured responses."
    ),
    # Tools: function tools and the enhanced agent as a callable tool
    tools=[get_current_time, get_fee_for_payment_method, get_exchange_rate, AgentTool(agent=enhanced_currency_agent)],
)

# Note: ADK looks for a variable called `root_agent` as the entrypoint for the agent.
# This file defines `root_agent` as the multi-tool LlmAgent.
