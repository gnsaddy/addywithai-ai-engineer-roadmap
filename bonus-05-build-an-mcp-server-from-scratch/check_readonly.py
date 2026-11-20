# check_readonly.py: prove the database connection the tools use cannot write.
from tools import read_only_db

con = read_only_db()
print("read works:", con.execute("SELECT COUNT(*) FROM orders").fetchone()[0], "orders")
try:
    con.execute("DELETE FROM orders")
except Exception as e:
    print("write blocked:", e)
