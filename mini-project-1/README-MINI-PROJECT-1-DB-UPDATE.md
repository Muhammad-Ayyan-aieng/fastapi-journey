# SFWE477 — Mini Project 1 · Database Update 🗄️

Welcome back to **Mini Project 1**.  
This update adds one new requirement to your existing project:

- **SQLite Database** — replacing your in-memory Python list with a real persistent database

You will **not** create a new branch or a new folder. Everything goes into your existing `mini-project-1/` folder on your existing branch.

---

## 📌 What You Are Building On

Your starting point is your already submitted Mini Project 1 — with the router, HTTP exceptions, and Jinja2 templates already in place. The only change in this update is how your data is stored.

> ⚠️ Your **mock database list will be removed** and replaced with a SQLite database. Do not keep the list alongside the database — having both is a fail.

---

## 📋 Requirement — Replace the Mock List with a SQLite Database

### Setup

No new installation needed — `sqlite3` is part of Python's standard library. You only need these imports at the top of `database.py`:

```python
from contextlib import contextmanager
import sqlite3
```

---

### New File: `database.py`

Create a new file named **`database.py`** inside your `mini-project-1/` folder.  
This file must contain a `Database` class and a `managed_db` context manager function.

**The class must have exactly these methods:**

| Method | Responsibility |
|---|---|
| `connect_to_db()` | Open the SQLite connection and cursor |
| `create_table()` | Create the table if it does not exist |
| `get_all()` | Return all rows as a list of dicts |
| `get(id)` | Return one row as a dict, or `None` if not found |
| `create(item)` | Insert a new row, auto-generate the ID |
| `update(id, item)` | Update an existing row by ID |
| `delete(id)` | Delete a row by ID |
| `close()` | Close the connection |

**Skeleton to follow — fill in the placeholders for your domain:**

```python
from contextlib import contextmanager
import sqlite3
    

class Database:

    def connect_to_db(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS {your_table_name} (
                id INTEGER PRIMARY KEY,
                -- TODO: add your columns here, matching your Pydantic model fields
            )
        """)

    def get_all(self) -> list:
        self.cur.execute("SELECT * FROM {your_table_name}")
        rows = self.cur.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get(self, id: int) -> dict | None:
        self.cur.execute("""
            SELECT * FROM {your_table_name} WHERE id = ?
        """, (id,))
        row = self.cur.fetchone()
        return self._row_to_dict(row) if row else None

    def create(self, item) -> int:
        self.cur.execute("SELECT MAX(id) FROM {your_table_name}")
        result = self.cur.fetchone()
        new_id = (result[0] or 0) + 1
        self.cur.execute("""
            INSERT INTO {your_table_name}
            VALUES (:id, :field1, :field2, ...)
        """, {"id": new_id, **item.model_dump()})
        self.conn.commit()
        return new_id

    def update(self, id: int, item) -> dict | None:
        self.cur.execute("""
            UPDATE {your_table_name}
            SET field1 = :field1, field2 = :field2, ...
            WHERE id = :id
        """, {"id": id, **item.model_dump()})
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cur.execute("""
            DELETE FROM {your_table_name} WHERE id = ?
        """, (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _row_to_dict(self, row) -> dict:
        # TODO: map each column position to its field name
        # Example: return {"id": row[0], "name": row[1], "age": row[2]}
        pass


@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table()
    try:
        yield db
    finally:
        db.close()
```

> Replace all `{your_table_name}`, `field1`, `field2` placeholders with your actual domain's table name and column names — matching the fields in your Pydantic model exactly.

---

### Parameter Style Rules

You must follow these rules for all SQL queries — mixing them up is a fail:

| Query type | Parameter style | Example |
|---|---|---|
| `INSERT` | Named — `:param` | `VALUES (:id, :name, :age)` |
| `UPDATE` | Named — `:param` | `SET name = :name WHERE id = :id` |
| `SELECT` | Positional — `?` | `WHERE id = ?` |
| `DELETE` | Positional — `?` | `WHERE id = ?` |

---

### Update `{router_file}.py` — Use the Database

Remove the mock list from the top of your router file. Every endpoint must now open a database connection using `with managed_db() as db:` and call the appropriate method.

**Before:**

```python
# This list must be removed entirely
patients = [
    {"id": 1, "name": "Cosmo", "age": 35, "ward": "Cardiology", "appointments": []},
    ...
]

@patient_router.get("/patients/")
async def get_all_patients():
    return {"patients": patients}
```

**After:**

```python
from database import managed_db

@patient_router.get("/patients/")
async def get_all_patients():
    with managed_db() as db:
        return {"patients": db.get_all()}
```

Apply the same pattern to all five endpoints:

| Endpoint | Database call |
|---|---|
| `GET /items/` | `db.get_all()` |
| `GET /items/{id}` | `db.get(id)` |
| `POST /items/` | `db.create(item)` |
| `PUT /items/{id}` | `db.update(id, item)` |
| `DELETE /items/{id}` | `db.delete(id)` |

> ⚠️ Your `HTTPException` logic must still work — if `db.get(id)` returns `None`, you must still raise a 404.

---

### DECISIONS.md — Add a New Section

Add a new section at the bottom of your existing `DECISIONS.md` titled `## Database` and answer all three of the following questions:

1. What is `@contextmanager` and why do we use it instead of a plain function here?
2. What does `check_same_thread=False` do and why is it necessary in a FastAPI application?
3. What happens to your data when the server restarts — with the old list vs. with SQLite?

> Answers must be specific to your own code. Generic one-line answers will not pass.

---

## 📁 Final Expected Structure

```
fastapi-journey/
└── mini-project-1/
    ├── main.py                  ← unchanged
    ├── models.py                ← unchanged
    ├── database.py              ← new file
    ├── {router_file}.py         ← updated: list removed, managed_db() used
    ├── DECISIONS.md             ← updated: new Database section added
    └── templates/
        ├── home.html
        └── {item_template}.html
```

---

## 💾 How to Commit

Push to the **same branch** you have been using. Two commits are required for this update:

```bash
# After creating database.py and updating the router
git add mini-project-1/database.py mini-project-1/{router_file}.py
git commit -m "mini-project-1: replace mock list with SQLite database"

# After updating DECISIONS.md
git add mini-project-1/DECISIONS.md
git commit -m "mini-project-1: update DECISIONS.md with database answers"
```

When done, push:

```bash
git push origin {your-branch-name}
```

---

## 📬 Submission

Your Moodle submission link remains the same — no new submission needed unless the link has changed.

```
https://github.com/<your-username>/fastapi-journey/tree/<your-branch-name>
```

---

## 🎯 Grading

This is a **Pass or Fail** assignment — you either receive the **full grade or nothing**. There is no partial credit.

### ✅ To pass, all criteria must be met:

| # | Criteria | Details |
|---|----------|---------|
| 1 | **`database.py` exists and is correct** | `Database` class with all 8 methods present, `managed_db` uses `@contextmanager` |
| 2 | **Mock list fully removed** | No Python list mock database remains anywhere in the codebase |
| 3 | **All endpoints use `managed_db()`** | Every endpoint opens the DB via `with managed_db() as db:` |
| 4 | **Correct parameter styles** | Named parameters for INSERT/UPDATE, positional for SELECT/DELETE |
| 5 | **404 still works** | `HTTPException` is still raised when `db.get(id)` returns `None` |
| 6 | **`DECISIONS.md` updated** | New Database section with all three questions answered specifically |
| 7 | **Two separate commits** | One for the database code, one for DECISIONS.md |
| 8 | **No AI-generated code** | Code must be written by you |

### ❌ You will automatically fail if:
- `database.py` is missing
- `managed_db` does not use `@contextmanager`
- The mock list is still present alongside the database
- Any endpoint still reads from a list instead of calling `managed_db()`
- Named/positional parameter styles are mixed up incorrectly
- `db.get(id)` returning `None` no longer raises a 404
- `DECISIONS.md` has no Database section or answers are generic
- Both commits are squashed into one

### ⏰ Deadline
Late submissions are **not accepted** under any circumstances.

