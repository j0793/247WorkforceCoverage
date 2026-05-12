import pandas as pd
from sqlalchemy import create_engine

# Update with your actual postgres password
engine = create_engine('postgresql://postgres:YOURPASSWORD@localhost:5432/workforce_optimization')

# Load CSVs
educators_df = pd.read_csv('../data/educators.csv')
students_df = pd.read_csv('../data/students.csv')

# Push to PostgreSQL
educators_df.to_sql('educators', engine, if_exists='replace', index=False)
students_df.to_sql('students', engine, if_exists='replace', index=False)

print("Data loaded into PostgreSQL successfully.")