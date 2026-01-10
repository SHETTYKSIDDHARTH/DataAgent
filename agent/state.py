# agent/state.py
from typing import TypedDict, Optional, Any, Dict, List

class AgentState(TypedDict):
    question: str
    intent: Optional[str]

    schema: Optional[Dict[str, Any]]
    sql: Optional[str]
    validation: Optional[Dict[str, Any]]
    result: Optional[Dict[str, Any]]

    answer: Optional[str]
    error: Optional[str]
