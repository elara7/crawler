# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 23:33:00 2018

@author: elara
"""

import pandas as pd
import codecs

data = pd.read_csv('C:/Elara/yufei.csv')
res = []
for i in range(len(data)):
    if type(data['正文'][i])==str:
        if len(data['正文'][i].split('营商环境'))>1:
            res.append(list(data[['分类(列表页)','索引号（正文顶栏）','发布机构（正文顶栏）', '发文日期（正文顶栏）', '标题（正文顶栏）', '文号（正文顶栏）','正文']].iloc[i,:]))

res = pd.DataFrame(res)
res.columns = ['分类','索引号','发布机构', '发文日期', '标题', '文号','正文']
f = codecs.open('C:/Elara/yufei.txt','w',encoding='utf-8')
for i in range(len(res)):
    f.write('分类：'+res['分类'].iloc[i]+'\r\n')
    f.write('索引号：'+res['索引号'].iloc[i]+'\r\n')
    f.write('发布机构：'+res['发布机构'].iloc[i]+'\r\n')
    f.write('发文日期：'+str(int(res['发文日期'].iloc[i]))+'\r\n')
    f.write('标题：'+res['标题'].iloc[i]+'\r\n')
    f.write('文号：'+res['文号'].iloc[i]+'\r\n')
    f.write('正文：'+'\r\n')
    for c in res['正文'].iloc[i].split('|||'):
        if c=='  ��':
            continue
        f.write(c+'\r\n')
    f.write('\r\n'+'\r\n'+'\r\n'+'\r\n'+'\r\n')
f.close()    
