from bs4 import BeautifulSoup

with open('index.html',) as f:
    doc = BeautifulSoup(f, 'html.parser')

# can access any tag on the html such as 'title', but only the first one
tag = doc.title
print(tag.string)

# can change the string inside a tag in html
tag.string = 'something'
print(tag.string)

# another way to find a tag called 'p', but only the first one
tag = doc.find('p')
print(tag)

# getting every 'p' tag here, also tags here is a list
tags = doc.find_all('p')
print(tags)