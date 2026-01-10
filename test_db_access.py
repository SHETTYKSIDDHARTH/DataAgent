from db.schema_introspection import get_database_schema
from services.query_service import ReadOnlyQueryService

print(get_database_schema())

sql = """
SELECT c.country, SUM(o.total_amount) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.country
"""

print(ReadOnlyQueryService.execute(sql))

