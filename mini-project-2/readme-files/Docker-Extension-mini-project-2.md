# SFWE477 — Mini Project 2 (Docker Extension) 🐳

You have already built your FastAPI + MongoDB Event Planner application.  
This extension asks you to **containerise it** — the API and the database both run in Docker, and the whole thing starts with a single command.

No rewriting. No new endpoints. You are wrapping what you already have.

---

## 📚 Resources

| Resource | What it covers | Link |
|----------|----------------|------|
| Running MongoDB with Docker | How to pull the mongo image, run it as a container, and connect to it | [Watch](https://www.youtube.com/watch?v=gFjpv-nZO0U) |
| mongo — Docker Hub official image | Available tags, environment variables, volume configuration | [hub.docker.com/_/mongo](https://hub.docker.com/_/mongo) |
| Docker Compose — getting started | Defining multi-container applications, networks, volumes | [docs.docker.com/compose](https://docs.docker.com/compose/) |
| Dockerfile reference | FROM, WORKDIR, COPY, RUN, EXPOSE, CMD instructions | [docs.docker.com/reference/dockerfile](https://docs.docker.com/reference/dockerfile/) |

---

## 🌿 Branch

Continue working on your existing branch:

```
firstinitial+surname-mini-project-2
```

Do **not** create a new branch. Add the Docker files directly to your `mini-project-2/` folder.

---

## 🗂️ Updated Folder Structure

Your existing code moves into an `app/` subfolder. Three new files are added at the root of `mini-project-2/`:

```
fastapi-journey/
└── mini-project-2/
    ├── app/                      ← move your existing code here
    │   ├── main.py
    │   ├── models/
    │   ├── database/
    │   └── routes/
    ├── Dockerfile                ← new
    ├── docker-compose.yml        ← new
    ├── .dockerignore             ← new
    ├── .env                      ← update DATABASE_URL only
    └── DECISIONS.md              ← add Part B answers
```

> ⚠️ Moving your code into `app/` is the only structural change to your existing work.

---

## ✅ What You Need to Add

### 1. Dockerfile

Create a `Dockerfile` at the `mini-project-2/` root:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 2. docker-compose.yml

Create a `docker-compose.yml` at the `mini-project-2/` root that defines two services — your FastAPI app and MongoDB:

```yaml
services:
  mongo:
    image: mongo:7
    container_name: mongo
    ports:
      - "27017:27017"
    volumes:
      - ./mongo-data:/data/db

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongo
    env_file:
      - .env

networks:
  default:
    name: planner-network
```

---

### 3. Update .env

Change your `DATABASE_URL` to point to the `mongo` container by name — **not** `localhost`:

```
DATABASE_URL=mongodb://mongo:27017/planner
```

> This works because Docker Compose puts both containers on the same network and lets them find each other by service name. Keeping `localhost` here will cause a connection error.

---

### 4. .dockerignore

Create a `.dockerignore` file to keep the image clean:

```
venv/
__pycache__/
.env
*.pyc
*.pyo
```

---

### 5. Verify It Works

Run everything with a single command from inside `mini-project-2/`:

```bash
docker compose up --build
```

Open **http://localhost:8000/docs** — all your existing endpoints must work exactly as before.

Then confirm data persists across restarts:

```bash
docker compose down
docker compose up
```

Data created before the restart must still be there.

---

### 6. Update DECISIONS.md

Add a **Part B** section to your existing `DECISIONS.md` and answer these four questions in your own words:

1. Why does `DATABASE_URL` use `mongo` as the hostname instead of `localhost`? What would happen if you kept `localhost`?
2. What does `depends_on` in `docker-compose.yml` do? Does it guarantee MongoDB is fully ready before FastAPI starts — and if not, what would?
3. What is the purpose of the volume in the `mongo` service? What happens to your data if you remove it and run `docker compose down`?
4. Why do we copy `requirements.txt` and run `pip install` before copying the rest of the app code in the Dockerfile?

> ⚠️ Write from what you observed while doing the project. Generic or AI-sounding answers will not be accepted.

---

## 💾 Commits

Each step must be its own commit:

```bash
git add mini-project-2/app/
git commit -m "mini-project-2: move app code into app/ subfolder"

git add mini-project-2/Dockerfile mini-project-2/docker-compose.yml mini-project-2/.dockerignore
git commit -m "mini-project-2: add Dockerfile and docker-compose"

git add mini-project-2/DECISIONS.md
git commit -m "mini-project-2: update DECISIONS.md with Docker reflection"
```

> ⚠️ Do **not** stage or commit `.env` — it must stay in `.gitignore`. Update the file locally only.

Push when done:
```bash
git push origin jsnow-mini-project-2
```

---

## 📬 Submission

Same Moodle submission link as before — just push to the same branch:

```
https://github.com/<your-username>/fastapi-journey/tree/jsnow-mini-project-2
```

---

## 🎯 Grading

Pass or Fail — same policy as before.

### ✅ To pass:

| # | Criteria | Details |
|---|----------|---------|
| 1 | **Docker works** | `docker compose up --build` starts with no errors, all existing endpoints work, data persists across restarts |
| 2 | **Correct commits** | Each step has its own commit on the existing branch |
| 3 | **DECISIONS.md Part B is genuine** | All 4 answers are specific to your experience, not generic or AI-generated |

### ❌ You will automatically fail if:
- `docker compose up` does not start successfully
- MongoDB runs locally instead of in a container
- `localhost` is used in `DATABASE_URL` instead of the service name
- No volume is defined for the `mongo` service
- `.env` is committed to the repository
- Part B of `DECISIONS.md` is missing or contains generic answers
- All Docker work is in a single commit
- The submission link is not updated on Moodle
