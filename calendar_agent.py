from langchain.agents import tool
from setup_google_calendar import view_events
from typing import List
from langchain.tools import BaseTool, StructuredTool, Tool
from calendar_api import CalendarAPI

calendar = CalendarAPI()

view_event_tool = Tool.from_function(
    func=calendar.view_events,
    name="View Calendar Events",
    description="View upcoming events from the calendar"
)

if __name__ == "__main__":
    print(view_event_tool.invoke({"input":"5"}))