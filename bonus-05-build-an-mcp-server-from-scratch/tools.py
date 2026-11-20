# tools.py: the two tools our MCP server offers, with Pydantic models for their arguments.
import os, sqlite3
from pydantic import BaseModel, Field
import courier_api

# Argument models: Pydantic checks the arguments AND writes each tool's JSON Schema.
class GetOrderArgs(BaseModel):
    order_id: str = Field(pattern=r"^PT-\d{4}$",
                          description="Order ID like PT-1002, from the customer's email")

class TrackParcelArgs(BaseModel):
    tracking_id: str = Field(pattern=r"^TRK-\d{4}$",
                             description="Tracking ID like TRK-7734, from get_order")

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shop.db")

def read_only_db():
    # mode=ro: SQLite itself refuses every write. query_only is a second lock.
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.execute("PRAGMA query_only = ON")
    return con

def get_order(args: GetOrderArgs) -> dict:
    con = read_only_db()
    row = con.execute(  # only the columns the AI needs: no phone number
        "SELECT order_id, status, total_rs, tracking_id, placed_on "
        "FROM orders WHERE order_id = ?", (args.order_id,)).fetchone()
    if row is None:
        con.close()
        raise LookupError(f"No order {args.order_id}. Check the ID and ask the customer.")
    items = con.execute("SELECT title, qty FROM items WHERE order_id = ? LIMIT 20",
                        (args.order_id,)).fetchall()
    con.close()
    keys = ["order_id", "status", "total_rs", "tracking_id", "placed_on"]
    return dict(zip(keys, row), items=[{"title": t, "qty": q} for t, q in items])

def track_parcel(args: TrackParcelArgs) -> dict:
    try:
        return courier_api.track(args.tracking_id, timeout_s=2.0)
    except courier_api.ApiError as e:
        raise LookupError(f"Courier service said: {e}. Try later or tell the customer.")

TOOLS = {
    "get_order": {
        "fn": get_order, "args": GetOrderArgs, "title": "Get order",
        "description": "Look up ONE PageTurn Books order by its ID. "
                       "Returns status, total in rupees, items and tracking ID. "
                       "Read-only. Use it when a customer asks about an order.",
    },
    "track_parcel": {
        "fn": track_parcel, "args": TrackParcelArgs, "title": "Track parcel",
        "description": "Ask the courier where a parcel is right now. "
                       "Needs the tracking ID that get_order returns. "
                       "Read-only. Returns status, current city and ETA.",
    },
}

def tool_list() -> list:
    return [{"name": name, "title": t["title"], "description": t["description"],
             "inputSchema": t["args"].model_json_schema(),
             "annotations": {"readOnlyHint": True, "openWorldHint": False}}
            for name, t in TOOLS.items()]
