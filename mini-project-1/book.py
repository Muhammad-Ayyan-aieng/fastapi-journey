from fastapi import FastAPI, HTTPException, APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
from models import Books


book_router = APIRouter()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Books from different domains - Maths, AI, Psychology, Software, Law
books_list = [
    # Mathematics Books
    {"id": 9780262033848, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "year": 2022, "publisher": "MIT Press", "professor": "Dr. Alan Turing", "department": "Mathematics", "rating": 4.8},
    {"id": 9780691118802, "title": "The Princeton Companion to Mathematics", "author": "Timothy Gowers", "year": 2020, "publisher": "Princeton University Press", "professor": "Prof. David Hilbert", "department": "Mathematics", "rating": 4.9},
    
    # AI & Machine Learning
    {"id": 9780262035613, "title": "Deep Learning", "author": "Ian Goodfellow", "year": 2023, "publisher": "MIT Press", "professor": "Dr. Geoffrey Hinton", "department": "Artificial Intelligence", "rating": 4.9},
    {"id": 9781492032649, "title": "Hands-On Machine Learning", "author": "Aurélien Géron", "year": 2023, "publisher": "O'Reilly Media", "professor": "Prof. Yann LeCun", "department": "Artificial Intelligence", "rating": 4.7},
    {"id": 9780262046305, "title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "year": 2024, "publisher": "Pearson", "professor": "Dr. Andrew Ng", "department": "Artificial Intelligence", "rating": 4.8},
    
    # Computer Science
    {"id": 9780131103627, "title": "The C Programming Language", "author": "Brian Kernighan", "year": 2021, "publisher": "Prentice Hall", "professor": "Dr. Dennis Ritchie", "department": "Computer Science", "rating": 4.9},
    
    # Psychology Books
    {"id": 9781462547566, "title": "Cognitive Psychology", "author": "E. Bruce Goldstein", "year": 2022, "publisher": "Cengage Learning", "professor": "Dr. Jean Piaget", "department": "Psychology", "rating": 4.5},
    {"id": 9780393337699, "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "year": 2021, "publisher": "Farrar, Straus and Giroux", "professor": "Prof. Amos Tversky", "department": "Psychology", "rating": 4.8},
    
    # Software Engineering
    {"id": 9780132350884, "title": "Clean Code", "author": "Robert C. Martin", "year": 2020, "publisher": "Prentice Hall", "professor": "Dr. Martin Fowler", "department": "Software Engineering", "rating": 4.9},
    {"id": 9781491950357, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "year": 2023, "publisher": "O'Reilly Media", "professor": "Prof. Barbara Liskov", "department": "Software Engineering", "rating": 4.9},
    
    # Physics
    {"id": 9781107189638, "title": "The Feynman Lectures on Physics", "author": "Richard Feynman", "year": 2021, "publisher": "Basic Books", "professor": "Dr. Albert Einstein", "department": "Physics", "rating": 5.0},
    
    # Engineering
    {"id": 9780073398206, "title": "Engineering Mechanics", "author": "Russell Hibbeler", "year": 2022, "publisher": "Pearson", "professor": "Dr. James Stewart", "department": "Engineering", "rating": 4.3},
    
    # Business
    {"id": 9780066620992, "title": "Good to Great", "author": "Jim Collins", "year": 2021, "publisher": "HarperBusiness", "professor": "Prof. Jim Collins", "department": "Business", "rating": 4.6},
    
    # Medicine
    {"id": 9780323358437, "title": "Gray's Anatomy", "author": "Henry Gray", "year": 2023, "publisher": "Elsevier", "professor": "Dr. Henry Gray", "department": "Medicine", "rating": 4.7},
    
    # Law Books
    {"id": 9786258117578, "title": "İDARE HUKUKU II", "author": "KEMAL GÖZLER", "year": 2025, "publisher": "EKİN YAYINCILIK", "professor": "PROF.DR. MEHMET MERDAN HEKİMOĞLU", "department": "Law", "rating": 4.5},
    {"id": 9786256545960, "title": "TÜRK HUKUK TARİHİ", "author": "COŞKUN ÜÇOK-AHMET MUMCU-GÜLNİHAL BOZKURT", "year": 2025, "publisher": "TURHAN KİTABEVİ", "professor": "YRD.DOÇ.DR.GÖZDE ERKİN", "department": "Law", "rating": 4.3},
    {"id": 9786050519693, "title": "VERGİ HUKUKU", "author": "YUSUF KARAKOÇ", "year": 2024, "publisher": "YETKİN YAYINLARI", "professor": "YRD.DOÇ.DR.GÖZDE ERKİN", "department": "Law", "rating": 4.4},
    {"id": 9786256545564, "title": "MİLLETLERARASI HUKUK II", "author": "HÜSEYİN PAZARCI, ERDEM DENK", "year": 2024, "publisher": "TURHAN KİTABEVİ", "professor": "YRD.DOÇ.DR.GÖZDE ERKİN", "department": "Law", "rating": 4.2},
    {"id": 9786050506815, "title": "İDARİ YARGI", "author": "Prof. Dr. Ali D. Ulusoy", "year": 2020, "publisher": "Yetkin", "professor": "Prof. Dr. Mehmet Merdan Hekimoğlu", "department": "Law", "rating": 4.1},
    {"id": 9789753537605, "title": "GENEL KAMU HUKUKU II", "author": "NİHAT BULUT, MEHMET AKAD, BİHTERİN VURAL DİNÇKOL", "year": 2024, "publisher": "DER YAYINLARI", "professor": "YRD.DOÇ.DR.GÖZDE ERKİN", "department": "Law", "rating": 4.0},
    {"id": 9786258117579, "title": "ANAYASA YARGISI", "author": "ŞEREF İBA/ ABBAS KILIÇ", "year": 2025, "publisher": "TURHAN KİTABEVİ", "professor": "PROF.DR. MEHMET MERDAN HEKİMOĞLU", "department": "Law", "rating": 4.6}
]

# HTML ROUTES
@book_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with all books"""
    return templates.TemplateResponse(
        "book.html", 
        {"request": request, "books": books_list}
    )

@book_router.get("/book/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: int):
    """Render single book detail page"""
    book = next((b for b in books_list if b["id"] == book_id), None)
    if not book:
        return templates.TemplateResponse(
            "book.html",
            {"request": request, "books": books_list, "error": "Book not found"}
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
        
        for existing_book in books_list:
            if existing_book["id"] == id:
                return RedirectResponse(url="/home?error=Book+ID+already+exists", status_code=303)
        
        # Convert to dict and ensure department is stored as string value, not enum
        book_dict = new_book.model_dump()
        # If department is still an enum object, convert to string
        if hasattr(book_dict['department'], 'value'):
            book_dict['department'] = book_dict['department'].value
        
        books_list.append(book_dict)
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
    
    for i, book in enumerate(books_list):
        if book["id"] == book_id:
            books_list.pop(i)
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
        
        # Find and update
        for i, book in enumerate(books_list):
            if book["id"] == book_id:
                # Convert to dict and ensure department is stored as string
                book_dict = updated_book.model_dump()
                # If department is still an enum object, convert to string
                if hasattr(book_dict['department'], 'value'):
                    book_dict['department'] = book_dict['department'].value
                
                books_list[i] = book_dict
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
    return books_list

@book_router.get("/books/{book_id}", response_model=Books)
async def get_book(book_id: int):
    """Return a single book by ID"""
    await asyncio.sleep(0.3)
    
    for book in books_list:
        if book["id"] == book_id:
            return book
    
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

@book_router.post("/books/", response_model=dict)
async def add_book(book: Books):
    """Add a new book"""
    await asyncio.sleep(1)
    
    new_book = book.model_dump()
    
    for existing_book in books_list:
        if existing_book["id"] == new_book["id"]:
            raise HTTPException(status_code=400, detail=f"Book with ID {new_book['id']} already exists")
    
    books_list.append(new_book)
    
    return {"message": "Book added successfully", "details": new_book}

@book_router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """Delete a book by ID"""
    await asyncio.sleep(0.3)
    
    for i, book in enumerate(books_list):
        if book["id"] == book_id:
            deleted_book = books_list.pop(i)
            return {"message": "Book deleted successfully", "deleted_book": deleted_book}
    
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

@book_router.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: Books):
    """Update an existing book"""
    await asyncio.sleep(0.5)
    
    book_update = updated_book.model_dump()
    
    for i, book in enumerate(books_list):
        if book["id"] == book_id:
            books_list[i] = book_update
            return {"message": "Book updated successfully", "details": books_list[i]}
    
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")