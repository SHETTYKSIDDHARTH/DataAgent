# agent/graph.py

import re
from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.llm import llm
from agent.prompts import SQL_GENERATION_PROMPT, INTENT_PROMPT
from agent.tools import (
    get_schema_tool,
    validate_sql_tool,
    run_sql_tool,
)

# =========================
# Intent Classification
# =========================

def classify_intent(state: AgentState) -> AgentState:
    prompt = INTENT_PROMPT.format(question=state["question"])
    response = llm.invoke(prompt)

    intent = str(response.content).strip().upper()

    # Defensive normalization
    if intent not in {"DATA_QUERY", "META_QUERY", "OUT_OF_SCOPE"}:
        intent = "OUT_OF_SCOPE"

    state["intent"] = intent

    print(f"\n[INTENT] Classified intent → {intent}")
    return state


def handle_non_data(state: AgentState) -> AgentState:
    state["answer"] = (
        "I can answer questions about customers, orders, revenue, and products. "
        "Please ask a data-related question."
    )
    return state


def intent_router(state: AgentState):
    if state["intent"] == "DATA_QUERY":
        return "get_schema"
    return "handle_non_data"


# =========================
# Data Flow Nodes
# =========================

def get_schema(state: AgentState) -> AgentState:
    state["schema"] = get_schema_tool()
    return state


def generate_sql(state: AgentState) -> AgentState:
    prompt = SQL_GENERATION_PROMPT.format(
        schema=state["schema"],
        question=state["question"],
    )

    response = llm.invoke(prompt)

    raw_sql = str(response.content)

    print("\n[LLM RAW OUTPUT]")
    print(raw_sql)

    # -----------------------------
    # SQL SANITIZATION
    # -----------------------------

    # Remove markdown fences
    cleaned = re.sub(r"```sql|```", "", raw_sql, flags=re.IGNORECASE).strip()

    # Extract first SELECT statement
    match = re.search(
        r"(select[\s\S]*?)(?:;|$)",
        cleaned,
        flags=re.IGNORECASE,
    )

    final_sql = match.group(1).strip() if match else cleaned

    state["sql"] = final_sql

    print("\n[SANITIZED SQL]")
    print(final_sql)

    return state


def validate_sql(state: AgentState) -> AgentState:
    validation = validate_sql_tool(state["sql"])
    state["validation"] = validation

    print("\n[SQL VALIDATION]")
    print(validation)

    return state


def run_sql(state: AgentState) -> AgentState:
    try:
        print("\n[EXECUTING SQL]")
        print(state["sql"])

        state["result"] = run_sql_tool(state["sql"])

    except Exception as e:
        state["result"] = None
        state["error"] = str(e)

    return state


def generate_answer(state: AgentState) -> AgentState:
    """
    Deterministic answer generation (NO LLM dependency)
    """

    if state.get("error"):
        state["answer"] = f"Error while executing query: {state['error']}"
        return state

    result = state.get("result")

    if not result or not result.get("rows"):
        state["answer"] = "No data found."
        return state

    columns = result["columns"]
    rows = result["rows"]

    lines = []
    for row in rows:
        line = ", ".join(
            f"{col}: {val}" for col, val in zip(columns, row)
        )
        lines.append(line)

    state["answer"] = "\n".join(lines)
    return state


# =========================
# Build Graph
# =========================

def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("handle_non_data", handle_non_data)
    graph.add_node("get_schema", get_schema)
    graph.add_node("generate_sql", generate_sql)
    graph.add_node("validate_sql", validate_sql)
    graph.add_node("run_sql", run_sql)
    graph.add_node("generate_answer", generate_answer)

    # Entry
    graph.set_entry_point("classify_intent")

    # Intent routing
    graph.add_conditional_edges(
        "classify_intent",
        intent_router,
        {
            "get_schema": "get_schema",
            "handle_non_data": "handle_non_data",
        },
    )

    # Data path
    graph.add_edge("get_schema", "generate_sql")
    graph.add_edge("generate_sql", "validate_sql")
    graph.add_edge("validate_sql", "run_sql")
    graph.add_edge("run_sql", "generate_answer")
    graph.add_edge("generate_answer", END)

    # Meta path
    graph.add_edge("handle_non_data", END)

    return graph.compile()
