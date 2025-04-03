-- query.sql
SELECT original_url, shortened_url, created_at, owner_id
FROM urls
ORDER BY created_at DESC
LIMIT 10;

SELECT *
FROM users
LIMIT 10;
