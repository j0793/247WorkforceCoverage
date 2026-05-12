# Data Dictionary

## Educators Table
| Column | Type | Description |
|--------|------|-------------|
| educator_id | INT | Unique identifier |
| name | VARCHAR | Educator full name |
| email | VARCHAR | Educator email |
| time_zone | VARCHAR | Educator's time zone |
| subject | VARCHAR | Subject they teach |
| availability_start | INT | Hour they become available (0-23) |
| availability_end | INT | Hour they stop being available (0-23) |
| employment_type | VARCHAR | Full-Time, Part-Time, or Contract |
| hire_date | DATE | Date they were hired |

## Students Table
| Column | Type | Description |
|--------|------|-------------|
| student_id | INT | Unique identifier |
| name | VARCHAR | Student full name |
| email | VARCHAR | Student email |
| time_zone | VARCHAR | Student's time zone |
| subject | VARCHAR | Subject being studied |
| session_date | DATE | Date of session |
| session_hour | INT | Hour session took place (0-23) |
| session_duration_min | INT | Length of session in minutes |
| grade_level | INT | Student grade level 1-12 |