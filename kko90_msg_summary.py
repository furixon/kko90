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

from selenium.webdriver.remote import remote_connection
from selenium.webdriver.remote.command import Command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kko90.settings")

# 장고 서버 패키지 로딩
import django
django.setup()

from cms.models import KkoMsg, Agency, MsgTemplate

# Generate Summary Data
def make_summary_data():
    agency_all = Agency.objects.all()
    agency_count = agency_all.count()

    print('### 전체 지점 수 => ', agency_count)

    # print(*agency_all, sep='\n')
    print(*agency_all)

    summary_data = []
    total_data = {}
    total_data['mag_total'] = 0
    total_data['total_request'] = 0
    total_data['total_success'] = 0
    total_data['total_error'] = 0
    total_data['total_no_content'] = 0

    agency_summary_msg_list = []

    for agency in agency_all:
        agency_summary = {}
        agency_summary['mag_total'] = KkoMsg.objects.filter(agency_name=agency.agency_name, request_at__date=date.today()).count()
        agency_summary['total_request'] = KkoMsg.objects.filter(agency_name=agency.agency_name, request_at__date=date.today(), result='요청').count()
        agency_summary['total_success'] = KkoMsg.objects.filter(agency_name=agency.agency_name, request_at__date=date.today(), result='전송완료').count()
        agency_summary['total_error'] = KkoMsg.objects.filter(agency_name=agency.agency_name, request_at__date=date.today(), result='에러').count()
        agency_summary['total_no_content'] = KkoMsg.objects.filter(agency_name=agency.agency_name, request_at__date=date.today(), result='미전송(내용없음)').count()
        agency_summary['agency_name'] = agency.agency_name

        summary_data.append(agency_summary)

        total_data['mag_total'] += agency_summary['mag_total']
        total_data['total_request'] += agency_summary['total_request']
        total_data['total_success'] += agency_summary['total_success']
        total_data['total_error'] += agency_summary['total_error']
        total_data['total_no_content'] += agency_summary['total_no_content']

        agency_summary_msg = '''
        ### 지점별 전송 현황
    # {} 지점
    전체 : {}건
    성공 : {}건
    실패 : {}건
    잔여 : {}건
    미전송(내용없음) : {}건
        '''.format(agency_summary['agency_name'], agency_summary['mag_total'], agency_summary['total_success'], agency_summary['total_error'], agency_summary['total_request'], agency_summary['total_no_content'])

        agency_summary_msg_list.append(agency_summary_msg)

    summary_msg = '''
    ### 90일 카톡 전송 현황
    전체 : {}건
    성공 : {}건
    실패 : {}건
    잔여 : {}건
    미전송(내용없음) : {}건
    '''.format(total_data['mag_total'], total_data['total_success'], total_data['total_error'], total_data['total_request'], total_data['total_no_content'])

    # Administrator
    admin = {}
    admin_agency = {}
    admin['agency'] = Agency.objects.get(agency_name='FURIXON')
    admin['repoter'] = ['https://center-pf.kakao.com/_wXqxlxj/chats/4854572686133408', 'https://center-pf.kakao.com/_wXqxlxj/chats/4883559030539350']
    admin['summary_msg'] = summary_msg
    admin['agency_summary_msg_list'] = agency_summary_msg_list

    admin_agency['agency'] = Agency.objects.get(agency_name='유비플러스')
    admin_agency['repoter'] = ['https://center-pf.kakao.com/_pZSNb/chats/4839158588628032', 'https://center-pf.kakao.com/_pZSNb/chats/4839174624892968']
    admin_agency['summary_msg'] = summary_msg
    admin_agency['agency_summary_msg_list'] = agency_summary_msg_list

    return [admin, admin_agency]

def job(receiver):
    admin, admin_agency = make_summary_data()

    if receiver == 'FURIXON':
        final_admin = admin
    elif receiver == '유비플러스':
        final_admin = admin_agency

    agency = final_admin['agency']
    print('### {} Summary 메시지 전송 시작'.format(agency.agency_name))

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

    ## Summary 리포트 전송
    for repoter in final_admin['repoter']:
        try:
            driver.get(repoter)
            total_summary_msg = final_admin['summary_msg']
            kko_msg_line = total_summary_msg.split('\n')
            print(kko_msg_line)
            # Total 메시지 전송
            for msg_line in kko_msg_line:
                chatWrite = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chatWrite"]')))
                chatWrite.send_keys(msg_line)
                chatWrite.send_keys(Keys.SHIFT + '\n')
            msg_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="kakaoWrap"]//button[text()="전송"]')))
            driver.execute_script("arguments[0].click();", msg_button)
            time.sleep(1)

            # Agency 메시지 전송
            # for agency_summary_msg in final_admin['agency_summary_msg_list']:
            #     kko_msg_line = agency_summary_msg.split('\n')
            #     for msg_line in kko_msg_line:
            #         time.sleep(0.5)
            #         driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(msg_line)
            #         driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(Keys.SHIFT + '\n')
            #     msg_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button')
            #     driver.execute_script("arguments[0].click();", msg_button)
            #     time.sleep(1)
            # driver.get(chatlist_url)
        except Exception as e:
            print('### Summary 메시지 전송 에러 : {}'.format(e))
            driver.get(chatlist_url)
            continue
    
    # 메시지 전송 완료 후 채팅 리스트로 복귀
    driver.get(chatlist_url)

## Start Summary report scheduler
print('### Summary report scheduler started')

schedule_weekday = schedule.Scheduler()
schedule_weekend = schedule.Scheduler()

# job('유비플러스')
job('FURIXON')
job('유비플러스')
schedule_weekday.every().day.at('17:30').do(job, 'FURIXON')
schedule_weekday.every().day.at('17:35').do(job, '유비플러스')
schedule_weekday.every().day.at('18:00').do(job, 'FURIXON')
schedule_weekday.every().day.at('18:30').do(job, 'FURIXON')
schedule_weekday.every().day.at('18:35').do(job, '유비플러스')
schedule_weekday.every().day.at('19:00').do(job, 'FURIXON')
schedule_weekday.every().day.at('19:30').do(job, 'FURIXON')
schedule_weekday.every().day.at('19:35').do(job, '유비플러스')

schedule_weekend.every().day.at('14:30').do(job, 'FURIXON')
schedule_weekend.every().day.at('14:35').do(job, '유비플러스')
schedule_weekend.every().day.at('15:00').do(job, 'FURIXON')
schedule_weekend.every().day.at('15:30').do(job, 'FURIXON')
schedule_weekend.every().day.at('15:35').do(job, '유비플러스')
schedule_weekend.every().day.at('16:00').do(job, 'FURIXON')
schedule_weekend.every().day.at('16:30').do(job, 'FURIXON')
schedule_weekend.every().day.at('16:35').do(job, '유비플러스')

# Test
# schedule_weekday.every(5).seconds.do(job, 'FURIXON')
# schedule_weekend.every(5).seconds.do(job, 'FURIXON')

while True:
    # print(datetime.now().weekday())
    if datetime.now().weekday() < 5:
        # print(datetime.now())
        # print(datetime.now().weekday())
        schedule_weekday.run_pending()
        time.sleep(1)  # 1초 주기
    elif datetime.now().weekday() == 5:
        # print(datetime.now())
        # print(datetime.now().weekday())
        schedule_weekend.run_pending()
        time.sleep(1)  # 1초 주기
    else:
        time.sleep(1)  # 1초 주기
        continue
