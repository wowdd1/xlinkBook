#!/usr/bin/env python


default_subject = "eecs"

subject_dict = {\
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
    "163-OCW" : "163-ocw",\
    "Design" : "design",\
    "Economics" : "economics-finance",\
    "Finance" : "economics-finance",\
    "Education" : "education",\
    "Electronics" : "eecs",\
    "Energy" : "energy-earth-sciences",\
    "Earth Sciences" : "energy-earth-sciences",\
    "Engineering" : "engineering",\
    "Environmental Studies" : "environmental-studies",\
    "Ethics" : "ethics",\
    "Food" : "food-nutrition",\
    "Nutrition" : "food-nutrition",\
    "Health" : "health-safety",\
    "Safety" : "health-safety",\
    "History" : "history",\
    "Humanities" : "humanities",\
    "Law" : "law",\
    "Literature" : "literature",\
    "Math" : "mathematics",\
    "Medicine" : "medicine",\
    "Music" : "music",\
    "Philanthropy" : "philanthropy",\
    "Philosophy" : "philosophy-ethics",\
    "Ethics" : "philosophy-ethics",\
    "Physics" : "physics",\
    "Social Sciences" : "social-sciences",\
    "Science" : "science",\
    "Statistics" : "statistics-data-analysis",\
    "Data Analysis" : "statistics-data-analysis"}

need_update_subject_list = [
    "eecs",
    "163-ocw",
    "mathematics"
]
def print_all_subject():
    for (k, v) in subject_dict.items():
        print v
