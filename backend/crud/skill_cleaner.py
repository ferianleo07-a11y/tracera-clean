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