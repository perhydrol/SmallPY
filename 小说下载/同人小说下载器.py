import requests as rq
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}

url = 'http://www.trxs.cc/tongren/5724.html'
index = rq.get(url, headers=header)
index_bs4 = BeautifulSoup(index.text, "lxml")
temp_list = index_bs4.find_all(attrs={'class': 'book_list clearfix'})[
    0].find_all('li')
index_list = []
for i in temp_list:
    index_list.append(i.a['href'])
index.close()

with open("./novel.txt", "w", encoding="utf8") as novel_txt:
    for i in index_list:
        temp_url = "http://www.trxs.cc"+str(i)
        print(temp_url)
        try:
            novel_html = rq.get(temp_url, headers=header)
        except:
            print("无法抓取网页")
            continue
        if(not novel_html.ok):
            print(novel_html.status_code)
            break
        novel_html.encoding = "gb2312"
        novel_bs4 = BeautifulSoup(novel_html.text, "lxml")
        novel = novel_bs4.find_all(attrs={"class": "read_chapterDetail"})[
            0].get_text(separator="\n")
        novel.encode(encoding='utf8', errors='ignore')
        novel_txt.writelines(novel)
        novel_html.close()
print("完成！")
