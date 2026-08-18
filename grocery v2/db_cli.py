"""
Smart Grocery Inventory & Billing System - Terminal Database CLI Tool
Usage:
    python db_cli.py                 (Interactive mode)
    python db_cli.py tables          (List all tables & row counts)
    python db_cli.py <table_name>    (View first 10 rows of a table)
    python db_cli.py query "<sql>"   (Run custom SQL query)
"""

import sqlite3
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'smart_grocery.db')

def get_connection():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def print_table(headers, rows):
    if not rows:
        print("  (Empty table / No records returned)")
        return

    # Calculate column widths
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            str_val = str(val) if val is not None else "NULL"
            if len(str_val) > widths[i]:
                widths[i] = min(len(str_val), 40) # cap width at 40 chars for display

    # Build format strings
    header_str = " | ".join(f"{str(h):<{widths[i]}}" for i, h in enumerate(headers))
    sep_str = "-+-".join("-" * widths[i] for i in range(len(headers)))

    print(header_str)
    print(sep_str)
    for row in rows:
        row_cells = []
        for i, val in enumerate(row):
            str_val = str(val) if val is not None else "NULL"
            if len(str_val) > 40:
                str_val = str_val[:37] + "..."
            row_cells.append(f"{str_val:<{widths[i]}}")
        print(" | ".join(row_cells))

def list_tables():
    conn = get_connection()
    cur = conn.cursor()
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()
    
    print("\n--- DATABASE TABLES ---")
    headers = ["Table Name", "Record Count"]
    data = []
    for t in tables:
        t_name = t['name']
        count = cur.execute(f"SELECT count(*) FROM {t_name}").fetchone()[0]
        data.append([t_name, count])
    print_table(headers, data)
    print()
    conn.close()

def view_table(table_name, limit=10):
    conn = get_connection()
    cur = conn.cursor()
    
    # Check if table exists
    tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    if table_name not in tables:
        print(f"Error: Table '{table_name}' does not exist.")
        print("Available tables:", ", ".join(tables))
        conn.close()
        return

    columns = [c[1] for c in cur.execute(f"PRAGMA table_info({table_name});").fetchall()]
    rows = cur.execute(f"SELECT * FROM {table_name} LIMIT {limit};").fetchall()
    
    print(f"\n--- TABLE: {table_name} (Showing top {len(rows)} rows) ---")
    print_table(columns, [list(r) for r in rows])
    print()
    conn.close()

def run_query(sql_query):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql_query)
        if sql_query.strip().lower().startswith("select") or "pragma" in sql_query.lower():
            rows = cur.fetchall()
            if cur.description:
                headers = [d[0] for d in cur.description]
                print_table(headers, [list(r) for r in rows])
            else:
                print("Query executed successfully.")
        else:
            conn.commit()
            print(f"Query executed successfully. Rows affected: {cur.rowcount}")
    except Exception as e:
        print(f"SQL Error: {e}")
    finally:
        conn.close()

def interactive_mode():
    print("==================================================")
    print("   Smart Grocery Database CLI Terminal Tool")
    print("==================================================")
    print("Commands:")
    print("  tables          - List all tables")
    print("  <table_name>    - View contents of a table (e.g., products, users)")
    print("  SELECT ...      - Run custom SQL query")
    print("  exit / quit     - Exit interactive mode")
    print("==================================================\n")

    while True:
        try:
            cmd = input("db-cli> ").strip()
            if not cmd:
                continue
            if cmd.lower() in ('exit', 'quit', 'q'):
                print("Goodbye!")
                break
            elif cmd.lower() == 'tables':
                list_tables()
            elif ' ' not in cmd and not cmd.lower().startswith("select"):
                view_table(cmd)
            else:
                run_query(cmd)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        interactive_mode()
    elif args[0] == 'tables':
        list_tables()
    elif args[0] == 'query' and len(args) > 1:
        run_query(" ".join(args[1:]))
    else:
        view_table(args[0])
