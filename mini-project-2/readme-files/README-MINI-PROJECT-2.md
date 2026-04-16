# SFWE477 — Mini Project 2 🗄️

Welcome to **Mini Project 2** for **SFWE477: Backend Development with FastAPI**.  
This project builds directly on Mini Project 1. You will take your existing domain API and migrate it from an in-memory data store to a **real MongoDB database** using **Beanie** as the ODM (Object Document Mapper).

By the end of this project, your API will read and write data to a persistent MongoDB collection — meaning data survives restarts, just like a production application.

---

## 📁 Repository Setup

1. Use the same **`fastapi-journey`** repository from your previous labs and Mini Project 1
2. Create a **new branch** for this project following the naming policy below
3. Your project must live in a folder named **`mini-project-2/`** at the root of your repo

---

## 🌿 Branch Naming Policy

Branch names follow this format:

```
firstinitial+surname-mini-project-2
```

**Example:** John Snow → `jsnow-mini-project-2`

> ⚠️ Do not work on `main`. Do not use spaces or capital letters in branch names.

To create and switch to your branch:
```bash
git checkout -b jsnow-mini-project-2
```

---

## 🧠 Project Brief

You will build a **FastAPI + MongoDB** application for the **Event Planner** domain.  
Every student works on the same domain this time — the focus is on the database integration, not the domain design.

You are **not** migrating your Mini Project 1 code. You are building a **new, standalone application** from scratch inside `mini-project-2/`, using what you learned in Mini Project 1 and the chapter on Connecting to a Database.

Your application must manage two entities: **Events** and **Users**.

---

## 📦 What You Need to Install

Before writing any code, set up your environment:

```bash
# 1. Activate your virtual environment
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# 2. Install required libraries
pip install fastapi uvicorn beanie motor python-dotenv email-validator
```

You also need **MongoDB** running locally on your machine.  
Install it from the official MongoDB documentation for your operating system:  
👉 https://www.mongodb.com/docs/manual/installation/

To start MongoDB:
```bash
# macOS/Linux
mongod --dbpath ./store

# Windows
mongod --dbpath "C:\data\db"
```

> 💡 Create the `store` folder manually if it does not exist: `mkdir store`

---

## 🗂️ Expected Folder Structure

```
fastapi-journey/
└── mini-project-2/
    ├── main.py               # App entry point, startup event, route registration
    ├── models/
    │   ├── events.py         # Event document + EventUpdate model
    │   └── users.py          # User document + UserSignIn model
    ├── database/
    │   └── connection.py     # Settings, initialize_database, Database class
    ├── routes/
    │   ├── events.py         # All event routes
    │   └── users.py          # Signup and signin routes
    ├── .env                  # Your MongoDB connection string (not committed)
    └── DECISIONS.md          # Your written reflection
```

> ⚠️ The `.env` file must **not** be committed. Add it to `.gitignore`.

---

## ✅ Requirements

### 1. MongoDB Documents

Define your database documents using **Beanie's `Document` class**:

- `Event` — with fields: `title`, `image`, `description`, `tags` (list), `location`
- `User` — with fields: `email`, `password`, `events` (optional linked list of Events)

Each document must include a `Settings` subclass that names the MongoDB collection.

---

### 2. Database Connection

In `database/connection.py`:

- Use **Pydantic's `BaseSettings`** to read `DATABASE_URL` from a `.env` file
- Implement an `initialize_database()` async method using `init_beanie`
- Implement a `Database` class that wraps CRUD operations for any document model

The `Database` class must implement these methods:

| Method | Description |
|--------|-------------|
| `save(document)` | Insert a new document |
| `get(id)` | Retrieve one document by ID |
| `get_all()` | Retrieve all documents |
| `update(id, body)` | Update a document by ID |
| `delete(id)` | Delete a document by ID |

---

### 3. Event Routes

Implement the following endpoints in `routes/events.py`:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/event/` | Return all events |
| `GET` | `/event/{id}` | Return a single event by ID |
| `POST` | `/event/new` | Create a new event |
| `PUT` | `/event/{id}` | Update an existing event |
| `DELETE` | `/event/{id}` | Delete an event |

All routes must use `async def` and use the `Database` class — **not** direct Beanie calls inside the route functions.

---

### 4. User Routes

Implement the following endpoints in `routes/users.py`:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/user/signup` | Register a new user (reject duplicates) |
| `POST` | `/user/signin` | Sign in with email and password |

---

### 5. App Startup

In `main.py`, use the `@app.on_event("startup")` decorator to call `initialize_database()` when the application starts.

---

### 6. Environment File

Create a `.env` file in your `mini-project-2/` folder:

```
DATABASE_URL=mongodb://localhost:27017/planner
```

Add `.env` to your `.gitignore` — never commit credentials.

---

### 7. DECISIONS.md

You must include a `DECISIONS.md` file that answers the following questions **in your own words**:

1. What is an ODM and why do we use Beanie instead of writing raw MongoDB queries?
2. What is the role of the `Database` class — why wrap Beanie methods inside it instead of calling them directly in routes?
3. What happens if `initialize_database()` is not called on startup? What would break and why?
4. What is the difference between the `Event` document and the `EventUpdate` model, and why are they two separate classes?

> ⚠️ Generic or AI-sounding answers will not be accepted. Write from what you observed while building the project.

---

## 💾 Commit Policy

Do **not** commit everything in one go. Each major step must have its own commit:

```bash
# After setting up models
git add mini-project-2/models/
git commit -m "mini-project-2: define Event and User Beanie documents"

# After setting up the database connection
git add mini-project-2/database/
git commit -m "mini-project-2: implement database connection and Database class"

# After implementing event routes
git add mini-project-2/routes/events.py
git commit -m "mini-project-2: implement event CRUD routes"

# After implementing user routes
git add mini-project-2/routes/users.py
git commit -m "mini-project-2: implement user signup and signin routes"

# After wiring everything in main.py
git add mini-project-2/main.py
git commit -m "mini-project-2: wire app startup and route registration"

# After writing your reflection
git add mini-project-2/DECISIONS.md
git commit -m "mini-project-2: add DECISIONS.md"
```

When done, push your branch:
```bash
git push origin jsnow-mini-project-2
```

---

## 📬 Submission

Once your branch is pushed, copy the URL of your branch from GitHub and submit it on Moodle.

The link should look like this:
```
https://github.com/<your-username>/fastapi-journey/tree/jsnow-mini-project-2
```

---

## 🎯 Grading

This is a **Pass or Fail** assignment — you either receive the **full grade or nothing**. There is no partial credit.

### ✅ To pass, all three criteria must be met:

| # | Criteria | Details |
|---|----------|---------|
| 1 | **All requirements completed** | All 7 endpoints work, Database class is implemented, MongoDB is connected via `.env`, startup event initializes the DB |
| 2 | **Correct branch & commits** | Branch follows `jsnow-mini-project-2` format, each major section has its own commit |
| 3 | **DECISIONS.md is genuine** | Answers are specific to your experience, not generic or AI-generated |

### ❌ You will automatically fail if:
- Any endpoint is missing or returns an error
- MongoDB is not used (e.g. data is stored in a list in memory)
- The `Database` class is missing — routes call Beanie directly
- `.env` is committed to the repository
- `DECISIONS.md` is missing or contains generic answers
- All work is in a single commit
- The branch is incorrectly named or missing
- The submission link is not provided on Moodle before the deadline
