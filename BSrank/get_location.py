import re
import requests

# # 设置socket 代理
# import socket
# import socks
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 2080)
# socket.socket = socks.socksocket
headers = {
"upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"sec-fetch-site":"same-origin",
"sec-fetch-mode":"navigate",
"sec-fetch-user":"?1",
"sec-fetch-dest":"document",
"accept-encoding":"gzip, deflate, br",
}
test_url = 'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_amazon-devices_1'


def change(zip_code='98345'):
    change_url = 'https://www.amazon.com/gp/delivery/ajax/address-change.html'
    data = {
        "locationType": "LOCATION_INPUT",
        "zipCode": zip_code,
        "storeContext": "boost",
        "deviceType": "web",
        "pageType": "zeitgeist",
        "actionSource": "glow",
        "almBrandId": "undefined",
    }
    resp = requests.post(change_url,data=data,headers=headers)
    cookies = resp.cookies.get_dict()
    resp = requests.get(test_url, headers=headers, cookies=cookies)
    try:
        re_search = re.search(r"(Deliver to[\s\S]*?)</div>", resp.text).groups()[0]
    except:
        re_search = ''
    if '98345' in re_search:
        cookies.update(resp.cookies.get_dict())
        return cookies
    else:
        print('递归请求+1----')
        return change()


if __name__ == "__main__":
    cookies = change()
    print(cookies)
    text = requests.get(test_url, headers=headers, cookies=cookies).text
    print(re.search(r"(Deliver to[\s\S]*?)</div>", text).groups()[0])