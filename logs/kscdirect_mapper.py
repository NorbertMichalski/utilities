import requests
from lxml import html

def scrap():
    f = open('kscdirect_links.csv', 'wb')
    f.close()
    for i in range(1, 1404):
        f = open('kscdirect_links.csv', 'ab')
        url = 'http://kscdirect.com/search_results.php?cn=&supplier=&q=BALDOR%20ELECTRIC%20COMPANY&p=' + str(i)
        print url
        resp = requests.get(url)
        x = html.fromstring(resp.content)
        links = x.xpath(".//div[@align='center']/a/@href")
        f.write(str(links) + '\n')
        f.close()


scrap()