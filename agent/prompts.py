# agent/prompts.py

INTENT_PROMPT = """
You are a classifier.

Classify the user's question into ONE of the following:

- DATA_QUERY: requires querying the database
- META_QUERY: asks about what the system can or cannot do
- OUT_OF_SCOPE: unrelated to the database

Respond with ONLY one of these labels.

Question:
{question}
"""


SQL_GENERATION_PROMPT = """
You are a senior data analyst.

Generate a SINGLE SQLite-compatible SELECT query.

Rules:
- Only SELECT queries
- Use only tables and columns from the schema
- Use explicit JOINs
- Do NOT explain anything
- Output ONLY SQL

Schema:
{schema}

Question:
{question}
"""

ANSWER_PROMPT = """
You are a data analyst.

Given the question and query result, produce a concise business answer.

Question:
{question}

Result:
{result}
"""
