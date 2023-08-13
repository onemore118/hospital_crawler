from src.hospital_item import HospitalItem, HospitalDetail, LabItem, DoctorItem, CommentItem
from bs4 import BeautifulSoup
import requests
import re

from src.utils.formaters import  obj_to_jsonstr


class HospitalCrawler(object):
    def __init__(self, url:str):
        self.url = url
        self.hospital_item:HospitalItem = HospitalItem()

    def parse(self):
        self.detail_page_parse()
        self.labs_page_parse()
        self.doctor_page_parse()
        self.comments_page_parse()

    def detail_page_parse(self):
        #将url格式化为https://yyk.39.net/hospital/1bcf2_detail.html
        detail_url:str = self.url.removesuffix('.html').replace('gz/zonghe/', 'hospital/') + '_detail.html'
        response = requests.get(detail_url)
        html_content = response.content
        hospital: HospitalDetail = HospitalDetail()

        soup = BeautifulSoup(html_content, 'html.parser')
        # 根据医院别名
        intro_element = soup.find('p', class_='intro')
        alias_name_content = intro_element.find('span').get_text(strip=True)

        # 根据医院名称
        hospital_name_element = soup.find('div', class_='hospitalname')
        hospital_name = hospital_name_element.find('strong').get_text(strip=True)

        # 根据医院名称标签
        tags = hospital_name_element.find_all('i')
        tags_content = [tag.get_text(strip=True) for tag in tags]

        introduction_section = soup.find('div', class_='introduction')

        # 提取电话信息
        hospital.phone = self.__get_hospital_info(introduction_section, 'tel')

        # 提取地址信息
        hospital.address = self.__get_hospital_info(introduction_section, 'address')

        # 提取分院信息
        branches = introduction_section.find('dl', string='分院：')
        if branches:
            branches = branches.dd.text.strip()
            hospital.branches = branches

        # 提取简介
        hospital.introduction = self.__get_intro(soup, '简介')

        # 提取科研成果
        hospital.achievement = self.__get_intro(soup, '科研成果')

        # 提取荣誉
        hospital.honor = self.__get_intro(soup, '获奖荣誉')

        # 提取先进设备
        hospital.equipment = self.__get_intro(soup, '先进设备')


        self.hospital_item.id = self.url.split('/')[-1].removesuffix('.html')
        self.hospital_item.alias_name = alias_name_content
        self.hospital_item.hospital_name = hospital_name
        self.hospital_item.tags = tags_content

        self.hospital_item.detail = hospital


    def labs_page_parse(self):
        # 将url格式化为诸如https://yyk.39.net/hospital/53c74_labs.html
        labs_url:str = self.url.removesuffix('.html').replace('gz/zonghe/', 'hospital/') + '_labs.html'
        response = requests.get(labs_url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到所有的<dt>标签和<dd>标签
        dt_tags = soup.find_all('dt')
        dd_tags = soup.find_all('dd', class_='threecolumn')

        # 初始化结果列表
        labs = []

        # 遍历每个<dt>和<dd>标签，提取对应的信息
        for dt_tag, dd_tag in zip(dt_tags, dd_tags):
            lab_item:LabItem = LabItem()
            first_class_lab = dt_tag.get_text(strip=True)
            second_class_labs = [a.get_text(strip=True) for a in dd_tag.find_all('a')]
            # 去除<b>标签的内容
            second_class_labs = [lab.split('(')[0] for lab in second_class_labs]

            lab_item.first_class_lab = first_class_lab
            lab_item.second_class_labs = second_class_labs
            # 将添加到结果列表
            labs.append(lab_item)
        self.hospital_item.labs = labs


    def doctor_page_parse(self):
        # 将url格式化为https://yyk.39.net/hospital/1fc85_doctors.html
        doctor_url:str = self.url.removesuffix('.html').replace('gz/zonghe/', 'hospital/') + '_doctors.html'
        response = requests.get(doctor_url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        last_page_number = self.__get_page_no(soup)

        doctors = []
        for i in range(1, last_page_number+1):

            doctor_url_page = f'{doctor_url}?page={i}'
            response = requests.get(doctor_url_page)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            doctortable_ul = soup.find('ul', class_='doctortable')
            for li in doctortable_ul.find_all('li'):
                doctor_item: DoctorItem = DoctorItem()
                # 提取姓名和职称
                name_tag = li.find('strong').find('a')
                doctor_item.name = name_tag.text

                # 如果职称存在于<p>标签中
                title_tag = li.find('p')
                if title_tag:
                    doctor_item.title = title_tag.text

                # 提取科室信息
                department_tag = li.find_all('p')[1]
                if department_tag:
                    department_content = department_tag.text.split(' ')
                    doctor_item.hospital_name = department_content[0]
                    doctor_item.lab_name = department_content[1]

                # 提取擅长疾病
                specialty_tag = li.find('b')
                if specialty_tag:
                    doctor_item.major = specialty_tag.text

                doctors.append(doctor_item)

        self.hospital_item.doctors = doctors







    def comments_page_parse(self):
        # 将url格式化为https://yyk.39.net/hospital/52ae6_comments.html
        comments_url:str = self.url.removesuffix('.html').replace('gz/zonghe/', 'hospital/') + '_comments.html'
        response = requests.get(comments_url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        last_page_number = self.__get_page_no(soup)

        comments = []
        for i in range(1, last_page_number + 1):
            comments_url_page = f'{comments_url}?page={i}'
            response = requests.get(comments_url_page)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            comment_ul = soup.find('ul', class_='commentlist')
            if comment_ul:
                comment_list = comment_ul.find_all('li')
                for comment_li in comment_list:
                    comment_item: CommentItem = CommentItem()

                    comment = comment_li.find('div', class_='content')

                    comment_item.disease = comment.find('i').text.strip()

                    comment_item.comment_content = comment.find('p').text.strip()
                    comment_item.doctor_name = comment.find('a').text

                    comments.append(comment_item)

        self.hospital_item.comments = comments



    def __get_intro(self, soup, part_name) -> str:
        # 找到包含科研成果部分的<strong>标签
        part_heading = soup.find('strong', string=part_name)
        # 如果找到了对应部分
        if part_heading:
            # 定位<strong>标签所在的父级<div>标签
            section = part_heading.find_parent('div', class_='blockart')
            if part_name == '简介':
                # 提取所有<p>标签
                paragraphs = section.find_all('p')
                # 以换行符分隔的形式输出对应部分内容
                text = '\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
            else:
                text = section.get_text(strip=True)
            return text
        return None

    def __get_hospital_info(self, introduction_section, classname) -> str:
        telephone = introduction_section.find('dl', class_=classname)
        if telephone:
            telephone = telephone.dd.text.strip()
            return telephone
        return None


    def __get_page_no(self, soup):
        last_page_number = 1
        pageno_elements = soup.find_all('p', class_='pageno')
        if pageno_elements:
            for pageno_element in pageno_elements:
                last_page_element = pageno_element.find('span', string='尾页')
                if last_page_element:
                    last_page_text = last_page_element.find_previous_sibling('a').get('href')
                    last_page_number = int(last_page_text.split('=')[-1])
                    break  # 找到最后一页的页码后退出循环
        return last_page_number


if __name__ == '__main__':
    hospital_crawler = HospitalCrawler('https://yyk.39.net/gz/zonghe/52ae6.html')
    hospital_crawler.comments_page_parse()
    print(obj_to_jsonstr(hospital_crawler.hospital_item))

