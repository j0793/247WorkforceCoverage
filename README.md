# Workforce Optimization: 24/7 Online Learning Coverage

## Problem Statement
A nationwide online learning platform operates 24/7 and must ensure adequate educator coverage across all hours and time zones. With hundreds of educators and thousands of students, the goal is to optimize staffing to meet demand without over or understaffing at any given time.

---

## Objectives
- Identify peak student demand by hour and time zone
- Analyze educator availability against demand
- Surface coverage gaps and overstaffing inefficiencies
- Provide actionable staffing recommendations

---

## Tools & Technologies
- Python (Pandas) - data generation, cleaning, transformation
- SQL (SQLite/PostgreSQL) - data storage and analysis
- Tableau / Power BI - dashboard and visualization
- GitHub  version control and documentation

---

## Project Structure
```
/data        : raw and cleaned datasets
/scripts     : Python scripts for cleaning and analysis
/sql         : SQL queries
/dashboard   : Tableau or Power BI files
/docs        : any supporting documentation or findings
```

---

## Process Overview
1. Define the problem
2. Generate/acquire datasets
3. Clean and transform data
4. Load into database
5. Analyze with SQL
6. Visualize findings
7. Summarizing insights and recommendations

---

## Data Dictionary
Two datasets were generated using Python and the Faker library.
Full column definitions can be found in [/docs/data_dictionary.md](docs/data_dictionary.md)

| Table | Rows | Description |
|-------|------|-------------|
| educators | 500 | Educator profiles, availability windows, and subject assignments |
| students | 10,000 | Student session activity including time, subject, and time zone |

---

## Considerations for Queries
-Demand: When and where are students most active? What hours have the highest session volume? Should be consider only regional (US) candidates, or global as well?

-Suppy: How are educators distributed across time zones? Are there coverage gaps? Ideally there is a seamless transition.

-Balance: What is is the student-educator ratio by hour and time zone? Where does it fall outside of acceptable ranges?

-Cost: Where is overlap happening? Where is understaffing creating risk?

-Forecasting: Can we predict peak demand periods to schedule proactively?

---

## Key Findings
Full analysis is available in [/docs/findings.md](docs/findings.md)

- Student demand is consistent 24/7 averaging ~416 sessions per hour
- Educator availability peaks at hours 11–12 and drops sharply overnight
- Hours 0 and 23 are critically understaffed at 11.24 and 8.58 students per educator
- Coverage gaps are time-of-day driven, not geography driven
- Overnight recruitment in US/Hawaii and US/Alaska time zones is recommended

---

## How to Run

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- PostgreSQL 16+
- pip packages: pandas, faker, psycopg2-binary, sqlalchemy, python-dotenv

Install dependencies:
pip install pandas faker psycopg2-binary sqlalchemy python-dotenv

### Setup

1. Clone the repository:
git clone https://github.com/j0793/247coverage.git

2. Create a .env file in the project root with your PostgreSQL credentials:
DB_PASSWORD=yourpassword

3. Create the PostgreSQL database:
psql -U postgres
CREATE DATABASE workforce_optimization;
\q

### Generate the Data
Navigate to the scripts folder and run:
cd scripts
python generate_data.py

This will create educators.csv and students.csv in the /data folder.

### Load Data into PostgreSQL
python load_data.py

This will create and populate the educators and students tables.

### Run the SQL Queries
psql -U postgres -d workforce_optimization -f "sql/analysis_queries.sql"

### View the Dashboard
Open the /dashboard folder and load the Tableau or Power BI file.

---

## Status/Changelog:
5/11/2026:
==============================================================
--Defined problem statement
--Created README
--Created Python files, create/load data
--Created SQL Queries
--Updated documentation with dictionary and findings

## Author
Julian Jimenez - [LinkedIn](http://linkedin.com/in/julianjimenez-manager) 