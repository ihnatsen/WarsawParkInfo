-- A = 90% B = 50% C = [25% - 50), D < 25%

WITH percentiles AS (  
    SELECT
        percentile_disc(0.25) WITHIN GROUP (ORDER BY rating) AS p25,
        percentile_disc(0.50) WITHIN GROUP (ORDER BY rating) AS p50,
        percentile_disc(0.90) WITHIN GROUP (ORDER BY rating) AS p90
    FROM park
	
),
category AS (SELECT park_id,
    CASE 
        WHEN rating < p25 THEN 'D'
        WHEN rating < p50 THEN 'C'
        WHEN rating < p90 THEN 'B'
        ELSE 'A'
    END AS rating_category
FROM park, percentiles),

park_and_category AS (
Select p.*, rating_category From  park AS p
JOIN category AS c ON c.park_id = p.park_id)

SELECT *
FROM park_and_category
WHERE (rating_category is null or (rating_category LIKE 'A'))
