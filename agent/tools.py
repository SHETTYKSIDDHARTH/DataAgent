# agent/tools.py

import re
from typing import Dict, Any

from db.schema_introspection import get_database_schema
from services.query_service import ReadOnlyQueryService


# ================================
# Tool 1: Get Database Schema
# ================================

def get_schema_tool() -> Dict[str, Any]:
    """
    Returns the database schema using automatic introspection.
    Works for SQLite (POC) and Snowflake (production).
    """
    return get_database_schema()


# ================================
# Tool 2: Validate SQL
# ================================

FORBIDDEN_KEYWORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "merge",
    "grant",
    "revoke"
]

def validate_sql_tool(sql: str) -> Dict[str, Any]:
    """
    Validates SQL query for safety.
    Enforces SELECT-only queries.
    """

    if not sql or not isinstance(sql, str):
        return {
            "valid": False,
            "reason": "SQL must be a non-empty string"
        }

    sql_clean = sql.strip().lower()

    # Must start with SELECT
    if not sql_clean.startswith("select"):
        return {
            "valid": False,
            "reason": "Only SELECT queries are allowed"
        }

    # Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_clean):
            return {
                "valid": False,
                "reason": f"Forbidden SQL keyword detected: {keyword}"
            }

    return {
        "valid": True
    }


# ================================
# Tool 3: Run SQL (Read-only)
# ================================

def run_sql_tool(sql: str) -> Dict[str, Any]:
    """
    Executes a validated SQL query in read-only mode.
    """

    validation = validate_sql_tool(sql)
    if not validation["valid"]:
        raise PermissionError(
            f"SQL validation failed: {validation['reason']}"
        )

    return ReadOnlyQueryService.execute(sql)
