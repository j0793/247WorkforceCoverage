# export_for_tableau.py
# Purpose: Export PostgreSQL query results to CSV for Tableau
# Output: CSV files saved to /data/tableau

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
password = os.getenv('DB_PASSWORD')

engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/workforce_optimization')

