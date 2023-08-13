import json



# 将字典转换为JSON字符串
def obj_to_jsonstr(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
