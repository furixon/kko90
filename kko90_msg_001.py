'''
    RakutenAuto
    * Auto uploader for Rakuten RMS Version 1.0
    * Copyright (c) 2018 Furixon, Inc. All Rights Reserved.
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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kko90.settings")


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
    msg_list = KkoMsg.objects.filter(result='요청', send_at__contains=today, agency_name='FURIXON')
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

        driver = webdriver.Remote(command_executor=url,desired_capabilities={})
        driver.close()   # this prevents the dummy browser
        driver.session_id = session_id

        kko_url = msg.kko_url
        kko_msg = MsgTemplate.objects.filter(msg_index=msg.msg_index)[0].msg_content

        print(kko_msg)
        print(kko_url)

        driver.get(kko_url)
        driver.find_element(By.XPATH, '//*[@id="chatWrite"]').send_keys(kko_msg)
        driver.find_element(By.XPATH, '//*[@id="kakaoWrap"]/div[1]/div[2]/div/div[2]/div/form/fieldset/button').click()
        time.sleep(2)

        msg.result = '전송완료'
        # msg.save()

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
schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    print('### 주기')
    time.sleep(1)  # 1초 주기