from google.adk.agents.llm_agent import Agent
from typing import Dict
import datetime
import pytz

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor

# Tool: Get current time for a given city
def get_current_time(city: str) -> Dict[str, str]:
    """
    Returns the current time in a specified city using the pytz library.
    If the city is invalid, returns an error message.
    """
    try:
        # Convert user input to a valid timezone
        timezone = pytz.timezone(city)
        current_time = datetime.datetime.now(timezone)
        formatted_time = current_time.strftime("%I:%M %p")
        return {"status": "success", "city": city, "time": formatted_time}
    except Exception:
        return {"status": "error", "message": f"Could not find timezone for '{city}'."}

# Root agent definition
root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Tells the current time in a specified city.",
    instruction=(
        "You are a helpful assistant that tells the current time in cities. "
        "Use the 'get_current_time' tool for this purpose. "
        "If the user gives a city name like 'Paris' or 'Tokyo', "
        "convert it into a timezone string like 'Europe/Paris' or 'Asia/Tokyo'."
    ),
    tools=[get_current_time],
)

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
