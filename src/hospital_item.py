from typing import List

class HospitalDetail(object):
    address: str
    phone:str
    branches:str   #分院
    introduction:str
    achievement:str
    honour:str
    equipment:str

class LabItem(object):
    first_class_lab: str
    sencond_class_labs:List[str]


class DoctorItem(object):
    name:str
    title:str
    hospital_name: str
    lab_name: str
    major: str  #擅长疾病


class CommentItem(object):
    doctor_name:str
    disease:str
    comment_content:str


# 注意：这里是图方便，使用了类属性来定义一下值的取值类型，实际赋值并不会用到，而是使用创建实例属性去获取
class HospitalItem(object):
    id:str
    hospital_name:str
    alias_name:str
    tags:List[str]
    detail_info:HospitalDetail
    labs:List[LabItem]
    doctors:List[DoctorItem]


