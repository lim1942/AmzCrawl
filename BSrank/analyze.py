import os
from tool.savior import get_file_content
from lxml.html import fromstring,tostring


FIELDS = ['all_review_cnt', 'top_three_review_cnt', 'top_three_review_rate', 'review_lt_50_rate', 'max_review', 'min_review', 'avg_review', 'max_star', 'min_star', 'avg_star', 'max_price', 'min_price', 'avg_price', 'available_cnt', 'first_star', 'first_price', 'first_review_cnt', 'first_review_rate', 'first_url', 'second_star', 'second_price', 'second_review_cnt', 'second_review_rate', 'second_url', 'third_star', 'third_price', 'third_review_cnt', 'third_review_rate', 'third_url', 'the_20th_star', 'the_20th_price', 'the_20th_review_cnt', 'the_20th_review_rate', 'the_20th_url', 'last_star', 'last_price', 'last_review_cnt', 'last_review_rate', 'last_url']

def handle(title):
    result = dict()

    # 总review
    all_review_cnt = 0
    # 前三名review
    top_three_review_cnt = 0
    # 前三名star 占比
    top_three_review_rate = None
    review_list = list()
    # 最大review
    max_review = 0
    # 最小review
    min_review = 0
    # 平均review
    avg_review = 0
    # 小于50个review的商品个数
    review_lt_50_cnt = 0
    # 小于50个review的商品个数占比
    review_lt_50_rate = 0
    star_list = list()
    # 最多star
    max_star = 0
    # 最小star
    min_star = 0
    # 平均star
    avg_star = 0
    price_list =list()
    # 最大价格
    max_price = 0
    # 最低价格
    min_price = 0
    # 平均价格
    avg_price = 0
    # 可用商品数
    available_cnt = 0

    # 第一名星级
    first_star = 0
    # 第一名星级
    first_price = 0
    # 第一名review
    first_review_cnt = 0
    # 第一名star 占比
    first_review_rate = 0
    # 第一名url
    first_url = ''

    # 第二名星级
    second_star = 0
    # 第二名价格
    second_price = 0
    # 第二名review
    second_review_cnt = 0
    # 第二名review占比
    second_review_rate = 0
    # 第二名url
    second_url = ''

    # 第三名星级
    third_star = 0
    # 第三名价格
    third_price = 0
    # 第三名review
    third_review_cnt = 0
    # 第三名review占比
    third_review_rate = 0
    # 第三名url
    third_url = ''

    # 20名星级
    the_20th_star = 0
    # 20名价格
    the_20th_price = 0
    # 20名review
    the_20th_review_cnt = 0
    # 20名review占比
    the_20th_review_rate = 0
    # 20名url
    the_20th_url = ''

    # 最后一名星级
    last_star = 0
    # 最后一名价格
    last_price = 0
    # 最后一名review
    last_review_cnt = 0
    # 最后一名review占比
    last_review_rate = 0
    # 最后一名url
    last_url = ''

    text = get_file_content('BSrank/item',title)

    xml = fromstring(text)
    items = list()
    lis = xml.xpath("//ol[@id='zg-ordered-list']/li")
    for li in lis:
        item = dict()
        # 商品排名
        item['rank'] = int(li.xpath(".//span[@class='zg-badge-text']/text()")[0].replace('#',''))
        # 商品链接
        try:
            item['url'] = 'https://www.amazon.com'+ li.xpath('.//a[contains(@href, "/dp/")][1]/@href')[0]
        except:
            # 过滤无效商品
            continue
        # 商品标题
        item['title'] = li.xpath('.//a[contains(@href, "/dp/")][1]//img/@alt')[0]
        # 商品星级
        try:
            item['star'] = float(li.xpath(".//a[contains(@title, 'star')]/@title")[0].split('out')[0])
        except:
            item['star'] = None
        # 商品评分个数
        try:
            item['reviews'] = int(li.xpath(".//a[contains(@href, '/product-reviews')]/text()")[-1].replace(',',''))
        except:
            item['reviews'] = None
        # 商品价格
        item_price = li.xpath(".//span[contains(text(),'$')]/text()")
        try:
            item['price_min'] = float(item_price[0].replace('$',''))
            item['price_max'] = float(item_price[-1].replace('$',''))
        except:
            item['price_min'] = None
            item['price_max'] = None
        items.append(item)

        # =========== 进行报表计算 ============
        if item['reviews'] is not None:
            all_review_cnt += item['reviews']
            if item['rank'] <=3:
                top_three_review_cnt += item['reviews']
            review_list.append(item['reviews'])
            if item['reviews']<50:
                review_lt_50_cnt +=1
        if item['star'] is not None:
            star_list.append(item['star'])
        if item['price_max'] is not None:
            price_list.append(item['price_max'])
        available_cnt +=1

        if item['rank'] == 1:
            first_star = item['star']
            first_price = item['price_max']
            first_review_cnt = item['reviews']
            first_url = item['url']
        elif item['rank'] == 2:
            second_star = item['star']
            second_price = item['price_max']
            second_review_cnt = item['reviews']
            second_url = item['url']
        elif item['rank'] == 3:
            third_star = item['star']
            third_price = item['price_max']
            third_review_cnt = item['reviews']
            third_url = item['url']
        elif item['rank'] == 20:
            the_20th_star = item['star']
            the_20th_price = item['price_max']
            the_20th_review_cnt = item['reviews']
            the_20th_url = item['url']
    if not items:
        return {}
    top_three_review_rate = round(top_three_review_cnt/all_review_cnt,4) if all_review_cnt else None
    max_review = max(review_list) if review_list else None
    min_review = min(review_list) if review_list else None
    avg_review = round(sum(review_list)/available_cnt,4) if review_list else None
    max_star = max(star_list) if star_list else None
    min_star = min(star_list) if star_list else None
    avg_star = round(sum(star_list)/available_cnt,4) if star_list else None
    max_price = max(price_list) if price_list else None
    min_price = min(price_list) if price_list else None
    avg_price = round(sum(price_list)/available_cnt,4) if price_list else None

    first_review_rate = round(first_review_cnt/all_review_cnt,4) if all_review_cnt and (first_review_cnt is not None) else None
    second_review_rate = round(second_review_cnt/all_review_cnt,4) if all_review_cnt and (second_review_cnt is not None) else None
    third_review_rate = round(third_review_cnt/all_review_cnt,4) if all_review_cnt and (third_review_cnt is not None) else None
    the_20th_review_rate = round(the_20th_review_cnt/all_review_cnt,4) if all_review_cnt and (the_20th_review_cnt is not None) else None

    last_star = items[-1]['star']
    last_price = items[-1]['price_max']
    last_review_cnt = items[-1]['reviews']
    last_review_rate = round(last_review_cnt/all_review_cnt,4) if all_review_cnt and (last_review_cnt is not None) else None
    last_url = items[-1]['url']

    result['all_review_cnt'] = int(all_review_cnt)
    result['top_three_review_cnt'] = int(top_three_review_cnt)
    result['top_three_review_rate'] = top_three_review_rate
    result['review_lt_50_rate'] = round(review_lt_50_cnt / available_cnt,4) if available_cnt else None
    result['max_review'] = max_review
    result['min_review'] = min_review
    result['avg_review'] = avg_review
    result['max_star'] = max_star
    result['min_star'] = min_star
    result['avg_star'] = avg_star
    result['max_price'] = max_price
    result['min_price'] = min_price
    result['avg_price'] = avg_price
    result['available_cnt'] =available_cnt
    result['first_star'] = first_star
    result['first_price'] = first_price
    result['first_review_cnt'] = first_review_cnt
    result['first_review_rate'] =first_review_rate
    result['first_url'] = first_url
    result['second_star'] = second_star
    result['second_price'] = second_price
    result['second_review_cnt'] = second_review_cnt
    result['second_review_rate'] = second_review_rate
    result['second_url'] = second_url
    result['third_star'] = third_star
    result['third_price'] = third_price
    result['third_review_cnt'] = third_review_cnt
    result['third_review_rate'] = third_review_rate
    result['third_url'] = third_url
    result['the_20th_star'] = the_20th_star
    result['the_20th_price'] = the_20th_price
    result['the_20th_review_cnt'] = the_20th_review_cnt
    result['the_20th_review_rate'] = the_20th_review_rate
    result['the_20th_url'] = the_20th_url
    result['last_star'] = last_star
    result['last_price'] = last_price
    result['last_review_cnt'] = last_review_cnt
    result['last_review_rate'] = last_review_rate
    result['last_url'] = last_url
    return result


if __name__ == "__main__":
    goods = os.listdir('/Users/apple/Documents/project/spider/amz/DATA/BSrank/item')
    total = len(goods)
    # for index, _ in enumerate(goods):
    #     print(index+1,total)
    #     print(handle(_))
    print(handle('Any Department|||Computers & Accessories|||Desktops'))