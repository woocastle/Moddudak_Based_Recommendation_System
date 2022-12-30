from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

# '치과', '안과',
# '479', '53',
# '447', '41',
# '96', '9',
# mjiju06@gmail.com


place = ['서울', '경기도', '인천']
category = ['안과']
pages = [50, 41, 9]
#
# place = ['서울', '경기도', '인천']
# category = ['안과'] #'치과'
#
# #  ['피부과', '성형외과', '산부인과', '정신건강의학과', '비뇨기과', '정형외과', '마취통증의학과', '신경외과',
# #             '재활의학과', '영상의학과', '외과', '신경과', '소아과', '내과', '이비인후과', '가정의학과', '한의원']
# pages = [53,
#          50, 41,
#          50, 9] #479,
# # [22, 8, 11, 8, 10, 23, 10, 6, 5, 5, 12, 2, 24, 52, 20, 13, 71]

# url입력
driver = webdriver.Chrome('./chromedriver.exe') # 크롬드라이버 경로 설정

review_button_xpath = '//*[@id="nav-tabs"]/li[4]'  # 리뷰 버튼
review_num_path = '/html/body/div[3]/div/div[4]/div[1]/div[5]/div[1]/h2/span'  # 총 리뷰 개수


idx = 0
for i in place:
    for j in category:
        idx += 1
        for k in range(1, pages[idx-1]):
            url = "https://www.modoodoc.com/hospitals/?search_query={}%20{}&page={}".format(i, j, k)  # 사이트 입력
            driver.get(url) # 사이트 오픈
            driver.maximize_window() # 전체창
            time.sleep(10) # 1초 지연

            hospitals = []
            reviews = []
            try:
                for hospitals_name in range(1, 11):
                    driver.get(url)  # 페이지 열기
                    time.sleep(0.3)
                    # 병원 이름 클릭
                    hospitals_name_xpath1 = '/html/body/div[2]/div[1]/div[4]/div[{}]/div/a/div/div[1]/div[1]'.format(hospitals_name)
                    hospitals_name_xpath2 = '/html/body/div[2]/div[1]/div[4]/div[{}]/div/a/div[1]/div/div[1]'.format(hospitals_name)
                    try:
                        name = driver.find_element('xpath', hospitals_name_xpath1).text
                        print('name', name)
                        driver.find_element('xpath', hospitals_name_xpath1).click()
                        time.sleep(0.1)
                    except:
                        try:
                            name = driver.find_element('xpath', hospitals_name_xpath2).text
                            print('name', name)
                            driver.find_element('xpath', hospitals_name_xpath2).click()
                            time.sleep(0.1)
                        except:
                            print('error')

                    try:
                        # 리뷰 버튼 클릭
                        driver.find_element('xpath', review_button_xpath).click()
                        time.sleep(3)  # 스크롤 충분한 시간 주기

                        # 리뷰 페이지의 수 찾기
                        review_num = driver.find_element('xpath', review_num_path).text
                        review_num = review_num.replace(',', '')  # 리뷰가 1000개가 넘어가면 ,를 찍는다. , 제거
                        review_range = (int(review_num) - 1) // 10 + 1  # 총 리뷰 페이지의 수
                        print(review_num)
                        print(review_range)
                        print('debug01')

                        # 첫번째 페이지 리뷰 크롤링
                        for review_contents in range(2, 16):
                            try:
                                review_contents_xpath = '/html/body/div[3]/div/div[4]/div[1]/div[5]/div[5]/div/div[{}]/div/div[2]'.format(review_contents)
                                review = driver.find_element('xpath', review_contents_xpath).text
                                hospitals.append(name)
                                reviews.append(review)
                                print(review)
                                print('debug02')  # reviews.append(review_2 + review_3)
                            except:
                                pass

                        # 리뷰 페이지 클릭
                        for q in range(1, review_range + 1):
                            page = 2 * q
                            if page > 5:
                                page = 5
                            print(page)
                            print('debug03')
                            review_page_button_xpath = '/html/body/div[3]/div/div[4]/div[1]/div[5]/div[5]/div/nav/ul/li[{}]'.format(page)
                            driver.find_element('xpath', review_page_button_xpath).click()
                            print('debug04')
                            time.sleep(5)
                            # 리뷰 내용 불러오기
                            for review_contents in range(2, 16):
                                try:
                                    review_contents_xpath = '/html/body/div[3]/div/div[4]/div[1]/div[5]/div[5]/div/div[{}]/div/div[2]'.format(review_contents)
                                    review = driver.find_element('xpath', review_contents_xpath).text
                                    hospitals.append(name)
                                    reviews.append(review)
                                    print(review)
                                    print('bebug05')
                                except:
                                    pass
                    except:
                        print('debug06')
                    df = pd.DataFrame({'hospitals': hospitals, 'reviews': reviews})
                    df.to_csv('./crawling_data/reviews_{}_{}_{}.csv'.format(i, j, k), index=False)
            except:
                print('error', pages)
driver.close() # 크롬드라이버 종료

# dldntjd3@naver.com