#!/usr/bin/env python


default_subject = "eecs"

subject_dict = {\
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
    "Statistics" : "statistics-data-analysis",\
    "Data Analysis" : "statistics-data-analysis",\
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
    "Media Arts and Sciences" : "others",\
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
    #'anthropology',
    'eecs',
    'mathematics',
    #'business-management',
    'economics',
    #'rank',
    #'physics',
    #'cognitive-science',
    #'neuroscience',
    #'literature',
    #'linguistic',
    #'philosophy',
    #"psychology",
    #'chemistry',
    #'others',
    'statistics-data-analysis'
]

def print_all_subject():
    print ' , '.join(subject_dict.values())


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

