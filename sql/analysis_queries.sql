--Query 1: Student Activity by Hour
SELECT
    session_hour,
    COUNT(*) AS total_sessions
FROM students
GROUP BY session_hour
ORDER BY session_hour;

--Query 2: Educator Availability by Hour
SELECT
    generate_series AS available_hour,
    COUNT(educator_id) AS educators_available
FROM educators,
    generate_series(availability_start, availability_end)
GROUP BY available_hour
ORDER BY available_hour;

--Query 3: Supply VS Demand Gap by Hour
WITH demand AS (
    SELECT
        session_hour,
        COUNT(*) AS total_sessions
        FROM students
        GROUP BY session_hour
),
supply AS(
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
    ROUND(d.total_sessions::numeric/ NULLIF(s.educators_available, 0), 2) AS students_per_educator
FROM demand d
LEFT JOIN supply s ON d.session_hour = s.available_hour
ORDER BY d.session_hour;

--Query 4:  Coverage by Time Zone
SELECT
    time_zone,
    COUNT(*) AS total_sessions
FROM students
GROUP BY time_zone
ORDER BY total_sessions DESC;

--Query 5: Subject Demand vs Educator Supply
SELECT
    s.subject,
    COUNT(s.student_id) AS student_sessions,
    COUNT(DISTINCT e.educator_id) AS educators_available
FROM students s
LEFT JOIN educators e ON s.subject = e.subject
GROUP BY s.subject
ORDER BY student_sessions DESC;