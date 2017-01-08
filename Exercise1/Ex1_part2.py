from Ex1 import *
import urllib2
import re

# req = urllib2.Request('https://www.debian.org/CD/http-ftp/')
# response = urllib2.urlopen(req)
# html = response.read()
# writeFile('html.txt',html)
text = open('html.txt',"r")
html = text.read()

conn = connect()
cur = conn.cursor()

result = re.findall(r'(<li>[\w+ \w+]+[: ][-\w+. \w+]+: <a rel="nofollow" href="\w+://[=<\>"-/:\w\d+. \w\d+]+)+', html)
print len(result)

alter_http = ""
alter_ftp = ""


for i in range(len(result)):
    country = re.search(r'(?<=<li>)[\w+ \w+]+(?=:)', result[i])
    image = re.search(r'(?<=: )[-\w+. \w+]+(?=: <a)', result[i])
    http = re.search(r'(?<="nofollow" href=")[http://].[-/:\w\d+. \w\d+]+', result[i])
    ftp = re.search(r'(?<="nofollow" href=")[ftp://].[-/:\w\d+. \w\d+]+', result[i])

    if http is None:
        alter_http = "None"
    else:
        alter_http = http.group()

    if ftp is None:
        alter_ftp = "None"
    else:
        alter_ftp = ftp.group()

    cur.execute("INSERT INTO academics.test (country,image, http, ftp) VALUES (%s, %s, %s, %s)", (str(country.group()), str(image.group()), alter_http, alter_ftp))

    conn.commit()
