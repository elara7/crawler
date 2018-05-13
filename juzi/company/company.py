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



data_type = 'company'
max_page = 5174
first_page = [int(i) for i in np.arange(1,max_page,int(max_page/4))]


def get_data(driver):
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "company-list-left"))) 
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "company-list-info")))     
    #print('1')
    company_name_element = driver.find_element_by_class_name("company-list-left") 
    company_name = [i.text for i in company_name_element.find_elements_by_tag_name('a') if len(i.text)>0]
    company_name_content = [i.get_attribute('data-content') for i in company_name_element.find_elements_by_tag_name('a') if len(i.text)>0]
    company_info_element = driver.find_element_by_class_name("company-list-info") 
    company_info = [[j.text for j in i.find_elements_by_tag_name('div')] for i in company_info_element.find_elements_by_tag_name('li')]

    data = pd.concat([pd.DataFrame(company_name),pd.DataFrame(company_name_content),pd.DataFrame(company_info[1:])],axis=1)
    return data



def get_data_n(page_num, n=int(max_page/4)+5):
    chromePath = r'D:\Elara\Downloads\chromedriver_win32new\chromedriver.exe' 
    login_url = 'https://www.itjuzi.com/user/login'
    data_url = 'http://radar.itjuzi.com//company'
    user_name = 
    pw = 、
    
    data_all = []

    driver = webdriver.Chrome(executable_path= chromePath) #开浏览器
    
    driver.get(login_url)
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "create_account_email")))      #等待载入 
    user_name_elem = driver.find_element_by_id("create_account_email") #找到用户名
    user_name_elem.send_keys(user_name) #输入用户名
    pw_elem = driver.find_element_by_id("create_account_password") #找到密码
    pw_elem.send_keys(pw) #输入密码
    driver.find_element_by_xpath('//*[@id="login_btn"]').click() #点击登录
    
    driver.get(data_url) #打开网页
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "goto_page_num")))   #等待载入   
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    page_num_elem = driver.find_element_by_id("goto_page_num") #找到页码框
    page_num_elem.clear()
    page_num_elem.send_keys(page_num) #输入页码
    driver.find_element_by_id('goto_page_btn').click() #点击确定
    flag = 0
    while flag==0:
        try:
            data = get_data(driver)
            if page_num<first_page[-1] and len(data)<20:
                data = get_data(driver)
                print(page_num)
            data_all.append(data)
            flag = 1
        except:
            flag = 0
    
    for i in range(2,n+5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        driver.find_element_by_class_name('next').find_element_by_tag_name('a').click()
        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "company-list-left"))) 
        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "company-list-info")))     
        flag = 0
        while flag==0:
            try:
                data = get_data(driver)
                if page_num<first_page[-1] and len(data)<20:
                    data = get_data(driver)
                    print(page_num,i)
                data_all.append(data)
                flag = 1
            except:
                flag = 0
      
    y = pd.concat(data_all, axis=0)
    y.to_csv('D:\\Elara\\Documents\\itjuzi\\company\\y\\'+str(page_num)+'_'+str(n)+'.csv')
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
    
    y = pd.concat(data,axis=0)
    y.to_csv('D:\\Elara\\Documents\\itjuzi\\company\\y.csv')

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

#y = pd.read_csv('D:\\Elara\\Downloads\\y.csv',encoding='gbk',engine='python')
#y.columns = ['index','公司名称','公司简介','行业','最新融资情况','融资总额','估值','成立时间','规模']
#
#
#temp1 = y.loc[np.logical_and(y['估值']!='未透露', y['估值']!='-'),['公司名称','公司简介','最新融资情况','估值']]
#temp2 = temp1[temp1['最新融资情况'].str.contains(r'2017|2018')]
#temp3 = temp2.drop_duplicates()
#temp3.to_csv('D:\\Elara\\Downloads\\估值不为空.csv')
#
#temp1 = y.loc[y['最新融资情况'].str.contains(r'2017|2018'),['公司名称','公司简介','最新融资情况','估值']]
#temp2 = temp1.drop_duplicates()
#temp2.to_csv('D:\\Elara\\Downloads\\估值可为空.csv')
    
    
    
#y = pd.read_csv('D:\\Elara\\Documents\\itjuzi\\company\\y.csv',encoding='gbk',engine='python')
#y.columns = ['index','公司名称','公司简介','行业','子行业','最新融资情况','融资总额','估值','地区','成立时间','运营状态','规模','新闻数量']
#y = y[['公司名称','公司简介','行业','子行业','最新融资情况','融资总额','估值','地区','成立时间','运营状态','规模','新闻数量']].drop_duplicates() 
#y.to_csv('D:\\Elara\\Documents\\itjuzi\\company\\yres.csv',index=False)
#
#temp1 = y.loc[np.logical_and(y['估值']!='未透露', y['估值']!='-'),y.columns]
#temp2 = temp1[temp1['最新融资情况'].str.contains(r'2017|2018')]
#temp3 = temp2.drop_duplicates()
#temp3.to_csv('D:\\Elara\\Documents\\itjuzi\\company\\估值不为空.csv',index=False)
#
#temp1 = y.loc[y['最新融资情况'].str.contains(r'2017|2018'),y.columns]
#temp2 = temp1.drop_duplicates()
#temp2.to_csv('D:\\Elara\\Documents\\itjuzi\\company\\估值可为空.csv',index=False)