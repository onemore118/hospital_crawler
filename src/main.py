import pandas as pd

from src.hospital_crawler import HospitalCrawler
from src.utils.formaters import obj_to_jsonstr


def handle():
    """
    1. 读取seeds的excel文件
    2. 遍历39url列
    3. 通过hospital_crawler爬取每条链接对应的信息
    4. 将返回对象以JSON格式保存到结果文件中
    :return:
    """
    hospital_seed = pd.read_excel('../seeds/广州三级医院.xlsx')
    result = []
    for url in hospital_seed['39url']:
        hospital_crawler = HospitalCrawler(url)
        hospital_item = hospital_crawler.parse()
        if hospital_item:
            result.append(hospital_item)

    file_path = "hospital_data.json"

    # 将JSON数据写入文件
    with open(file_path, "w", encoding="utf-8") as json_file:
        json_file.write(obj_to_jsonstr(result))







if __name__ == '__main__':
    handle()