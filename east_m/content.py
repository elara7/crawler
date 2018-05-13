# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 21:54:18 2017

@author: elara
"""
#901274476714889
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import multiprocessing as mp
import random
import time





headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}

#f=open('D:\\host\\host.txt','r')
#ips = f.readlines()
#f.close()
class get_news(object):
    def __init__(self):
        self.api_url =  'http://dev.kuaidaili.com/api/getproxy/?orderid=901274476714889&num=999&area=%E4%B8%AD%E5%9B%BD&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_tr=1&an_an=1&an_ha=1&sp1=1&sep=2'
        #self.ip_pool = requests.request('GET',self.api_url).text.split('\n')
    
    

    def check_ip(self,ip):
        #url = 'http://ip.chinaz.com/getip.aspx'
        url = 'http://finance.eastmoney.com/'
        proxy = 'http://' +  ip.strip()
        #print(proxy)
        proxies = {'http':proxy}
        try :
            response = requests.get(url,proxies = proxies,timeout=1)
            #if response.status_code==200 and len(str(response.content,'utf-8')) <= 100 and 'address' in str(response.content,'utf-8') and '福建省漳州市 电信' not in str(response.content,'utf-8'):
            if response.status_code==200:
                print (proxies)
                return proxy
        except:
            return None
        
    def update_ip_pool(self):
        self.ip_pool = requests.request('GET',self.api_url).text.split('\n')
        
    def get_response_ip(self,url,ip):
        proxy = 'http://' +  ip
        proxies = {'http':proxy}
        t = 1
        while t<=2:
            try:
                response = requests.request("GET", url, headers=headers,timeout=10,proxies = proxies)
                if response.status_code==200:
                    break
            except:
                t += 1
        if t>=3:
            print(url,'                                                        proxy get failed')
            return []
        else:
            return response
        

    def get_response(self,url):
        #print('getting ',url)
        
        t = 1
        while t<=3:
            try:
                response = requests.request("GET", url, headers=headers,timeout=10)
                break
            except:
                t += 1
        if t>=4:
            print(url,'                                                          get response failed')
            return []
        elif response.status_code != 200:
            print(url,'                                                          get response failed')
            return []
        else:
            return response
       
    
    
    def get_soup(self,response):
        try:
            if len(response) == 0:
                return []
        except:
            pass
        try:
            response_text = str(response.content,'utf-8')
            soup = BeautifulSoup(response_text,'html5lib')
        except:
            print(response.url,'                                                          get soup failed')
            return []
    
        all_content=[]
        try:
            all_content = [i['href'] for i in soup.find('div',class_='pagesize').find_all('a') if i.text=='阅读全文']
        except:
            pass
        if len(all_content)>0:
            urlsplit = response.url.split('/')
            urlsplit[4] = all_content[0]
            url = 'http://'+'/'.join(urlsplit[-3:])
            response = self.get_response(url)
            
            try:
                if len(response) == 0:
                    return []
            except:
                pass
            try:
                response_text = str(response.content,'utf-8')
                soup = BeautifulSoup(response_text,'html5lib')
            except:
                print(response.url,'                                                          get soup failed')
                return []
        
        return soup
    
    def get_raw_content(self,soup):
        try:
            if len(soup) == 0:
                return None
        except:
            pass
        try:
            return ' '.join([i.text.strip() for i in soup.find('div',id='ContentBody').find_all('p') if len(i.text)>=10 and not (i.find('span') == None and i.find('a') != None )  and '原标题' not in i.text and '东方财富网每日为您精选行业研报' not in i.text and '责任编辑' not in i.text and '数据来源' not in i.text and '金股)' not in i.text and '点击查看' not in i.text  and '>>>' not in i.text])
        except:
            print('                                                          get raw_content failed')
            return None
    
    def get_cate(self,soup):
        try:
            if len(soup) == 0:
                return None
        except:
            pass
        try:
            return ' '.join([i.text for i in soup.find('div',id='Column_Navigation').find_all('a')])
        except:
            print('                                                          get cate failed')
            return None
    
    def get_source(self,soup):
        try:
            if len(soup) == 0:
                return None
        except:
            pass
        try:
            return soup.find('div',class_='source').text.split('：')[1].strip()
        except:
            print('                                                          get source failed')
            return None
    
    def get_comment_num(self,soup):
        try:
            if len(soup) == 0:
                return None
        except:
            pass
        try:
            return int(soup.find('div',class_='about-left').find('span',class_='cNumShow num').text) #评论数
        except:
            #print('                                                          get comment_num failed')
            return None
    
    def get_uv(self,soup):
        try:
            if len(soup) == 0:
                return None
        except:
            pass
        try:
            return int(soup.find('div',class_='about-left').find('span',class_='num ml5').text) #uv
        except:
            #print('                                                          get uv failed')
            return None
        

        
    
    def get_content(self,url):
        response = self.get_response(url)
        soup = self.get_soup(response)
        content = self.get_raw_content(soup)
        cate = self.get_cate(soup)
        source = self.get_source(soup)
        comment_num = self.get_comment_num(soup)
        uv = self.get_uv(soup)
        return [content, cate, source, comment_num, uv]
    
    def process(self,urlinfo):
        url = urlinfo[1]
        
        content = self.get_content(url)
        try:
            if content[0] != None:
                pass
                #print('get ',urlinfo[1])
            else:
                print('get ',urlinfo[1],'                     failed')
        except:
            print('get ',urlinfo[1],'                     failed')
        
        return urlinfo + content

def check_ip(ip):
    #url = 'http://ip.chinaz.com/getip.aspx'
    url = 'http://finance.eastmoney.com/'
    proxy = 'http://' +  ip.strip()
    #print(proxy)
    proxies = {'http':proxy}
    try :
        response = requests.get(url,proxies = proxies,timeout=1)
        #if response.status_code==200 and len(str(response.content,'utf-8')) <= 100 and 'address' in str(response.content,'utf-8') and '福建省漳州市 电信' not in str(response.content,'utf-8'):
        if response.status_code==200:
            print (proxies)
            return proxy
    except:
        return None
if __name__ == '__main__':
    
    
    
    #for i in os.listdir('D:\\Elara\\Documents\\paper\\corpus_urllist\\'):
    for i in os.listdir('/mnt/d/Elara/Documents/paper/corpus_urllist/'):
        
        ipp = get_news()
        
        cores = mp.cpu_count()*2
        #urllist=pd.read_csv("D:\\Elara\\Documents\\paper\\corpus_urllist\\"+i, engine='python')
        urllist=pd.read_csv("/mnt/d/Elara/Documents/paper/corpus_urllist/"+i, engine='python',encoding="gbk")
        urllist = [list(urllist.iloc[i])[1:] for i in range(len(urllist)) if urllist['1'][i].split('.')[0].split('/')[-1] not in ('stock','sec','video') and '只市净率' not in urllist['1'][i] and '交易提示' not in urllist['1'][i] and '融资融券信息' not in urllist['1'][i] and '股破净' not in urllist['1'][i]]
        url_len = len(urllist)
        a = 0
        b = a+int(random.uniform(500,1500))
        res = []
        while a<url_len:
            print('getting',a,b,url_len)
            urllist_temp = urllist[a:b]
            
            pool = mp.Pool(processes = cores)
            res = res + pool.map(ipp.process,urllist_temp)
            pool.close()
            
            a = b
            b = a + int(random.uniform(500,1500))
            print('break')
            time.sleep(int(random.uniform(10,60)))
        
        res = pd.DataFrame(res)
        #res.to_csv('D:\\Elara\\Documents\\paper\\corpus\\'+i)
        res.to_csv('/mnt/d/Elara/Documents/paper/corpus/'+i)
        print(i,'ok')
        time.sleep(int(random.uniform(60,180)))