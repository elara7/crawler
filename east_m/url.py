# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 19:19:45 2017

@author: elara
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import multiprocessing 
cores=multiprocessing.cpu_count()*2
cores = 5


def get_url_list(keyword):
    driver = webdriver.Chrome() #开浏览器
    driver.get("http://so.eastmoney.com") #打开网页
    try:
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "searchSuggest")))
        print(keyword, 'get searchSuggest succeed')
    except:
        print(keyword, 'get searchSuggest failed')
        return 0
    elem = driver.find_element_by_id("searchSuggest") #找到搜索框
    elem.send_keys(keyword) #输入关键字
    elem.send_keys(Keys.RETURN)
    urllist=[]
    i=1
    while 1:
        try:
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "news-item")))
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "page-group-active")))
            print(keyword,str(i),'get news-item and page succeed')
        except:
            print(keyword,str(i),'get news-item and page failed')
            break
        news = driver.find_elements_by_class_name('news-item')
        content = pd.DataFrame([
                [i.find_element_by_tag_name('a').text, 
                 i.find_element_by_tag_name('a').get_attribute('href'), 
                 i.find_element_by_tag_name('a').get_attribute('href').split(',')[-1].split('.')[0][:8]] 
                for i in news])
    
        if i ==1:
            urllist = content
            next_page = driver.find_element_by_xpath('/html/body/div[2]/div[3]/ul/li[11]')
        else:
            urllist = urllist.append(content)
            next_page = driver.find_element_by_xpath('/html/body/div[2]/div[3]/ul/li[12]')
        next_page.click()
        i+= 1
        if int(max(content[2])) < 20150101:
            break
    urllist.to_csv('D:\\Elara\\Documents\\paper\\urllist'+keyword+'.csv')
    driver.quit()


if __name__ ==  '__main__':

    a = '浦发银行 (600000)	民生银行 (600016)	中国石化 (600028) 南方航空 (600029)	中信证券 (600030)	招商银行 (600036) 保利地产 (600048)	中国联通 (600050)	同方股份 (600100) 上汽集团 (600104)	北方稀土 (600111)	华夏幸福 (600340) 信威集团 (600485)	康美药业 (600518)	贵州茅台 (600519) 山东黄金 (600547)	绿地控股 (600606)	海通证券 (600837) 伊利股份 (600887)	江苏银行 (600919)	东方证券 (600958) 招商证券 (600999)	大秦铁路 (601006)	中国神华 (601088) 兴业银行 (601166)	北京银行 (601169)	中国铁建 (601186) 东兴证券 (601198)	国泰君安 (601211)	上海银行 (601229) 农业银行 (601288)	中国平安 (601318)	交通银行 (601328) 新华保险 (601336)	中国中铁 (601390)	工商银行 (601398) 中国太保 (601601)	中国人寿 (601628)	中国建筑 (601668) 华泰证券 (601688)	中国中车 (601766)	光大证券 (601788) 中国交建 (601800)	光大银行 (601818)	中国石油 (601857) 中国银河 (601881)	方正证券 (601901)	中国核电 (601985) 中国银行 (601988)	中国重工 (601989)	'
    a=a.split()    
    
    key_word_set = [a[i] for i in range(len(a)) if i%2 == 0]
    
    for i in range(50//5):
        pool = multiprocessing.Pool(processes = cores)
        print('set cores=',cores)
        result = pool.map(get_url_list, key_word_set[i:(i+5)])
        pool.close()

