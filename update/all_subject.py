#!/usr/bin/env python


default_subject = "eecs"

subject_dict = {\
    'Config' : 'config',\
    'Accounting' : 'economics',\
    "Architecture" : "architecture",\
    "Art" : "art-culture",\
    "Anthropology" : "anthropology",\
    "Culture" : "art-culture",\
    "Brain" : "cognitive-science",\
    "Biology" : "neuroscience",\
    "Biological" : "neuroscience",\
    "Cognitive Science" : "cognitive-science",\
    "Life Sciences" : "neuroscience",\
    "Business" : "business-management",\
    "Management" : "business-management",\
    "Chemistry" : "chemistry",\
    "Communication" : "communication",\
    "Computer Science" : "eecs",\
    "EECS" : "eecs",\
    "Computing" : "eecs",\
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
    "Energy" : "energy-earth-sciences",\
    "Earth Sciences" : "energy-earth-sciences",\
    "Engineering" : "engineering",\
    "Environmental Studies" : "environmental-studies",\
    "Ethics" : "ethics",\
    "Food" : "food-nutrition",\
    'GSB General & Interdisciplinary' : 'economics',\
    "Nutrition" : "food-nutrition",\
    "Health" : "health-safety",\
    "Safety" : "health-safety",\
    "History" : "history",\
    "Humanities" : "humanities",\
    "Human Resource Management" : 'economics',\
    "Law" : "law",\
    "Linguistic" : "linguistic",\
    "Literature" : "literature",\
    "Math" : "mathematics",\
    'Marketing' : 'economics',\
    "Medicine" : "medicine",\
    "Music" : "art",\
    "Neurobiology" : "neuroscience",\
    "Neuroscience" : "neuroscience",\
    "Philanthropy" : "philosophy",\
    "Philosophy" : "philosophy",\
    "Psychology" : "psychology",\
    "Ethics" : "ethics",\
    'Operations Information & Technology' : 'economics',\
    'Organizational Behavior' : 'economics',\
    "Physics" : "physics",\
    "Physical" : "physics",\
    'Strategic Management' : 'economics',\
    "Social Sciences" : "social-sciences",\
    "Statistics" : "data-science",\
    "Data Analysis" : "data-science",\
    "Civil and Environmental Engineering" : "engineering",\
    "Mechanical Engineering" : "engineering",\
    "Materials Science and Engineering" : "engineering",\
    "Chemical Engineering" : "chemistry",\
    "Urban Studies and Planning" : "architecture",\
    "Earth, Atmospheric, and Planetary Sciences" : "energy-earth-sciences",\
    "Aeronautics and Astronautics" : "engineering",\
    "Political Science" : "political",\
    "Biological Engineering" : "engineering",\
    "Global Studies and Languages" : "education",\
    "Music and Theater Arts" : "art",\
    "Nuclear Science and Engineering" : "engineering",\
    "Media Arts and Sciences" : "eecs",\
    "Aerospace Studies" : "others",\
    "Comparative Media Studies" : "others",\
    "Computational and Systems Biology" : "others",\
    "Concourse" : "others",\
    "Edgerton Center" : "others",\
    "Engineering Systems" : "engineering",\
    "Experimental Study Group" : "others",\
    "Health Sciences and Technology" : "others",\
    "Military Science" : "others",\
    "Naval Science" : "others",\
    "Science, Technology, and Society" : "others",\
    "Special Programs" : "others",\
    "Women's and Gender Studies" : "others"}

need_update_subject_list = [
    'config',
    #'anthropology',
    'eecs',
    'mathematics',
    #'business-management',
    'economics',
    #'rank',
    'physics',
    #'cognitive-science',
    #'neuroscience',
    #'literature',
    #'linguistic',
    #'philosophy',
    #"psychology",
    #'chemistry',
    #'others',
    #'art-culture',
    'data-science'
]

def print_all_subject():
    print ', '.join(subject_dict.values())

# reference subjects #
''' harvard
Introductory Notes
Dramatic Arts
Middle Eastern Studies
General Education
Earth and Planetary Sciences
Mind, Brain, and Behavior
Graduate Seminars in General Education and in Undergraduate Education
East Asian Languages and Civilizations
Molecular and Cellular Biology
Core Curriculum
Economics
Music
Freshman Seminars and House Seminars
Education
Near Eastern Languages and Civilizations
African and African American Studies
Engineering Sciences
Neurobiology
African Studies
English
Oceanography
American Studies
Environmental Science and Public Policy
Organismic and Evolutionary Biology
Anthropology
Ethnicity, Migration, Rights
Philosophy
Applied Computation
Ethnic Studies
Physical Sciences
Applied Mathematics
European Studies
Physics
Applied Physics
Expository Writing
Political Economy and Government
Archaeology
Film and Visual Studies
Psychology
Architecture, Landscape Architecture and Urban Planning
Folklore and Mythology
Public Policy
Arts and Humanities
Germanic Languages and Literatures
The Study of Religion
Asian Studies Programs
Global Health and Health Policy
Romance Languages and Literatures
Astronomy
Government
ROTC
Biological Sciences in Dental Medicine
Health Policy
Russia, Eastern Europe, and Central Asia
Biological Sciences in Public Health
History
Slavic Languages and Literatures
Biomedical Engineering
History and Literature
Social Policy
Biophysics
History of American Civilization
Social Studies
Biostatistics
History of Art and Architecture
Sociology
Business Studies
History of Science
South Asian Studies
Celtic Languages and Literatures
Human Evolutionary Biology
Special Concentrations
Chemical and Physical Biology
Inner Asian and Altaic Studies
Statistics
Chemical Biology
Latin American and Iberian Studies
Stem Cell and Regenerative Biology
Chemical Physics
Life Sciences
Systems Biology
Chemistry and Chemical Biology
Linguistics
Ukrainian Studies
The Classics
Mathematics
Visual and Environmental Studies
Comparative Literature
Medical Sciences
Women, Gender, and Sexuality
Computer Science
Medieval Studies
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
