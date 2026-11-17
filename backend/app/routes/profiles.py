# Profile Query &amp; CSV Streaming Export

import io
import csv
from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.app.core.database import get_database
from backend.app.core.config import settings
from backend.app.crud.analytics import build_filter_query
router = APIRouter(prefix="/profiles", tags=["Profiles"])
@router.get("/export/download")
async def download_csv_file(
    university: Optional[str] = Query(None),
    study_program: Optional[str] = Query(None),
    target_role: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Streaming CSV download untuk tombol Export CSV di Header Dashboard."""
    query = build_filter_query(university, study_program, target_role, industry)
    coll = db[settings.PROCESSED_COLLECTION_NAME]
    cursor = coll.find(query)
    async def csv_generator():
        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(["Public Identifier", "Industry", "Universities", "Study Programs", "Target Role", "Latest Work Year", "Skills List"])
        yield stream.getvalue()
        stream.seek(0)
        stream.truncate(0)
        async for doc in cursor:
            skills_str = "; ".join([s.get('name', '') for s in doc.get('skills', [])])
            unis_str = "; ".join(doc.get('universities', []))
            progs_str = "; ".join(doc.get('study_programs', []))
            writer.writerow([
                doc.get('public_identifier', ''),
                doc.get('industry', ''),
                unis_str,
                progs_str,
                doc.get('target_role', ''),
                doc.get('latest_work_year', ''),
                skills_str
            ])
            yield stream.getvalue()
            stream.seek(0)
            stream.truncate(0)
    return StreamingResponse(
        csv_generator(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=skills_intelligence_export.csv"}
    )