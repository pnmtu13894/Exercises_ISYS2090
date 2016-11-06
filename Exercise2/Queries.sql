SELECT * FROM academic;
SELECT academic.famname as family_name, academic.givename as given_name
FROM academic INNER JOIN interest ON academic.acnum = interest.acnum
WHERE interest.fieldnum = 292;
SELECT paper.panum as paper_number, paper.title as paper_title
FROM paper
WHERE paper.title ILIKE '%database%';
SELECT interest.fieldnum, COUNT(academic.acnum) as number_of_academic
FROM academic INNER JOIN interest ON academic.acnum = interest.acnum
GROUP BY interest.fieldnum
ORDER BY number_of_academic DESC;