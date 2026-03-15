# ============================================================
# Practice 3 — Defining the Root Endpoint
# ============================================================
# In this practice you will:
#   1. Import FastAPI and create an app instance
from fastapi import FastAPI
app = FastAPI()
#   2. Define a GET endpoint at the root path "/"
@app.get("/")
def read_root():
    return {"message": "Greetings from your FastAPI spaceship!"}
#   3. Return a JSON welcome message
#
# To run:
#   uvicorn practice3:app --port 8000 --reload
#
# Then open your browser at: http://127.0.0.1:8000/
#
# Expected response:
#   {"message": "Greetings from your FastAPI spaceship!"}
# ============================================================


# TODO: Import FastAPI from fastapi


# TODO: Initialize a FastAPI app instance


# TODO: Define a root endpoint using @app.get("/")
#       The function should return:
#       {"message": "Greetings from your FastAPI spaceship!"}
