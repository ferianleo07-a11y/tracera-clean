from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class SkillCategoryEnum(str, Enum):
    TECHNICAL = "Technical & Engineering"
    SOFT = "Soft Skills & Leadership"
    BUSINESS = "Business & Product Strategy"
    TOOLS = "Tools & Software Platforms"
    OTHER = "Other Skills"

class SkillModel(BaseModel):
    name: str = Field(..., description="Nama kanonikal keahlian")
    category: SkillCategoryEnum = Field(default=SkillCategoryEnum.TECHNICAL)
    is_soft: bool = Field(default=False, description="Flag penanda Soft Skill vs Hard Skill")
    endorsements_count: int = Field(default=0, ge=0)
    alumni_holder_count: int = Field(default=0, ge=0)

class SkillFrequencyModel(BaseModel):
    skill_name: str
    frequency: int
    is_soft: bool = False
    average_endorsements: float = 0.0