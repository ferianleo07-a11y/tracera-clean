import os
import re
from datetime import datetime, timezone
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv

from backend.utils.skill_cleaner import (
    normalize_skill, clean_job_title, normalize_target_role,
    clean_universities, clean_indonesian_university, normalize_industry,
    normalize_study_program
)

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'tracera')
RAW_COLLECTION = os.getenv('COLLECTION_NAME', 'raw_linkedin')
PROCESSED_COLLECTION = os.getenv('PROCESSED_COLLECTION_NAME', 'profiles_db')

def parse_and_clean_document(doc):
    """Membersihkan dan memvalidasi satu dokumen alumni dari raw_linkedin."""
    if not doc or not isinstance(doc, dict):
        return None

    raw_list = doc.get('raw_data', [{}])
    p = raw_list[0] if isinstance(raw_list, list) and len(raw_list) > 0 else {}

    pid = p.get('publicIdentifier')
    if not pid or not isinstance(pid, str) or not pid.strip():
        return None

    raw_exps = p.get('experience', [])
    experiences = []
    years = []
    exp_candidates = []
    for e in raw_exps:
        pos_raw = (e.get('position') or '').strip()
        yr = e.get('startDate', {}).get('year') if isinstance(e.get('startDate'), dict) else None
        yr_int = int(yr) if yr and str(yr).isdigit() else None
        if pos_raw:
            exp_candidates.append((yr_int if yr_int and 1980 <= yr_int <= 2027 else 9999, pos_raw))
        if yr_int and 1980 <= yr_int <= 2027:
            years.append(yr_int)
            clean_title = clean_job_title(pos_raw)
            experiences.append({
                'year': yr_int,
                'title': clean_title,
                'company': (e.get('companyName') or '').strip()
            })

    if exp_candidates:
        if all(c[0] == 9999 for c in exp_candidates):
            earliest_pos = exp_candidates[-1][1]
        else:
            earliest_pos = min(exp_candidates, key=lambda x: x[0])[1]
        starting_role = normalize_target_role(clean_job_title(earliest_pos))
    else:
        starting_role = None

    ind = p.get('industry')
    ind_name = ind.get('name') if isinstance(ind, dict) else (ind or 'Other')
    ind_clean = ind_name.strip() if isinstance(ind_name, str) and ind_name.strip() else 'Other'

    fa = doc.get('metadata', {}).get('fetched_at')
    try:
        fetched_dt = datetime.fromisoformat(fa) if fa else datetime.now(timezone.utc)
    except Exception:
        fetched_dt = datetime.now(timezone.utc)

    skill_map = {}
    for s in p.get('skills', []):
        if isinstance(s, dict) and s.get('name'):
            s_raw = s['name'].strip()
            s_norm = normalize_skill(s_raw)
            if len(s_norm) > 1:
                raw_end = s.get('endorsements')
                num_end = int(re.search(r'(\d+)', str(raw_end)).group(1)) if raw_end and re.search(r'(\d+)', str(raw_end)) else 0
                key = s_norm.lower()
                if key not in skill_map or num_end > skill_map[key]['endorsements']:
                    skill_map[key] = {'name': s_norm, 'endorsements': num_end}

    for s_top in (p.get('topSkills') or []):
        if isinstance(s_top, str) and len(s_top.strip()) > 1:
            s_norm = normalize_skill(s_top)
            key = s_norm.lower()
            if key not in skill_map:
                skill_map[key] = {'name': s_norm, 'endorsements': 0}

    raw_schools = []
    study_programs = []
    uni_grad_years = []
    all_grad_years = []
    for edu in p.get('education', []):
        school = edu.get('schoolName')
        if school and isinstance(school, str) and school.strip():
            raw_schools.append(school.strip())
        ed = edu.get('endDate')
        grad_yr = None
        if isinstance(ed, dict) and ed.get('year') and str(ed.get('year')).isdigit():
            grad_yr = int(ed['year'])
        elif isinstance(ed, (int, str)) and str(ed).isdigit():
            grad_yr = int(ed)
        if grad_yr and 1980 <= grad_yr <= 2027:
            all_grad_years.append(grad_yr)
            if school and isinstance(school, str) and clean_indonesian_university(school.strip()):
                uni_grad_years.append(grad_yr)
        fos = edu.get('fieldOfStudy')
        if fos and isinstance(fos, str):
            fos_clean = fos.strip()
            if len(fos_clean) > 2 and fos_clean.lower() not in ['-', '.', '...', 'null', 'none']:
                if fos_clean not in study_programs:
                    study_programs.append(fos_clean)

    graduation_year = max(uni_grad_years) if uni_grad_years else (max(all_grad_years) if all_grad_years else None)
    universities = clean_universities(raw_schools)
    target_role = normalize_target_role(experiences[0]['title']) if experiences else 'Software Engineer'
    final_starting_role = starting_role if starting_role else target_role
    canonical_industry = normalize_industry(ind_clean, target_role, final_starting_role)
    canonical_study_prog = normalize_study_program(study_programs, target_role, final_starting_role)

    return {
        'public_identifier': pid.strip(),
        'industry': canonical_industry,
        'universities': universities if universities else ['Universitas Gadjah Mada'],
        'study_programs': [canonical_study_prog],
        'target_role': target_role,
        'starting_role': final_starting_role,
        'graduation_year': graduation_year,
        'fetched_at': fetched_dt,
        'skills': list(skill_map.values()),
        'experiences': experiences,
        'latest_work_year': max(years, default=None),
        'updated_at': datetime.now(timezone.utc)
    }

def run_cleaning_pipeline():
    """Mengeksekusi pembersihan batch dan upsert ke koleksi profiles_db."""
    if not MONGO_URI:
        raise ValueError("MONGO_URI belum dikonfigurasi dalam .env!")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    raw_coll = db[RAW_COLLECTION]
    proc_coll = db[PROCESSED_COLLECTION]

    print(f"[*] Membaca data mentah dari {RAW_COLLECTION}...")
    raw_cursor = raw_coll.find({})
    cleaned_count = 0
    bulk_ops = []

    for doc in raw_cursor:
        clean_data = parse_and_clean_document(doc)
        if clean_data:
            bulk_ops.append(
                UpdateOne(
                    {'public_identifier': clean_data['public_identifier']},
                    {'$set': clean_data},
                    upsert=True
                )
            )
            cleaned_count += 1

        if len(bulk_ops) >= 500:
            proc_coll.bulk_write(bulk_ops)
            bulk_ops = []

    if bulk_ops:
        proc_coll.bulk_write(bulk_ops)

    # Indeksasi untuk performa agregasi
    proc_coll.create_index('public_identifier', unique=True)
    proc_coll.create_index('industry')
    proc_coll.create_index('universities')
    proc_coll.create_index('study_programs')
    proc_coll.create_index('target_role')
    proc_coll.create_index('starting_role')
    proc_coll.create_index('graduation_year')
    proc_coll.create_index('latest_work_year')

    print(f"[OK] Berhasil memproses dan menyimpan {cleaned_count} profil bersih ke '{PROCESSED_COLLECTION}'.")

if __name__ == '__main__':
    run_cleaning_pipeline()