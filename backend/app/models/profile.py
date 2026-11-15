from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ExperienceItem(BaseModel):
    year: int = Field(..., ge=1980, le=2027, description="Tahun mulai posisi kerja")
    title: str = Field(..., description="Nama posisi atau jabatan bersih")
    company: Optional[str] = Field(default="", description="Nama institusi perusahaan")

class SkillEntry(BaseModel):
    name: str = Field(..., description="Nama keahlian hasil normalisasi kanonikal")
    endorsements: int = Field(default=0, ge=0, description="Jumlah validasi rekan kerja")

class ProfileModel(BaseModel):
    public_identifier: str = Field(..., description="ID unik profil LinkedIn")
    industry: str = Field(default="Other", description="Kategori industri utama")
    universities: List[str] = Field(default_factory=list, description="Daftar perguruan tinggi")
    study_programs: List[str] = Field(default_factory=list, description="Daftar program studi")
    target_role: str = Field(default="Professional", description="Jabatan terakhir atau target")
    skills: List[SkillEntry] = Field(default_factory=list, description="Daftar keahlian unik & validasi")
    experiences: List[ExperienceItem] = Field(default_factory=list, description="Riwayat pengalaman kerja")
    latest_work_year: Optional[int] = Field(default=None, description="Tahun kerja paling mutakhir")
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "public_identifier": "alumni-ugm-001",
                "industry": "Information Technology",
                "universities": ["Universitas Gadjah Mada"],
                "study_programs": ["Ilmu Komputer"],
                "target_role": "Data Engineer",
                "skills": [
                    {"name": "Python", "endorsements": 12},
                    {"name": "Data Analysis", "endorsements": 8}
                ],
                "experiences": [{"year": 2024, "title": "Data Engineer", "company": "Tech Corp"}],
                "latest_work_year": 2024
            }
        }
    }