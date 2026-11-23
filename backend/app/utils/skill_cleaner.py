import re

# 1. KAMUS TRANSLASI & NORMALISASI SKILLS (Bilingual Indonesian -> English)
SKILL_TRANSLATIONS = {
    # a. Hard Skills - Desain, Media & Kreatif Teknis
    'desain': 'Design',
    'design': 'Design',
    'desain grafis': 'Graphic Design',
    'design grafis': 'Graphic Design',
    'graphic design': 'Graphic Design',
    'pemikiran desain': 'Design Thinking',
    'creative direction': 'Creative Direction',
    'creative strategy': 'Creative Strategy',
    'penulisan': 'Writing',
    'writing': 'Writing',
    'creative writing': 'Creative Writing',
    'penulisan kreatif': 'Creative Writing',
    'report writing': 'Report Writing',
    'penulisan laporan': 'Report Writing',
    'technical writing': 'Technical Writing',
    'penulisan teknis': 'Technical Writing',
    'scientific writing': 'Scientific Writing',
    'penulisan ilmiah': 'Scientific Writing',
    'proposal writing': 'Proposal Writing',
    'penulisan proposal': 'Proposal Writing',

    # b. Hard Skills - Data & Analisis
    'analisis data': 'Data Analysis',
    'analisa data': 'Data Analysis',
    'analisis': 'Data Analysis',
    'analitik data': 'Data Analytics',
    'data analysis': 'Data Analysis',
    'analisis bisnis': 'Business Analysis',
    'business analysis': 'Business Analysis',
    'analisis keuangan': 'Financial Analysis',
    'financial analysis': 'Financial Analysis',
    'analisis sosial': 'Social Analysis',
    'pengolahan data': 'Data Processing',
    'entri data': 'Data Entry',
    'data entry': 'Data Entry',
    'mangalisis suatu proyek': 'Project Analysis',
    'riset': 'Research',
    'penelitian': 'Research',
    'research': 'Research',
    'research skills': 'Research',
    'analytical skills': 'Analytical Skills',
    'keahlian analitis': 'Analytical Skills',
    'analytic problem solving': 'Analytical Skills',

    # c. Hard Skills - Manajemen Proyek, Operasional & IT / Tools
    'manajemen proyek': 'Project Management',
    'project management': 'Project Management',
    'dokumen proyek': 'Project Documentation',
    'manajemen operasional': 'Operations Management',
    'operations management': 'Operations Management',
    'pengembangan web': 'Web Development',
    'manajemen file': 'File Management',
    'sistem informasi geografis (gis)': 'GIS',
    'geographic information systems (gis)': 'GIS',
    'arcgis': 'GIS',
    'sistem manajemen keselamatan dan kesehatan kerja': 'Occupational Health and Safety (OHS)',
    'kesehatan, keselamatan, dan lingkungan (hse)': 'Health, Safety, and Environment (HSE)',
    'peningkatan proses bisnis': 'Business Process Improvement',
    'monitoring dan evaluasi': 'Monitoring & Evaluation',
    'perencanaan strategis': 'Strategic Planning',
    'strategic planning': 'Strategic Planning',
    'manajemen perubahan': 'Change Management',
    'change management': 'Change Management',
    'organizational development': 'Organizational Development',
    'pengembangan organisasi': 'Organizational Development',
    'collaboration solutions': 'Collaboration Tools',
    'python (programming language)': 'Python',
    'go (programming language)': 'Go',
    'golang': 'Go',
    'c (programming language)': 'C',
    'r (programming language)': 'R',
    'java (programming language)': 'Java',
    'powerpoint': 'Microsoft PowerPoint',
    'excel': 'Microsoft Excel',
    'word': 'Microsoft Word',

    # d. Hard Skills - Keuangan, Akuntansi & Hukum Bisnis
    'keuangan': 'Finance',
    'finance': 'Finance',
    'jasa keuangan': 'Financial Services',
    'manajemen keuangan': 'Financial Management',
    'financial management': 'Financial Management',
    'perencanaan keuangan': 'Financial Planning',
    'financial planning': 'Financial Planning',
    'akuntansi': 'Accounting',
    'accounting': 'Accounting',
    'akuntansi keuangan': 'Financial Accounting',
    'financial accounting': 'Financial Accounting',
    'pembukuan': 'Bookkeeping',
    'bookkeeping': 'Bookkeeping',
    'perpajakan': 'Taxation',
    'tax': 'Taxation',
    'taxations': 'Taxation',
    'perencanaan anggaran': 'Budgeting',
    'budgeting': 'Budgeting',
    'budgets': 'Budgeting',
    'budget management': 'Budgeting',
    'auditing': 'Auditing',
    'internal audits': 'Auditing',
    'financial audits': 'Auditing',
    'financial reporting': 'Financial Reporting',
    'financial statements': 'Financial Reporting',
    'mengolah data biaya': 'Cost Accounting',
    'cost accounting': 'Cost Accounting',
    'konsultan manajemen': 'Management Consulting',
    'konsultan lingkungan': 'Environmental Consulting',
    'hukum': 'Legal & Law',
    'negosiasi kontrak': 'Contract Negotiation',
    'contract negotiation': 'Contract Negotiation',

    # e. Hard Skills - Pemasaran, Komunikasi Korporat, Penjualan & SDM
    'pemasaran': 'Marketing',
    'marketing': 'Marketing',
    'pemasaran digital': 'Digital Marketing',
    'pemasaran media sosial': 'Social Media Marketing',
    'social media marketing': 'Social Media Marketing',
    'pemasaran produk': 'Product Marketing',
    'strategi pemasaran': 'Marketing Strategy',
    'marketing strategy': 'Marketing Strategy',
    'strategi konten': 'Content Strategy',
    'content strategy': 'Content Strategy',
    'pengoptimalan media sosial (social media optimization/smo)': 'Social Media Optimization (SMO)',
    'komunikasi merek': 'Brand Communication',
    'brand communication': 'Brand Communication',
    'social media communications': 'Social Media Marketing',
    'hubungan masyarakat': 'Public Relations',
    'public relations': 'Public Relations',
    'penjualan': 'Sales',
    'sales': 'Sales',
    'perencanaan acara': 'Event Planning',
    'event planning': 'Event Planning',
    'event management': 'Event Planning',
    'sumber daya manusia (sdm)': 'Human Resources (HR)',
    'human resources (hr)': 'Human Resources (HR)',
    'human resources': 'Human Resources (HR)',
    'perencanaan sumber daya manusia strategis': 'Strategic Human Resource Planning',
    'administrasi': 'Administration',
    'administration': 'Administration',
    'office administration': 'Administration',
    'administrasi perkantoran': 'Administration',
    'bekerja di shift': 'Shift Work',
    'opname kerja': 'Stock Opname',

    # f. Hard Skills - Bahasa & Pengajaran
    'english': 'English',
    'bahasa inggris': 'English',
    'bahasa indonesia': 'Indonesian',
    'teaching': 'Teaching',
    'pengajaran': 'Teaching',

    # g. Soft Skills - Komunikasi & Interpersonal
    'komunikasi': 'Communication',
    'communication': 'Communication',
    'communications': 'Communication',
    'kemampuan komunikasi': 'Communication',
    'interpersonal communication': 'Communication',
    'written communication': 'Communication',
    'strategic communications': 'Communication',
    'intercultural communication': 'Communication',
    'cross-cultural communication skills': 'Communication',
    'komunikasi interpersonal': 'Communication',
    'komunikasi tertulis': 'Communication',
    'active listening': 'Active Listening',
    'mendengarkan aktif': 'Active Listening',
    'persuasi': 'Persuasion',
    'persuasion': 'Persuasion',
    'layanan pelanggan': 'Customer Service',
    'customer service': 'Customer Service',
    'pelayanan': 'Customer Service',
    'keahlian interpersonal': 'Interpersonal Skills',
    'interpersonal skills': 'Interpersonal Skills',
    'interpersonal': 'Interpersonal Skills',
    'keahlian presentasi': 'Presentation Skills',
    'presentation skills': 'Presentation Skills',
    'presentation': 'Presentation Skills',
    'presentations': 'Presentation Skills',
    'presentasi': 'Presentation Skills',
    'public speaking': 'Public Speaking',
    'berbicara di depan umum': 'Public Speaking',
    'relationship building': 'Relationship Building',
    'membangun relasi': 'Relationship Building',

    # h. Soft Skills - Tim & Kerjasama
    'kerja sama tim': 'Teamwork',
    'kerja tim': 'Teamwork',
    'kerjasama tim': 'Teamwork',
    'kemampuan kerja tim': 'Teamwork',
    'teamwork': 'Teamwork',
    'team work': 'Teamwork',
    'kolaborasi tim': 'Collaboration',
    'collaboration': 'Collaboration',
    'team collaboration': 'Collaboration',
    'cross-team collaboration': 'Collaboration',
    'cross-functional collaborations': 'Collaboration',
    'resolusi konflik': 'Conflict Resolution',
    'conflict resolution': 'Conflict Resolution',
    'conflict management': 'Conflict Resolution',
    'manajemen konflik': 'Conflict Resolution',

    # i. Soft Skills - Kepemimpinan & Manajemen Orang
    'kepemimpinan': 'Leadership',
    'leadership': 'Leadership',
    'team leadership': 'Leadership',
    'kepemimpinan tim': 'Leadership',
    'project leadership': 'Leadership',
    'organizational leadership': 'Leadership',
    'strategic leadership': 'Leadership',
    'cross-functional team leadership': 'Leadership',
    'leadership development': 'Leadership Development',
    'pengembangan kepemimpinan': 'Leadership Development',
    'manajemen tim': 'Team Management',
    'team management': 'Team Management',
    'team coordination': 'Team Management',
    'team building': 'Team Management',
    'team motivation': 'Team Management',
    'people management': 'People Management',
    'manajemen orang': 'People Management',
    'people development': 'People Development',
    'team development': 'People Development',
    'pengembangan tim': 'People Development',
    'coaching': 'Coaching & Mentoring',
    'mentoring': 'Coaching & Mentoring',
    'coaching & mentoring': 'Coaching & Mentoring',
    'training & mentoring': 'Coaching & Mentoring',
    'pelatihan & mentoring': 'Coaching & Mentoring',
    'sales coaching': 'Coaching & Mentoring',
    'kemampuan berorganisasi': 'Organization Skills',
    'organization skills': 'Organization Skills',
    'organizational skills': 'Organization Skills',
    'manajemen': 'Management',
    'management': 'Management',

    # j. Soft Skills - Pemecahan Masalah & Berpikir Kritis
    'pemecahan masalah': 'Problem Solving',
    'memecahkan masalah': 'Problem Solving',
    'problem solving': 'Problem Solving',
    'creative problem solving': 'Problem Solving',
    'collaborative problem solving': 'Problem Solving',
    'team problem solving': 'Problem Solving',
    'berpikir kritis': 'Critical Thinking',
    'critical thinking': 'Critical Thinking',
    'critical thinker': 'Critical Thinking',
    'analytical thinking': 'Critical Thinking',
    'pengambilan keputusan': 'Decision Making',
    'decision making': 'Decision Making',
    'decision-making': 'Decision Making',
    'data-driven decision making': 'Decision Making',
    'strategic thinking': 'Strategic Thinking',
    'creativity': 'Creativity',
    'kreativitas': 'Creativity',
    'creative thinking': 'Creativity',
    'creativity skills': 'Creativity',
    'creativity and innovation': 'Creativity',

    # k. Soft Skills - Manajemen Diri & Sikap Kerja
    'manajemen waktu': 'Time Management',
    'time management': 'Time Management',
    'manajemen diri': 'Self Management',
    'self management': 'Self Management',
    'adaptability': 'Adaptability',
    'adaptable': 'Adaptability',
    'easily adaptable': 'Adaptability',
    'adaptation': 'Adaptability',
    'flexibility': 'Adaptability',
    'negosiasi': 'Negotiation',
    'negotiation': 'Negotiation',
    'negotiation skills': 'Negotiation',
    'emotional intelligence': 'Emotional Intelligence',
    'work ethic': 'Work Ethic',
    'etika kerja': 'Work Ethic',
    'working under pressure': 'Working Under Pressure',
    'bekerja dalam tekanan': 'Working Under Pressure',
    'hard working': 'Work Ethic',
    'bekerja keras': 'Work Ethic',
    'jujur dan disiplin': 'Honesty & Discipline',
    'honesty & discipline': 'Honesty & Discipline',
    'bintal dan jasmani': 'Mental & Physical Discipline',
    'mental & physical discipline': 'Mental & Physical Discipline',
    'organizational culture': 'Organizational Culture'
}

# 2. TAKSONOMI RESMI SOFT SKILLS (Bentuk Kanonikal Hasil Normalisasi)
SOFT_SKILLS = {
    # Komunikasi & Interpersonal
    'communication', 'public speaking', 'presentation skills',
    'active listening', 'persuasion', 'customer service',
    'interpersonal skills', 'relationship building',
    # Tim, Kerjasama, & Hubungan
    'teamwork', 'collaboration', 'conflict resolution',
    # Kepemimpinan & People Management
    'leadership', 'leadership development', 'team management',
    'people management', 'people development', 'coaching & mentoring',
    'organization skills', 'management', 'organizational culture',
    # Pemecahan Masalah & Berpikir Kritis
    'problem solving', 'critical thinking', 'decision making',
    'strategic thinking', 'creativity',
    # Adaptabilitas, Manajemen Waktu, & Sikap Kerja
    'adaptability', 'time management', 'self management',
    'negotiation', 'emotional intelligence', 'work ethic',
    'working under pressure', 'honesty & discipline',
    'mental & physical discipline'
}

def normalize_skill(name: str) -> str:
    """Membersihkan dan menstandardisasi nama keahlian."""
    if not name or not isinstance(name, str):
        return ''
    clean = name.strip()
    return SKILL_TRANSLATIONS.get(clean.lower(), clean)

def is_soft_skill(name: str) -> bool:
    """Mengecek apakah keahlian tergolong Soft Skill berdasarkan taksonomi."""
    if not name or not isinstance(name, str):
        return False
    norm = normalize_skill(name).lower()
    return norm in SOFT_SKILLS

def clean_job_title(title: str) -> str:
    """Membersihkan nama jabatan dari noise keterangan atau institusi."""
    if not title or not isinstance(title, str):
        return ''
    t = (
        title.split(' at ')[0]
        .split(' - ')[0]
        .split(' | ')[0]
        .split(' @ ')[0]
        .strip()
    )
    low = t.lower()
    noise_keywords = [
        'experience', 'endorsed', 'across', 'grade:', 'passed',
        'college', 'academy', 'universitas', 'gpa', 'alumni', "'--"
    ]
    if any(k in low for k in noise_keywords):
        return ''
    if len(t) < 3 or len(t) > 42:
        return ''
    return t

ROLE_TRANSLATIONS = {
    'software engineer / tech roles': 'Software Engineer',
    'software engineer': 'Software Engineer',
    'analis data': 'Data Analyst',
    'data analyst': 'Data Analyst',
    'staff of data scientist': 'Data Scientist',
    'desainer grafis': 'Graphic Designer',
    'guru': 'Teacher',
    'pelajar': 'Student',
    'asisten laboratorium': 'Laboratory Assistant',
    'asisten dosen': 'Teaching Assistant',
    'asisten penjahit': 'Tailoring Assistant',
    'admin keuangan': 'Finance Administrator',
    'pengelola keuangan dan anggaran': 'Finance & Budget Officer',
    'tenaga administrasi': 'Administrative Staff',
    'kepala tata usaha': 'Head of Administration',
    'geologi minyak bumi assistant': 'Petroleum Geology Assistant',
    'asisten administrasi underwriting': 'Underwriting Administration Assistant',
    'staf consultant': 'Consultant',
    'sales marketing': 'Sales & Marketing',
    'sales marketing positions': 'Sales & Marketing',
    'staff of education': 'Education Staff',
    'sekretariat': 'Secretariat',
    'mpk sma n 3 boyolali': 'Student Council Committee',
    'outlet head setir kanan store surabaya': 'Retail Store Manager',
    'private tutor (fisika matematika kimia)': 'Science & Math Tutor',
    'pvc foam sheets,pvc pipes,polymer pipes': 'Manufacturing & Operations Specialist',
    'finance staff': 'Finance Staff',
    'junior staff accounting': 'Junior Accounting Staff',
    'staff accountant and finance': 'Accounting & Finance Staff',
    'staff tax accountant': 'Tax Accountant Staff',
    'fresh graduate in geological engineering': 'Geological Engineer (Fresh Graduate)',
    'spv mine plan engineer': 'Mining Plan Supervisor',
    'tc assistant (organic)': 'Technical Assistant',
    'kol specialist': 'KOL Specialist',
    'senior ios developer': 'Senior iOS Developer',
    'e-board': 'Executive Board',
    'creative': 'Creative Designer',
    'video production': 'Video Producer',
    'staff': 'General Staff',
    '': 'Software Engineer'
}

def normalize_target_role(title: str) -> str:
    """Menormalisasi target role ke 17 Standar Peran Resmi Tracera (5 Job Families)."""
    if not title or not isinstance(title, str):
        return 'Software Engineer'
    t_clean = clean_job_title(title)
    if not t_clean:
        return 'Software Engineer'
    return map_to_tracera_17(t_clean)

def map_to_tracera_17(raw_role: str) -> str:
    """Mengelompokkan peran kerja spesifik ke dalam 17 Target Role Resmi Tracera (career-paths-page.js)."""
    r = str(raw_role).lower().strip()
    
    # 1. DATA FAMILY
    if any(k in r for k in ['data lead', 'head of data', 'data governance', 'chief scientist', 'director of data']):
        return "Data Lead"
    if any(k in r for k in ['senior data scientist', 'lead data scientist', 'associate director, machine learning', 'data scientist', 'machine learning', 'artificial intelligence', 'ai ']):
        return "Data Scientist"
    if any(k in r for k in ['data analyst', 'analis data', 'bi ', 'business intelligence', 'analytics', 'statistic']):
        return "Data Analyst"

    # 2. PRODUCT FAMILY
    if any(k in r for k in ['head of product', 'vp product', 'director of product', 'cpo']):
        return "Head of Product"
    if any(k in r for k in ['product manager', 'project manager', 'program manager', 'project management']):
        return "Product Manager"
    if any(k in r for k in ['product owner', 'scrum master', 'associate product']):
        return "Product Owner"

    # 3. MARKETING FAMILY
    if any(k in r for k in ['marketing manager', 'brand development manager', 'head of marketing', 'marketing director', 'vp, global marketing']):
        return "Marketing Manager"
    if any(k in r for k in [
        'marketing', 'brand', 'sales', 'graphic', 'designer', 'creat', 'content', 
        'writer', 'public relation', 'pr ', 'social media', 'stylist', 'illustrat', 
        'video', 'telemarketing', 'kol '
    ]):
        return "Marketing Associate"

    # 4. ENGINEERING FAMILY
    if any(k in r for k in ['engineering manager', 'vp engineering', 'head of engineering', 'director of technology']):
        return "Engineering Manager"
    if any(k in r for k in ['technical lead', 'development engineer lead', 'lead developer', 'staff software engineer', 'lead engineer']):
        return "Technical Lead"
    if any(k in r for k in [
        'senior software', 'senior developer', 'senior backend', 'senior ios', 'software architect', 'senior consultant iii',
        'junior software', 'intern developer', 'student intern', 'junior dev',
        'software', 'developer', 'programmer', 'architect', 'devops', 'backend', 
        'frontend', 'cloud', 'datacenter', 'network engineer', 'full stack', 'web'
    ]):
        return "Software Engineer"

    # 5. BUSINESS FAMILY
    if any(k in r for k in [
        'business analyst', 'financ', 'keuangan', 'account', 'akuntan', 'audit', 
        'tax', 'pajak', 'credit', 'bank', 'invest', 'treasury', 'receivable', 
        'billing', 'cash management', 'underwriting', 'economic planning', 
        'policy analyst', 'health policy', 'estimator'
    ]):
        return "Business Analyst"

    if any(k in r for k in [
        'consult', 'advisory', 'specialist', 'research', 'peneliti', 'fellow', 
        'legal', 'compliance', 'facilitator', 'trainer', 'tutor', 'teacher', 
        'lecturer', 'dosen', 'professor', 'assistant'
    ]):
        return "Consultant"

    if any(k in r for k in [
        'manager', 'director', 'chief', 'ceo', 'coo', 'founder', 'owner', 'partner', 
        'lead', 'head of', 'vice president', 'vp', 'executive', 'operations', 
        'supervisor', 'foreman', 'superintendent', 'administrator', 'admin', 
        'secretary', 'secretariat', 'hsse', 'officer', 'engineer', 'geologist', 
        'metallurg', 'process', 'operator', 'drilling', 'plant', 'surveyor'
    ]):
        return "Operations Manager"

    return "Software Engineer"


def normalize_industry(raw_ind: str, target_role: str = '', starting_role: str = '') -> str:
    """Menormalisasi industri profil ke 5 Industri Standar Tracera, disesuaikan dengan Starting Role & Target Role."""
    s = (raw_ind or '').lower().strip()
    roles_str = f"{target_role or ''} {starting_role or ''}".lower()

    if any(k in s for k in ['telecommunication', 'telecom', 'network', 'broadcast media', 'advertising']):
        return 'Telecommunications'
    if any(k in s for k in ['financial', 'banking', 'accounting', 'investment', 'insurance', 'venture capital', 'private equity']):
        return 'Financial Services'
    if any(k in s for k in [
        'consulting', 'advisory', 'research', 'training', 'coaching', 'strategic management',
        'law', 'human resources', 'outsourcing', 'public relations', 'higher education',
        'education', 'government', 'public policy', 'international affairs', 'legislative',
        'non-profit', 'civic', 'environmental', 'events', 'writing'
    ]):
        return 'Consulting'
    if any(k in s for k in [
        'software', 'it services', 'technology', 'internet', 'computer',
        'information technology', 'semiconductor', 'automation', 'graphic design'
    ]):
        return 'Technology'
    if any(k in s for k in [
        'consumer goods', 'retail', 'food', 'beverage', 'manufacturing', 'farming', 'apparel',
        'wholesale', 'hospitality', 'restaurants', 'wellness', 'entertainment', 'pharmaceutical',
        'chemical', 'machinery', 'mining', 'oil and gas', 'utilities', 'construction',
        'civil engineering', 'real estate', 'transportation', 'maritime', 'aviation', 'defense',
        'fisheries', 'hospitals', 'health care', 'biotechnology', 'architecture', 'facilities'
    ]):
        return 'Consumer Goods'

    # Fallback selaras dengan Target Role & Starting Role
    if 'business analyst' in roles_str:
        return 'Financial Services'
    if 'consultant' in roles_str:
        return 'Consulting'
    if 'marketing' in roles_str:
        return 'Telecommunications'
    if 'operations manager' in roles_str:
        return 'Consumer Goods'
    return 'Technology'


def normalize_study_program(fos_list, target_role: str = '', starting_role: str = '') -> str:
    """Mengelompokkan program studi ke dalam 5 Cohort Filters Standar Tracera (English)."""
    clean_fos = [
        str(f).lower().strip()
        for f in (fos_list or [])
        if f and str(f).lower().strip() not in ['all study programs', 'all', '-']
    ]
    joined = ' | '.join(clean_fos)

    # 1. Data Science & Quantitative Analytics
    if any(k in joined for k in [
        'data analysis', 'data science', 'actuarial', 'aktuaria', 'computational science',
        'applied geostatistics', 'geostatistics', 'information systems', 'sistem informasi',
        'information system', 'management information systems', 'statistics', 'statistika'
    ]) or (any(k in joined for k in ['mathematics', 'matematika']) and 'natural science' not in joined):
        return 'Data Science & Quantitative Analytics'

    # 2. Computer Science & Software Engineering
    if any(k in joined for k in [
        'computer science', 'informatics', 'teknik informatika', 'informatika',
        'software engineering', 'computer programming', 'information technology',
        'back end javascript', 'javascript', 'full stack', 'rekayasa perangkat lunak',
        'ilmu komputer', 'artificial intelligence', 'teknik komputer', 'computer engineering'
    ]):
        return 'Computer Science & Software Engineering'

    # 3. Finance, Banking & Accounting
    if any(k in joined for k in [
        'accounting', 'akuntansi', 'banking', 'perbankan', 'financial', 'finance',
        'keuangan', 'sharia accounting', 'tax', 'pajak', 'perpajakan'
    ]):
        return 'Finance, Banking & Accounting'

    # 4. Engineering & Industrial Technology
    if any(k in joined for k in [
        'chemical', 'civil', 'mechanical', 'geological', 'geophysical', 'geologi', 'geofisika',
        'mining', 'mineral', 'tambang', 'pertambangan', 'petroleum', 'perminyakan',
        'electrical', 'elektro', 'industrial engineering', 'teknik industri', 'architecture', 'arsitektur',
        'teknik kimia', 'teknik mesin', 'mesin', 'teknik sipil', 'sipil', 'metalurgi', 'metallurgy',
        'mekatronik', 'robotik', 'energi', 'energy', 'lingkungan', 'environmental', 'structural',
        'urban', 'hutan', 'forestry', 'pulp', 'paper', 'engineering', 'teknik', 'fisika', 'physics',
        'kimia', 'chemistry', 'biologi', 'biology', 'geografi', 'geography', 'pertanian', 'agriculture',
        'soil', 'water'
    ]):
        return 'Engineering & Industrial Technology'

    # 5. Business, Management & Economics
    if any(k in joined for k in [
        'business', 'bisnis', 'management', 'manajemen', 'marketing', 'pemasaran',
        'economics', 'ekonomi', 'entrepreneurship', 'mba', 'administrasi', 'administration',
        'public relations', 'communication', 'komunikasi', 'law', 'hukum', 'psychology', 'psikologi',
        'international relations', 'sociology', 'sosiologi', 'political', 'politik', 'public health',
        'kesehatan', 'nursing', 'education', 'pendidikan', 'humanities', 'philosoph',
        'literature', 'sastra', 'english', 'governance', 'government', 'anthropology', 'crimino', 'tourist', 'travel', 'media'
    ]):
        return 'Business, Management & Economics'

    # Fallback selaras dengan Target Role & Starting Role apabila fieldOfStudy kosong / SMA
    roles = f"{target_role or ''} {starting_role or ''}".lower()
    if 'data' in roles:
        return 'Data Science & Quantitative Analytics'
    if 'business analyst' in roles:
        return 'Finance, Banking & Accounting'
    if 'operations manager' in roles:
        return 'Engineering & Industrial Technology'
    if any(k in roles for k in ['marketing', 'consultant', 'product']):
        return 'Business, Management & Economics'
    return 'Computer Science & Software Engineering'

# ==============================================================================
# 4. FILTER KETAT UNIVERSITAS (KHUSUS PERGURUAN TINGGI INDONESIA)
# ==============================================================================
EXCLUDE_PATTERNS = [
    # Sekolah Menengah & Dasar (SMA, SMK, SMP, Madrasah, dll)
    r'\bsma\b', r'\bsman\b', r'\bsmkn?\b', r'\bsmp\b', r'\bsmpn\b', r'\bsd\b',
    r'\bmadrasah\b', r'\baliyah\b', r'\btsanawiyah\b', r'\bpesantren\b',
    r'\bhigh\s*school\b', r'\bsecondary\b', r'\bmiddle\s*school\b', r'\belementary\b',
    r'\bpreparatory\b', r'\bmatriculation\b', r'\bjunior\s*college\b',
    r'\bboarding\s*school\b', r'\binternational\s*school\b', r'\bkindergarten\b',
    
    # Kursus, Bootcamp, Pelatihan Non-Kampus
    r'\bacademy\b', r'\bacamedy\b', r'\bacademies\b', r'\bbootcamp\b', r'\bcourse\b',
    r'\btraining\b', r'\bblk\b', r'\blearning\b', r'\bstartup\s*campus\b',
    
    # Lembaga & Universitas Asing (Foreign Institutions)
    r'\bcolumbia\b', r'\bharvard\b', r'\bimperial\b', r'\bjohns\s*hopkins\b',
    r'\bcornell\b', r'\bmaryland\b', r'\bsan\s*diego\b', r'\bmissouri\b',
    r'\bbradford\b', r'\bcurtin\b', r'\brmit\b', r'\bunsw\b', r'\bpetronas\b',
    r'\bnazarbayev\b', r'\bben-gurion\b', r'\bking\s*fahd\b', r'\btowson\b',
    r'\bwoosong\b', r'\bastana\b', r'\bkakinada\b', r'\blondon\b', r'\baustralia\b',
    r'\bmelbourne\b', r'\bsingapore\b', r'\bmalaysia\b', r'\bamerican\b',
    r'\bcalifornia\b', r'\bbritish\b', r'\bqatar\b', r'\bdoha\b', r'\bchina\b',
    r'\bsun\s*yat-sen\b', r'\bestonian\b', r'\bchaco\b', r'\bargentina\b',
    r'\blima\b', r'\bperu\b', r'\bcollege\b', r'\bkolled', r'\bsalahuddin\s*abdul\s*aziz\b'
]

INDONESIAN_UNI_MAPPINGS = [
    # --- Tracera Big 6 (Top Priority) ---
    ("Universitas Gadjah Mada", [
        r'gadjah\s*mada', r'\bugm\b', r'sekolah\s*vokasi.*gadjah\s*mada'
    ]),
    ("Universitas Indonesia", [
        r'universitas\s*indonesia', r'university\s*of\s*indonesia', r'\bui\b'
    ]),
    ("Institut Teknologi Bandung", [
        r'teknologi\s*bandung', r'bandung\s*institute\s*of\s*technology', r'\bitb\b'
    ]),
    ("Institut Teknologi Sepuluh Nopember", [
        r'sepuluh\s*nopember', r'\bits\b'
    ]),
    ("Universitas Airlangga", [
        r'airlangga', r'\bunair\b'
    ]),
    ("BINUS University", [
        r'binus', r'bina\s*nusantara'
    ]),

    # --- Kampus Negeri & Swasta Terkemuka Indonesia ---
    ("Universitas Pembangunan Nasional Veteran Yogyakarta", [
        r'pembangunan\s*nasional\s*veteran\s*yogyakarta', r'upn.*veteran.*yogyakarta', r'upnvy'
    ]),
    ("Universitas Pembangunan Nasional Veteran Jawa Timur", [
        r'pembangunan\s*nasional\s*veteran\s*jawa\s*timur', r'upn.*veteran.*jawa\s*timur', r'upn.*jatim'
    ]),
    ("Universitas Diponegoro", [
        r'diponegoro', r'\bundip\b'
    ]),
    ("IPB University", [
        r'ipb', r'institut\s*pertanian\s*bogor', r'bogor\s*agricultural'
    ]),
    ("Universitas Brawijaya", [
        r'brawijaya', r'\bub\b'
    ]),
    ("Universitas Padjadjaran", [
        r'padjadjaran', r'\bunpad\b'
    ]),
    ("Universitas Negeri Malang", [
        r'negeri\s*malang', r'state\s*university\s*of\s*malang'
    ]),
    ("Universitas Negeri Yogyakarta", [
        r'negeri\s*yogyakarta', r'yogyakarta\s*state\s*university', r'\buny\b'
    ]),
    ("Universitas Negeri Semarang", [
        r'negeri\s*semarang', r'\bunnes\b'
    ]),
    ("Universitas Negeri Jakarta", [
        r'negeri\s*jakarta', r'\bunj\b'
    ]),
    ("Universitas Pendidikan Indonesia", [
        r'pendidikan\s*indonesia', r'\bupi\b'
    ]),
    ("Universitas Terbuka", [
        r'universitas\s*terbuka', r'indonesia\s*open\s*university', r'\but\b'
    ]),
    ("Universitas Gunadarma", [
        r'gunadarma'
    ]),
    ("Universitas Mercu Buana", [
        r'mercu\s*buana'
    ]),
    ("Universitas Andalas", [
        r'andalas', r'\bunand\b'
    ]),
    ("Universitas Sriwijaya", [
        r'sriwijaya', r'\bunsri\b'
    ]),
    ("Universitas Lampung", [
        r'universitas\s*lampung', r'\bunila\b'
    ]),
    ("Universitas Mulawarman", [
        r'mulawarman', r'\bunmul\b'
    ]),
    ("Universitas Islam Indonesia", [
        r'islam\s*indonesia', r'\buii\b'
    ]),
    ("Universitas Sebelas Maret", [
        r'sebelas\s*maret', r'\buns\b'
    ]),
    ("Universitas Jenderal Soedirman", [
        r'jenderal\s*soedirman', r'\bunsoed\b'
    ]),
    ("Universitas Sumatera Utara", [
        r'sumatera\s*utara', r'\busu\b'
    ]),
    ("Universitas Hasanuddin", [
        r'hasanuddin', r'\bunhas\b'
    ]),
    ("Universitas Riau", [
        r'university\s*of\s*riau', r'universitas\s*riau', r'\bunri\b'
    ]),
    ("Telkom University", [
        r'telkom\s*university', r'universitas\s*telkom'
    ]),
    ("Universitas Katolik Parahyangan", [
        r'parahyangan', r'\bunpar\b'
    ]),
    ("Universitas Katolik Indonesia Atma Jaya", [
        r'atma\s*jaya'
    ]),
    ("Universitas Muhammadiyah Malang", [
        r'muhammadiyah\s*malang', r'\bumm\b'
    ]),
    ("Universitas Muhammadiyah Yogyakarta", [
        r'muhammadiyah\s*yogyakarta', r'\bumy\b'
    ]),
    ("Universitas Muhammadiyah Surakarta", [
        r'muhammadiyah\s*surakarta', r'\bums\b'
    ]),
    ("Universitas Muhammadiyah Kendari", [
        r'muhammadiyah\s*kendari'
    ]),
    ("Universitas Pertamina", [
        r'universitas\s*pertamina'
    ]),
    ("Universitas Pakuan", [
        r'pakuan'
    ]),
    ("Universitas Pamulang", [
        r'pamulang', r'\bunpam\b'
    ]),
    ("Universitas Esa Unggul", [
        r'esa\s*unggul'
    ]),
    ("Universitas Tarumanagara", [
        r'tarumanagara', r'\buntar\b'
    ]),
    ("Universitas Pelita Harapan", [
        r'pelita\s*harapan', r'\buph\b'
    ]),
    ("Universitas Trisakti", [
        r'trisakti'
    ]),
    ("Universitas Bung Hatta", [
        r'bung\s*hatta'
    ]),
    ("Universitas Sultan Ageng Tirtayasa", [
        r'sultan\s*ageng\s*tirtayasa', r'\buntirta\b'
    ]),
    ("UIN Syarif Hidayatullah Jakarta", [
        r'syarif\s*hidayatullah', r'uin\s*jakarta', r'islam\s*negeri\s*jakarta'
    ]),
    ("UIN Sunan Gunung Djati Bandung", [
        r'sunan\s*gunung\s*djati', r'islam\s*negeri\s*bandung', r'uin\s*bandung'
    ]),
    ("UIN Sunan Kalijaga Yogyakarta", [
        r'sunan\s*kalijaga', r'uin\s*yogyakarta'
    ]),
    ("UIN Raden Intan Lampung", [
        r'raden\s*intan'
    ]),
    ("Institut Teknologi Sumatera", [
        r'teknologi\s*sumatera', r'\bitera\b'
    ]),
    ("Institut Teknologi Medan", [
        r'teknologi\s*medan', r'\bitm\b'
    ]),
    ("Politeknik Negeri Jakarta", [
        r'politeknik\s*negeri\s*jakarta', r'\bpnj\b'
    ]),
    ("Politeknik Negeri Bandung", [
        r'politeknik\s*negeri\s*bandung', r'\bpolban\b'
    ]),
    ("Politeknik Negeri Batam", [
        r'polytechnic\s*of\s*batam', r'politeknik\s*negeri\s*batam'
    ]),
    ("Politeknik Negeri Padang", [
        r'politeknik\s*negeri\s*padang'
    ]),
    ("Politeknik Caltex Riau", [
        r'caltex\s*riau', r'\bpcr\b'
    ])
]

def clean_indonesian_university(raw_name: str) -> str:
    """Menyaring hanya perguruan tinggi Indonesia terakreditasi dan membuang SMA/SMK/luar negeri."""
    if not raw_name or not isinstance(raw_name, str):
        return ""
    s = raw_name.strip()
    s_low = s.lower()
    
    # Tolak jika termasuk pola sekolah menengah, kursus/bootcamp, atau kampus luar negeri
    if any(re.search(p, s_low) for p in EXCLUDE_PATTERNS):
        return ""
        
    # Cocokkan dengan kamus kanonikal
    for canonical, patterns in INDONESIAN_UNI_MAPPINGS:
        if any(re.search(p, s_low) for p in patterns):
            return canonical
            
    # Pola perguruan tinggi Indonesia umum (harus memiliki kata kunci kampus resmi)
    indo_keywords = [
        r'\buniversitas\b', r'\binstitut\b', r'\bpoliteknik\b', 
        r'\bsekolah\s*tinggi\b', r'\buin\b', r'\biain\b', r'\bstie\b', r'\bstmik\b'
    ]
    if any(re.search(k, s_low) for k in indo_keywords):
        cleaned = re.sub(r'\s*\([A-Z0-9\s-]+\)$', '', s).strip()
        return cleaned
        
    return ""

def clean_universities(raw_list):
    """Menghasilkan list kampus Indonesia bersih tanpa SMA/SMK/asing."""
    if not raw_list:
        return ['Universitas Gadjah Mada']
    cleaned = []
    for u in raw_list:
        norm = clean_indonesian_university(u)
        if norm and norm not in cleaned:
            cleaned.append(norm)
    return cleaned if cleaned else ['Universitas Gadjah Mada']
