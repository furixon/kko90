'''
    * KKO90 Auto Message Sender v1.0
    * Copyright (c) 2022 Furixon, Inc. All Rights Reserved.
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

from datetime import datetime
import sys
import time
import schedule
import requests
import os
import pickle


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kko90.settings")

import django
django.setup()


from cms.models import KkoMsg, Agency


def get_agency_driver(agency):
    LOGIN_INFO = {
        'siteUrl': 'https://business.kakao.com/',
        'loginUrl': 'https://center-pf.kakao.com/',
    }

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_argument('disable-gpu')
    options.add_argument('user-agent=' + user_agent)
    # options.add_argument("incognito")
    # options.add_argument("no-sandbox")
    # options.add_argument("disable-dev-shm-usage")
    # options.add_argument('user-data-dir=/Users/withna/Devcenter/kko90/drivers')
        
    try:
        jobDriver = webdriver.Chrome(service=Service('./drivers/chromedriver'), options=options)

    except Exception as e:
        jobDriver = webdriver.Chrome(service=Service(ChromeDriverManager(path='./drivers').install()))

    jobDriver.implicitly_wait(3)
    jobDriver.get(LOGIN_INFO['siteUrl'])
    time.sleep(1)

    cookies = pickle.load(open("{}.pickle".format(agency.agency_name), 'rb'))
    print(cookies)

    for cookie in cookies:

        print(cookie)
        jobDriver.add_cookie(cookie)

    jobDriver.get(LOGIN_INFO['loginUrl'])
    time.sleep(1)

    # # 카카오 로그인
    # jobDriver.find_element(By.XPATH, '//*[@id="loginId--1"]').send_keys(agency.kko_id)
    # jobDriver.find_element(By.XPATH, '//*[@id="password--2"]').send_keys(agency.kko_pass)

    # try:
    #     jobDriver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()

    #     print('### 로그인이 완료되었습니다............\n')

    # except Exception as e:
    #     print('로그인 실패!')
    #     jobDriver.find_element(By.NAME, 'txtLoginID').clear()
    #     jobDriver.find_element(By.XPATH, '//*[@id="id_email_2"]').send_keys(agency.kko_id)
    #     jobDriver.find_element(By.XPATH, '//*[@id="id_password_3"]').send_keys(agency.kko_pass)

    #     jobDriver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]').click()

    #     print('로그인이 완료되었습니다............\n')
    
    input('### 로그인이 완료되었습니다. 엔터를 누르면 계속 진행합니다.')

    url = jobDriver.command_executor._url
    session_id = jobDriver.session_id

    print('Browser URL : ', url)
    print('Session ID : ', session_id)

    # url, session_id 파일로 저장
    with open('./kko90_session_{}_2.txt'.format(agency.agency_name), 'w') as f:
        f.write(url)
        f.write('||')
        f.write(session_id)

    return jobDriver


def job():
    now = datetime.now()
    print(now.hour)
    if (now.hour >= 13 and now.hour <= 14) or (now.hour >= 17 and now.hour <= 18):
        print('### Off keep alive')
        pass
    else:
        # 드라이버 로딩
        agencyName = agency.agency_name  # 에이전시 이름

        print('### {} 지점 Keep Alive!'.format(agencyName))
        jobDriver.refresh()
        time.sleep(1)

        url = jobDriver.command_executor._url
        session_id = jobDriver.session_id

        print('Browser URL : ', url)
        print('Session ID : ', session_id)

        # URLS
        dashboard_url = agency.report_url.split('chats/')[0]
        chatlist_url = dashboard_url + 'chats/'

        jobDriver.get(chatlist_url)


# 상용 지점 계정
agency_all = Agency.objects.all()
agency_count = agency_all.count()

print('### 전체 지점 수 => ', agency_count)

for a in agency_all:
    print(a.agency_name)

# 지점 선택
select_agency_name = input('### 지점 선택 => ')

try:
    agency = agency_all.get(agency_name=select_agency_name)
except Exception as e:
    print('### 해당 지점 정보가 없습니다.', e)
    exit()

LOGIN_INFO = {
    'siteUrl': 'https://business.kakao.com/',
    'loginUrl': 'https://center-pf.kakao.com/',
}

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('disable-gpu')
options.add_argument('user-agent=' + user_agent)
# options.add_argument("incognito")
# options.add_argument("no-sandbox")
# options.add_argument("disable-dev-shm-usage")
# options.add_argument('user-data-dir=/Users/withna/Devcenter/kko90/drivers')
        
try:
    jobDriver = webdriver.Chrome(service=Service('./drivers/chromedriver'), options=options)

except Exception as e:
    jobDriver = webdriver.Chrome(service=Service(ChromeDriverManager(path='./drivers').install()))

jobDriver.implicitly_wait(3)
jobDriver.get(LOGIN_INFO['siteUrl'])
time.sleep(1)

cookies = pickle.load(open("{}.pickle".format(agency.agency_name), 'rb'))
print(cookies)

for cookie in cookies:

    print(cookie)
    jobDriver.add_cookie(cookie)

jobDriver.get(LOGIN_INFO['loginUrl'])
time.sleep(1)

# # 카카오 로그인
# jobDriver.find_element(By.XPATH, '//*[@id="loginId--1"]').send_keys(agency.kko_id)
# jobDriver.find_element(By.XPATH, '//*[@id="password--2"]').send_keys(agency.kko_pass)

# try:
#     jobDriver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()

#     print('### 로그인이 완료되었습니다............\n')

# except Exception as e:
#     print('로그인 실패!')
#     jobDriver.find_element(By.NAME, 'txtLoginID').clear()
#     jobDriver.find_element(By.XPATH, '//*[@id="id_email_2"]').send_keys(agency.kko_id)
#     jobDriver.find_element(By.XPATH, '//*[@id="id_password_3"]').send_keys(agency.kko_pass)

#     jobDriver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]').click()

#     print('로그인이 완료되었습니다............\n')

input('### 로그인이 완료되었습니다. 엔터를 누르면 계속 진행합니다.')

url = jobDriver.command_executor._url
session_id = jobDriver.session_id

print('Browser URL : ', url)
print('Session ID : ', session_id)

# url, session_id 파일로 저장
with open('./kko90_session_{}_2.txt'.format(agency.agency_name), 'w') as f:
    f.write(url)
    f.write('||')
    f.write(session_id)


job()
schedule.every(5).minutes.do(job)
# schedule.every(10).seconds.do(job, agency)

while True:
    schedule.run_pending()
    time.sleep(1)
