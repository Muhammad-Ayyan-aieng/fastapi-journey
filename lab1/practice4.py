# ============================================================
# Practice 4 — Path & Query Parameters
# ============================================================

from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob",   "role": "Scientist"},
]


# Get all crew members
@app.get("/crew")
def read_crew():
    return {"crew": crew}


# ============================================================
# PATH Parameter Endpoint
# Example:
#   http://127.0.0.1:8000/crew_with_path/1
# ============================================================

@app.get("/crew_with_path/{crew_id}")
def crew_with_path(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            return member
    return {"message": "Crew member not found"}


# ============================================================
# QUERY Parameter Endpoint
# Example:
#   http://127.0.0.1:8000/crew_with_query/member?crew_id=1
# ============================================================

@app.get("/crew_with_query/member")
def crew_with_query(crew_id: int):
    for member in crew:
        if member["id"] == crew_id:
            return member
    return {"message": "Crew member not found"}