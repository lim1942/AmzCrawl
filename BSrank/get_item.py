import os
import re
import sys
import time
import requests
from datetime import datetime
from lxml.html import fromstring
from tool.savior import save_to_file,file_exists,get_file_content
from BSrank.change_location import change
from BSrank.analyze import handle,FIELDS

# # 设置socket 代理
# import socket
# import socks
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 2080)
# socket.socket = socks.socksocket


DATA = list()
HEADERS = {
"upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"sec-fetch-site":"same-origin",
"sec-fetch-mode":"navigate",
"sec-fetch-user":"?1",
"sec-fetch-dest":"document",
"referer":"https://www.amazon.com/Best-Sellers/zgbs/amazon-devices/ref=zg_bs_nav_0",
"accept-encoding":"gzip, deflate, br",
}


def get_all(title,department_url,cookies):
    item = {'title':title,'url':department_url,'date':datetime.now()}
    DATA.append(item)
    print('crawl',item)
    # 缓存数据
    if file_exists('BSrank/item',title):
        text = get_file_content('BSrank/item',title)
    else:
        resp = requests.get(department_url,headers=HEADERS,cookies=cookies)
        resp.encoding = 'utf-8'
        text = resp.text
        re_search = re.search(r"(Deliver to[\s\S]*?)</div>", text).groups()[0]
        if '98345' not in re_search:
            raise Exception('bad location !!!')
        save_to_file('BSrank/item',title,text)
    xml = fromstring(text)
    # 当前点击span
    zg_selected_span = xml.xpath("//span[@class='zg_selected']")[0]
    # 当前点击所在ul
    zg_selected_ul = zg_selected_span.xpath('./../..')[0]
    # 当前点击是否为根节点
    if zg_selected_ul.xpath('./ul'):
        for li in  zg_selected_ul.xpath('./ul/li'):
            current_department_name = li.xpath('./a/text()')[0].replace(os.sep,' ')
            current_department_url = li.xpath('./a/@href')[0]
            current_title = title + '|||' + current_department_name
            get_all(current_title,current_department_url,cookies)


def main(target):
    cookies = change()
    url = 'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_amazon-devices_1'
    resp = requests.get(url,headers=HEADERS,cookies=cookies)
    resp.encoding = 'utf-8'
    xml = fromstring(resp.text)
    department_lis = xml.xpath("//ul[@id='zg_browseRoot']/ul/li")
    # 获取所有大类
    count = len(department_lis)
    for index,li in enumerate(department_lis):
        department_name = li.xpath('./a/text()')[0]
        department_url = li.xpath('./a/@href')[0]
        # 需要跟进的大类
        if department_name == target:
            print('\n************************************'+ department_name,department_url,f' {index+1}/{count} ************************************')
            title = 'Any Department' + '|||' + department_name
            get_all(title,department_url,cookies)

    # 分析爬取的数据得到报表
    items = list()
    count = len(DATA)
    for index,data in enumerate(DATA):
        print(f"analyze ==================  {index+1}/{count} ================== {target}")
        analyze_data = handle(data['title'])
        data.update(analyze_data)
        items.append(data)
    fields = ['title','url','date'] + FIELDS
    save_to_file('BSrank',target,items, _type='csv',columns=fields)



if __name__ == "__main__":
    target = sys.argv[1]
    while 1:
        try:
            print(target)
            main(target)
            break
        except Exception as e:
            print(e)
            time.sleep(60)
