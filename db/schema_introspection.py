# db/schema_introspection.py
from sqlalchemy import inspect
from db.session import engine

def get_database_schema():
    inspector = inspect(engine)
    schema = {}

    for table in inspector.get_table_names():
        schema[table] = [
            {
                "column": col["name"],
                "type": str(col["type"])
            }
            for col in inspector.get_columns(table)
        ]

    return schema
