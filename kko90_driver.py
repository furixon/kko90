'''
    Qoo10 Auto Browser
    * Automation for Qoo10 QSM Version 1.0
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

import sys
import time
import schedule
import requests
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kko90.settings")

import django
django.setup()


from cms.models import KkoMsg, Agency


# 상용 지점 계정
agency_all = Agency.objects.all()

# 테스트 지점
# agency_all = Agency.objects.filter(agency_name='FURIXON')

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
    'siteUrl': 'https://center-pf.kakao.com/',
}

def get_driver(agency):
    print('### {} 지점 드라이버 세팅 시작'.format(agency.agency_name))
    # 크롬 드라이버 로딩
    jobDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    jobDriver.implicitly_wait(3)
    jobDriver.get(LOGIN_INFO['siteUrl'])

    print('### 웹 드라이버 로딩을 시작합니다.........\n')
    
    # 카카오 로그인
    jobDriver.find_element(By.XPATH, '//*[@id="loginKey--1"]').send_keys(agency.kko_id)
    jobDriver.find_element(By.XPATH, '//*[@id="password--2"]').send_keys(agency.kko_pass)

    try:
        jobDriver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()

        print('### 로그인이 완료되었습니다............\n')

    except Exception as e:
        print('로그인 실패!')
        jobDriver.find_element(By.NAME, 'txtLoginID').clear()
        jobDriver.find_element(By.XPATH, '//*[@id="id_email_2"]').send_keys(agency.kko_id)
        jobDriver.find_element(By.XPATH, '//*[@id="id_password_3"]').send_keys(agency.kko_pass)

        jobDriver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]').click()

        print('로그인이 완료되었습니다............\n')

    url = jobDriver.command_executor._url
    session_id = jobDriver.session_id

    print('Browser URL : ', url)
    print('Session ID : ', session_id)

    # url, session_id 파일로 저장
    with open('./kko90_session_{}.txt'.format(agency.agency_name), 'w') as f:
        f.write(url)
        f.write('||')
        f.write(session_id)

    return jobDriver

def job(driverData):
    jobDriver = driverData[0]  # 크롬 드라이버
    agencyName = driverData[1].agency_name  # 에이전시

    
    print('### {} 지점 Keep Alive!'.format(agencyName))
    jobDriver.refresh()

    url = jobDriver.command_executor._url
    session_id = jobDriver.session_id

    print('Browser URL : ', url)
    print('Session ID : ', session_id)

    with open('./kko90_session_{}.txt'.format(agencyName), 'w') as f:
        f.write(url)
        f.write('||')
        f.write(session_id)

    # Q Analytics 페이지 이동
    # driver.get('https://qsm.qoo10.jp/GMKT.INC.Gsm.Web/Goods/GoodsAnalytics.aspx')


# driver_name = "{}".format(agency.agency_name)
driver = get_driver(agency)
schedule.every().hour.at(":00").do(job, [driver, agency])  # 매시 00분에 리프레쉬

while True:
    schedule.run_pending()
    time.sleep(1)