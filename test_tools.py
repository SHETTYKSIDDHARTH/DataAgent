from agent.tools import get_schema_tool, validate_sql_tool, run_sql_tool

print("SCHEMA:")
print(get_schema_tool())

sql = """
SELECT c.country, SUM(o.total_amount) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.country
"""

print("\nVALIDATION:")
print(validate_sql_tool(sql))

print("\nRESULT:")
print(run_sql_tool(sql))
