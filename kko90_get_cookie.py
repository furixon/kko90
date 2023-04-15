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
from selenium.webdriver.support.select import Select

from webdriver_manager.chrome import ChromeDriverManager

# from bs4 import BeautifulSoup
# from rakutenAutoLib_oy import *
import sys
import time
from datetime import datetime, timedelta, date
import schedule
import csv
import os
import pickle

from selenium.webdriver.remote import remote_connection
from selenium.webdriver.remote.command import Command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kko90.settings")

# 장고 서버 패키지 로딩
import django
django.setup()

from cms.models import KkoMsg, Agency, MsgTemplate

import django
django.setup()

from cms.models import KkoMsg, Agency, MsgTemplate

def get_cookie_file(agency):
    # URLS
    dashboard_url = agency.report_url.split('chats/')[0]
    chatlist_url = dashboard_url + 'chats/'

    # 웹드라이버 딜레이 시간
    delay = 3

    # 드라이버 로딩
    try:
        with open('./kko90_session_{}.txt'.format(agency.agency_name), 'r') as f:
            session_list = f.readline().split('||')
        url = session_list[0]
        session_id = session_list[1]

        print('### 접속 드라이버 => ', url, session_id)

    except Exception as e:
        print('### 드라이버 세션 파일 로딩 에러 : {}'.format(e))
        exit()

    # 파일 업로드 에러 방지를 위해 remote_connection.py 파일의 selenium site-package에서 218행을 다음에서 다음으로 변경
    rmt_con = remote_connection.RemoteConnection(url)
    rmt_con._commands.update({
        Command.UPLOAD_FILE: ("POST", "/session/$sessionId/file")
    })

    driver = webdriver.Remote(command_executor=rmt_con,desired_capabilities={})
    driver.close()   # this prevents the dummy browser
    driver.session_id = session_id

    driver.get(chatlist_url)
    time.sleep(1)

    with open("{}.pickle".format(agency.agency_name), 'wb') as fw:
        print('### 쿠키 파일 저장')
        pickle.dump(driver.get_cookies(), fw)


# 지점 선택
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

get_cookie_file(agency)
