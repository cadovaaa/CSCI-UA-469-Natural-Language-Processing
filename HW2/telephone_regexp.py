import re
import sys

if len(sys.argv) > 1:
    file_path = '../HW2/regexp_corpora/' + sys.argv[1]
else: 
    file_path = '../HW2/regexp_corpora/all-OANC.txt'

f = open(file_path, 'r')
content = f.read()

pattern = r"\(?\d{3}\)?-?\s?\d{3}-?\d{4}"

list = re.findall(pattern, content, flags=re.IGNORECASE)

for i in list:
    print(i)
