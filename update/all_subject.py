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
    "Music" : "music",\
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
    "Science" : "science",\
    "Statistics" : "statistics-data-analysis",\
    "Data Analysis" : "statistics-data-analysis"}

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
    'statistics-data-analysis'
]

def print_all_subject():
    print ' , '.join(subject_dict.values())
