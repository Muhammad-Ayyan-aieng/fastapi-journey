from fastapi import FastAPI, HTTPException, APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
from models import Books
from database import managed_db, Database

book_router = APIRouter()

# Setup templates
templates = Jinja2Templates(directory="templates")

# HTML ROUTES
@book_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with all books"""
    with managed_db() as db:
        books = db.get_all()
    return templates.TemplateResponse(
        "book.html", 
        {"request": request, "books": books}
    )

@book_router.get("/book/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: int):
    """Render single book detail page"""
    with managed_db() as db:
        book = db.get(book_id)
    if not book:
        with managed_db() as db:
            all_books = db.get_all()
        return templates.TemplateResponse(
            "book.html",
            {"request": request, "books": all_books, "error": "Book not found"}
        )
    return templates.TemplateResponse(
        "book.html",
        {"request": request, "book": book}
    )

@book_router.post("/books/add")
async def add_book_web(
    request: Request,
    id: int = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    publisher: str = Form(...),
    professor: str = Form(...),
    department: str = Form("Computer Science"),
    rating: float = Form(0.0)
):
    """Add a new book from web form"""
    await asyncio.sleep(0.5)
    
    try:
        new_book = Books(
            id=id,
            title=title,
            author=author,
            year=year,
            publisher=publisher,
            professor=professor,
            department=department,
            rating=rating
        )
        
        # Convert to dict and ensure department is stored as string value, not enum
        book_dict = new_book.model_dump()
        if hasattr(book_dict['department'], 'value'):
            book_dict['department'] = book_dict['department'].value
        
        with managed_db() as db:
            # Check if book already exists
            existing_book = db.get(id)
            if existing_book:
                return RedirectResponse(url="/home?error=Book+ID+already+exists", status_code=303)
            
            db.create(book_dict)
        return RedirectResponse(url="/home?success=Book+added+successfully", status_code=303)
        
    except ValueError as e:
        error_str = str(e)
        if "Value error, " in error_str:
            error_message = error_str.split("Value error, ")[1]
        else:
            error_message = error_str
        error_message = error_message.replace("Department.", "")
        error_message = error_message.replace(" ", "+")
        return RedirectResponse(url=f"/home?error={error_message}", status_code=303)

@book_router.post("/books/delete/{book_id}")
async def delete_book_web(request: Request, book_id: int):
    """Delete a book from web form"""
    await asyncio.sleep(0.3)
    
    with managed_db() as db:
        book = db.get(book_id)
        if book:
            db.delete(book_id)
            return RedirectResponse(url="/home?success=Book+deleted+successfully", status_code=303)
    
    return RedirectResponse(url="/home?error=Book+not+found", status_code=303)

@book_router.post("/books/update/{book_id}")
async def update_book_web(
    request: Request,
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    publisher: str = Form(...),
    professor: str = Form(...),
    department: str = Form(...),
    rating: float = Form(0.0)
):
    """Update a book from web form"""
    await asyncio.sleep(0.5)
    
    try:
        # Create updated book object
        updated_book = Books(
            id=book_id,
            title=title,
            author=author,
            year=year,
            publisher=publisher,
            professor=professor,
            department=department,
            rating=rating
        )
        
        # Convert to dict and ensure department is stored as string
        book_dict = updated_book.model_dump()
        if hasattr(book_dict['department'], 'value'):
            book_dict['department'] = book_dict['department'].value
        
        # Find and update
        with managed_db() as db:
            book = db.get(book_id)
            if book:
                db.update(book_id, book_dict)
                return RedirectResponse(url=f"/book/{book_id}?success=Book+updated+successfully", status_code=303)
        
        return RedirectResponse(url="/home?error=Book+not+found", status_code=303)
         
    except ValueError as e:
        error_str = str(e)
        if "Value error, " in error_str:
            error_message = error_str.split("Value error, ")[1]
        else:
            error_message = error_str
        error_message = error_message.replace("Department.", "")
        error_message = error_message.replace(" ", "+")
        return RedirectResponse(url=f"/book/{book_id}?error={error_message}", status_code=303)

# API ROUTES
@book_router.get("/books/", response_model=list[Books])
async def get_books():
    """Return all books - with simulated async delay"""
    await asyncio.sleep(0.5)
    with managed_db() as db:
        return db.get_all()

@book_router.get("/books/{book_id}", response_model=Books)
async def get_book(book_id: int):
    """Return a single book by ID"""
    await asyncio.sleep(0.3)
    
    with managed_db() as db:
        book = db.get(book_id)
        if book:
            return book
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

@book_router.post("/books/", response_model=dict)
async def add_book(book: Books):
    """Add a new book"""
    await asyncio.sleep(1)
    
    new_book = book.model_dump()
    
    with managed_db() as db:
        # Check if book already exists
        existing_book = db.get(new_book["id"])
        if existing_book:
            raise HTTPException(status_code=400, detail=f"Book with ID {new_book['id']} already exists")
        
        db.create(new_book)
    
    return {"message": "Book added successfully", "details": new_book}

@book_router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """Delete a book by ID"""
    await asyncio.sleep(0.3)
    
    with managed_db() as db:
        book = db.get(book_id)
        if book:
            db.delete(book_id)
            return {"message": "Book deleted successfully", "deleted_book": book}
    
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

@book_router.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: Books):
    """Update an existing book"""
    await asyncio.sleep(0.5)
    
    book_update = updated_book.model_dump()
    
    with managed_db() as db:
        book = db.get(book_id)
        if book:
            db.update(book_id, updated_book)
            return {"message": "Book updated successfully", "details": db.get(book_id)}
    
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")