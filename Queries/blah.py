
from bs4 import BeautifulSoup


s = HTMLSession()

url = 'https://www.amazon.in/s?k=bags&ref=sr_pg_20'

def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getnextpage(soup):
    # this will return the next page URL
    pages = soup.find('span', {'class': 's-pagination-strip'})
    if not pages.find('span', {'class': 's-pagination-item s-pagination-disabled'}):
       url = 'https://www.amazon.in/?&ext_vrnc=hi&ref=pd_sl_96612yg6jw_e&adgrpid=60571832564&hvpone=&hvptwo=&hvadid=486453138860&hvpos=&hvnetw=g&hvrand=7297005819250841959&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1007772&hvtargid=kwd-296458795081&hydadcr=14452_2154371'
       return url
    else:
        return


while True:
    data = getdata(url)
    url = getnextpage(data)
    if not url:
        break
    print(url)