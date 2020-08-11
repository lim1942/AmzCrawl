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
# 根节点名
ROOT = 'Any Department'
# 节点分级符号
NODE_SEP = "|||"


# 页面对象
class Page:
    def __init__(self):
        self.title = None
        self.url = None
        self.date = None

def get_all(node_name,node_url,target=ROOT):
    global COOKIES
    # 1.记录当前节点页面位置和地址
    print(time.strftime("%Y-%m-%d %H:%M:%S"),node_name,node_url)
    page = Page()
    page.title = node_name
    page.url = node_url
    page.date = datetime.now()
    DATA.append(page)
    # 2.获取节点页面，本地缓存或请求
    if file_exists('BSrank/item',node_name):
        text = get_file_content('BSrank/item',node_name)
    else:
        while True:
            try:
                resp = requests.get(node_url,headers=HEADERS,cookies=COOKIES,timeout=10)
                resp.encoding = 'utf-8'
                text = resp.text
                if 'Keyport 98345' not in text:
                    COOKIES = change()
                    raise Exception('bad location !!!')
                save_to_file('BSrank/item',node_name,text)
                break
            except Exception as e:
                print("!!! Error in request",node_name,node_url,str(e))
                time.sleep(30)
    # 3.遍历目录节点，只递归调用target节点
    xml = fromstring(text)
    for li in  xml.xpath("//span[@class='zg_selected']/../../ul/li"):
        li_node_name = node_name + NODE_SEP + li.xpath('./a/text()')[0].replace(os.sep,' ')
        li_node_url = li.xpath('./a/@href')[0]
        if li_node_name.startswith(target) or target.startswith(li_node_name):
            get_all(li_node_name,li_node_url)

def main(target):
    # 指定节点下target节点的页面
    url = 'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_amazon-devices_1'
    get_all(ROOT,url,target)
    cols = list()
    for index,page in enumerate(DATA[1:]):
        print(f"analyze ================== {index+1}/{len(DATA)} ================== {target}")
        analyze_data = handle(page.title)
        analyze_data.update(page.__dict__)
        cols.append(analyze_data)
    fields = list(Page().__dict__) + FIELDS
    save_to_file('BSrank',target,cols, _type='csv',columns=fields)


if __name__ == "__main__":
    target_list = sys.argv[1:].copy()
    if target_list[0] != ROOT:
        target_list.insert(0,ROOT)
    target = NODE_SEP .join(target_list)
    main(target)