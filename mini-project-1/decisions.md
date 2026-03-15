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