# make_db.py: create shop.db, a tiny made-up bookshop database (PageTurn Books).
# Run once: python make_db.py
import sqlite3, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shop.db")
if os.path.exists(DB):
    os.remove(DB)
con = sqlite3.connect(DB)
con.executescript("""
CREATE TABLE orders (
  order_id TEXT PRIMARY KEY, customer TEXT, phone TEXT,
  status TEXT, total_rs INTEGER, tracking_id TEXT, placed_on TEXT);
CREATE TABLE items (order_id TEXT, title TEXT, qty INTEGER);
""")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", [
    ("PT-1001", "Riya", "98450-11111", "delivered", 649, "TRK-5521", "2026-11-12"),
    ("PT-1002", "Kabir", "98450-22222", "shipped", 1198, "TRK-7734", "2026-11-17"),
    ("PT-1003", "Meera", "98450-33333", "packing", 399, None, "2026-11-19"),
])
con.executemany("INSERT INTO items VALUES (?,?,?)", [
    ("PT-1001", "Python for Beginners", 1),
    ("PT-1002", "Deep Learning Basics", 1), ("PT-1002", "The Data Notebook", 2),
    ("PT-1003", "Clean Code Stories", 1),
])
con.commit()
con.close()
print("created shop.db with 3 orders")
