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

    return jobDriver


def job(agency):
    now = datetime.now()
    print(now.hour)
    if now.hour > 16 and now.hour < 19:
        print('### Off keep alive')
        pass
    else:
        agencyName = agency.agency_name  # 에이전시 이름

        driver = get_agency_driver(agency)

        print('### {} 지점 Keep Alive!'.format(agencyName))
        driver.refresh()


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


schedule.every().hours.do(job, agency)
# schedule.every(10).seconds.do(job, agency)

while True:
    schedule.run_pending()
    time.sleep(1)
