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
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

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

LOGIN_INFO = {
    'siteUrl': 'https://center-pf.kakao.com/',
    'admin_id': 'javis.furixon@gmail.com',
    'admin_pass': 'const209!!',
}

# 웹드라이버 딜레이 시간
delay = 3

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 드라이버 로딩
try:
    driver = webdriver.Chrome(options=chrome_options, service=Service('./drivers/chromedriver'))
except:
    print('### 크롬 드라이버 로딩 실패, installing chromedriver.......\n')
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager(path='./drivers').install()))

driver.implicitly_wait(3)
driver.get(LOGIN_INFO['siteUrl'])

print('### 웹 드라이버 로딩을 시작합니다.........\n')

# 카카오 어드민 로그인
driver.find_element(By.XPATH, '//*[@id="loginId--1"]').send_keys(LOGIN_INFO['admin_id'])
driver.find_element(By.XPATH, '//*[@id="password--2"]').send_keys(LOGIN_INFO['admin_pass'])

try:
    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()

    print('### 로그인이 완료되었습니다............\n')

except Exception as e:
    print('로그인 실패!')
    driver.find_element(By.NAME, 'txtLoginID').clear()
    driver.find_element(By.XPATH, '//*[@id="id_email_2"]').send_keys(agency.kko_id)
    driver.find_element(By.XPATH, '//*[@id="id_password_3"]').send_keys(agency.kko_pass)

    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]').click()

    print('로그인이 완료되었습니다............\n')

input('### 인증이 완료되면 엔터키를 눌러주세요............\n')

def job(agency_all):
    for agency in agency_all:
        print('### {} 지점 메시지 전송 시작'.format(agency.agency_name))

        # URLS
        dashboard_url = agency.report_url.split('chats/')[0]
        chatlist_url = dashboard_url + 'chats/'

        # 지점의 메시지 리스트 불러오기
        today = date.today()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('### 현재시간 {}'.format(now))

        # msg_list = KkoMsg.objects.filter(result='요청', request_at__icontains=today)
        msg_list = KkoMsg.objects.filter(agency_name=agency.agency_name, result='요청')

        if msg_list.exists():
            # Move to chatlist
            driver.get(chatlist_url)
            print('### {} 지점 메시지 전송 시작'.format(agency.agency_name))

            try:
                # 미확인 메시지 리스트 전송
                report_msg = '### 미확인 메시지 (확인시간 : {})'.format(now)
                driver.get(chatlist_url)
                
                ## 읽지 않은 상담 리스트 필터링
                filter_button_select = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[2]/div[1]/div[1]/button')
                driver.execute_script("arguments[0].click();", filter_button_select)

                unread_button_select = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mArticle"]/div[2]/div[1]/div[1]/div[2]/div/ul/li[3]/button')))
                driver.execute_script("arguments[0].click();", unread_button_select)

                ## 읽지 않은 상담 조회 및 리포트 생성
                time.sleep(1)
                element_chat_list = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'ReactVirtualized__List')))
                # element_chat_list = driver.find_element(By.CLASS_NAME, 'ReactVirtualized__List')
                txt_name_list = element_chat_list.find_elements(By.CLASS_NAME, 'txt_name')
                num_round_list = element_chat_list.find_elements(By.CLASS_NAME, 'num_round')

                if len(txt_name_list) > 0:
                    for txt_name, num_round in zip(txt_name_list, num_round_list):
                        print(txt_name.text, num_round.text)
                        report_msg = report_msg + '\n 고객명: {} / 건수: {}'.format(txt_name.text, num_round.text)
                else:
                    report_msg = report_msg + '\n 읽지 않은 상담이 없습니다.'

                ## 읽지 않은 상담 리포트 전송
                driver.get(agency.report_url)
                kko_msg_line = report_msg.split('\n')
                print(kko_msg_line)

                # 메시지 전송
                for msg_line in kko_msg_line:
                    driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(msg_line)
                    driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(Keys.SHIFT + '\n')
                # msg_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button')
                msg_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="kakaoWrap"]//button[text()="전송"]')))
                # msg_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]//button[text()="전송"]')
                driver.execute_script("arguments[0].click();", msg_button)
                time.sleep(0.5)
            except Exception as e:
                print('### 미확인 메시지 리포트 전송 에러 : {}'.format(e))

            # 메시지 전송
            for msg in msg_list:
                
                # 메시지 전송 시작
                try:
                    kko_url = msg.kko_url
                    kko_msg = MsgTemplate.objects.filter(msg_index=msg.msg_index)[0].msg_content
                    
                    if kko_msg is None:  # 메시지 내용이 없을 경우 다음 대상자로 패스
                        print('### 미전송 / 메시지 내용 없음 : {} {} {}'.format(msg.agency_name, msg.client_name, msg.msg_index))
                        msg.result = '미전송(내용없음)'
                        msg.save()
                        continue
                    kko_msg_line = kko_msg.replace('\n', '\r').split('\r')
                    kko_image = os.getcwd() + '/media/' + str(MsgTemplate.objects.filter(msg_index=msg.msg_index)[0].img_content)
                    kko_link = MsgTemplate.objects.filter(msg_index=msg.msg_index)[0].link_content

                    driver.get(kko_url)
                    # 메시지 전송
                    for msg_line in kko_msg_line:
                        chatWrite = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chatWrite"]')))
                        chatWrite.send_keys(msg_line)
                        chatWrite.send_keys(Keys.SHIFT + '\n')
                        # driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(msg_line)
                        # driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(Keys.SHIFT + '\n')
                    # msg_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button')
                    msg_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="kakaoWrap"]//button[text()="전송"]')))
                    # msg_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]//button[text()="전송"]')
                    driver.execute_script("arguments[0].click();", msg_button)
                    time.sleep(0.5)

                    # 이미지 전송
                    # img_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/div[2]/div[1]/div[1]/input[@type="file"]')
                    
                    # img_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]//input[@type="file"]')
                    if kko_image == os.getcwd() + '/media/':
                        print('### No images')
                    else:
                        img_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="kakaoWrap"]//input[@type="file"]')))
                        # print('### 이미지 업로드 {}'.format(kko_image)) 
                        img_button.send_keys(kko_image)
                        time.sleep(0.5)

                    # 링크 전송
                    if kko_link:
                        chatWrite = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chatWrite"]')))
                        chatWrite.send_keys(kko_link)
                        # driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(kko_link)
                        driver.execute_script("arguments[0].click();", msg_button)

                    time.sleep(0.5)
                    print('### {}지점 {}고객 {} 메시지 전송 완료'.format(msg.agency_name, msg.client_name, msg.msg_index))
                    msg.result = '전송완료'
                    msg.save()
                except Exception as e:
                    print('### 전송 에러', e)
                    # 에러 중 채널 추가 요청 안내 팝업 레이어가 원인일 경우 Change layer                    
                    try:
                        # msg_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[3]/div/form/fieldset/button')
                        msg_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="kakaoWrap"]//button[text()="전송"]')))
                        driver.execute_script("arguments[0].click();", msg_button)
                        time.sleep(0.5)

                        # 이미지 전송
                        # img_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[3]/div/form/fieldset/div[2]/div[1]/div[1]/input[@type="file"]')
                        if kko_image == os.getcwd() + '/media/':
                            print('### No images')
                        else:
                            img_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="kakaoWrap"]//input[@type="file"]')))
                            # print('### 이미지 업로드 {}'.format(kko_image)) 
                            img_button.send_keys(kko_image)
                            time.sleep(0.5)

                        # 링크 전송
                        if kko_link:
                            chatWrite = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chatWrite"]')))
                            chatWrite.send_keys(kko_link)
                            # driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(kko_link)
                            driver.execute_script("arguments[0].click();", msg_button)

                        time.sleep(0.5)
                        print('### {}지점 {}고객 {} 메시지 전송 완료'.format(msg.agency_name, msg.client_name, msg.msg_index))
                        msg.result = '전송완료'
                        msg.save()
                        continue
                    except Exception as e:
                        print('### 전송 에러', e)
                        time.sleep(1)
                        print('### {}지점 {}고객 {} 메시지 전송 ERROR!'.format(msg.agency_name, msg.client_name, msg.msg_index))
                        msg.result = '에러'
                        msg.save()
                        continue
            # 메시지 전송 완료 후 채팅 리스트로 복귀
            driver.get(chatlist_url)
        else:
            print('### {}지점 메시지 요청이 없습니다.'.format(agency.agency_name))


def job_refrsh(agency_all):
    now = datetime.now()
    print(now.hour)
    if (now.hour >= 13 and now.hour <= 14) or (now.hour >= 17 and now.hour <= 18):
        print('### Off keep alive')
        pass
    else:

        for agency in agency_all:
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
                print('### 드라이버 세션 파일 로딩 에러 : {}'.format(agency.agency_name))
                print(e)
                exit()

            # 파일 업로드 에러 방지를 위해 remote_connection.py 파일의 selenium site-package에서 218행을 다음에서 다음으로 변경
            rmt_con = remote_connection.RemoteConnection(url)
            rmt_con._commands.update({
                Command.UPLOAD_FILE: ("POST", "/session/$sessionId/file")
            })

            driver = webdriver.Remote(command_executor=rmt_con,desired_capabilities={})
            driver.close()   # this prevents the dummy browser
            driver.session_id = session_id

            print('### {} 지점 Keep Alive!'.format(agency.agency_name))
            driver.refresh()
            time.sleep(1)

            url = driver.command_executor._url
            session_id = driver.session_id

            print('Browser URL : ', url)
            print('Session ID : ', session_id)


# 지점 선택
# target_agency = ['FURIXON']
target_agency = ['대전점', '안양평촌점', '수원점', '일산점', '인천점']
# target_agency = ['대전점', '안양평촌점', ]
agency_all = Agency.objects.filter(agency_name__in=target_agency)
agency_count = agency_all.count()

print('### 전체 지점 수 => ', agency_count)

# print(*agency_all, sep='\n')
print(*agency_all)

# 지점 선택
# select_agency_name = input('### 지점 선택 => ')

# try:
#     agency = agency_all.get(agency_name=select_agency_name)
# except Exception as e:
#     print('### 해당 지점 정보가 없습니다.', e)
#     exit()

# job(agency_all)
# schedule.every().monday.at('17:00').do(job, agency_all)
# schedule.every().tuesday.at('17:00').do(job, agency_all)
# schedule.every().wednesday.at('17:00').do(job, agency_all)
# schedule.every().thursday.at('17:00').do(job, agency_all)
# schedule.every().friday.at('17:00').do(job, agency_all)
# schedule.every().saturday.at('13:30').do(job, agency_all)

schedule.every().day.at('14:10').do(job, agency_all)
schedule.every().day.at('17:40').do(job, agency_all)

# Refresh
# schedule.every(3).minutes.do(job_refrsh, agency_all)

while True:
    schedule.run_pending()
    # print('### 전체 지점 스케줄 데몬 실행중')
    time.sleep(1)  # 1초 주기