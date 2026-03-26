# SFWE477 — Mini Project 1 · Update 🔧

Welcome back to **Mini Project 1**.  
This update extends your existing work with three new concepts covered in class:

- **HTTP Exceptions** — replacing default responses with proper error handling
- **APIRouter** — splitting your app into multiple files with a dedicated router
- **Jinja2 Templating** — serving HTML pages directly from your FastAPI app

You will **not** create a new branch or a new folder. Everything goes into your existing `mini-project-1/` folder on your existing branch.

---

## 📌 What You Are Building On

Your starting point is the code you already submitted for Mini Project 1. You must refactor and extend it — not rewrite it from scratch. Your existing Pydantic models, mock database, and endpoint logic must be preserved and reorganised into the new structure described below.

---

## 📦 Step 0 — Download Your Template Files

Template files have been uploaded to Moodle as separate ZIP files — **one per domain**.

### ⚠️ Download only the ZIP that matches your domain. Ignore the rest.

| Domain | File to download |
|---|---|
| 🏥 Clinic | `templates_clinic.zip` |
| 📚 Library | `templates_library.zip` |
| 🏋️ Gym | `templates_gym.zip` |
| 🎓 Course Enrollment | `templates_enrollment.zip` |
| 💰 Budget Tracker | `templates_budget.zip` |

### How to set up your template files — follow these steps exactly

**1. Download** your ZIP from Moodle to your computer.

**2. Extract** the ZIP somewhere **outside** your repo — for example your Desktop or Downloads folder:

```
Desktop/
└── templates_clinic/        ← extract here, outside the repo
    ├── home.html
    └── patient.html
```

**3. Create** the `templates/` folder inside your project if it does not exist yet:

```bash
mkdir mini-project-1/templates
```

**4. Copy** the two HTML files from the extracted folder into your `templates/` folder:

```
fastapi-journey/
└── mini-project-1/
    └── templates/
        ├── home.html        ← copied from the extracted ZIP
        └── patient.html     ← copied from the extracted ZIP (name depends on your domain)
```

**5. Delete** the ZIP file and the extracted folder from your Desktop — they are not needed anymore.

> ⚠️ **Never drag the ZIP file into your repo. Never push `.zip` files to GitHub.**  
> Only the two `.html` files inside `templates/` should ever be committed.  
> A `.zip` file found anywhere in your repository is an **automatic fail**.

---

## 📁 New Folder Structure

After Step 0, your `mini-project-1/` folder must match this structure exactly:

```
mini-project-1/
├── main.py
├── models.py
├── {router_file}.py
└── templates/
    ├── home.html
    └── {item_template}.html
```

The `{router_file}` and `{item_template}` names depend on your assigned domain — see the naming table below.

---

## 🏷️ Domain Naming Convention

Every domain has a **fixed router file name**, **router variable name**, and **item template name**. You must follow these exactly — no variations accepted.

| Domain | Router File | Router Variable | Item Template |
|---|---|---|---|
| 🏥 Clinic | `patient.py` | `patient_router` | `patient.html` |
| 📚 Library | `book.py` | `book_router` | `book.html` |
| 🏋️ Gym | `member.py` | `member_router` | `member.html` |
| 🎓 Course Enrollment | `enrollment.py` | `enrollment_router` | `enrollment.html` |
| 💰 Budget Tracker | `transaction.py` | `transaction_router` | `transaction.html` |

> ⚠️ Using the wrong file name, wrong variable name, or wrong template name is an automatic fail. Copy your values from the table above — do not invent your own.

---

## 📋 Requirement 1 — Restructure into APIRouter

### `main.py` — Entry Point Only

`main.py` must now serve as the **entry point only**. It must not contain any endpoint logic from your domain. Its only responsibilities are:

- Creating the FastAPI app instance
- Serving the root route `GET /`
- Importing and registering your router

```python
from fastapi import FastAPI
from {router_file} import {router_variable}

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to the {Domain} API"}

app.include_router({router_variable})
```

Replace `{router_file}`, `{router_variable}`, and `{Domain}` with the values from your domain row in the naming table above.

---

### `{router_file}.py` — All Your Endpoint Logic

All five endpoints from Mini Project 1 (`GET /items/`, `GET /items/{id}`, `POST /items/`, `PUT /items/{id}`, `DELETE /items/{id}`) must be moved into this file and attached to an `APIRouter` instance.

The router must be declared at the top of the file like this:

```python
from fastapi import APIRouter, HTTPException
from models import YourModel

{router_variable} = APIRouter()
```

All endpoints are then defined using `@{router_variable}.get(...)`, `@{router_variable}.post(...)`, etc. instead of `@app.get(...)`.

---

### `models.py` — Unchanged

Your Pydantic models stay in `models.py` exactly as before. No changes required here beyond what is needed for Requirement 2.

---

## 📋 Requirement 2 — Replace Default Responses with HTTP Exceptions

In Mini Project 1, when an item was not found you returned a plain dictionary like:

```python
return {"message": "Item not found"}
```

This must now be replaced with a proper `HTTPException` in **every endpoint** where a not-found or invalid condition can occur.

### Rules

- Use `HTTPException` with `status_code=404` when an item is not found by ID
- Use `HTTPException` with `status_code=400` for invalid input that passes Pydantic but fails business logic
- The `detail` field must be a meaningful message — not just `"Not found"`

### Example — Before (Mini Project 1)

```python
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    return {"message": "Patient not found"}
```

### Example — After (This Update)

```python
@patient_router.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(
        status_code=404,
        detail=f"Patient with ID {patient_id} was not found"
    )
```

### Where HTTPException is required

| Endpoint | Condition | Status Code |
|---|---|---|
| `GET /items/{id}` | ID does not exist | 404 |
| `PUT /items/{id}` | ID does not exist | 404 |
| `DELETE /items/{id}` | ID does not exist | 404 |

---

## 📋 Requirement 3 — Jinja2 Templating

### Setup

Install the required dependency:

```bash
pip install jinja2 python-multipart
```

### Template Files

You already copied your two HTML files from Moodle into `mini-project-1/templates/` in Step 0. If you have not done this yet, go back to Step 0 before continuing.

The files are provided as a **starting point only**. You must open them and adapt them to match your own code — specifically the field names you used in your Pydantic models. The comments inside the HTML files will guide you on exactly what to change.

### What You Must Implement

Add the following to your `{router_file}.py`:

**1. Set up the Jinja2 template engine** at the top of your router file:

```python
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

{router_variable} = APIRouter()

templates = Jinja2Templates(directory="mini-project-1/templates")
```

**2. Add a `GET /home` HTML route** that renders `home.html` and passes the full list of items as context:

```python
@{router_variable}.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "items": your_mock_database
    })
```

**3. Add a `GET /{domain}/{id}` HTML route** that renders the item template for a single item:

```python
@{router_variable}.get("/{domain}/{id}", response_class=HTMLResponse)
async def get_item_page(request: Request, id: int):
    for item in your_mock_database:
        if item["id"] == id:
            return templates.TemplateResponse("{item_template}.html", {
                "request": request,
                "item": item
            })
    raise HTTPException(status_code=404, detail="Item not found")
```

Replace all `{placeholders}` with the values from your domain row in the naming table.

### Template Context Variables

The variable names you pass inside `TemplateResponse` must match exactly what the HTML templates expect:

| Domain | List variable | Single item variable | URL path |
|---|---|---|---|
| 🏥 Clinic | `patients` | `patient` | `/patient/{id}` |
| 📚 Library | `books` | `book` | `/book/{id}` |
| 🏋️ Gym | `members` | `member` | `/member/{id}` |
| 🎓 Course Enrollment | `enrollments` | `enrollment` | `/enrollment/{id}` |
| 💰 Budget Tracker | `transactions` | `transaction` | `/transaction/{id}` |

> ⚠️ If your variable names do not match, the templates will render blank. This is an automatic fail.

---

## 💾 How to Commit — One Requirement at a Time

Push to the **same branch** you used for Mini Project 1. Each requirement must have its own commit.

```bash
# After restructuring into router file + updated main.py
git add mini-project-1/main.py mini-project-1/book.py
git commit -m "mini-project-1: refactor into APIRouter"

# After replacing all return dicts with HTTPException
git add mini-project-1/book.py
git commit -m "mini-project-1: replace default responses with HTTPException"

# After adding templates folder and Jinja2 routes
git add mini-project-1/templates/ mini-project-1/book.py
git commit -m "mini-project-1: add Jinja2 templating"
```

When done, push:

```bash
git push origin {your-branch-name}
```

> Your branch name is the same one you used for Mini Project 1 — do not create a new branch.

---

## 📁 Final Expected Structure

```
fastapi-journey/
└── mini-project-1/
    ├── main.py                  ← entry point only, no domain logic
    ├── models.py                ← Pydantic models (unchanged)
    ├── {router_file}.py         ← all endpoint logic + Jinja2 routes
    └── templates/
        ├── home.html            ← copied from your domain ZIP (Moodle)
        └── {item_template}.html ← copied from your domain ZIP (Moodle)
```

> ⚠️ The `.zip` file must **not** appear anywhere in your repo.

---

## 🏷️ Quick Reference — Your Domain

| Domain | Router File | Router Variable | Templates |
|---|---|---|---|
| 🏥 Clinic | `patient.py` | `patient_router` | `home.html` + `patient.html` |
| 📚 Library | `book.py` | `book_router` | `home.html` + `book.html` |
| 🏋️ Gym | `member.py` | `member_router` | `home.html` + `member.html` |
| 🎓 Course Enrollment | `enrollment.py` | `enrollment_router` | `home.html` + `enrollment.html` |
| 💰 Budget Tracker | `transaction.py` | `transaction_router` | `home.html` + `transaction.html` |

---

## 📬 Submission

Your branch is already submitted from Mini Project 1. After pushing your new commits, your Moodle submission link remains the same — no new submission is needed unless the link has changed.

If you need to resubmit:

```
https://github.com/<your-username>/fastapi-journey/tree/<your-branch-name>
```

---

## 🎯 Grading

This is a **Pass or Fail** assignment — you either receive the **full grade or nothing**. There is no partial credit.

### ✅ To pass, all criteria must be met:

| # | Criteria | Details |
|---|----------|---------|
| 1 | **APIRouter correctly used** | All domain endpoints are in `{router_file}.py` and registered in `main.py` via `include_router` |
| 2 | **Correct file and variable names** | File name, router variable, and template names must match the naming table exactly |
| 3 | **HTTPException used everywhere** | No endpoint returns a plain `{"message": "not found"}` — all not-found cases use `raise HTTPException` |
| 4 | **Templates render correctly** | `/home` and `/{domain}/{id}` return HTML using the provided templates |
| 5 | **Correct context variables** | Template context uses the exact variable names from the context table |
| 6 | **Commits are separated** | Each requirement has its own commit — one commit for all changes is a fail |
| 7 | **No ZIP files in repo** | The `.zip` file from Moodle must never be committed or pushed |
| 8 | **No AI-generated code** | Code must be written by you |

### ❌ You will automatically fail if:
- `main.py` contains domain endpoint logic
- Router file or variable name does not match the naming table
- Any not-found case still returns a plain dict instead of `HTTPException`
- `templates/` folder is missing or template files are renamed
- Template routes render blank because context variable names are wrong
- A `.zip` file is found anywhere in your repository
- All changes are pushed in a single commit

### ⏰ Deadline
Late submissions are **not accepted** under any circumstances.

---

*SFWE477 · Final International University*



