import sqlite3
import random
from datetime import date, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "company.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# Drop tables if rerun (dev-safe)
for table in ["order_items", "orders", "products", "customers"]:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

cursor.execute("""
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    country TEXT NOT NULL,
    created_at DATE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0)
)
""")

cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    total_amount REAL NOT NULL CHECK(total_amount >= 0),
    status TEXT NOT NULL CHECK(status IN ('completed','cancelled','returned')),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
""")

cursor.execute("""
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

# Indexes
cursor.execute("CREATE INDEX idx_orders_customer_id ON orders(customer_id)")
cursor.execute("CREATE INDEX idx_orders_order_date ON orders(order_date)")
cursor.execute("CREATE INDEX idx_customers_country ON customers(country)")
cursor.execute("CREATE INDEX idx_products_category ON products(category)")

# Seed data
customers = [
    ("Alice", "alice@mail.com", "USA"),
    ("Bob", "bob@mail.com", "India"),
    ("Charlie", "charlie@mail.com", "Germany"),
    ("Diana", "diana@mail.com", "UK"),
    ("Ethan", "ethan@mail.com", "Canada")
]

for i, (name, email, country) in enumerate(customers, start=1):
    cursor.execute(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
        (i, name, email, country, date.today() - timedelta(days=random.randint(30, 300)))
    )

products = [
    ("Laptop", "Electronics", 800),
    ("Phone", "Electronics", 500),
    ("Shoes", "Fashion", 120),
    ("Watch", "Accessories", 200),
    ("Backpack", "Accessories", 90)
]

for i, (name, category, price) in enumerate(products, start=1):
    cursor.execute(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        (i, name, category, price)
    )

order_id = 1
item_id = 1

for _ in range(40):
    customer_id = random.randint(1, 5)
    order_date = date.today() - timedelta(days=random.randint(1, 90))
    status = random.choice(["completed", "cancelled", "returned"])
    total = random.randint(100, 1500)

    cursor.execute(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
        (order_id, customer_id, order_date, total, status)
    )

    for _ in range(random.randint(1, 3)):
        cursor.execute(
            "INSERT INTO order_items VALUES (?, ?, ?, ?)",
            (item_id, order_id, random.randint(1, 5), random.randint(1, 4))
        )
        item_id += 1

    order_id += 1

conn.commit()
conn.close()

print("✅ Production-style database created")
