
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "sales_data.db"

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS sales;")
    cur.execute(
        """
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        );
        """
    )
    rows = [
        ("Pen", 10, 5.0),
        ("Pen", 7, 5.0),
        ("Notebook", 5, 50.0),
        ("Notebook", 3, 45.0),
        ("Pencil", 20, 2.0),
        ("Pencil", 15, 2.5),
        ("Marker", 8, 25.0),
        ("Marker", 4, 30.0),
        ("Eraser", 12, 3.0),
    ]
    cur.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?);", rows)
    conn.commit()
    return conn

def main():
    # 1) Build tiny DB
    conn = build_db()

    # 2) Query
    query = """
    SELECT 
        product, 
        SUM(quantity) AS total_qty, 
        SUM(quantity * price) AS revenue
    FROM sales
    GROUP BY product
    ORDER BY revenue DESC;
    """
    df = pd.read_sql_query(query, conn)

    # 3) Show and save
    print("Sales Summary (by product):")
    print(df)
    df.to_csv("sales_summary.csv", index=False)

    # 4) Chart
    plt.figure(figsize=(8, 5))
    plt.bar(df["product"], df["revenue"])
    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("sales_chart.png")
    plt.show()

    conn.close()

if __name__ == "__main__":
    main()
