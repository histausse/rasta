 SELECT apk1.first_seen_year, (COUNT(*) * 100) / (SELECT 20 * COUNT(*)
     FROM apk AS apk2 WHERE apk2.first_seen_year = apk1.first_seen_year
 )
 FROM exec JOIN apk AS apk1 ON exec.sha256 = apk1.sha256
 WHERE exec.tool_status = 'FINISHED' OR exec.tool_status = 'UNKNOWN'
 GROUP BY apk1.first_seen_year ORDER BY apk1.first_seen_year;
