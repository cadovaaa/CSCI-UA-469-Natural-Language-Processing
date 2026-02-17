import re
import sys

if len(sys.argv) > 1:
    file_path = '../HW2/regexp_corpora/' + sys.argv[1]
else: 
    file_path = '../HW2/regexp_corpora/all-OANC.txt'

f = open(file_path, 'r')
content = f.read()

with_sign_pattern = r"\$\d[\d,]*(?:\.\d+)?"
with_dollars_pattern = r"\d[\d,\.]*(?:\s(?:dollars?|cents?))(?:\sand\s\d[\d,\.]*\scents?)?"

number_word = r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)"
number_word_phrase = rf"{number_word}(?:\s+{number_word})*"
with_word_pattern = rf"{number_word_phrase}(?:\s(?:dollars?|cents?))(?:\sand\s{number_word_phrase}\scents?)?"
    
list = re.findall(with_sign_pattern, content, flags=re.IGNORECASE)
list += re.findall(with_dollars_pattern, content, flags=re.IGNORECASE)
list += re.findall(with_word_pattern, content, flags=re.IGNORECASE)

for i in list:
    print(i)


