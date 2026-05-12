import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv('DB_PASSWORD')
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/workforce_optimization')


# Load CSVs
educators_df = pd.read_csv('../data/educators.csv')
students_df = pd.read_csv('../data/students.csv')

# Push to PostgreSQL
educators_df.to_sql('educators', engine, if_exists='replace', index=False)
students_df.to_sql('students', engine, if_exists='replace', index=False)

print("Data loaded into PostgreSQL successfully.")