from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory='', note=''):
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note)
        )

        return {"status": "success", "id": curr.lastrowid}

@mcp.tool()
def list_expenses(start_date, end_date):
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )

        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, row)) for row in curr.fetchall()]

@mcp.tool()
def summarize(start_date: str | None = None, end_date: str | None = None, category: str | None = None):
    with sqlite3.connect(DB_PATH) as conn:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE 1 = 1
            """
        )
        params = []

        if start_date is not None:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date is not None:
            query += " AND date <= ?"
            params.append(end_date)

        if category is not None:
            query += " AND category = ?"
            params.append(category)

        query += "GROUP BY category ORDER BY category ASC"
        curr = conn.execute(query, params)
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, rows)) for rows in curr.fetchall()]

@mcp.resource("expenses://categories", mime_type="application/json")
def categories():
    with open(CATEGORIES, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()
