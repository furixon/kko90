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


def job():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kko90.settings")

    import django
    django.setup()

    from cms.models import KkoMsg, Agency, MsgTemplate

    today = date.today()
    print(today)
    msg_list = KkoMsg.objects.filter(result='요청', request_at__icontains=today)
    # msg_list = KkoMsg.objects.filter(agency_name='FURIXON', result='요청')
    print(msg_list)


    for msg in msg_list:

        # 세션 파일에서 URL, 세션정보 가져와 기존 큐텐 브라우저 드라이버 연결
        try:
            with open('./kko90_session_{}.txt'.format(msg.agency_name), 'r') as f:
                session_list = f.readline().split('||')
            url = session_list[0]
            session_id = session_list[1]

            print('### 접속 드라이버 => ', url, session_id)

        except Exception as e:
            print('### 드라이버 세션 파일 로딩 에러 : {}'.format(e))

        # 파일 업로드 에러 방지를 위해 remote_connection.py 파일의 selenium site-package에서 218행을 다음에서 다음으로 변경
        rmt_con = remote_connection.RemoteConnection(url)
        rmt_con._commands.update({
            Command.UPLOAD_FILE: ("POST", "/session/$sessionId/file")
        })

        driver = webdriver.Remote(command_executor=rmt_con,desired_capabilities={})
        driver.close()   # this prevents the dummy browser
        driver.session_id = session_id

        # 미확인 메시지 리스트 생성
        chat_list_url = msg.kko_url.split('chats/')[0] + 'chats'
        chat_id = msg.kko_url.split('chats/')[1]
        print(chat_list_url, chat_id)
        driver.get(chat_list_url)
        time.sleep(1)

        chat_select_id = 'chat-select-' + chat_id
        chat_element = driver.find_element(By.ID, chat_select_id)
        chat_element_parent = chat_element.find_element(By.XPATH, '../../../../..')

        try:  # 미확인 메시지 수 확인
            num_round = int(chat_element_parent.find_element(By.CLASS_NAME, 'num_round').text)
            txt_name = chat_element_parent.find_element(By.CLASS_NAME, 'txt_name').text
        except Exception as e:
            print('### 미확인 메시지 없음 : {}'.format(e))
            num_round = 0
            txt_name = chat_element_parent.find_element(By.CLASS_NAME, 'txt_name').text
        
        if num_round > 0:
            print('### 미확인 메시지')
            print('고객명: {} / 건수: {} / 확인시간:{}'.format(txt_name, num_round, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            # 미확인 메시지 내역 전송
        
        # 메시지 전송 시작
        kko_url = msg.kko_url
        kko_msg = MsgTemplate.objects.filter(msg_index=msg.msg_index)[0].msg_content
        kko_msg_line = kko_msg.replace('\n', '\r').split('\r')
        # kko_image = 'http://furixon501.iptime.org:8001/media/' + str(MsgTemplate.objects.filter(msg_index=msg.msg_index)[0].img_content)
        kko_image = os.getcwd() + '/media/' + str(MsgTemplate.objects.filter(msg_index=msg.msg_index)[0].img_content)
        kko_link = MsgTemplate.objects.filter(msg_index=msg.msg_index)[0].link_content

        driver.get(kko_url)
        # 메시지 전송
        for msg_line in kko_msg_line:
            driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(msg_line)
            driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(Keys.SHIFT + '\n')
        msg_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button')
        driver.execute_script("arguments[0].click();", msg_button)

        # 이미지 전송
        img_button = driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/div[2]/div[1]/div[1]/input[@type="file"]')
        if kko_image == os.getcwd() + '/media/':
            print('### No images')
        else:
            time.sleep(0.5)
            print('### 이미지 업로드 {}'.format(kko_image)) 
            img_button.send_keys(kko_image)

        # 링크 전송
        if kko_link:
            time.sleep(0.5)
            driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(kko_link)
            driver.execute_script("arguments[0].click();", msg_button)

        time.sleep(1)

        msg.result = '요청'
        msg.save()

# def job_set(adData):
#     print('### job_set 실행')
#     print(driver)
#     delay = 3

#     # Q스페셜 페이지 이동
#     driver.get('https://qsm.qoo10.jp/GMKT.INC.Gsm.Web/QSpecial/QSpecialPlus.aspx')
#     driver.find_element_by_xpath('//*[@id="s_sid"]').send_keys(adData[2])
#     driver.find_element_by_xpath('//*[@id="qSpecialSearchBtn"]').click()

#     # driver.implicitly_wait(500)

#     try:
#         sid_result = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__grid_Grid_QSpecialSearchList"]/div[2]/table/tbody/tr[2]/td[1]')))
#         sid_resultAction = ActionChains(driver)
#         sid_resultAction.double_click(sid_result).perform()

#         picker_btn = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[9]/h2')))
#         # picker_btnAction = ActionChains(driver)
#         # picker_btnAction.move_to_element(picker_btn).perform()
#         picker_btn.location_once_scrolled_into_view

#         # driver.find_element_by_xpath('//*[@id="setting_qspecial_plus_info_date"]').click()
#         # preminum_date = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="display_date_tbl"]')))


#         js = """
#             var el_1 = document.createElement("tbody");
#             var el_2 = document.createElement("tr");
#             var el_3 = document.createElement("td");
#             el_3.setAttribute("class", "ctgdt_lst");
#             var el_4 = document.createElement("div");
#             el_4.setAttribute("value", "{}");
#             var el_5 = document.createElement("input");
#             el_5.setAttribute("type", "text");
#             el_5.setAttribute("name", "qspecial_selected_date_text");
#             el_5.setAttribute("size", "30");
#             el_5.setAttribute("value", "{}");
#             el_5.setAttribute("overcheck", "N");
            
#             el_4.appendChild(el_5);
#             el_3.appendChild(el_4);
#             el_2.appendChild(el_3);
#             el_1.appendChild(el_2);
#             document.getElementById("display_date_tbl").appendChild(el_1);

#             document.getElementById("setting_qspecial_plus_info_date_text").setAttribute("value", "{}");            
#         """.format(adData[1], adData[1], adData[1])

#         driver.execute_script(js)

#         if adData[3] == 'M':
#             set_landing_js = '''
#                 document.getElementById("rdo_detail_landing_type_qspecial").removeAttribute("checked")
#                 document.getElementById("rdo_detail_landing_type_sellershop").setAttribute("checked", "checked")
#             '''
#             driver.execute_script(set_landing_js)

#     except Exception as e:
#         print(e)
        

# def job_click(jobDriver):
#     print('### job_click 실행')
#     delay = 10

#     try:
#         # elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="display_date_tbl"]/tbody/tr/td/div/input')))

#         # if elem:
#         #     print('속성 변경')
#         #     jobDriver.execute_script("arguments[0].setAttribute('overcheck','N')", elem)
#         #     jobDriver.execute_script("arguments[0].setAttribute('value', ad_date)", elem)

#         while True:
#             jobDriver.find_element_by_xpath('//*[@id="QspecialPlus_request"]').click()
#             WebDriverWait(jobDriver, delay).until(EC.alert_is_present())
#             alert = jobDriver.switch_to.alert
#             print(alert.text)
#             alert.accept()
#             WebDriverWait(jobDriver, delay).until(EC.alert_is_present())
#             alert = jobDriver.switch_to.alert
#             print(alert.text)
#             alert.accept()

#     except Exception as e:
#         print(e)


# # schedule.every().day.at("22:11:00").do(job_set, driver)
# # schedule.every().day.at("22:11:10").do(job_click, driver)

# # scheduler1 = schedule.Scheduler()

# # job_set(today_ad_list[today_ad_no - 1])
# schedule.every().day.at("10:59:40").do(job_set, today_ad_list[today_ad_no - 1])
schedule.every(1).seconds.do(job)

while True:
    schedule.run_pending()
    print('### 주기')
    time.sleep(1)  # 1초 주기