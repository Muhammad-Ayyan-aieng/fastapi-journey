import sqlite3
import json

# Your books data
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

def seed_database():
    """Insert all books into the database"""
    
    # Connect to database
    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    
    # Check if books already exist
    cur.execute("SELECT COUNT(*) FROM Books")
    count = cur.fetchone()[0]
    
    if count > 0:
        print(f"Database already has {count} books.")
        response = input("Do you want to clear existing data and insert new data? (y/n): ")
        if response.lower() == 'y':
            print("Clearing existing books...")
            cur.execute("DELETE FROM Books")
            conn.commit()
            print(f"Removed {count} books.")
        else:
            print("Keeping existing data. No changes made.")
            conn.close()
            return
    
    # Insert all books
    inserted = 0
    skipped = 0
    
    for book in books_list:
        try:
            # Check if book with this ID already exists
            cur.execute("SELECT id FROM Books WHERE id = ?", (book['id'],))
            existing = cur.fetchone()
            
            if existing:
                print(f"Skipping duplicate: {book['title']} (ID: {book['id']})")
                skipped += 1
                continue
            
            # Insert the book using named parameters
            cur.execute("""
                INSERT INTO Books (id, title, author, year, publisher, professor, department, rating)
                VALUES (:id, :title, :author, :year, :publisher, :professor, :department, :rating)
            """, book)
            inserted += 1
            print(f"✓ Added: {book['title']}")
            
        except Exception as e:
            print(f"✗ Error adding {book['title']}: {e}")
    
    conn.commit()
    
    # Show summary
    print("\n" + "="*50)
    print(f"✅ Successfully inserted: {inserted} books")
    print(f"⏭️ Skipped (duplicates): {skipped} books")
    print(f"📚 Total books in database: {inserted + (count if count > 0 else 0)}")
    print("="*50)
    
    # Show some statistics
    cur.execute("SELECT department, COUNT(*) FROM Books GROUP BY department")
    departments = cur.fetchall()
    print("\n📊 Books by Department:")
    for dept, count in departments:
        print(f"   {dept}: {count} books")
    
    conn.close()

if __name__ == "__main__":
    print("📚 Seeding database with books...\n")
    seed_database()
    print("\n✨ Database seeding complete!")