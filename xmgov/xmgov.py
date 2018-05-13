# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:54:32 2018

@author: elara
"""

urllist = []

import requests
from bs4 import BeautifulSoup
import pandas as pd
import multiprocessing as mp
cpu_cnt = mp.cpu_count()

headers = {
        'cache-control': "no-cache",
        'postman-token': "988735dc-122e-92fc-ba7a-bd7f47a74f4f"
        }

home_pages = [['http://www.xm.gov.cn/zwgk/flfg/zfgz/',6],
             ['http://www.xm.gov.cn/zwgk/flfg/sfwj/',34],
             ['http://www.xm.gov.cn/zwgk/flfg/sfbwj/',34],
             ['http://www.xm.gov.cn/zwgk/flfg/gqwj/',34],
             ['http://www.xm.gov.cn/zwgk/flfg/bmwj/',34],
             ['http://www.xm.gov.cn/zwgk/flfg/qtwj/',34]]

print('getting urllist')
for home_page in home_pages:
    ch = home_page[0].split('/')[-2]
    max_page = home_page[1]
    for page_index in range(1,max_page):
        if page_index==1:
            url = home_page[0] + 'index.htm?page=1'
        else:
            url = home_page[0] + 'index_'+str(page_index-1)+'.htm?page='+str(page_index)
    
    
        response = requests.request("GET", url, headers=headers)
        response.encoding=('gb2312')
    
        soup = BeautifulSoup(response.text,'lxml')
        x=soup.find_all('div',class_='gl_list1')[0].find_all('li')
        if len(x)>18 or len(x)<1:
            print('get urllist warning, page=',page_index)
        for li in x:
            date = li.find_all('span')[0].text.strip('[').strip(']').strip()
            index = li.find_all('span')[1].text.strip('[').strip(']').strip()
            href = li.find_all('a')[0]['href']
            href_s = href.split('../')
            back_time = len(href_s)-1
            if back_time!=0:
                back_index=len(home_page[0])-2
                splash_cnt = 0
                while 1:
                    if home_page[0][back_index]!='/':
                        back_index-=1
                        continue
                    else:
                        splash_cnt+=1
                        back_index-=1
                    if splash_cnt>=back_time:
                        break
            else:
                back_index=len(home_page[0])-2
            addr = home_page[0][:back_index+2] + href_s[-1].strip('./')
            title = li.find_all('a')[0]['title']
            urllist.append([ch,date,index,addr,title])

print('getting content with total:',len(urllist))

def get_content(url_info):
    url_info_id = url_info[2]
    url_info_title = url_info[4]
    
    content_url = url_info[3]
    response = requests.request("GET", content_url, headers=headers)
    response.encoding=('gb2312')
        
    soup = BeautifulSoup(response.text,'lxml')
    
    try:
        box_info = [td.text for td in soup.find_all('div',class_='box')[0].find_all('td') if len(td.text)>0][0:5]
        box_index = [i.strip().replace(u'\u3000', ' ') for i in box_info[0].split('：')]
        box_gov = [i.strip().replace(u'\u3000', ' ') for i in box_info[1].split('：')]
        box_date = [i.strip().replace(u'\u3000', ' ') for i in box_info[2].split('：')]
        box_title = [i.strip().replace(u'\u3000', ' ') for i in box_info[3].split('：')]
#        if box_title[1]!=url_info_title:
#            print(box_title,url_info_title)
        box_id = [i.strip().replace(u'\u3000', ' ') for i in box_info[4].split('：')]
#        if box_id[1]!=url_info_id:
#            print(box_id,url_info_id)
    except:
        print(content_url)
        box_index=[None,None]
        box_gov=[None,None]
        box_date=[None,None]
        box_title=[None,None]
        box_id=[None,None]
    try:
        content_title = soup.find_all('div',class_='zfxx_xl_tit1')[0].text.strip().replace(u'\u3000', ' ')
#        if content_title!=url_info_title:
#            print(content_title,url_info_title)
        content_id = soup.find_all('h4',style="font-size:18px; text-align:center;font-weight: normal;font-family:'微软雅黑';color: #333; margin-top:20px; margin-bottom:20px")[0].text.strip()
#        if content_id!=url_info_id:
#            print(content_id,url_info_id)
        content = '|||'.join([p.text.replace(u'\u3000', ' ') for p in soup.find_all('div',class_='zfxx_xl_con1')[0].find_all('p') if len(p)>0])
    except:
        print(content_url)
        content_title=None
        content_id=None
        content=None
    return url_info+[box_index[1],box_gov[1],box_date[1],box_title[1],box_id[1],content_title,content_id,content]

if __name__=='__main__':
    pool = mp.Pool(cpu_cnt)
    content_info = pool.map(get_content,urllist)
    
    content_pd = pd.DataFrame(content_info)
    content_pd.columns=['分类(列表页)','日期(列表页)','文号(列表页)','地址(列表页)','标题(列表页)','索引号（正文顶栏）','发布机构（正文顶栏）','发文日期（正文顶栏）','标题（正文顶栏）','文号（正文顶栏）','标题（正文）','文号（正文）','正文']
    
    content_pd.to_csv('/mnt/c/Elara/yufei.csv',index=False)
