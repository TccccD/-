# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 00:56:35 2019

@author: tianc
"""

import os
load_txt = False

if load_txt == True:
    a='C:/Users/tianc/Desktop/111.txt'
    f = open(a, 'r')
    d = {}
    ss = []
    sheng = ''
    last_sch = ''
    nor_sch = {}
    for line in f.readlines():
        if len(line.split()) == 1 and '[' in line and ']' in line:
            sheng = line.strip()[1:-1]
            if sheng not in d:
                d[sheng] = {}
                ss.append(sheng)
                sheng = ss[-1]
        if len(line.split()) == 2:
            nor, school = line.strip().split()
            d[sheng][school] = {}
            nor_sch[school] = nor
            last_sch = school
        if len(line.split()) >= 8:
            if '+' in line.split()[3]:
                year = int(line.split()[3].split('+')[0]+line.split()[3].split('+')[1])
            else:
                year = int(line.split()[3])
            if year < 4:
                continue
            pro = line.split()[0]
            line1 = line.split()[-5]
            line2 = line.split()[-3]
            line3 = line.split()[-1]
            d[sheng][last_sch][pro] = [line1, line2, line3]
        if '艺术类平行投档' in line:
            break
    ff = open('C:/Users/tianc/Desktop/222.txt', 'w')
    ff.write(str(d))
#
f = open('C:/Users/tianc/Desktop/222.txt', 'r')
d = eval(f.read())
to_pro = '工商管理'#'经济学'
your_grade = 75000#100000#90000#70000#84000#80000
your_grade_end = 101000#105000#102000#78000#102000#110000
name = 'zhangnan_mate_{}_{}'.format(str(your_grade), str(your_grade_end))
result = []
filter_school = []#['独立', '民办']
vip_sheng = []

# 100000-105000
#filter_sheng = ['内蒙古', '吉林', '黑龙江', '新疆', '宁夏', '青海', '河北', '山西',
#                '海南', '辽宁', '陕西', '甘肃', '云南', '四川', '重庆', '广西',
#                '河南', '山东', '天津', '广东', '湖南', '湖北', '江西','贵州']
#filter_pro = ['生物', '环境', '化工', '生态', '电子', '信息', '技术', '科学', '工业', 
#              '机械', '土木', '材料', '车辆', '护理', '工程', '电气',
#              '化学', '焊接', '医', '农', '动物', '计算机', '自动化',
#              '测控', '民族', '师范']

## 70000-78000
#filter_sheng = ['吉林', '黑龙江', '新疆', '辽宁', '河南']
#filter_pro = ['生物', '环境', '化工', '生态', '电子', '信息', '技术', '科学', '工业', 
#              '机械', '土木', '材料', '车辆', '护理', '工程', '电气',
#              '化学', '焊接', '医', '农', '动物', '计算机', '自动化',
#              '测控', '民族', '数学', '统计', '会计']

# 84000-102000
#filter_sheng = ['内蒙古', '吉林', '黑龙江', '新疆', '宁夏', '青海', '山西',
#                '云南', '广西', '甘肃', '天津', '湖北', '贵州']
#filter_pro = ['旅游', '海洋', '生物', '环境', '化工', '生态', '教育', 
#              '机械', '土木', '材料', '园', '服务', '车辆', '心理', '护理',
#              '化学', '轻', '酒店', '焊接', '医', '农', '动物', '社会',
#              '保险', '测控', '民族']
#vip_sheng = ['福建', '江苏', '上海']#['浙江', '福建', '江苏', '上海']

# 80000-101000
filter_sheng = ['内蒙古', '吉林', '黑龙江', '新疆', '宁夏', '青海', '山西',
                '云南', '广西', '甘肃', '天津', '湖北', '贵州']
filter_pro = ['中外']
vip_sheng = ['浙江', '福建', '江苏', '上海', '湖南', '重庆', '江西']#['福建', '江苏', '上海']#['浙江', '福建', '江苏', '上海']

def filter_by_list(key, filter_list):
    con = 0
    for i in filter_list:
        if i in key:
            con = 1
            break
    return con

result_file = 'C:/Users/tianc/Desktop/{}.txt'.format(name)
if os.path.exists(result_file):
    os.remove(result_file)
ff = open(result_file, 'a')
for sheng in d:
    if sheng in filter_sheng or sheng not in vip_sheng:  
        continue
    if sheng not in vip_sheng:
        continue
    for school in d[sheng]:
        if sheng not in vip_sheng and filter_by_list(school, filter_school) == 1:
            continue
        for pro in d[sheng][school]:
            if filter_by_list(pro, filter_pro) == 1:
                continue
            line2 = int(d[sheng][school][pro][1])
            if line2 >= your_grade and line2 != 0 and line2 < your_grade_end:
#                result.append([sheng, school, pro, line2])
                re = '{} 专业：{} 名次：{} \n'.format(school, pro, line2)
                result.append(re)
                print(re)
                ff.write(re)
ff.close()
f.close()

#for sheng in d:
#    for school in d[sheng]:
#        for pro in d[sheng][school]:
#            if to_pro in pro:
#                line2 = int(d[sheng][school][pro][1])
#                if line2 >= your_grade and line2 != 0:
#                    result.append([sheng, school, pro, line2])
#                    print(result[-1])
    
    
    
    
    
    
    
    
    
    
    
    


