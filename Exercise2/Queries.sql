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
SELECT interest.fieldnum, COUNT(academic.acnum) as number_of_academic
FROM academic INNER JOIN interest ON academic.acnum = interest.acnum
GROUP BY interest.fieldnum
ORDER BY number_of_academic DESC;
SELECT academic.famname, academic.givename
FROM academic
WHERE academic.acnum
NOT IN (SELECT acnum FROM author);
SELECT academic.famname, academic.givename
FROM academic
WHERE academic.acnum
NOT IN (SELECT acnum FROM interest);
SELECT academic.famname, academic.givename, paper.title
FROM academic INNER JOIN author ON academic.acnum = author.acnum
				INNER JOIN paper ON author.panum = paper.panum;
SELECT academic.famname, academic.givename, paper.title
FROM academic INNER JOIN author ON academic.acnum = author.acnum
				INNER JOIN paper ON author.panum = paper.panum
WHERE academic.acnum
IN (SELECT acnum FROM interest WHERE fieldnum >= 200)
ORDER BY academic.acnum ASC
LIMIT 100
OFFSET 1;
SELECT academic.famname, academic.givename, paper.title
FROM academic INNER JOIN author ON academic.acnum = author.acnum
				INNER JOIN paper ON author.panum = paper.panum
WHERE academic.acnum
IN (SELECT acnum FROM interest WHERE fieldnum >= 200)
ORDER BY academic.acnum ASC;
SELECT COUNT(academic.acnum), academic.deptnum, department.deptname
FROM academic LEFT JOIN department ON academic.deptnum = department.deptnum
WHERE department.deptnum IN (SELECT academic.deptnum FROM academic)
GROUP BY academic.deptnum, department.deptname
ORDER BY COUNT(academic.acnum) ASC;