import pandas as pd
import requests # 웹 요청
from bs4 import BeautifulSoup as bs # HTML 파싱
from datetime import datetime

# 다음 뉴스 URL 설정
url = 'https://news.daum.net/breakingnews/'

# URL로부터 HTML 데이터 요청
response = requests.get(url)

# 응답된 HTML을 BeautifulSoup으로 파싱
html = bs(response.text, 'html.parser')

# 현재 시간 포매팅
current_time = datetime.now()
formatted_time = current_time.strftime('%H:%M') # HH:MM 형식 (현재 시간 검증용)
file_time = current_time.strftime('%H시 %M분') # HH시 MM분 형식 (파일 이름 삽입용)

# CSV 파일 저장 경로 설정
file = f'C:/Users/doni/Downloads/daum_news({file_time}).csv'

news_list = [] # 뉴스 리스트 초기화
news_items = html.find_all('strong', class_='tit_thumb')
for item in news_items:
    time_element = item.find('span', class_='info_time')
    # info_time 태그가 있으면 시간 앞뒤 공백 제거
    if time_element:
        time = time_element.text.strip()
        # 시간 정보가 현재 시간과 일치하면 뉴스 정보 저장
        if time == formatted_time:
            news = item.find('a', class_='link_txt')
            title = news.text.strip() # 제목
            link = news['href'] # 링크
            news_list.append((title, link)) # 리스트에 추가

# 뉴스 데이터를 데이터프레임으로 변환
df = pd.DataFrame(news_list, columns=['제목', '링크'])

# 현재 시간 뉴스 정보 CSV 파일 저장
df.to_csv(file, index=False, encoding='utf-8-sig')
# with pd.ExcelWriter(file, engine='xlsxwriter') as writer:
#     df.to_excel(writer, index=False)

# 파일 저장 완료 메시지 출력
print(f'{file} 저장 완료')