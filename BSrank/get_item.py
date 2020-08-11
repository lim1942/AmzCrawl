import os
import sys
import time
import requests
from datetime import datetime
from lxml.html import fromstring
from tool.savior import save_to_file,file_exists,get_file_content
from BSrank.get_location import change
from BSrank.analyze import handle,FIELDS
# # 设置socket 代理
# import socket
# import socks
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 2080)
# socket.socket = socks.socksocket

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
# 更改亚马逊发货地后cookies
COOKIES = change()
# 存储所有页面对象
DATA = list()


# 页面对象
class Page:
    def __init__(self):
        self.title = None
        self.url = None
        self.date = None

def storage_page(title,url):
    global COOKIES
    # 1.记录当前页面位置和地址
    print(time.strftime("%Y-%m-%d %H:%M:%S"),title,url)
    page = Page()
    page.title = title
    page.url = url
    page.date = datetime.now()
    DATA.append(page)
    # 2.读取本地页面或请求页面
    if file_exists('BSrank/item',title):
        text = get_file_content('BSrank/item',title)
    else:
        while True:
            try:
                resp = requests.get(url,headers=HEADERS,cookies=COOKIES,timeout=10)
                resp.encoding = 'utf-8'
                text = resp.text
                if 'Keyport 98345' not in text:
                    COOKIES = change()
                    raise Exception('bad location !!!')
                save_to_file('BSrank/item',title,text)
                break
            except Exception as e:
                print("!!! Error in request",title,url,str(e))
                time.sleep(30)
    return text

def get_all(title,department_url,target='Any Department'):
    # 当前点击ul还有子ul继续递归
    xml = fromstring(storage_page(title,department_url))
    zg_selected_ul = xml.xpath("//span[@class='zg_selected']/../..")[0]
    if zg_selected_ul.xpath('./ul'):
        for li in  zg_selected_ul.xpath('./ul/li'):
            current_department_name = li.xpath('./a/text()')[0].replace(os.sep,' ')
            current_department_url = li.xpath('./a/@href')[0]
            current_title = title + '|||' + current_department_name
            # 只递归调用target子节点
            if current_title.startswith(target) or target.startswith(current_title):
                get_all(current_title,current_department_url)

def main(target_list):
    # 1.请求节点下target节点的页面
    url = 'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_amazon-devices_1'
    if target_list[0] != 'Any Department': target_list.insert(0,'Any Department')
    target = "|||" .join(target_list)
    get_all('Any Department',url,target)
    # 2.分析所采集页面
    cols = list()
    for index,page in enumerate(DATA[1:]):
        print(f"analyze ==================  {index+1}/{len(DATA)} ================== {target}")
        analyze_data = handle(page.title)
        analyze_data.update(page.__dict__)
        cols.append(analyze_data)
    fields = list(Page().__dict__) + FIELDS
    filename = "|||".join(target_list[1:])
    save_to_file('BSrank',filename,cols, _type='csv',columns=fields)


if __name__ == "__main__":
    main(sys.argv[1:].copy())