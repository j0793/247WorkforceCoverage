# visualizations.py
# Purpose: Generate visual charts from workforce optimization data
# Output: PNG chart files saved to /docs/images/
# Data Souce: PostgreSQL workforce_optimization database
# Charts Generated
# Charts Generated:
#   1. Student Sessions vs Educator Availability by Hour (Line Chart)
#   2. Students per Educator by Hour with Risk Threshold (Bar Chart)
#   3. Student Sessions by Time Zone (Bar Chart)
#   4. Subject Demand vs Educator Count (Horizontal Bar Chart)

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv


# Configuration

load_dotenv()
password = os.getenv('DB_PASSWORD')

engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/workforce_optimization')

# Set a consistent visual style for all charts
# "whitegrid" adds subtle gridlines which helps readability
sns.set_theme(style="whitegrid")

# Define a consistent color palette to use across charts
COLOR_BLUE = "#4C72B0"
COLOR_ORANGE = "#DD8452"
COLOR_RED = "#C44E52"
COLOR_GREEN = "#55A868"

# Create the output directory if it doesn't already exist
# This is where all chart PNG files will be saved
output_dir = "../docs/images"
os.makedirs(output_dir, exist_ok=True)

# Query Data from PostgreSQL

# Query 1: Student demand by hour
# Counts how many sessions occur at each hour of the day
demand_query = """
    SELECT 
        session_hour,
        COUNT(*) AS total_sessions
    FROM students
    GROUP BY session_hour
    ORDER BY session_hour;
"""
 
# Query 2: Educator availability by hour
# Uses generate_series to expand each educator's availability
# window into individual hourly slots, then counts per hour
supply_query = """
    SELECT 
        generate_series AS available_hour,
        COUNT(educator_id) AS educators_available
    FROM educators,
        generate_series(availability_start, availability_end)
    GROUP BY available_hour
    ORDER BY available_hour;
"""
 
# Query 3: Supply vs demand gap
# Joins demand and supply to calculate students per educator
# This is the core metric for identifying coverage gaps
gap_query = """
    WITH demand AS (
        SELECT 
            session_hour,
            COUNT(*) AS total_sessions
        FROM students
        GROUP BY session_hour
    ),
    supply AS (
        SELECT 
            generate_series AS available_hour,
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
"""
 
# Query 4: Sessions by time zone
# Counts total student sessions per time zone
timezone_query = """
    SELECT 
        time_zone,
        COUNT(*) AS total_sessions
    FROM students
    GROUP BY time_zone
    ORDER BY total_sessions DESC;
"""
 
# Query 5: Subject demand vs educator supply
# Compares how many student sessions exist per subject
# against how many educators are available for that subject
subject_query = """
    SELECT 
        s.subject,
        COUNT(s.student_id) AS student_sessions,
        COUNT(DISTINCT e.educator_id) AS educators_available
    FROM students s
    LEFT JOIN educators e ON s.subject = e.subject
    GROUP BY s.subject
    ORDER BY student_sessions DESC;
"""
 
# Load all query results into Pandas DataFrames
print("Fetching data from PostgreSQL...")
demand_df = pd.read_sql(demand_query, engine)
supply_df = pd.read_sql(supply_query, engine)
gap_df = pd.read_sql(gap_query, engine)
timezone_df = pd.read_sql(timezone_query, engine)
subject_df = pd.read_sql(subject_query, engine)
print("Data loaded successfully.")


# Chart 1
# This line chart overlays demand and supply on the same axis
# to visually show where they diverge throughout the day
 
print("Chart 1: Supply vs Demand by Hour")
 
fig, ax1 = plt.subplots(figsize=(14, 6))
 
# Plot student sessions on the left Y axis
ax1.plot(
    demand_df['session_hour'],
    demand_df['total_sessions'],
    color=COLOR_BLUE,
    linewidth=2.5,
    marker='o',
    label='Student Sessions'
)
ax1.set_xlabel('Hour of Day (0 = Midnight, 12 = Noon)', fontsize=12)
ax1.set_ylabel('Total Student Sessions', fontsize=12, color=COLOR_BLUE)
ax1.tick_params(axis='y', labelcolor=COLOR_BLUE)

# Plot educator availability on the right Y axis
# Using a second Y axis since the scales are different
ax2 = ax1.twinx()
ax2.plot(
    supply_df['available_hour'],
    supply_df['educators_available'],
    color=COLOR_ORANGE,
    linewidth=2.5,
    marker='s',
    linestyle='--',
    label='Educators Available'
)
ax2.set_ylabel('Educators Available', fontsize=12, color=COLOR_ORANGE)
ax2.tick_params(axis='y', labelcolor=COLOR_ORANGE)
 
# Add title and combined legend from both axes
plt.title('Student Demand vs Educator Availability by Hour', fontsize=15, fontweight='bold')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
 
# Set X axis ticks to show every hour clearly
ax1.set_xticks(range(0, 24))
plt.tight_layout()
plt.savefig(f"{output_dir}/chart1_supply_vs_demand.png", dpi=150)
plt.close()
print("Chart 1 saved.")


# Chart 2: Students per Educator by Hour with Risk Threshold
# This bar chart shows the staffing ratio per hour
# A red threshold line at 2.0 marks the coverage risk zone
# Bars above the line are understaffed hours
 
print("Chart 2: Students per Educator by Hour")
 
fig, ax = plt.subplots(figsize=(14, 6))
 
# Color bars based on risk level
# Red = critical (above 4.0), orange = at risk (2.0-4.0), green = healthy (below 2.0)
colors = []
for ratio in gap_df['students_per_educator']:
    if ratio >= 4.0:
        colors.append(COLOR_RED)
    elif ratio >= 2.0:
        colors.append(COLOR_ORANGE)
    else:
        colors.append(COLOR_GREEN)
 
ax.bar(
    gap_df['session_hour'],
    gap_df['students_per_educator'],
    color=colors,
    edgecolor='white',
    width=0.7
)
 
# Add a horizontal threshold line at 2.0 to mark coverage risk
ax.axhline(
    y=2.0,
    color=COLOR_RED,
    linestyle='--',
    linewidth=1.5,
    label='Coverage Risk Threshold (2.0)'
)
 
# Add labels and formatting
ax.set_xlabel('Hour of Day (0 = Midnight, 12 = Noon)', fontsize=12)
ax.set_ylabel('Students per Educator', fontsize=12)
ax.set_title('Students per Educator by Hour — Coverage Gap Analysis', fontsize=15, fontweight='bold')
ax.set_xticks(range(0, 24))
ax.legend()
 
# Add a custom legend for bar colors
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=COLOR_RED, label='Critical (4.0+)'),
    Patch(facecolor=COLOR_ORANGE, label='At Risk (2.0–4.0)'),
    Patch(facecolor=COLOR_GREEN, label='Healthy (below 2.0)'),
]
ax.legend(handles=legend_elements, loc='upper right')
 
plt.tight_layout()
plt.savefig(f"{output_dir}/chart2_students_per_educator.png", dpi=150)
plt.close()
print("Chart 2 saved.")
 

# Chart 3: Student Sessions by Time Zone
# Simple bar chart showing total sessions per time zone
# Helps identify if any region is underserved geographically
 
print("Chart 3: Sessions by Time Zone")
 
fig, ax = plt.subplots(figsize=(10, 6))
 
ax.bar(
    timezone_df['time_zone'],
    timezone_df['total_sessions'],
    color=COLOR_BLUE,
    edgecolor='white',
    width=0.6
)
 
# Add value labels on top of each bar for easy reading
for i, val in enumerate(timezone_df['total_sessions']):
    ax.text(i, val + 10, str(val), ha='center', va='bottom', fontsize=10)
 
ax.set_xlabel('Time Zone', fontsize=12)
ax.set_ylabel('Total Student Sessions', fontsize=12)
ax.set_title('Student Sessions by Time Zone', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{output_dir}/chart3_sessions_by_timezone.png", dpi=150)
plt.close()
print("Chart 3 saved.")


# Chart 4
# Horizontal grouped bar chart comparing student sessions
# and educator count side by side for each subject
# Helps identify subject-level staffing imbalances
 
print("Chart 4: Subject Demand vs Educator Count")
 
fig, ax = plt.subplots(figsize=(12, 7))
 
# Normalize student sessions to thousands for readability
# so it can be compared visually alongside educator counts
subject_df['sessions_normalized'] = subject_df['student_sessions'] / 1000
 
# Set up bar positions for grouped bars
bar_width = 0.35
y = range(len(subject_df))
 
bars1 = ax.barh(
    [i + bar_width / 2 for i in y],
    subject_df['sessions_normalized'],
    height=bar_width,
    color=COLOR_BLUE,
    label='Student Sessions (thousands)'
)
bars2 = ax.barh(
    [i - bar_width / 2 for i in y],
    subject_df['educators_available'],
    height=bar_width,
    color=COLOR_ORANGE,
    label='Educators Available'
)
 
# Set Y axis labels to subject names
ax.set_yticks(list(y))
ax.set_yticklabels(subject_df['subject'], fontsize=11)
ax.set_xlabel('Count', fontsize=12)
ax.set_title('Subject Demand vs Educator Availability', fontsize=15, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/chart4_subject_demand_vs_supply.png", dpi=150)
plt.close()
print("Chart 4 saved.")

# Done

print("\nAll charts saved to /docs/images/")
print("Files generated:")
print("  - chart1_supply_vs_demand.png")
print("  - chart2_students_per_educator.png")
print("  - chart3_sessions_by_timezone.png")
print("  - chart4_subject_demand_vs_supply.png")
 