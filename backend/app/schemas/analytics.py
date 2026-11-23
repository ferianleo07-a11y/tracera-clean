from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class KPIMetricsResponse(BaseModel):
    matched_alumni: int = Field(..., description="Total alumni yang lolos kriteria filter kohor")
    total_unique_skills: int = Field(..., description="Total jenis keahlian unik dalam kohort")
    skill_type_ratio: str = Field(..., description="Rasio keahlian Hard Skills vs Soft Skills (e.g., '72% : 28%')")
    trending_skills_count: int = Field(..., description="Keahlian baru era terkini (MoM Growth)")
    mom_growth_str: str = Field(default="+18% MoM", description="String pertumbuhan MoM")
    avg_skills_per_profile: float = Field(default=8.1)
    top_endorsed_skills: int = Field(default=740)

class HardSoftBarItem(BaseModel):
    rank: int
    skill_name: str
    count: int
    percentage: float
    endorsements: int
    demand_badge: str     
    bar_color: str         

class HardSoftSkillsResponse(BaseModel):
    hard_skills: List[HardSoftBarItem]
    soft_skills: List[HardSoftBarItem]
    hard_summary: str = "72% of skill ecosystem (Average 8.1 per profile)"
    soft_summary: str = "28% of skill ecosystem (Average 3.2 per profile)"

class CategoryDistributionItem(BaseModel):
    category: str
    percentage: float
    total: int
    subcategories: Dict[str, int]

class SkillsDistributionResponse(BaseModel):
    categories: List[CategoryDistributionItem]
    total_skills_count: int = 2850
    unique_skills_count: Optional[int] = None  # Field dinamis unique skills

class NetworkNode(BaseModel):
    id: str
    label: str
    category: str
    dimension: str
    endorsements: int
    frequency: int
    pct: float
    size: float
    color: str
    x: float
    y: float

class NetworkEdge(BaseModel):
    source: str
    target: str
    weight: float

class SkillNetworkResponse(BaseModel):
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]
    central_hub: str = "Python"

class TrendingGapItem(BaseModel):
    no: str
    skill_name: str
    skill_type: str       
    alumni_count: int
    alumni_pct: float
    trend_30d_pct: float   
    market_demand_pct: float
    gap_score: float       
    gap_status: str        
    target_roles: List[str]

class TrendingGapResponse(BaseModel):
    items: List[TrendingGapItem]
    total_job_postings_analyzed: int = 1200
    summary_insights: Dict[str, Any]

class FilterOptionsResponse(BaseModel):
    universities: List[str]
    study_programs: List[str]
    target_roles: List[str]
    industries: List[str]
    graduation_years: List[str] = []
    starting_roles: List[str] = []
    career_levels: List[str]
    locations: List[str]

class FullDashboardResponse(BaseModel):
    kpi: KPIMetricsResponse
    hard_soft_skills: HardSoftSkillsResponse
    skills_distribution: SkillsDistributionResponse
    skill_network: SkillNetworkResponse
    trending_gap: TrendingGapResponse

class MicroSummaryMetrics(BaseModel):
    matched_alumni: int
    skill_type_ratio: str          
    market_alignment_pct: float    
    market_alignment_label: str    
    highest_velocity_skill: str    

class ComparisonSkillItem(BaseModel):
    rank: int
    skill_name: str
    count: int
    percentage: float
    demand_badge: str
    badge_type: str

class SignatureSkillItem(BaseModel):
    skill_name: str
    diff_pct: str
    delta_vs_cohort: Optional[float] = 0.0

class ExecutiveTakeawayItem(BaseModel):
    title: str
    description: str
    card_type: str = "default"

class UniversityComparisonCard(BaseModel):
    university_name: str
    micro_summary: MicroSummaryMetrics
    top_hard_skills: List[ComparisonSkillItem]
    top_soft_skills: List[ComparisonSkillItem]
    signature_skills: List[SignatureSkillItem]

class SkillsComparisonResponse(BaseModel):
    selected_universities: List[str]
    comparison_cards: List[UniversityComparisonCard]
    executive_takeaways: Optional[List[ExecutiveTakeawayItem]] = []