from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio
from models import Books

app = FastAPI()

# Fixed duplicate IDs - changed the last book's ID
books = [
    {"id": 9786258117578, "title": "İDARE HUKUKU II", "author": "KEMAL GÖZLER", "year": 2025, "publisher": "EKİN YAYINCILIK", "professor": "PROF.DR. MEHMET MERDAN HEKİMOĞLU"},
    {"id": 9786256545960, "title": "TÜRK HUKUK TARİHİ", "author": "COŞKUN ÜÇOK-AHMET MUMCU-GÜLNİHAL BOZKURT", "year": 2025, "publisher": "TURHAN KİTABEVİ", "professor": "YRD.DOÇ.DR.GÖZDE ERKİN"},
    {"id": 9786050519693, "title": "VERGİ HUKUKU", "author": "YUSUF KARAKOÇ", "year": 2024, "publisher": "YETKİN YAYINLARI", "professor": "YRD.DOÇ.DR.GÖZDE ERKİN"},
    {"id": 9786256545564, "title": "MİLLETLERARASI HUKUK II", "author": "HÜSEYİN PAZARCI, ERDEM DENK", "year": 2024, "publisher": "TURHAN KİTABEVİ", "professor": "YRD.DOÇ.DR.GÖZDE ERKİN"},
    {"id": 9786050506815, "title": "İDARİ YARGI", "author": "Prof. Dr. Ali D. Ulusoy", "year": 2020, "publisher": "Yetkin", "professor": "Prof. Dr. Mehmet Merdan Hekimoğlu"},
    {"id": 9789753537605, "title": "GENEL KAMU HUKUKU II", "author": "NİHAT BULUT, MEHMET AKAD, BİHTERİN VURAL DİNÇKOL", "year": 2024, "publisher": "DER YAYINLARI", "professor": "YRD.DOÇ.DR.GÖZDE ERKİN"},
    {"id": 9786258117579, "title": "ANAYASA YARGISI", "author": "ŞEREF İBA/ ABBAS KILIÇ", "year": 2025, "publisher": "TURHAN KİTABEVİ", "professor": "PROF.DR. MEHMET MERDAN HEKİMOĞLU"}  # Changed last digit to 9
]

@app.get("/books/", response_model=list[Books])
async def get_books():
    """Return all books - with simulated async delay"""
    await asyncio.sleep(0.5)  # Simulate database query delay
    return books

@app.get("/books/{book_id}", response_model=Books)
async def get_book(book_id: int):
    """Return a single book by ID"""
    # Simulate async operation
    await asyncio.sleep(0.3)
    
    # Find the book
    for book in books:
        if book["id"] == book_id:
            return book
    
    # If no book found, raise 404 exception
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
        
@app.post("/books/", response_model=dict)
async def add_book(book: Books):
    """Add a new book"""
    # Simulate async database operation
    await asyncio.sleep(1)  # This satisfies the async requirement
    
    # Convert Pydantic model to dict
    new_book = book.model_dump()  # Pydantic v2 syntax
    
    # Check if book with same ID already exists
    for existing_book in books:
        if existing_book["id"] == new_book["id"]:
            raise HTTPException(status_code=400, detail=f"Book with ID {new_book['id']} already exists")
    
    # Add to database
    books.append(new_book)
    
    return {"message": "Book added successfully", "details": new_book}

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """Delete a book by ID"""
    # Simulate async operation
    await asyncio.sleep(0.3)
    
    for i, book in enumerate(books):
        if book["id"] == book_id:
            deleted_book = books.pop(i)
            return {"message": "Book deleted successfully", "deleted_book": deleted_book}
    
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: Books):
    """Update an existing book"""
    # Simulate async operation
    await asyncio.sleep(0.5)
    
    # Convert to dict using Pydantic v2 syntax
    book_update = updated_book.model_dump()
    
    for i, book in enumerate(books):
        if book["id"] == book_id:
            # Preserve the original ID if needed, or use the new one
            books[i] = book_update
            return {"message": "Book updated successfully", "details": books[i]}
    
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")