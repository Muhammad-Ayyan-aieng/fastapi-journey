# SFWE477 — Mini Project 1 🚀

Welcome to **Mini Project 1** for **SFWE477: Backend Development with FastAPI**.  
This project brings together everything you have practiced across Labs 1–4: routing, async endpoints, CRUD operations, Pydantic models, data validation, and nested models.

---

## 📁 Repository Setup

1. Use the same **`fastapi-journey`** repository from your labs
2. Create a **new branch** for this project following the naming policy below
3. Your project must live in a folder named **`mini-project-1/`** at the root of your repo

---

## 🌿 Branch Naming Policy

This project must be worked on its **own branch**. Branch names follow this format:

```
firstinitial+surname-mini-project-1
```

Use the **first letter of your first name** followed by your **surname** — no spaces, all lowercase.

**Example:** John Snow → `jsnow-mini-project-1`

> ⚠️ Do not work on the `main` branch. Do not use spaces or capital letters in branch names.

To create and switch to your branch:
```bash
git checkout -b jsnow-mini-project-1
```

---

## 🧠 Project Brief

You will build a **RESTful API** for the domain assigned to you by your instructor.  
Your API must manage at least **two related entities** using a clean FastAPI application with Pydantic validation throughout.

### Domain Assignments

Your domain is assigned — check the table below. You may not switch domains.

| Student ID | Full Name | Domain |
|---|---|---|
| 2003010152 | MOHAMMED SALEH SALMEN AL-JABERI | 📚 Library |
| 2003060127 | SALIH SAMIER S. OTMAN | 🎓 Course Enrollment |
| 2103060004 | SELİN TÜRKDOĞAN | 🏋️ Gym |
| 2103060010 | ALİM ÖZGÜR ÖZTÜRK | 🏥 Clinic |
| 2103060163 | BELLY DYNELLA SABUSHIMIKE | 📚 Library |
| 2203060011 | HAYRUNNİSA İYİKÖŞKER | 📚 Library |
| 2203060017 | GAYE İLERİ | 🏋️ Gym |
| 2203060018 | SÜLEYMAN FARUK ŞAHAL | 🎓 Course Enrollment |
| 2203060043 | MERYEM BALILI | 💰 Budget Tracker |
| 2203060071 | MOUNCIF BELRHRIB | 🏋️ Gym |
| 2203060085 | GERMAN RACHKOV | 🎓 Course Enrollment |
| 2203060207 | POLINA ZIMINA | 🏥 Clinic |
| 2203060248 | AYYOUB ASRI | 🎓 Course Enrollment |
| 2203060251 | NIKITA IGNATEV | 💰 Budget Tracker |
| 2203060271 | AHMED SULTAN AHMED | 📚 Library |
| 2203060272 | SALOUA OURICH | 🏥 Clinic |
| 2203070012 | ABDULLAH NABIL ABDULLAH GHANEM | 🏋️ Gym |
| 2303060049 | HAYTAM CHARAFI | 💰 Budget Tracker |
| 2303060053 | ALEYA ABDULMOMEN KEWSEEDIN | 🎓 Course Enrollment |
| 2315030014 | AHMET ŞENEL | 🏥 Clinic |
| 2415030013 | DOĞANCAN YILMAZER | 🏥 Clinic |

### Domain Details

| Domain | Primary Entity | Secondary Entity |
|--------|---------------|-----------------|
| 🏥 Clinic | Patient | Appointment |
| 📚 Library | Book | BorrowRecord |
| 🏋️ Gym | Member | WorkoutSession |
| 🎓 Course Enrollment | Student | Enrollment |
| 💰 Budget Tracker | Transaction | Category |

---

## ✅ Requirements

### 1. Entities & Nested Models
- Define **two Pydantic models** — one for each entity
- The primary entity must **contain a nested list** of the secondary entity (as in Lab 4)
- Both models must use **proper type annotations** for all fields

### 2. Endpoints
Your API must implement the following endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/items/` | Return all primary entities |
| `GET` | `/items/{id}` | Return a single entity by ID with nested data |
| `POST` | `/items/` | Add a new entity (validated via Pydantic) |
| `PUT` | `/items/{id}` | Update an existing entity |
| `DELETE` | `/items/{id}` | Remove an entity |

> Replace `items` with the name relevant to your domain (e.g. `/patients/`, `/books/`)

### 3. Data Validation
Your models must include **at least three** of the following validation rules:

- A numeric field constrained with `gt`, `ge`, `lt`, or `le`
- A string field with `min_length` or `max_length`
- A field validated with a **custom `@model_validator`**
- An optional field with a sensible default value
- An enum field restricting values to a fixed set

### 4. Async Endpoints
- All endpoints must use `async def`
- At least **one endpoint** must simulate a delay using `await asyncio.sleep(1)` to reflect a real-world async operation

### 5. DECISIONS.md
You must include a **`DECISIONS.md`** file inside your `mini-project-1/` folder that answers:
- Why did you choose each Pydantic field type?
- What does each validation rule protect against?
- Which endpoint uses `async` in a meaningful way, and why?

---

## 💾 How to Commit — One Requirement at a Time

Do **not** commit everything at the end. Each major piece of work must have its own commit.

```bash
# After defining your Pydantic models
git add mini-project-1/models.py
git commit -m "mini-project-1: define Pydantic models with validation"

# After implementing GET endpoints
git add mini-project-1/main.py
git commit -m "mini-project-1: add GET endpoints"

# After implementing POST/PUT/DELETE
git add mini-project-1/main.py
git commit -m "mini-project-1: add POST, PUT, DELETE endpoints"

# After writing your decisions file
git add mini-project-1/DECISIONS.md
git commit -m "mini-project-1: add DECISIONS.md"
```

When you are done, push your branch:
```bash
git push origin jsnow-mini-project-1
```

---

## 📁 Expected Folder Structure

```
fastapi-journey/
└── mini-project-1/
    ├── main.py          # All routes and app setup
    ├── models.py        # Pydantic models (can be in main.py if preferred)
    └── DECISIONS.md     # Your written explanation
```

---

## 📬 Submission

Once your branch is pushed, copy the URL of your branch from GitHub and submit it on Moodle.

The link should look like this:
```
https://github.com/<your-username>/fastapi-journey/tree/jsnow-mini-project-1
```

---

## 🎯 Grading

This is a **Pass or Fail** assignment — you either receive the **full grade or nothing**. There is no partial credit.

### ✅ To pass, all three criteria must be met:

| # | Criteria | Details |
|---|----------|---------|
| 1 | **All requirements completed** | All endpoints work, all validation rules are implemented, nested models are used correctly |
| 2 | **Correct branch & commits** | Branch must follow the `jsnow-mini-project-1` format, and each major section must have its own separate commit |
| 3 | **No AI-generated code** | Code must be written by you. AI-assisted submissions will result in a zero and be reported |

### ❌ You will automatically fail if:
- Any endpoint is missing or non-functional
- Pydantic validation is absent or copied directly from lab files without adaptation
- `DECISIONS.md` is missing or contains generic/AI-sounding answers
- All work is in a single commit
- The branch is incorrectly named or missing
- The submission link is not provided on Moodle before the deadline
---
