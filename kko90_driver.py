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


agency_all = Agency.objects.all()
# agency_all = Agency.objects.filter(agency_name='FURIXON')
agency_count = agency_all.count()

print('### 전체 지점 수 => ', agency_count)


# LOGIN_INFO = {
#     'siteUrl': 'https://center-pf.kakao.com/',
#     'homeUrl': 'https://qsm.qoo10.jp/GMKT.INC.Gsm.Web/default.aspx',
#     'userId': 'javis.furixon@gmail.com',
#     'userPassword': 'const209!!'
# }

LOGIN_INFO = {
    'siteUrl': 'https://center-pf.kakao.com/',
}

def get_driver(agency):
    # 크롬 드라이버 로딩
    jobDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    jobDriver.implicitly_wait(3)
    jobDriver.get(LOGIN_INFO['siteUrl'])

    print('### 웹 드라이버 로딩을 시작합니다.........\n')

    # 카카오 로그인
    jobDriver.find_element(By.XPATH, '//*[@id="id_email_2"]').send_keys(agency.kko_id)
    jobDriver.find_element(By.XPATH, '//*[@id="id_password_3"]').send_keys(agency.kko_pass)

    try:
        # 캡챠 처리
        # capcha = input('Input Capcha Text : ')
        # jobDriver.find_element_by_xpath('recaptcha_response_field').send_keys(capcha)
        jobDriver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]').click()

        print('### 로그인이 완료되었습니다............\n')

    except Exception as e:
        print('로그인 실패!')
        jobDriver.find_element(By.NAME, 'txtLoginID').clear()
        jobDriver.find_element(By.XPATH, '//*[@id="id_email_2"]').send_keys(agency.kko_id)
        jobDriver.find_element(By.XPATH, '//*[@id="id_password_3"]').send_keys(agency.kko_pass)

        jobDriver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]').click()

        print('로그인이 완료되었습니다............\n')

    # # 한국어로 변경
    # jobDriver.find_element_by_xpath('//*[@id="header"]/div[1]/div[1]/a/span').click()
    # jobDriver.find_element_by_xpath('//*[@id="LayerSelectLang"]/ul/li[1]/span/a').click()

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
    jobDriver = driverData[0]
    driverName = driverData[1].agency_name

    print('### Keep Alive!')
    jobDriver.refresh()

    url = jobDriver.command_executor._url
    session_id = jobDriver.session_id

    print('Browser URL : ', url)
    print('Session ID : ', session_id)

    with open('./kko90_session_{}.txt'.format(driverName), 'w') as f:
        f.write(url)
        f.write('||')
        f.write(session_id)

    # Q Analytics 페이지 이동
    # driver.get('https://qsm.qoo10.jp/GMKT.INC.Gsm.Web/Goods/GoodsAnalytics.aspx')


# 드라이버 갯수 입력
# driver_count = int(input('### 드라이버 갯수 입력 (1~9) => '))
# driver_count = agency_count

for agency in agency_all:
    # driver_name = "{}".format(agency.agency_name)
    driver = get_driver(agency)
    schedule.every().hour.at(":33").do(job, [driver, agency])  # 매시 10분에 리프레쉬



# schedule.every().hour.at(":10").do(job, [driver1, "d1"])  # 매시 10분에 리프레쉬
# schedule.every().hour.at(":10").do(job, [driver2, "d2"])
# schedule.every().hour.at(":10").do(job, [driver3, "d3"])
# schedule.every().hour.at(":10").do(job, [driver4, "d4"])
# schedule.every().hour.at(":10").do(job, [driver5, "d5"])
# schedule.every().hour.at(":10").do(job, [driver6, "d6"])
# schedule.every().hour.at(":10").do(job, [driver7, "d7"])
# schedule.every().hour.at(":10").do(job, [driver8, "d8"])
# schedule.every().hour.at(":10").do(job, [driver9, "d9"])

while True:
    schedule.run_pending()
    time.sleep(1)