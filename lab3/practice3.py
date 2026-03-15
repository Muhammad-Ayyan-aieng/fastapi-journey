from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain", "experience": 10, "specialty": "Leadership"},
    {"id": 2, "name": "Alice", "role": "Engineer", "experience": 8, "specialty": "Mechanical"},
    {"id": 3, "name": "Bob", "role": "Scientist", "experience": 5, "specialty": "Biology"}
]


# TODO: Define a Pydantic model for the crew member with:
# - name
# - role
# - experience
# - specialty

class Crew_Member(BaseModel):
    name: str
    role: str
    experience: int
    specialty: str


# TODO: Define a POST endpoint receiving a crew member model
# Use the code provided in the description to handle the database and response

@app.post("/crew/")
async def add_crew_member(member: Crew_Member):
    # Generating new id
    member_id = max(m["id"] for m in crew) + 1 if crew else 1
    # TODO: Modify the code to create new_member
    data_dict= {"id": member_id, **member.dict() } # or member.model_dump() in newer versions of pydantic
    # Adding new member to database
    crew.append(data_dict)
    # Returning message and new member details
    return {"message": "Crew member added successfully", "details": data_dict}
