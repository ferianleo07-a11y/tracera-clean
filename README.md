# Skills Intelligence - Tracera Analytics Ecosystem (OJT 2026 UGM STP)

Sistem analitik kompetensi alumni terintegrasi berbasis arsitektur REST API **FastAPI** (Backend) dan dashboard interaktif **Streamlit** (Frontend) dengan basis data NoSQL **MongoDB Atlas**.
Antarmuka dashboard (UI) disajikan dalam standar bahasa Inggris profesional (Clean Light Mode).

## Arsitektur & Alur Data End-to-End

1. **Data Ingestion**: Scraper mengekstraksi profil alumni mentah dari LinkedIn ke MongoDB Atlas koleksi `raw_linkedin`.
2. **Data Cleansing**: Batch cleaner membersihkan noise jabatan, memvalidasi rentang tahun (1980–2027), mengekstrak nama universitas, dan melakukan upsert ke koleksi terindeks `profiles_db`.
3. **Skill Normalization**: Pemetaan 150+ keahlian bilingual (Indo -&gt; Eng) serta taksonomi resmi 35+ Soft Skills kanonikal.
4. **Analytics Engine**: Perhitungan 4 metrik KPI, dual progress bar Hard vs Soft Skills, stacked bar 4 kategori keahlian, graf jejaring ko-okurensi NetworkX, analisis kesenjangan pasar (Mark
   et Gap), serta modul komparasi multi-universitas (Skills Comparison).
5. **REST API**: Endpoint FastAPI asinkron terproteksi header otorisasi `X-API-KEY`.
6. **Frontend Dashboard**: Antarmuka Streamlit Clean Light Mode dengan visualisasi Plotly interaktif, 3 Tab (Skills Explorer, Skills Comparison, Skill Details), Sub-view Toggle (Ranking vs Ec
   osystem), Reset, Export CSV, dan Share View copy link.

## Pembagian Peran Anggota Tim

- **Orang 3 (Backend Lead)**: Arsitektur REST API FastAPI, APIRouter endpoints, middleware keamanan, Pydantic settings, dan server lifespan.

## Panduan Cepat Menjalankan Sistem

1. Setup Backend: `cd backend &amp;&amp; python -m venv .venv &amp;&amp; .\.venv\Scripts\Activate.ps1 &amp;&amp; pip install -r requirements.txt`
2. Jalankan Backend: `uvicorn app.main:app --reload --port 8000`
3. Setup Frontend: `cd frontend &amp;&amp; python -m venv .venv &amp;&amp; .\.venv\Scripts\Activate.ps1 &amp;&amp; pip install -r requirements.txt`
4. Jalankan Frontend: `streamlit run app.py --server.port 8501`
