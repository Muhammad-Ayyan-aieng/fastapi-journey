from contextlib import contextmanager
import sqlite3

class Database:

    def __init__(self):
        # Auto-connect when Database object is created
        self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                publisher TEXT,
                professor TEXT,
                department TEXT,
                rating REAL
            )
        """)
        self.conn.commit()

    def get_all(self) -> list:
        self.cur.execute("SELECT * FROM Books")
        rows = self.cur.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get(self, id: int) -> dict | None:
        self.cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
        row = self.cur.fetchone()
        return self._row_to_dict(row) if row else None

    def create(self, item) -> int:
        # Handle both dict and Pydantic model
        if hasattr(item, 'model_dump'):
            data = item.model_dump()
        else:
            data = item
            
        # Use NAMED parameters for INSERT
        self.cur.execute("""
            INSERT INTO Books (id, title, author, year, publisher, professor, department, rating)
            VALUES (:id, :title, :author, :year, :publisher, :professor, :department, :rating)
        """, {
            "id": data['id'],
            "title": data['title'],
            "author": data['author'],
            "year": data['year'],
            "publisher": data['publisher'],
            "professor": data['professor'],
            "department": data['department'],
            "rating": data['rating']
        })
        self.conn.commit()
        return data['id']

    def update(self, id: int, item) -> dict | None:
        # Handle both dict and Pydantic model
        if hasattr(item, 'model_dump'):
            data = item.model_dump()
        else:
            data = item
            
        # Use NAMED parameters for UPDATE
        self.cur.execute("""
            UPDATE Books
            SET title = :title, author = :author, year = :year,
                publisher = :publisher, professor = :professor,
                department = :department, rating = :rating
            WHERE id = :id
        """, {
            "id": id,
            "title": data['title'],
            "author": data['author'],
            "year": data['year'],
            "publisher": data['publisher'],
            "professor": data['professor'],
            "department": data['department'],
            "rating": data['rating']
        })
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cur.execute("DELETE FROM Books WHERE id = ?", (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _row_to_dict(self, row) -> dict:
        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "year": row[3],
            "publisher": row[4],
            "professor": row[5],
            "department": row[6],
            "rating": row[7]
        }

@contextmanager
def managed_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()
