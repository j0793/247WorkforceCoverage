import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:P4ssword@localhost:5432/workforce_optimization')

# load csvs

educators_df = pd.read_csv('../data/educators.csv')
students_df = pd.read_csv('../data/students.csv')

# push to postgresql

educators_df.to_sql('educators' engine, if_exists='replace', index=False)
students_df.to_sql('students', engine, if_exists='replace', index=False)