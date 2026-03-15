from pydantic import BaseModel, field_validator, model_validator
from enum import Enum
from typing import Optional

class Department(str, Enum):
    """Enum for restricting professor department"""
    PUBLIC_LAW = "Public Law"
    PRIVATE_LAW = "Private Law"
    CONSTITUTIONAL_LAW = "Constitutional Law"
    ADMINISTRATIVE_LAW = "Administrative Law"

class Books(BaseModel):
    id: int
    title: str
    author: str
    year: int
    publisher: str
    professor: str
    department: Optional[Department] = Department.PUBLIC_LAW  # Optional with default
    rating: Optional[float] = 0.0  # Optional field with default
    
    # 1. Numeric field with constraints (gt, le)
    @field_validator("year")
    @classmethod
    def validate_year(cls, year: int) -> int:
        if year < 1900 or year > 2026:
            raise ValueError(f"Year {year} must be between 1900 and 2026")
        return year
    
    # 2. Custom model validator for cross-field validation
    @model_validator(mode="after")
    def validate_book(self) -> 'Books':
        # Check if professor name matches title subject area
        # This is a simple example - you can make it more sophisticated
        if "HUKUK" in self.title.upper() and "HUKUK" not in self.professor.upper():
            # Just a warning, not an error - but demonstrates cross-field validation
            print(f"Warning: Professor {self.professor} might not specialize in {self.title}")
        return self
    
    # 3. String field with min/max length
    @field_validator("title", "author", "publisher", "professor")
    @classmethod
    def validate_string_length(cls, value: str) -> str:
        if len(value.strip()) < 2:
            raise ValueError("Field must be at least 2 characters")
        if len(value) > 200:
            raise ValueError("Field must be less than 200 characters")
        return value.strip()
    
    # 4. ISBN validation (numeric constraint)
    @field_validator("id")
    @classmethod
    def validate_isbn(cls, id: int) -> int:
        # ISBN-13 should be exactly 13 digits
        if id < 1_000_000_000_000 or id > 9_999_999_999_999:
            raise ValueError(f"ID {id} must be a 13-digit ISBN number")
        return id
    
    # 5. Rating validation (float with constraints)
    @field_validator("rating")
    @classmethod
    def validate_rating(cls, rating: float) -> float:
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        return rating