# Project Decisions

## Pydantic Field Type Choices

1. **`id: int`** - ISBN numbers are numeric identifiers. Using `int` ensures exact matching and prevents formatting issues.

2. **`title: str`, `author: str`, `publisher: str`, `professor: str`** - All text fields use `str` for flexibility in handling various character sets (Turkish characters, punctuation).

3. **`year: int`** - Year is naturally numeric; using `int` allows range validation and comparisons.

4. **`department: Optional[Department]`** - Enum restricts values to predefined departments, preventing typos and ensuring consistency.

5. **`rating: Optional[float]`** - Float allows decimal ratings (e.g., 4.5 stars) with default 0 for new books.

## Validation Rules & What They Protect Against

1. **Year range (1900-2026)** - Prevents unrealistic publication dates (future books or ancient texts) that could break sorting/searching.

2. **ISBN 13-digit validation** - Ensures ID follows international standard; prevents data entry errors like missing digits.

3. **String length constraints (2-200 chars)** - Prevents empty strings or excessively long entries that could cause display issues.

4. **Professor-title cross-validation** - Early warning system for potential data mismatches (e.g., Constitutional Law taught by a mathematician).

5. **Rating range (0-5)** - Ensures rating system integrity; prevents invalid values like 10/5 stars.

## Async Implementation

The `POST /books/` endpoint uses `await asyncio.sleep(1)` to simulate a meaningful async operation. This represents:
- Database write operations (typically 50-500ms)
- External API calls for ISBN verification
- File system operations for book cover uploads

In production, this would be replaced with actual async database drivers or HTTP clients, but the sleep demonstrates non-blocking behavior - other requests can be processed while this "operation" completes.

## Database

### 1. What is `@contextmanager` and why do we use it instead of a plain function here?

`@contextmanager` is a decorator from Python's `contextlib` module that transforms a generator function into a context manager. In our `managed_db()` function, we use it to create a context manager that automatically handles database connection lifecycle.

We use it instead of a plain function because it guarantees proper resource cleanup. The `yield` statement splits the function into two parts: setup code before `yield` (connecting to database, creating tables) runs when entering the `with` block, and cleanup code after `yield` (closing the connection) runs when exiting the block - even if an exception occurs. A plain function would require manual `try/finally` blocks in every endpoint, which is repetitive, error-prone, and increases the risk of connection leaks.

### 2. What does `check_same_thread=False` do and why is it necessary in a FastAPI application?

`check_same_thread=False` disables SQLite's default thread-safety check that prevents a database connection from being used in a different thread than the one that created it.

This is necessary in FastAPI because FastAPI uses an asynchronous event loop with multiple threads to handle concurrent requests. When multiple requests come in simultaneously, they may be processed in different threads. Without `check_same_thread=False`, SQLite would throw "SQLite objects created in a thread can only be used in that same thread" errors whenever a request is handled by a different thread than the one that opened the connection. By setting this to `False`, we allow our database connections to be safely used across threads, enabling proper concurrent request handling.

### 3. What happens to your data when the server restarts — with the old list vs. with SQLite?

**With the old Python list (mock database):** All data was stored in memory only. When the server restarted (whether due to code changes, crashes, or intentional restarts), the list was reinitialized to empty, and all previously added books were permanently lost. This made the application unsuitable for production use as data persistence was nonexistent.

**With SQLite:** Data is persistently stored in the `sqlite.db` file on disk. When the server restarts, the database reconnects to the same file, and all previously added books remain available. This ensures data survival across server restarts, code deployments, and even system reboots. The only way data is lost is through explicit deletion operations or manual file removal, making the application suitable for real-world use where data persistence is critical.

## Database Query Parameter Styles

Following the project requirements, our SQL queries use specific parameter styles:

1. **INSERT and UPDATE queries** use **named parameters** (`:param`) - This makes the query more readable and self-documenting, as each parameter name clearly indicates what data it represents (e.g., `:title`, `:author`).

2. **SELECT and DELETE queries** use **positional parameters** (`?`) - These simpler queries don't need named parameters, and positional placeholders are more concise for single-value lookups.

This mixed approach balances readability with simplicity, following the exact requirements specified in the project guidelines.
