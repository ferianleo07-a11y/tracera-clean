# Skills Intelligence - Tracera Analytics Ecosystem (OJT 2026 UGM STP)

Sistem analitik kompetensi alumni terintegrasi berbasis arsitektur REST API **FastAPI** (Backend) dan dashboard interaktif **Streamlit** (Frontend) dengan basis data NoSQL **MongoDB Atlas**.
Antarmuka dashboard (UI) disajikan dalam standar bahasa Inggris profesional (Clean Light Mode).

## Arsitektur & Alur Data End-to-End

1. **Data Ingestion**: Scraper mengekstraksi profil alumni mentah dari LinkedIn ke MongoDB Atlas koleksi `raw_linkedin`.
2. **Data Cleansing**: Batch cleaner membersihkan noise jabatan, memvalidasi rentang tahun (1980–2027), mengekstrak nama universitas, dan melakukan upsert ke koleksi terindeks `profiles_db`.
3. **Skill Normalization**: Pemetaan 150+ keahlian bilingual (Indo -&gt; Eng) serta taksonomi resmi 35+ Soft Skills kanonikal.
4. **Analytics Engine**: Perhitungan 4 metrik KPI, dual progress bar Hard vs Soft Skills, stacked bar 4 kategori keahlian, graf jejaring ko-okurensi NetworkX, analisis kesenjangan pasar (Market Gap), serta modul komparasi multi-universitas (Skills Comparison).
5. **REST API**: Endpoint FastAPI asinkron terproteksi header otorisasi `X-API-KEY`.
6. **Frontend Dashboard**: Antarmuka Streamlit Clean Light Mode dengan visualisasi Plotly interaktif, 3 Tab (Skills Explorer, Skills Comparison, Skill Details), Sub-view Toggle (Ranking vs Ecosystem), Reset, Export CSV, dan Share View copy link.

## Pembagian Peran Anggota Tim

- **Orang 1 (Data Engineer & Data Cleaning)**: Koneksi & ekstraksi `database_connection.py`, `clean_raw_data.py`, `skill_cleaner.py`, `database.py` & models.
- **Orang 2 (Data Analyst ‐ Pilar 1, 2, 3 Analyst)**: DTO response, agregasi MongoDB analitik, formula market gap & visualizer chart Plotly/Tab 2.
- **Orang 3 (Backend Lead)**: Arsitektur REST API FastAPI, APIRouter endpoints, middleware keamanan, Pydantic settings, dan server lifespan.
- **Orang 4 (Frontend Lead)**: Proteksi Git, HTTP client caching, shell UI Streamlit (header, filter, card KPI), dan orkestrasi 3 Tab `app.py`.

## Panduan Instalasi & Menjalankan Aplikasi

Jalankan _Backend_ dan _Frontend_ pada dua jendela terminal terpisah agar keduanya berjalan bersamaan.

### Opsi 1: Windows PowerShell

```powershell
# ==========================================
# LANGKAH A: SETUP BACKEND (Terminal PowerShell 1)
# ==========================================
# 1. Masuk ke direktori backend
cd my_project/backend

# 2. Buat virtual environment baru khusus backend
python -m venv .venv

# 3. Berikan izin eksekusi script PowerShell jika dibatasi (ExecutionPolicy)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 4. Aktivasi virtual environment backend
.\.venv\Scripts\Activate.ps1

# 5. Perbarui pip dan pasang seluruh dependensi backend
python -m pip install --upgrade pip
pip install -r requirements.txt

# 6. Salin template konfigurasi dan sesuaikan kredensial MongoDB Atlas Anda
copy .env.example .env

# 7. Jalankan server backend FastAPI pada port 8000 dengan fitur reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Verifikasi Endpoint Backend:
# - API Health: http://localhost:8000/health
# - Swagger UI: http://localhost:8000/docs
# - Redoc UI:   http://localhost:8000/redoc


# ==========================================
# LANGKAH B: SETUP FRONTEND (Terminal PowerShell 2 - buka jendela baru)
# ==========================================
# 1. Masuk ke direktori frontend (pastikan berada di root proyek terlebih dahulu jika perlu)
cd my_project/frontend

# 2. Buat virtual environment baru khusus frontend
python -m venv .venv

# 3. Berikan izin eksekusi script PowerShell jika dibatasi (ExecutionPolicy)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 4. Aktivasi virtual environment frontend
.\.venv\Scripts\Activate.ps1

# 5. Perbarui pip dan pasang dependensi antarmuka frontend
python -m pip install --upgrade pip
pip install -r requirements.txt

# 6. Salin konfigurasi environment frontend dan sesuaikan URL API backend jika diperlukan
copy .env.example .env

# 7. Jalankan aplikasi Streamlit pada port 8501
streamlit run app.py --server.port 8501

# Verifikasi Tampilan Frontend:
# - Buka peramban pada: http://localhost:8501
# - Pastikan status antarmuka bersih dan visualisasi ter-render dengan sempurna
```
