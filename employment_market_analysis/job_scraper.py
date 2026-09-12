import requests
import parsel
import csv
import time
import random
import os
from urllib.parse import urljoin

base_url = "https://sz.58.com/{area}/quanzhizhaopin/"
areas = ['baoan', 'nanshan']  # 可添加更多区域

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
    'Cookie': os.getenv('FIFTY_EIGHT_COOKIE', '')
}

target_benefits = [
    "五险一金", "包住", "包吃", "年底双薪", "周末双休",
    "交通补助", "加班补助", "饭补", "话补", "房补"
]

results = []

for area in areas:
    for page in range(1, 2):  # 可增大页数
        if page == 1:
            url = base_url.format(area=area) + "?key=%E9%94%80%E5%94%AE%E4%B8%93%E5%91%98&cmcskey=%E9%94%80%E5%94%AE%E4%B8%93%E5%91%98&final=1&jump=1&specialtype=gls&classpolicy=LBGguide_A,main_B,job_B,hitword_false,uuid_aJhibZxne7MSzbKpxMmTdxtsH8haDGAG,displocalid_4,from_main,to_jump,tradeline_job,classify_A&search_uuid=aJhibZxne7MSzbKpxMmTdxtsH8haDGAG&search_type=suggest&pid=817173548212584448&PGTID=0d3002a2-0071-4c4b-9fc9-e9877870081a&ClickID=1"
        else:
            url = base_url.format(area=area) + f"pn{page}/?key=%E9%94%80%E5%94%AE%E4%B8%93%E5%91%98&cmcskey=%E9%94%80%E5%94%AE%E4%B8%93%E5%91%98&final=1&jump=1&specialtype=gls&classpolicy=LBGguide_A,main_B,job_B,hitword_false,uuid_aJhibZxne7MSzbKpxMmTdxtsH8haDGAG,displocalid_4,from_main,to_jump,tradeline_job,classify_A&search_uuid=aJhibZxne7MSzbKpxMmTdxtsH8haDGAG&search_type=suggest&pid=817173548212584448&PGTID=0d3002a2-0071-4c4b-9fc9-e9877870081a&ClickID=1"
        
        print(f"访问列表页：{url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            selector = parsel.Selector(response.text)

            job_items = selector.css('ul#list_con > li.job_item.clearfix')
            for index, job in enumerate(job_items, start=1):
                href = job.css('div.job_name a::attr(href)').get()
                if not href:
                    continue
                detail_url = urljoin(url, href)
                print(f"  → 进入详情页（li位置: {index}）：{detail_url}")

                try:
                    detail_resp = requests.get(detail_url, headers=headers, timeout=10)
                    detail_resp.raise_for_status()
                    detail_sel = parsel.Selector(detail_resp.text)
                    jobs = selector.css('ul#list_con > li.job_item.clearfix')

                    for job in jobs:
                        job_salary = job.css('p.job_salary::text').get() or "无"
                        job_wel_list = job.css('div.job_wel.clearfix span::text').getall()
                        job_wel_list = [w.strip() for w in job_wel_list]

                        # 构造数据项
                        job_data = {'工资': job_salary}
                        for benefit in target_benefits:
                            job_data[benefit] = "有" if benefit in job_wel_list else ""

                        results.append(job_data)
                

                    time.sleep(random.uniform(0.8, 1.5))  # 防封

                except Exception as e:
                    print(f"❌ 详情页出错（跳过）：{detail_url} → {e}")
                    continue

            time.sleep(random.uniform(1.5, 2.5))  # 防封
        except Exception as e:
            print(f"❌ 列表页失败：{url} → {e}")
            continue

# 写入 CSV
fieldnames = ['工资'] + target_benefits
with open('jobs_详细信息.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("✅ 数据已成功写入 jobs_详细信息.csv")
