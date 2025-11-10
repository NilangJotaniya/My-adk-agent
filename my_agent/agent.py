from google.adk.agents.llm_agent import Agent
from typing import Dict
import datetime
import pytz

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

