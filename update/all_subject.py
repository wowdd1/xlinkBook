#!/usr/bin/env python
# -*- coding: utf-8-*-

import sys
sys.path.append("..")
from config import Config

default_subject = Config.default_subject

subject_dict = {\
    'Config' : 'config',\
    'Accounting' : 'economics',\
    "Architecture" : "architecture",\
    "Art" : "art",\
    "Anthropology" : "anthropology",\
    "Culture" : "culture",\
    "Neuroinformatics" : "neuroinformatics",\
    "Bioinformatics" : "biology",\
    "Brain" : "neuroscience",\
    "Neurobiology" : "neuroscience",\
    "Neuro" : "neuroscience",\
    "Biology" : "biology",\
    "Biological" : "biology",\
    "Bioengineering" : "biology",\
    "Bio Science" : "biology",\
    "Biochemistry" : "biology",\
    "Genetics" : "biology",\
    "volutionary Biol" : "biology",\
    "Stem Cell & Regenerative Biol" : "biology",\
    "Cognitive Science" : "neuroscience",\
    "Life Sciences" : "biology",\
    "Business" : "economics",\
    "Management" : "management",\
    "Chemistry" : "chemistry",\
    "Communication" : "communication",\
    'Computational' : 'eecs',\
    "Computer Science" : "eecs",\
    "EECS" : "eecs",\
    "Computing" : "eecs",\
    "Computation" : "eecs",\
    "Information" : 'eecs',\
    'Economic Analysis & Policy' : 'economics',\
    "Programming" : "eecs",\
    "Rank" : 'rank',\
    "Design" : "design",\
    "Economics" : "economics",\
    "Finance" : "economics",\
    "Financial" : "economics",\
    "Education" : "education",\
    "Electronic" : "eecs",\
    "Electrical Engineering" : "eecs",\
    "Electronic Engineering" : "eecs",\
    "Energy" : "energy",\
    "Earth Sciences" : "earth-science",\
    "Engineering" : "engineering",\
    "Environmental" : "earth-science",\
    "Ethics" : "ethics",\
    "Food" : "medicine",\
    "Epidemiology" : "medicine",\
    "Immunology" : "medicine",\
    "Biomedical" : "medicine",\
    "Health" : "medicine",\
    'GSB General & Interdisciplinary' : 'economics',\
    "Nutrition" : "medicine",\
    "Biogerontology" : "medicine",\
    "Health" : "medicine",\
    "Safety" : "humanities",\
    "History" : "history",\
    "Humanities" : "humanities",\
    "Human Resource Management" : 'economics',\
    'Business' : 'business-finance',\
    'Entrepreneurship' : 'business-finance',\
    "Law" : "law",\
    "Transportation" : "transportation",\
    "Sociology" : "Sociology",\
    "Society" : "Sociology",\
    "Social" : "Sociology",\
    "Linguistic" : "linguistics",\
    "Linguistics" : "linguistics",\
    "Literature" : "literature",\
    "Math" : "mathematics",\
    'Marketing' : 'economics',\
    "Medicine" : "medicine",\
    "Medical" : "medicine",\
    "Music" : "art",\
    "Dance" : "art",\
    "Neurobiology" : "neuroscience",\
    "Neuroscience" : "neuroscience",\
    "Philanthropy" : "philosophy",\
    "Philosophy" : "philosophy",\
    "Psychology" : "psychology",\
    'Operations Information & Technology' : 'economics',\
    'Organizational Behavior' : 'economics',\
    'Optics' : 'physics',\
    "Physics" : "physics",\
    "Physical" : "physics",\
    "Astrophysics" : "physics",\
    'Strategic Management' : 'management',\
    "Social Sciences" : "social-science",\
    "Statistics" : "data-science",\
    "Data Analysis" : "data-science",\
    "Civil and Environmental Engineering" : "civil-and-environmental",\
    "Mechanical Engineering" : "mechanical",\
    "Materials" : "materials-science",\
    "Materials Science and Engineering" : "materials-science",\
    "Materials Science" : "materials-science",\
    "Material" : "materials-science",\
    "Chemical Engineering" : "chemistry",\
    "Urban Studies and Planning" : "urban",\
    "Earth, Atmospheric, and Planetary Sciences" : "earth-science",\
    "Earth" : "earth-science",\
    "Atmospheric" : "earth-science",\
    "Aeronautics and Astronautics" : "aeronautics",\
    "Aeronautics" : "aeronautics",\
    "Astronautics" : "aeronautics",\
    "Political Science" : "political",\
    "Government" : "political",\
    "Public Policy" : "political",\
    "Political" : "political",\
    "Divinity" : "theology",\
    "Biological Engineering" : "biology",\
    "Global Studies and Languages" : "education",\
    "Music and Theater Arts" : "art",\
    "Nuclear Science and Engineering" : "nuclear-science",\
    "Astronomy" : "astronomy",\
    "Media Arts and Sciences" : "eecs",\
    "Aerospace Studies" : "others",\
    "Comparative Media Studies" : "others",\
    "Computational and Systems Biology" : "biology",\
    "Concourse" : "others",\
    "Edgerton Center" : "others",\
    'Engineering' : 'engineering',\
    "Engineering Systems" : "engineering",\
    "Experimental Study Group" : "others",\
    "Health Sciences and Technology" : "medicine",\
    "Military Science" : "military-science",\
    "Naval Science" : "naval-science",\
    "Science, Technology, and Society" : "others",\
    "Special Programs" : "others",\
    "Women's and Gender Studies" : "education"}

need_update_subject_list = [
    #'config',
    #'anthropology',
    'eecs',
    #'mathematics',
    #'economics',
    #'rank',
    #'physics',
    #'biology',
    #'neuroscience',
    #'literature',
    #'linguistics',
    #'philosophy',
    #"psychology",
    #'chemistry',
    #'others',
    #'art-culture',
    #'astronomy',
    #'political',
    #'humanities',
    #'history',
    #'management',
    #'medicine',
    #'business-finance',
    'data-science'
]

#need_update_subject_list = ['biology']

def print_all_subject():
    print ', '.join(subject_dict.values())

# reference subjects #
# CIP
# http://localhost:5000/?db=other/&key=cip2016&column=2


''' harvard
African & African Amer Studies
American Studies
Anthropology
Applied Computation
Applied Mathematics
Applied Physics
Arch, Landscape & Urban Plan
Architecture
Astronomy
Bio Sciences in Dental Med
Bio Sciences in Public Health
Biological Science
Biomedical Engineering
Biophysics
Biostatistics
Biostatistics
Celtic Languages & Literatures
Chan School of Public Health
Chemical & Physical Biology
Chemical Biology
Chemistry & Chemical Biology
Classics, The
Comparative Literature
Computer Science
Core Curriculum
Divinity School
Doctor of Public Health
Earth & Planetary Sciences
East Asian Langs & Civ
Economics
Education
Engineering Sciences
English
Envi Science & Public Policy
Environmental Health
Epidemiology
Ethnicity, Migration, Rights
European Studies
Expository Writing
Folklore & Mythology
Freshman Seminars
General Education
Genetics & Complex Diseases
Germanic Languages & Lit
Global Health & Health Policy
Global Health & Population
Government
Graduate School of Design
Graduate School of Education
HKS Government
Health Policy
Health Policy & Management
History
History & Literature
History of Art & Architecture
History of Science
House Seminars
Human Evolutionary Biology
Humanities
Immunology Infectious Disease
Landscape Architecture
Life Sciences
Linguistics
Mathematics
Medical Sciences
Medieval Studies
Middle Eastern Studies
Mind, Brain & Behavior
Molecular & Cellular Biology
Music
Near Eastern Languages & Civ
Neurobiology
No Department
Nutrition
Organismic & Evolutionary Biol
Philosophy
Physical Sciences
Physics
Population Health Sciences
Psychology
Regional Studies-East Asia
Religion, The Study of
Romance Languages & Lit
Russia, E Europe, Central Asia
Sanskrit & Indian Studies
Slavic Languages & Literatures
Social & Behavioral Sciences
Social Policy
Social Studies
Society, Human Dev & Health
Society, Human Dev & Health
Sociology
South Asian Studies
Special Concentrations
Statistics
Stem Cell & Regenerative Biol
Systems Biology
Theater, Dance & Media
Ukrainian Studies
Urban Planning & Design
Visual & Environmental Studies
Women, Gender & Sexuality
'''

''' MIT
Course 1  Civil and Environmental Engineering
Course 2  Mechanical Engineering
Course 3  Materials Science and Engineering
Course 4  Architecture
Course 5  Chemistry
Course 6  Electrical Engineering and Computer Science
Course 7  Biology
Course 8  Physics
Course 9  Brain and Cognitive Sciences
Course 10  Chemical Engineering
Course 11  Urban Studies and Planning
Course 12  Earth, Atmospheric, and Planetary Sciences
Course 14  Economics
Course 15  Management
Course 16  Aeronautics and Astronautics
Course 17  Political Science
Course 18  Mathematics
Course 20  Biological Engineering
Course 21  Humanities
Course 21A  Anthropology
Course 21H  History
Course 21G  Global Studies and Languages
Course 21L  Literature
Course 21M  Music and Theater Arts
Course 21W  Comparative Media Studies / Writing
Course 22  Nuclear Science and Engineering
Course 24  Linguistics and Philosophy
AS  Aerospace Studies
CC  Concourse
CMS/W  Comparative Media Studies / Writing
CSB  Computational and Systems Biology
EC  Edgerton Center
ESG  Experimental Study Group
ESD  Engineering Systems
HST  Health Sciences and Technology
MAS  Media Arts and Sciences
MS  Military Science
NS  Naval Science
SP  Special Programs
STS  Science, Technology, and Society
WGS  Women's and Gender Studies
'''

'''  mit research
aeronautics and astronautics
architecture
anthropology
arts
astronomy
biology/bioengineering
business and management
cancer
chemistry/chemical engineering
civil and environmental engineering
cognitive science
comparative media
computer science
earth, atmospheric and planetary sciences
economics
education
electrical engineering
energy
entrepreneurship and invention
global languages
history
humanities
international studies
libraries
linguistics
media arts and sciences
materials science and engineering
mathematics
mechanical engineering
medical sciences
music
nanoscience and nanotechnology
neuroscience
nuclear science and engineering
oceanography and ocean engineering
physics
philosophy
political science
robotics and artificial intelligence
social sciences
transportation
urban studies and planning
writing
'''

''' stanford
Graduate School of Business
Accounting (ACCT)
Economic Analysis & Policy (MGTECON)
Finance (FINANCE)
GSB General & Interdisciplinary (GSBGEN)
Human Resource Management (HRMGT)
Marketing (MKTG)
Operations Information & Technology (OIT)
Organizational Behavior (OB)
Political Economics (POLECON)
Strategic Management (STRAMGT)
School of Earth, Energy and Environmental Sciences
Earth, Energy, and Environmental Sciences (EARTH)
Earth Systems (EARTHSYS)
Earth, Energy, & Environmental Sciences (EEES)
Energy Resources Engineering (ENERGY)
Environment and Resources (ENVRES)
Earth System Science (ESS)
Geological Sciences (GS)
Geophysics (GEOPHYS)
Woods Institute for the Environment (ENVRINST)
School of Education
Education (EDUC)
School of Engineering
Aeronautics & Astronautics (AA)
Bioengineering (BIOE)
Chemical Engineering (CHEMENG)
Civil & Environmental Engineering (CEE)
Computational & Mathematical Engineering (CME)
Computer Science (CS)
Design Institute (DESINST)
Electrical Engineering (EE)
Engineering (ENGR)
Management Science & Engineering (MS&E)
Materials Science & Engineer (MATSCI)
Mechanical Engineering (ME)
Scientific Computing & Comput'l Math (SCCM)
School of Humanities & Sciences
African & African American Studies (AFRICAAM)
African & Middle Eastern Languages (AMELANG)
African Studies (AFRICAST)
American Studies (AMSTUD)
Anthropology (ANTHRO)
Applied Physics (APPPHYS)
Arabic Language (ARABLANG)
Archaeology (ARCHLGY)
Archaeology (ARCHLGY)
Art History (ARTHIST)
Arts Institute (ARTSINST)
Art Studio (ARTSTUDI)
Asian American Studies (ASNAMST)
Asian Languages (ASNLANG)
Astronomy (ASTRNMY)
Biology (BIO)
Biology/Hopkins Marine (BIOHOPK)
Biophysics (BIOPHYS)
Catalan Language Courses (CATLANG)
Chemistry (CHEM)
Chicana/o-Latina/o Studies (CHILATST)
Chinese General (CHINGEN)
Chinese Language (CHINLANG)
Chinese Literature (CHINLIT)
Classics (CLASSICS)
Communication (COMM)
Comparative Literature (COMPLIT)
Comparative Studies in Race & Ethnicity (CSRE)
Dance (DANCE)
Division of Literatures, Cultures, & Languages (DLCL)
Drama (TAPS)
East Asian Studies (EASTASN)
Economics (ECON)
English (ENGLISH)
English for Foreign Students (EFSLANG)
Ethics in Society (ETHICSOC)
Feminist, Gender and Sexuality Studies (FEMGEN)
Film Production (FILMPROD)
Film Studies (FILMSTUD)
French Language (FRENLANG)
French Studies (FRENCH)
German Language (GERLANG)
German Studies (GERMAN)
Global Studies (GLOBAL)
History (HISTORY)
History & Philosophy of Science (HPS)
Human Biology (HUMBIO)
Humanities & Sciences (HUMSCI)
Iberian & Latin American Cultures (ILAC)
Institute for International Studies (FSI) (IIS)
International Policy Studies (IPS)
International Relations (INTNLREL)
Italian Language (ITALLANG)
Italian Studies (ITALIAN)
Japanese General (JAPANGEN)
Japanese Language (JAPANLNG)
Japanese Literature (JAPANLIT)
Jewish Studies (JEWISHST)
Korean General (KORGEN)
Korean Language (KORLANG)
Korean Literature (KORLIT)
Latin American Studies (LATINAM)
Linguistics (LINGUIST)
Mathematical & Computational Science (MCS)
Mathematics (MATH)
Medieval Studies (MEDVLST)
Modern Thought & Literature (MTL)
Music (MUSIC)
Native American Studies (NATIVEAM)
Philosophy (PHIL)
Physics (PHYSICS)
Political Science (POLISCI)
Portuguese Language (PORTLANG)
Psychology (PSYCH)
Public Policy (PUBLPOL)
Religious Studies (RELIGST)
Russian, East European, & Eurasian Studies (REES)
Science, Technology, & Society (STS)
Slavic Language (SLAVLANG)
Slavic Studies (SLAVIC)
Sociology (SOC)
Spanish Language (SPANLANG)
Spanish, Portuguese, & Catalan Literature (ILAC)
Special Language Program (SPECLANG)
Stanford in Washington (SIW)
Statistics (STATS)
Symbolic Systems (SYMSYS)
Theater and Performance Studies (TAPS)
Tibetan Language (TIBETLNG)
Urban Studies (URBANST)
Law School
Law (LAW)
Law, Nonprofessional (LAWGEN)
School of Medicine
Anesthesia (ANES)
Biochemistry (BIOC)
Biomedical Informatics (BIOMEDIN)
Biosciences Interdisciplinary (BIOS)
Cancer Biology (CBIO)
Cardiothoracic Surgery (CTS)
Chemical & Systems Biology (CSB)
Community Health and Prevention Research (CHPR)
Comparative Medicine (COMPMED)
Dermatology (DERM)
Developmental Biology (DBIO)
Family and Community Medicine (FAMMED)
Genetics (GENE)
Health Research & Policy (HRP)
Immunology (IMMUNOL)
Medicine (MED)
Medicine Interdisciplinary (INDE)
Microbiology & Immunology (MI)
Molecular & Cellular Physiology (MCP)
Neurobiology (NBIO)
Neurology & Neurological Sciences (NENS)
Neurosciences Program (NEPR)
Neurosurgery (NSUR)
Obstetrics & Gynecology (OBGYN)
Ophthalmology (OPHT)
Orthopedic Surgery (ORTHO)
Otolaryngology (OTOHNS)
Pathology (PATH)
Pediatrics (PEDS)
Psychiatry (PSYC)
Radiation Oncology (RADO)
Radiology (RAD)
School of Medicine General (SOMGEN)
Stem Cell Biology and Regenerative Medicine (STEMREM)
Structural Biology (SBIO)
Surgery (SURG)
Urology (UROL)
Office of Vice Provost for Undergraduate Education
Education as Self-Fashioning (ESF)
Immersion in the Arts (ITALIC)
Leadership Intensive (LEAD)
Oral Communications (ORALCOMM)
Overseas Studies General (OSPGEN)
Overseas Studies in Australia (OSPAUSTL)
Overseas Studies in Barcelona (CASB) (OSPBARCL)
Overseas Studies in Beijing (OSPBEIJ)
Overseas Studies in Berlin (OSPBER)
Overseas Studies in Cape Town (OSPCPTWN)
Overseas Studies in Florence (OSPFLOR)
Overseas Studies in Istanbul (OSPISTAN)
Overseas Studies in Kyoto (OSPKYOTO)
Overseas Studies in Kyoto (KCJS) (OSPKYOCT)
Overseas Studies in Madrid (OSPMADRD)
Overseas Studies in Oxford (OSPOXFRD)
Overseas Studies in Paris (OSPPARIS)
Overseas Studies in Santiago (OSPSANTG)
ROTC Air Force (ROTCAF)
ROTC Army (ROTCARMY)
ROTC Navy (ROTCNAVY)
Structured Liberal Education (SLE)
Thinking Matters (THINK)
Undergraduate Advising and Research (UAR)
Writing & Rhetoric, Program in (PWR)
Office of Vice Provost for Teaching and Learning
Teaching and Learning (VPTL)
Athletics, Physical Education, and Recreation
Athletics, Club Sports, Martial Arts (ATHLETIC)
Outdoor Education (OUTDOOR)
Physical Education (PE)
Wellness Education (WELLNESS)
Stanford Continuing Studies
Master of Liberal Arts (MLA)
Undergraduate General Education Requirements
WAY-A-II: Aesthetic and Interpretive Inquiry
WAY-AQR: Applied Quantitative Reasoning
WAY-CE: Creative Expression
WAY-ED: Engaging Diversity
WAY-ER: Ethical Reasoning
WAY-FR: Formal Reasoning
WAY-SI: Social Inquiry
WAY-SMA: Scientific Method and Analysis
DB-EngrAppSci: Engineering and Applied Sciences
DB-Hum: Humanities
DB-Math: Mathematics
DB-NatSci: Natural Sciences
DB-SocSci: Social Sciences
EC-AmerCul: American Cultures
EC-GlobalCom: Global Community
EC-Gender: Gender Studies
EC-EthicReas: Ethical Reasoning
EC-EthicReas: Ethical Reasoning
More Course Lists
Introductory Seminars
Arts Intensive Program
Community Global Health
Service Learning Courses (certified by Haas Center)
Design Institute
'''

''' 
QS
Accounting & Finance
Agriculture & Forestry
Anthropology
Archaeology
Architecture / Built Environment
Art & Design
Biological Sciences
Business & Management Studies
Chemistry
Communication & Media Studies
Computer Science & Information Systems
Dentistry
Development Studies
Earth & Marine Sciences
Economics & Econometrics
Education
Engineering - Chemical
Engineering - Civil & Structural
Engineering - Electrical & Electronic
Engineering - Mechanical, Aeronautical & Manufacturing
Engineering - Mineral & Mining
English Language & Literature
Environmental Sciences
Geography & Area Studies
History
Law
Linguistics
Materials Science
Mathematics
Medicine
Modern Languages
Nursing
Performing Arts
Pharmacy & Pharmacology
Philosophy
Physics & Astronomy
Politics & International Studies
Psychology
Social Policy & Administration
Sociology
Statistics & Operational Research
Veterinary Science
'''
