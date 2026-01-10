# services/query_service.py
from sqlalchemy import text
from db.session import engine

class ReadOnlyQueryService:

    @staticmethod
    def execute(sql: str):
        if not sql.strip().lower().startswith("select"):
            raise PermissionError("Only SELECT queries are allowed")

        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()

        return {
            "columns": list(columns),
            "rows": [list(r) for r in rows]
        }
