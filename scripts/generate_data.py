# generate_data.py
# Purpose: Generate syntethic educator and student datasets
# Output: /data/educators.csv and /data/students.csv
# Records: 500 educators, 10,000 students

import pandas as pd
from faker import Faker
import random

fake = Faker()
random.seed(42)

# Generate data python file

# Educator dataset (500 rows)

time_zones = [
    'US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific',
    'US/Alaska', 'US/Hawaii'
]

subjects = [
    'Front End Development', 'Back End Development', 'Data Science', 'Graphic Design', 
    'Game Development', 'Marketing', 'Artificial Intelligence', 'Business Intelligence'
]

educators = []
for i in range(1,501):
    educators.append({
        'educator_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'time_zone': random.choice(time_zones),
        'subject': random.choice(subjects),
        'availability_start': random.randint(0,11), # hour 0-11
        'availability_end': random.randint(12,23),  # hour 12-23 
        'employment_type': random.choice(['Full-Time','Part-Time','Contract']),
        'hire_date': fake.date_between(start_date='-5y', end_date='today')
    })

educators_df = pd.DataFrame(educators)
educators_df.to_csv('../data/educators.csv', index=False)
print("Educators dataset created.")

# Student dataset (10,000 rows)

students = []
for i in range(1,10001):
    students.append({
        'student_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'time_zone': random.choice(time_zones),
        'subject': random.choice(subjects),
        'session_date': fake.date_between(start_date='-1y', end_date='today'),
        'session_hour': random.randint(0,23), # hour of day, 0-23
        'session_duration_min': random.randint(30,120),
        'grade_level': random.randint(1,12)
    })

students_df = pd.DataFrame(students)
students_df.to_csv('../data/students.csv', index=False)
print("Students dataset created.") 
