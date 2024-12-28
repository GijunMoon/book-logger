#2020-07-18
# @gijunmoon

import requests
import lxml.html
from lxml.html import HtmlElement, fromstring, tostring
from bs4 import BeautifulSoup as bs

def detailpage(deatilpage): #상품 페이지 접속 후
    detail_text = []
    page = "http://www.yes24.com"
    finalpage = requests.get(page + deatilpage)

    soup = bs(finalpage.text, "html.parser")

    # 특정 위치 데이터 추출
    categories = [a.get_text(strip=True) for a in soup.select('ul.yesAlertLi li a')]

    # 결과 출력
    if categories:
        del categories[0:3] #카테고리 정리
        del categories[-4:]

        print(categories)
    else:
        print("해당 요소를 찾을 수 없습니다.")


    # 목차 추출
    titles = soup.find_all('b')  # 굵은 글씨로 된 부제목 찾기
    content = soup.find('div', class_='infoWrap_txt').text

    # 부제목과 내용 출력
    for title in titles:
        print(title.get_text())


#MAIN -------------------------------------------------------------------------------------------------------
def find():
    page = "http://www.yes24.com/Product/Search?domain=BOOK&query="
    #띄어쓰기는 %20
    search_keyword = input('검색할 단어를 입력해주세요 > ')
    mod_search_keyword = search_keyword.replace(" ", "%20") #띄어쓰기 치환

    finalpage = requests.get(page + mod_search_keyword)

    soup = bs(finalpage.text, "html.parser")

    if soup.find('div', 'class') == "noData schData": #검색결과 있는지 판단
        print("검색결과가없습니다.")
    else:
        try:
            book_result = soup.find('a', class_='gd_name').string
            book_detailpage = soup.find('a', class_='gd_name').get('href')
            print(book_result + " 이 맞나요?")

            detailpage(book_detailpage)
        except:
            print("검색결과가없습니다.")

#find()