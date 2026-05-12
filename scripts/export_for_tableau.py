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

# Create the output folder
output_dir = r"C:\Users\julia\Desktop\BI Projects\247Coverage\data\tableau"
os.makedirs(output_dir, exist_ok=True)

# Supply vs Demand by Hour
gap_df = pd.read_sql("""
    WITH demand AS (
        SELECT session_hour, COUNT(*) AS total_sessions
        FROM students GROUP BY session_hour
    ),
    supply AS (
        SELECT generate_series AS available_hour,
        COUNT(educator_id) AS educators_available
        FROM educators,
        generate_series(availability_start, availability_end)
        GROUP BY available_hour
    )
    SELECT 
        d.session_hour,
        d.total_sessions,
        s.educators_available,
        ROUND(d.total_sessions::numeric / NULLIF(s.educators_available, 0), 2) AS students_per_educator
    FROM demand d
    LEFT JOIN supply s ON d.session_hour = s.available_hour
    ORDER BY d.session_hour;
""", engine)
gap_df.to_csv(f"{output_dir}/supply_vs_demand.csv", index=False)
print("Exported supply_vs_demand.csv")

# Sessions by Time Zone
timezone_df = pd.read_sql("""
    SELECT time_zone, COUNT(*) AS total_sessions
    FROM students
    GROUP BY time_zone
    ORDER BY total_sessions DESC;
""", engine)
timezone_df.to_csv(f"{output_dir}/sessions_by_timezone.csv", index=False)
print("Exported sessions_by_timezone.csv")

# Subject Demand vs Educator Supply
subject_df = pd.read_sql("""
    SELECT 
        s.subject,
        COUNT(s.student_id) AS student_sessions,
        COUNT(DISTINCT e.educator_id) AS educators_available
    FROM students s
    LEFT JOIN educators e ON s.subject = e.subject
    GROUP BY s.subject
    ORDER BY student_sessions DESC;
""", engine)
subject_df.to_csv(f"{output_dir}/subject_demand_vs_supply.csv", index=False)
print("Exported subject_demand_vs_supply.csv")

print("\nAll files exported to /data/tableau/")

