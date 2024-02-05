from bs4 import BeautifulSoup
import re

with open('index2.html') as f:
    doc = BeautifulSoup(f, 'html.parser')

# searching for tag
tag = doc.find('option')
print(tag)
# <option selected="" value="course-type">Course type*</option>

# how to change attributes like 'selected' and 'value'
tag = doc.find('option')
tag['value'] = 'new value'
tag['color'] = 'blue'
print(tag)
# <option color="blue" selected="" value="new value">Course type*</option>

# to see all attributes
tag = doc.find('option')
print(tag.attrs)
# {'value': 'new value', 'selected': ''}

# searching for multiple tags
tags = doc.find_all(['p', 'div', 'li'])
print(tags)

# search for combination of things
tags = doc.find_all(['option'], text='Undergraduate', value='undergraduate')
print(tags)
# [<option value="undergraduate">Undergraduate</option>]

# how to look for different class names
tags = doc.find_all(class_='btn-item')
print(tags)

# using regexes
tags = doc.find_all(text=re.compile('\$.*'))
for tag in tags:
    print(tag.strip())

# how to limit number of result you get
tags = doc.find_all(text=re.compile('\$.*'), limit=1)
for tag in tags:
    print(tag.strip())

# save the modifications you make to the document
tags = doc.find_all('input', type='text')
for tag in tags:
    tag['placeholder'] = 'i change you'
with open('change.html', 'w') as f:
    f.write(str(doc))