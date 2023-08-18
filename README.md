## 说明
爬取[39健康网](https://yyk.39.net/guangzhou/hospitals/)，包括医院基本信息、医院科室、医生信息、医生评价。

将数据以JSON格式存放于文件中, 示例文件在[hospital_data.json](https://github.com/onemore118/hospital_crawler/blob/c1e3fea563c2a29123dece3c152c77c004122611/src/hospital_data.json)

> 注意：本项目只用于学习，不可商用，请遵守网站的robots.txt 协议

## 启动方式
0. 配置python3环境
1. 安装依赖
```shell
pip install beautifulsoup4
pip install pandas
```
2. 启动命令
```shell
python src/main.py
```

