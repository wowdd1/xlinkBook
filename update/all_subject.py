#!/usr/bin/env python


default_subject = "eecs"

subject_dict = {\
    'Accounting' : 'economics',\
    "Architecture" : "architecture",\
    "Art" : "art-culture",\
    "Culture" : "art-culture",\
    "Biology" : "biology-life-sciences",\
    "Biological" : "biology-life-sciences",\
    "Life Sciences" : "biology-life-sciences",\
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
    "Literature" : "literature",\
    "Math" : "mathematics",\
    'Marketing' : 'economics',\
    "Medicine" : "medicine",\
    "Music" : "music",\
    "Philanthropy" : "philanthropy",\
    "Philosophy" : "philosophy",\
    "Ethics" : "ethics",\
    'Operations Information & Technology' : 'economics',\
    'Organizational Behavior' : 'economics',\
    "Physics" : "physics",\
    'Strategic Management' : 'economics',\
    "Social Sciences" : "social-sciences",\
    "Science" : "science",\
    "Statistics" : "statistics-data-analysis",\
    "Data Analysis" : "statistics-data-analysis"}

need_update_subject_list = [
    'eecs',
    'mathematics',
    #'business-management',
    'economics',
    'rank',
    #'physics',
    #'biology-life-sciences',
    #'literature',
    #'philosophy',
    'statistics-data-analysis'
]
def print_all_subject():
    print ' , '.join(subject_dict.values())
