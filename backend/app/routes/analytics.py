# REST API APIRouter Endpoints

from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.app.core.database import get_database
from backend.app.core.config import settings
from backend.app.core.security import verify_api_key
from backend.app.schemas.analytics import (
    FullDashboardResponse, FilterOptionsResponse, KPIMetricsResponse,
    HardSoftSkillsResponse, SkillsDistributionResponse,
    SkillNetworkResponse, TrendingGapResponse, SkillsComparisonResponse
)
from backend.app.crud.analytics import (
    build_filter_query, get_filter_options, calculate_kpi_metrics,
    analyze_hard_vs_soft_skills, analyze_skills_distribution_by_category,
    analyze_skill_network, analyze_trending_gap, calculate_skills_comparison
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])
@router.get("/filters", response_model=FilterOptionsResponse)
async def get_filters_endpoint(
    db: AsyncIOMotorDatabase = Depends(get_database),
    authorized: bool = Depends(verify_api_key)
):
    """Mendapatkan opsi daftar unik University, Study Program, Target Role, dan Industry."""
    data = await get_filter_options(db)
    return FilterOptionsResponse(**data)

@router.get("/dashboard", response_model=FullDashboardResponse)
async def get_full_dashboard(
    university: Optional[str] = Query(None),
    study_program: Optional[str] = Query(None),
    target_role: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_database),
    authorized: bool = Depends(verify_api_key)
):
    """Endpoint utama pengambil seluruh data dashboard secara terpadu."""
    query = build_filter_query(university, study_program, target_role, industry)
    coll = db[settings.PROCESSED_COLLECTION_NAME]
    proj = {
        "skills": 1,
        "universities": 1,
        "study_programs": 1,
        "target_role": 1,
        "industry": 1,
        "latest_work_year": 1
    }
    docs = await coll.find(query, proj).to_list(length=10000)

    kpi = await calculate_kpi_metrics(db, query, docs=docs)
    hard_soft = await analyze_hard_vs_soft_skills(db, query, docs=docs)
    skills_dist = await analyze_skills_distribution_by_category(db, query, docs=docs)
    network = await analyze_skill_network(db, query, docs=docs)
    trending_gap = await analyze_trending_gap(db, query, docs=docs)
    return FullDashboardResponse(
        kpi=KPIMetricsResponse(**kpi),
        hard_soft_skills=HardSoftSkillsResponse(**hard_soft),
        skills_distribution=SkillsDistributionResponse(**skills_dist),
        skill_network=SkillNetworkResponse(**network),
        trending_gap=TrendingGapResponse(**trending_gap)
    )

@router.get("/skills/comparison", response_model=SkillsComparisonResponse)
async def get_skills_comparison_endpoint(
    universities: str = Query("Universitas Gadjah Mada,Universitas Indonesia,Institut Teknologi Bandung"),
    study_program: Optional[str] = Query(None),
    target_role: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_database),
    authorized: bool = Depends(verify_api_key)
):
    """Endpoint komparasi multi-universitas berdampingan secara dinamis dari MongoDB."""
    target_unis = [u.strip() for u in universities.split(",") if u.strip()]
    base_query = build_filter_query(None, study_program, target_role, industry)
    comparison_data = await calculate_skills_comparison(db, target_unis, base_query)
    return SkillsComparisonResponse(**comparison_data)