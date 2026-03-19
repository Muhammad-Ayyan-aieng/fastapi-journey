from pydantic import BaseModel, field_validator
from enum import Enum
from typing import Optional

class Department(str, Enum):
    """Enum for restricting book departments/subjects"""
    MATHEMATICS = "Mathematics"
    COMPUTER_SCIENCE = "Computer Science"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    PSYCHOLOGY = "Psychology"
    SOFTWARE_ENGINEERING = "Software Engineering"
    PHYSICS = "Physics"
    LAW = "Law"
    BUSINESS = "Business"
    ENGINEERING = "Engineering"
    MEDICINE = "Medicine"

class Books(BaseModel):
    id: int
    title: str
    author: str
    year: int
    publisher: str
    professor: str
    department: Optional[Department] = Department.COMPUTER_SCIENCE
    rating: Optional[float] = 0.0
    
    # String length validation
    @field_validator("title", "author", "publisher", "professor")
    @classmethod
    def validate_string_length(cls, value: str) -> str:
        if len(value.strip()) < 2:
            raise ValueError("Field must be at least 2 characters")
        if len(value) > 200:
            raise ValueError("Field must be less than 200 characters")
        return value.strip()
    
    # Year validation
    @field_validator("year")
    @classmethod
    def validate_year(cls, year: int) -> int:
        if year < 1900 or year > 2026:
            raise ValueError(f"Year {year} must be between 1900 and 2026")
        return year
    
    # ISBN validation
    @field_validator("id")
    @classmethod
    def validate_isbn(cls, id: int) -> int:
        if id < 1_000_000_000_000 or id > 9_999_999_999_999:
            raise ValueError(f"ID {id} must be a 13-digit ISBN number")
        return id
    
    # Rating validation
    @field_validator("rating") 
    @classmethod
    def validate_rating(cls, rating: float) -> float:
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        return rating