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
