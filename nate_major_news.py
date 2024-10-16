import pandas as pd # 데이터프레임 작업
import time # 대기시간
from selenium import webdriver # 브라우저 자동화
from selenium.webdriver.common.action_chains import ActionChains # 마우스 액션
from selenium.webdriver.common.by import By # 요소 검색
from selenium.webdriver.support.ui import WebDriverWait # 요소 대기
from selenium.webdriver.support import expected_conditions as EC # 대기 조건

# 크롬 드라이버로 브라우저 열기
driver = webdriver.Chrome()

# 네이트 사이트 이동
driver.get('https://www.nate.com/')

# 검색창이 클릭 가능할 때까지 대기 (최대 5초)
element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'acWrap')))

# 네이트 뉴스 페이지로 이동
driver.find_element(By.CLASS_NAME, 'news').click()
time.sleep(3)

# 전날 뉴스 페이지로 이동
driver.find_element(By.XPATH, '//button[@data-travel="prev"]').click()
time.sleep(3)

# 슬라이더 드래그&드롭 액션체인
ac = ActionChains(driver)
source_element = driver.find_element(By.CLASS_NAME, 'timeKnob')
ac.click_and_hold(source_element) # 마우스 drag
ac.move_by_offset(-600, 0) # 00:00 으로 이동
ac.release() # 마우스 drop
ac.perform() # 액션 실행
time.sleep(3)

# 엑셀 파일명, 저장 경로 설정
year = driver.find_element(By.CLASS_NAME, 'year').text[-2:] # 연 (뒤 2자리 슬라이싱)
month = driver.find_element(By.CLASS_NAME, 'month').text # 월
date = driver.find_element(By.CLASS_NAME, 'date').text # 일
yesterday = f'({year}_{month}_{date})'
file = f'C:/Users/doni/Downloads/nate_major_news{yesterday}.xlsx' # 파일명에 날짜 추가

# 시간대, 뉴스 정보 저장 리스트 초기화
time_list = []
news_list = []

for i in range(0, 49):
    hh = driver.find_element(By.CLASS_NAME, 'hh').text # 시
    mm = driver.find_element(By.CLASS_NAME, 'mm').text # 분
    time_text = f'{hh}시 {mm}분' # 시트 제목에 유효한 형식으로 변환
    time_list.append(time_text) # 시간대 리스트에 추가

    # news_list
    news_data = []
    for rank in range(0, 10): # 1~10위 뉴스 크롤링
        bubble = driver.find_element(By.CLASS_NAME, f'n{rank}')
        tspans = bubble.find_elements(By.CLASS_NAME, 'lineBreak')
        news_title = ' '.join(tspan.text for tspan in tspans) # tspan 요소 텍스트 결합
        news_data.append([f'{rank + 1}위', news_title]) # 뉴스 데이터 리스트에 추가
    
    # 뉴스 데이터를 데이터프레임으로 변환
    df = pd.DataFrame(news_data, columns=["순위", "기사 제목"])
    news_list.append(df) # 기사 제목 리스트에 추가

    ac.click_and_hold(source_element)
    ac.move_by_offset(11.5, 0) # 30분씩 오른쪽으로 이동
    ac.release()
    ac.perform()
    time.sleep(1)

# pandas ExcelWriter를 이용해 모든 시간대별 뉴스 정보 엑셀 파일 저장
with pd.ExcelWriter(file, engine='xlsxwriter') as writer:
    for i in range(0, len(news_list)):
        news_list[i].to_excel(writer, sheet_name=time_list[i], index=False) # 시간대별 시트 생성하여 저장

# 파일 저장 완료 메시지 출력
print(f'{file} 저장 완료')

# 브라우저 종료
driver.quit()