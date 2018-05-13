# -*- coding: utf-8 -*-
"""
Created on Fri May 11 12:07:16 2018

@author: elara
"""




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import math
import multiprocessing 
cores=4
import requests
from bs4 import BeautifulSoup
import numpy as np
from time import sleep

data_type = 'invtout'
max_page = 499
first_page = [int(i) for i in np.arange(1,max_page,int(max_page/4))]



def get_data(driver):
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))   
    #print('1')
    table_body = driver.find_element_by_tag_name('tbody')
    table_line = table_body.find_elements_by_tag_name('tr')
    table = pd.DataFrame([[j.text for j in i.find_elements_by_tag_name('td') if len(j.text)>0] for i in table_line])
    return table



def get_data_n(page_num, n=int(max_page/4)+5):
    print('start',page_num)
    chromePath = r'D:\Elara\Downloads\chromedriver_win32new\chromedriver.exe' 
    login_url = 'https://www.itjuzi.com/user/login'
    if data_type == 'investevent':
        data_url = 'http://radar.itjuzi.com/investevent'
    else:
        data_url = 'http://radar.itjuzi.com/investevent/' + data_type
    user_name = 
    pw = 
    
    data_all = []

    driver = webdriver.Chrome(executable_path= chromePath) #开浏览器
    driver.implicitly_wait(30)
    driver.get(login_url)
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "create_account_email")))      #等待载入 
    user_name_elem = driver.find_element_by_id("create_account_email") #找到用户名
    user_name_elem.send_keys(user_name) #输入用户名
    pw_elem = driver.find_element_by_id("create_account_password") #找到密码
    pw_elem.send_keys(pw) #输入密码
    driver.find_element_by_xpath('//*[@id="login_btn"]').click() #点击登录
    
    driver.get(data_url) #打开网页
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))   #等待载入   
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "goto_page_num")))
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    page_num_elem = driver.find_element_by_id("goto_page_num") #找到页码框
    page_num_elem.clear()
    page_num_elem.send_keys(page_num) #输入页码
    sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    driver.find_element_by_id('goto_page_btn').click() #点击确定
    flag = 0
    while flag==0:
        try:
            data = get_data(driver)
            if page_num<first_page[-1] and len(data)<15:
                data = get_data(driver)
                print(page_num)
            data_all.append(data)
            flag = 1
        except:
            flag = 0
    
    for i in range(2,n+5):

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        driver.find_element_by_class_name('next').find_element_by_tag_name('a').click()
        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        flag = 0
        while flag==0:
            try:
                data = get_data(driver)
                if page_num<first_page[-1] and len(data)<15:
                    data = get_data(driver)
                    print(page_num,i)
                data_all.append(data)
                flag = 1
            except:
                flag = 0
      
    x = pd.concat(data_all, axis=0)
    x.to_csv('D:\\Elara\\Documents\\itjuzi\\investevent\\'+data_type+'\\'+'x\\'+str(page_num)+'_'+str(n)+'.csv')
    return data_all



if __name__ ==  '__main__':
    
    first_page = [int(i) for i in np.arange(1,max_page,int(max_page/4))]
    
    multiprocessing.freeze_support() 
    pool = multiprocessing.Pool(processes = cores)
    res = pool.map(get_data_n,first_page)
    pool.close()
    
    data = []
    for i in res:
        data += i
    
    x = pd.concat(data,axis=0)
    x.to_csv('D:\\Elara\\Documents\\itjuzi\\investevent\\'+data_type+'\\'+data_type+'.csv')

#x = get_data_n(5172,12)
#
#
#y = pd.concat(x,axis=0)




#req = requests.Session()
#
#cookies = driver.get_cookies()
#cookies.append({'name':'_gat','value':'1'})
#for cookie in cookies:
#        req.cookies.set(cookie['name'],cookie['value'])
#r = req.get('http://radar.itjuzi.com/company/infonew?page=2')
#r.text

#y = pd.read_csv('D:\\Elara\\Documents\\itjuzi\\investevent\\investevent\\x.csv',encoding='gbk',engine='python')
#y.columns = ['index','时间','公司名称','轮次','金额','投资方']

y = pd.read_csv('D:\\Elara\\Documents\\itjuzi\\investevent\\'+data_type+'\\'+data_type+'.csv',encoding='gbk',engine='python')
y.columns = ['index','时间','公司名称','轮次','金额','投资方']
y = y[['时间','公司名称','轮次','金额','投资方']].drop_duplicates()  

y.to_csv('D:\\Elara\\Documents\\itjuzi\\investevent\\'+data_type+'\\'+data_type+'res.csv',index=False)
