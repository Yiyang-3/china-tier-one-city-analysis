# 发送请求
import requests  # 数据请求模块
from bs4 import BeautifulSoup
import re
import csv
import time
import random
import os

# other 函数
def extract_house_info(house_info):
    # 初始化默认值
    num_rooms = area = orientation = renovation = floor = build_time = house_type = None
    
    for info in house_info:
        info = info.strip()  # 去除前后空格
        if re.match(r'\d室\d厅', info):  # 几室几厅
            num_rooms = info
        elif re.match(r'\d+\.?\d*平米', info):  # 房屋面积
            area = info
        elif re.match(r'[东南西北]+', info):  # 房屋朝向
            orientation = info
        elif info in ['精装', '简装', '毛坯', '其他']:  # 装修
            renovation = info
        elif '楼层' in info or '层' in info:  # 楼层信息
            floor = info
        elif re.match(r'\d{4}年', info):  # 建立时间
            build_time = info
        elif info in ['板楼', '板塔结合', '塔楼']:  # 户型
            house_type = info
    
    return num_rooms, area, orientation, renovation, floor, build_time, house_type


def extract_tag_info(tag_info):
    # 初始化默认值
    vr_info = taxfree_info = subway_info = five_info = haskey_info = None
    
    for tag in tag_info:
        tag_text = tag.text.strip()  # 获取标签文本并去除空白字符
        if 'VR' in tag_text:  # VR相关标签
            vr_info = tag_text
        elif '房本满五年' in tag_text:  # 房本满五年
            taxfree_info = tag_text
        elif '近地铁' in tag_text:  # 近地铁
            subway_info = tag_text
        elif '房本满两年' in tag_text:  # 房本满两年
            five_info = tag_text
        elif '随时看房' in tag_text:  # 随时看房
            haskey_info = tag_text
    
    return vr_info, taxfree_info, subway_info, five_info, haskey_info



# 子模块爬取函数
def crawl_detail_page(url, headers):
    # 预定义所有字段模板
    detail_template = {
        # 新增字段
        '分区': None,
        '小区名称': None,
        '所在区域': None,
        # 原有上模块字段
        '房屋户型': None,
        '建筑面积': None,
        '套内面积': None,
        '房屋朝向': None,
        '装修情况': None,
        '供暖方式': None,
        '楼层高度': None,
        '所在楼层': None,
        '户型结构': None,
        '建筑类型': None,
        '建筑结构': None,
        '梯户比例': None,
        '配备电梯': None,
        # 下模块字段
        '挂牌时间': None,
        '上次交易': None,
        '房屋年限': None,
        '抵押信息': None,
        '交易权属': None,
        '房屋用途': None,
        '产权所属': None,
        '房本备件': None
    }


    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return detail_template

        soup = BeautifulSoup(response.text, 'html.parser')
        detail_data = detail_template.copy()  # 使用模板初始化

        # 新增分区提取逻辑
        def extract_district(soup):
            bread_links = soup.select('.intro.clear[mod-id="lj-common-bread"] a[href*="ershoufang"]')
            # 提取逻辑优化
            if len(bread_links) >= 2:
                # 典型结构：北京二手房 > 顺义二手房 > 李桥二手房
                district_text = bread_links[1].text  # 第二个二手房链接
                return district_text.replace('二手房', '')
            else:
                return None

        # 在数据初始化后添加
        detail_data = detail_template.copy()
        detail_data['分区'] = extract_district(soup)  # 新增提取

        # 提取小区名称
        community_elem = soup.select_one('.communityName a.info')
        if community_elem:
            detail_data['小区名称'] = community_elem.text.strip()

        # 提取所在区域（需要处理可能的颜色样式）
        area_elem = soup.select_one('.areaName .info')
        if area_elem:
            # 去除可能存在的颜色样式代码
            area_text = area_elem.text.strip()
            detail_data['所在区域'] = re.sub(r'style=".*?"', '', area_text).strip()


        # 通用数据提取函数
        def extract_section(section_selector, fields):
            section = soup.select_one(section_selector)
            if not section:
                return

            for li in section.select('li'):
                try:
                    label_elem = li.select_one('.label')
                    if not label_elem:
                        continue

                    # 清洗标签文本
                    label = label_elem.text.strip('：').replace(' ', '')
                    
                    # 特殊处理抵押信息
                    if label == '抵押信息':
                        value_elem = li.select_one('span[title]')
                        value = value_elem['title'] if value_elem else li.text.strip()
                    else:
                        # 提取值并清洗
                        raw_value = li.text.replace(label_elem.text, '').strip()
                        value = raw_value.strip('“”').strip()  # 去除中文引号

                    # 统一空值处理
                    value = value if value and value not in ['暂无数据', '暂无'] else None
                    
                    # 更新到对应字段
                    if label in fields:
                        detail_data[label] = value
                except Exception as e:
                    print(f"字段解析异常: {str(e)}")
                    continue

        # 提取上模块（基本属性）
        extract_section('.base .content ul', [
            '房屋户型', '建筑面积', '套内面积', '房屋朝向', '装修情况',
            '供暖方式', '楼层高度', '所在楼层', '户型结构', '建筑类型',
            '建筑结构', '梯户比例', '配备电梯'
        ])

        # 提取下模块（交易属性）
        extract_section('.transaction .content ul', [
            '挂牌时间', '上次交易', '房屋年限', '抵押信息',
            '交易权属', '房屋用途', '产权所属', '房本备件'
        ])

        return detail_data

    except Exception as e:
        print(f"详情页抓取异常: {str(e)}")
        return detail_template



'''
# 登录功能
def login(session):
    login_url = 'https://sh.lianjia.com/login' 
    login_data = {
        'username': '13043253917', 
        'password': 'yqx251406'
    }
    response = session.post(login_url, data=login_data)
    if response.status_code == 200:
        print("登录成功")
        return True
    else:
        print("登录失败")
        return False
'''

# 写入数据
'''
f = open('测试数据.csv', mode='w', encoding='utf-8',newline='') # 修改1
csv_writer = csv.DictWriter(f, fieldnames=['房屋户型', '建筑面积', '套内面积', '房屋朝向', '装修情况','供暖方式', '楼层高度', '所在楼层', '户型结构', '建筑类型','建筑结构', '梯户比例', '配备电梯','挂牌时间', '上次交易', '房屋年限', '抵押信息','交易权属', '房屋用途', '产权所属', '房本备件','标题', '总价', '单价','地区', '几室几厅', '房屋面积', '楼层', '建立时间', '户型', '关注人数', '发布日期', 'VR看装修', '房本满五年', '近地铁', '房本满两年', '随看房','详情页'])
csv_writer.writeheader()
'''

# 修改1
with open('D:/data_analysis/get_data/data/深圳数据(51-100页).csv', mode='w', encoding='utf-8', newline='') as f:
    csv_writer = csv.DictWriter(f, fieldnames=[
        '分区','小区名称', '所在区域', '房屋户型', '建筑面积', '套内面积', '房屋朝向', '装修情况', 
        '供暖方式', '楼层高度', '所在楼层', '户型结构', '建筑类型',
        '建筑结构', '梯户比例', '配备电梯', '挂牌时间', '上次交易',
        '房屋年限', '抵押信息', '交易权属', '房屋用途', '产权所属',
        '房本备件', '标题', '总价', '单价', '地区', '几室几厅',
        '房屋面积', '楼层', '建立时间', '户型', '关注人数', '发布日期',
        'VR看装修', '房本满五年', '近地铁', '房本满两年', '随时看房', '详情页'
    ])
    csv_writer.writeheader()
    
    # 修改2
    for page in range(51,101):
    # 获取数据 获取网页源代码
    # 发送请求的url地址
        time.sleep(10)
        url = f'https://sz.lianjia.com/ershoufang/pg{page}/'   # 修改3
        print(f"正在爬取：第{page}页")
        # print(f"正在处理page{page}")
        # headers: 请求头（伪装成浏览器）

        '''
        session = requests.Session()
        if not login(session):
            print(f"第{page}页无法继续爬取，请检查登录信息")
            continue
        '''

        # 修改4
        cookie = os.getenv('LIANJIA_COOKIE', '')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/115 SLBVPV/64-bit',
            'Cookie': cookie.encode("utf-8").decode("latin1")
        }

        response = requests.get(url=url, headers=headers)  # get的请求工具
        # print(response.text)

        # 解析数据 提取想要的内容:re css xpath parser
        soup = BeautifulSoup(response.text, 'html.parser')
        # 第一次提取，提取所有li标签内容，返回列表（列表里面是selector对象）
        lis = soup.select('.sellListContent li')
        # print(lis)
        for li in lis:
            title_tag = li.select('.title a')
            if title_tag:
                try:
                    # 提取详情页
                    href = title_tag[0].get('href')  # 使用 get 方法获取 href 属性
                    detail_soup = crawl_detail_page(href, headers)

                    # print(href)
                    # 提取标题
                    title = title_tag[0].text.strip()  # 获取第一个匹配的标签的文本，并去除空白字符
                    # detail_soup['标题'] = title

                    # 提取地区
                    region_list = li.select('.flood a')
                    regions = [region.text for region in region_list]
                    region = '-'.join(regions)

                    # 提取房屋信息
                    house_info = li.select('.houseInfo')[0].text.split('|')
                    # print(house_info)
                    '''
                    num_rooms = house_info[0]  # 几室几厅
                    area = house_info[1]  # 房屋面积
                    orientation = house_info[2]  # 房屋朝向
                    renovation = house_info[3]  # 装修
                    floor = house_info[4]  # 楼层
                    build_time = house_info[5]  # 建立时间
                    house_type = house_info[6]  # 户型
                    '''
                    num_rooms, area, orientation, renovation, floor, build_time, house_type = extract_house_info(house_info)
                    #print(num_rooms, area, orientation, renovation, floor, build_time, house_type )

                    # 提取关注人数信息
                    follow_info = li.select('.followInfo')[0].text.split(' / ')
                    person_num = follow_info[0]  # 关注人数信息
                    update_build_time = follow_info[1]  # 发布日期信息

                    # 提取标签信息
                    tag_info = li.select('.tag span')
                    # tags = [tag.text for tag in tag_info]
                    # tag = '-'.join(tags)
                    vr_info, taxfree_info, subway_info, five_info, haskey_info = extract_tag_info(tag_info)

                    # 提取单价和总价
                    total_price = li.select('.totalPrice span')[0].text +'万'
                    unit_price = li.select('.unitPrice span')[0].text
                    # print(unit_price)
                    detail_soup['标题'] = title
                    detail_soup['总价'] = total_price
                    detail_soup['单价'] = unit_price
                    detail_soup['地区'] = region
                    detail_soup['几室几厅'] = num_rooms
                    detail_soup['房屋面积'] = area
                    detail_soup['楼层'] = floor,
                    detail_soup['建立时间'] = build_time

                    detail_soup['户型'] = house_type
                    detail_soup['关注人数'] = person_num
                    detail_soup['发布日期'] = update_build_time
                    detail_soup['VR看装修'] = vr_info

                    detail_soup['房本满五年'] = taxfree_info
                    detail_soup['近地铁'] = subway_info
                    detail_soup['房本满两年'] = five_info
                    detail_soup['随时看房'] = haskey_info
                    detail_soup['详情页'] = href

                    print(detail_soup)
                    try:
                        csv_writer.writerow(detail_soup)
                    except Exception as e:
                        print(f"数据写入失败: {str(e)}")
                    # print(title, region, num_rooms, area, orientation, renovation, floor, build_time, house_type, person_num, update_build_time, vr_info, taxfree_info, subway_info, five_info, haskey_info,total_price, unit_price, sep='|')
                except:
                    pass


