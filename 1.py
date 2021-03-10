# from jsonpath import jsonpath
# # jsonpath里真有jsonpath模块jsonpath
# data = {'key1': {'key2': {'key3': {'key4': {'key5': {'key6':'python'}}}}}}
# #键值索引
# print(data['key1']['key2']['key3']['key4']['key5']['key6'])
#
# print(jsonpath(data,'$..key6')[0])
# print(jsonpath(data,'$.key1.key2.key3.key4.key5.key6')[0])
#
from jsonpath import jsonpath

data ={"username1":{"us":{"a":"1"}}}
print(data["username1"]["us"])
print(jsonpath(data,'$..username1'))
print(jsonpath.jsonpath(data,'$.username1'))


# import requests
# import jsonpath
# import json
#
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
# }
# response = requests.get('https://www.lagou.com/lbs/getAllCitySearchLabels.json', headers=headers)
# dict_data = json.loads(response.content.decode())
# print(dict_data)
# print(jsonpath.jsonpath(dict_data, '$..name'))
