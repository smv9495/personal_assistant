from langchain.agents import tool
from setup_google_calendar import view_events
from typing import List
from langchain_core.tools import StructuredTool

@tool
def view_events_tool() -> List[str]:
    """
    List the upcoming events in the calendar
    """
    return view_events()

if __name__ == "__main__":
    print(view_events_tool.invoke({"input":""}))