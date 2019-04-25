# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import time
import random


# set up time for buying
BUY_TIME = "2018-11-11 0:00:00"



# set up maximum reconnect attempts
MAX_LOGIN_RETRY_TIMES = 6

current_retry_login_times = 0
login_success = False
buy_time_object = datetime.datetime.strptime(BUY_TIME, '%Y-%m-%d %H:%M:%S')

now_time = datetime.datetime.now()
if now_time > buy_time_object:
    print("Unexpected time configuration. Please check...")
    exit(0)

print("Openining Chrome...")
option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
driver = webdriver.Chrome(chrome_options=option)
print("Successfully opened Chrome!")


def __login_operates():
    driver.get("https://www.taobao.com")
    try:
        if driver.find_element_by_link_text("亲，请登录"):
            print("Hasn't signed in. Start login now...")
            driver.find_element_by_link_text("亲，请登录").click()
            print("Please scan the QR code to complete login")
            time.sleep(10)
    except:
        print("Successfully login! Redirecting...")
        global login_success
        global current_retry_login_times
        login_success = True
        current_retry_login_times = 0

def login():
    print("Start attempting to login...")
    __login_operates()
    global current_retry_login_times
    while current_retry_login_times < MAX_LOGIN_RETRY_TIMES:
        current_retry_login_times = current_retry_login_times + 1
        print("Current login attempt：" + str(current_retry_login_times))
        __login_operates()
        if login_success:
            print("Success!")
            break;
        else:
            print("Pending...")

    if not login_success:
        print("Login failed. Exiting...")
        exit(0);
    


    # time.sleep(3)
    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))

def __refresh_keep_alive():
    #重新加载购物车页面，定时操作，防止长时间不操作退出登录
    driver.get("https://cart.taobao.com/cart.htm")
    print("Refreshing to stay alive...")
    time.sleep(60)


def keep_login_and_wait():
    print("Start refreshing to stay alive...")
    while True:
        currentTime = datetime.datetime.now()
        if (buy_time_object - currentTime).seconds > 180:
            __refresh_keep_alive()
        else:
            print("Almost there! Stop refreshing and prepare for purchase...")
            break
    



def buy():
    #打开购物车
    driver.get("https://cart.taobao.com/cart.htm")
    time.sleep(1)
 
    #点击购物车里全选按钮
    if driver.find_element_by_id("J_SelectAll1"):
        driver.find_element_by_id("J_SelectAll1").click()
        print("Selected all goods in the cart...")

    submit_succ = False
    retry_submit_times = 0
    while True:
        now = datetime.datetime.now()
        if now >= buy_time_object:
            print("Start purchasing... Attempts：" + str(retry_submit_times))
            if submit_succ:
                print("Successfully purchased!")
                break
            if retry_submit_times > 50:
                print("Too many times of retrying.. You must have missed the chance..")
                break

            retry_submit_times = retry_submit_times + 1

            try:
                #点击结算按钮
                if driver.find_element_by_id("J_Go"):
                    driver.find_element_by_id("J_Go").click()
                    print("Trying to click submit button...")
                    click_submit_times = 0
                    while True:
                        try:
                            if click_submit_times < 10:
                                driver.find_element_by_link_text('提交订单').click()
                                print("Has clicked submit button!")
                                submit_succ = True
                                break
                            else:
                                print("Submit failed...")
                        except Exception as ee:
                            #print(ee)
                            print("Cannot find submit button... Reload and retry...")
                            click_submit_times = click_submit_times + 1
                            time.sleep(0.1)
            except Exception as e:
                print(e)
                print("Oops... Failed..")

        time.sleep(0.1)


login()
keep_login_and_wait()
buy()
 