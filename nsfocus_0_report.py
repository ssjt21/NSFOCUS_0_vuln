# -*- coding: utf-8 -*-
import jinja2
import shutil
import argparse
import os
import glob
import re
import time

import decimal
decimal.getcontext().prec=4
#模板路径
TMP_DIR=os.path.join(os.path.dirname(__file__),'template')
#index.html文件路径
INDEX_TPL=os.path.join(TMP_DIR,'index.html')

#host.html文件路径
HOST_TPL=os.path.join(TMP_DIR,'hosts/id-ip.html')

#是否打开压缩包生成 默认开启 True
MAKE_ZIP=True
# print TMP_DIR

#需要批量处理的资产路径
ASSET_DIR='assets'

def get_files(dir_path=ASSET_DIR,file_suffix='.txt'):
    return map(lambda file:os.path.join(dir_path,file),glob.glob1(dir_path,'*'+file_suffix))

#测试
# print get_files()


# 解析 txt 格式是每行 IP OSTYPE格式
def parse_txt(txt_file):
    resutl=[]
    key=['ip','ostype']
    if txt_file:
        try:
            empty_chars_pattern=re.compile('\s+')
            with open(txt_file,'r') as f:
                ip_lst=[]
                for line in f.readlines():
                    line=line.strip()#去掉多余的空格
                    if line:
                        data_lst=empty_chars_pattern.split(line)

                        if len(data_lst)>2:
                            data_lst=data_lst[:2]
                        elif len(data_lst)==2:
                            data_lst=data_lst[:]
                        else:
                            data_lst=data_lst[:]+['']
                    else:
                        continue
                    if data_lst[0] not in ip_lst:#IP去重操作
                        resutl.append(dict(zip(key,data_lst)))
                        ip_lst.append(data_lst[0])
                # ip_lst=map()
                # result=filter(lambda )
            return  resutl

        except Exception as e:
            print e
            return []

    else:
        print 'txt_file_lst is NULL'
        return []


# 测试

# for txt_file in get_files():
#     print parse_txt(txt_file)


def make_project(project_name):
    if os.path.exists(project_name):#如果项目文件存在，就使用时间将其变成唯一
        return False
        only=str(time.strftime("%Y%m%d%H%M%S",time.localtime()))
        project_name=project_name+only
    if os.path.exists(project_name+'.zip'):
        return False
    try:

        #复制模板数据到项目目录
        # print TMP_DIR
        shutil.copytree(TMP_DIR,project_name)
        #删除多余的模板文件
        os.remove(INDEX_TPL.replace(TMP_DIR,project_name))
        os.remove(HOST_TPL.replace(TMP_DIR,project_name))
        return project_name
    except Exception as e:
        print e,'Make project failed!'
        return False


# # 测试
# for txt_file in get_files():
#     datas=parse_txt(txt_file)
#     project_name=os.path.splitext(txt_file)[0]
#     make_project(project_name)


def build_hosts(datas,project_name):
    tplenv=jinja2.FileSystemLoader(os.path.dirname(HOST_TPL),encoding='utf-8')
    tplenv=jinja2.Environment(loader=tplenv)

    if datas:
        for data in datas:
            filename=data.get('ip',str(time.time()))+'.html'
            # print data
            tpl=tplenv.get_template('id-ip.html')
            html=tpl.render(**data)
            filename=os.path.join(project_name,'hosts/'+filename)
            # print filename
            with open(filename,'w') as f:
                f.write(html.encode('utf-8'))


# test
# for txt_file in get_files():
#     datas=parse_txt(txt_file)
#     project_name=os.path.splitext(txt_file)[0]
#     project_name=make_project(project_name)
#     if project_name:
#         build_hosts(datas,project_name)

#统计操作系统类型和占比
def Statistics_os(datas):

    ostype_dic={}
    ostype_dic['other'] =0
    statistics = []
    if datas:
        for data in datas:
            ostype=data.get('ostype',None)
            if ostype:
                if ostype_dic.has_key(ostype):
                    ostype_dic[ostype]=ostype_dic[ostype]+1
                else:
                    ostype_dic[ostype]=1
            else:
                ostype_dic['other']=ostype_dic['other']+1

        totalnum=len(datas)

        for key,value in ostype_dic.items():
            percentage=str(decimal.Decimal(value)/decimal.Decimal(totalnum)*decimal.Decimal(100))+'%'
            if percentage!='0%':
                statistics.append({'num':value,'ostype':key,'avg':percentage})


    return statistics


# test
# for txt_file in get_files():
#     datas=parse_txt(txt_file)
#     print Statistics_os(datas)



def gettime(num):
    import datetime
    import random

    Year=2018
    Month=7
    Day=random.choice([4,5,6])
    H=random.choice(list(range(9,20)))
    M=random.choice(list(range(0,60)))
    S=random.choice(list(range(0,60)))
    start=datetime.datetime(Year,Month,Day,H,M,S)
    end=(start+datetime.timedelta(minutes=random.choice(range(num*3,num*4)),seconds=random.choice(range(0,60)))).strftime("%Y-%m-%d %H:%M:%S")
    start = start.strftime("%Y-%m-%d %H:%M:%S")
    return start,end

#test
# print gettime(4)


def build_index(datas,project_name):
    tplenv = jinja2.FileSystemLoader(os.path.dirname(INDEX_TPL), encoding='utf-8')
    tplenv = jinja2.Environment(loader=tplenv)
    render_data={}
    if datas:
        tpl=tplenv.get_template('index.html')
        render_data['scan_name']=project_name.decode('gbk')
        render_data['ip_num']=str(len(datas))
        render_data['scan_time_start'],render_data['scan_time_end']=gettime(int(render_data['ip_num']))
        render_data['os_list']=Statistics_os(datas)
        render_data['items']=datas

        tpl = tplenv.get_template('index.html')
        html=tpl.render(**render_data)
        filename=os.path.join(project_name,'index.html')
        with open (filename,'w') as f:
            f.write(html.encode('utf-8'))




def main():

    for txt_file in get_files():
        datas=parse_txt(txt_file)
        # print txt_file
        project_name = os.path.basename(txt_file)
        # print project_name
        project_name = os.path.splitext(project_name)[0]
        # print project_name
        project_name=make_project(project_name)
        if project_name:
            build_hosts(datas,project_name)
            build_index(datas,project_name)
            if MAKE_ZIP:
                shutil.make_archive(project_name,'zip',project_name)
                shutil.rmtree(project_name)
            print '\033[1;31m %s compelted !\033[0m' % txt_file.decode('gbk')
        else:

            print '\033[1;34m %s already handled !\033[0m' % txt_file.decode('gbk')


if __name__ == '__main__':
    main()