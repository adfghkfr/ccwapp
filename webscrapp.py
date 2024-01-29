from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.ieeuc.com.tw/page/rank/p2.aspx?page=1&kind=1018&year=2022')
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup.prettify())
a_tags = soup.find_all('div', class_ = 'scname')
#print(a_tags)
#for k in soup.find_all('a'):
#    print(k['href'])


#b = soup.select('div a')
#print(b)

#a_tags = soup.find_all('span', class_ = 'txt-en', string = 'Harvard University')
#print(a_tags)
#print(a_tags)
results = soup.find('span', class_ = 'txt-en', string = 'Harvard University')
#print(results)
#parent = results.find_parent('a')
#print(parent)
#print(parent['href'])
##intro_link_url = 'https://www.ieeuc.com.tw' + parent['href']
#print(intro_link_url)
#c = soup.find(string = 'nonon')
#print(c)
#p_tag = a_tags.parent.previous_sibling.get_text()
#print(p_tag)

#a_tags = soup.find_all('a')
#print(a_tags)
#for tag in a_tags:
#    print(tag.get('href'))

#b = soup.find_previous_siblings('span', class_ = 'txt-en')
#print(b)


html_doc = """
<body><p class="my_par">
<a id="link1" href="/my_link1">Link 1</a>
<a id="link2" href="/my_link2">Link 2</a>
<a id="link3" href="/my_link3">Link 3</a>
<a id="link3" href="/my_link4">Link 4</a>
</p></body>
"""
soup = BeautifulSoup(html_doc, 'html.parser')
link2_tag = soup.find(id="link2")
#print(link2_tag)

# 往上層尋找 p 節點
p_tag = link2_tag.find_parents("p")
#print(p_tag)


r = requests.get('https://www.ieeuc.com.tw/page/school/show.aspx?num=171')
#r = requests.get('https://www.ieeuc.com.tw/page/school/show.aspx?num=235')
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup.prettify())


#results = soup.find('span', style = 'font-family:微軟正黑體;')
#print(results)
#results = soup.find('span', style = 'style="color:#000000;').text
#print(results)
#results = soup.find('div', class_ = 'txt editor').text
#print(results)
#print(len(results)) # 9
#for i in results.contents:
#    print(i)
#print(results)
#print(results[3])
#print(results.contents[3])

#results = soup.find('div', id = 'menu1').text
#print(results)

results = soup.find_all('a', href = '#', limit = 3)
#results = results.find('img')
#print(results)
#print(results['src'])

#im = []
#for i in results:
#    image = i.find('img')
#    im.append('https://www.ieeuc.com.tw/' + image['src'])

#print(im)
#print(results)
#image = results.select('img')
#print(image)
#image = soup.select('div.col-md-4 img')
#print(image)
#image = soup.find_all('img', class_='img-responsive', limit = 3)
#print(image)
college_name = 'London Business School'
for i in range(1, 10):
    url1 = 'https://www.ieeuc.com.tw/page/rank/p2.aspx?page=' + str(i) + '&kind=1018&year=2022'
    response1 = requests.get(url1)
    soup = BeautifulSoup(response1.text, "html.parser")
    if soup.find('span', class_ = 'txt-en', string = college_name) != None:
        break
    else:
        continue
print(i)
#print(range(1, 9))
url1 = 'https://www.ieeuc.com.tw/page/rank/p2.aspx?page=' + str(i) + '&kind=1018&year=2022'
print(url1)
#Princeton University #1
#University of Florida #2
#Loyola Marymount University #3
response1 = requests.get(url1)
# 只關注html的部分
soup = BeautifulSoup(response1.text, "html.parser")
#results = soup.find('span', class_ = 'txt-en', string = college_name)
#print(results)
#parent = results.find_parent('a')
if soup.find('span', class_ = 'txt-en', string = college_name) == None:
    print('no')
else:
    results = soup.find('span', class_ = 'txt-en', string = college_name)
    parent = results.find_parent('a')
    print(parent['href'])

from googlesearch import search
query = 'California Institute of Technology (Caltech)'
for j in search(query, tld="co.in", num=10, stop=1, pause=2):
    url = j

print(url)