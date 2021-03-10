import pytest
import requests
import jsonpath
import json
import yaml
from string import Template
import os
import allure

def pytest_collect_file(parent,path):
    # 获取文件.yml文件，匹配规则
    if path.ext == ".yml" and path.basename.startswith("test"):
        # print(path)
        # print(parent)
        return YamlFile(path,parent)


class YamlFile(pytest.File):
    # 读取文件内容
    def collect(self):
        # import yaml
        yml_raw = self.fspath.open(encoding='utf-8').read() #yml文件数据，转列表
        yml_var = Template(yml_raw).safe_substitute(os.environ)
        yml_data = yaml.safe_load(yml_var)
        for yaml_case in yml_data:
            name = yaml_case["test"]["name"]
            values = yaml_case["test"]
            yield YamlTest(name,self,values)


class YamlTest(pytest.Item):
    def __init__(self,name,parent,values):
        super(YamlTest,self).__init__(name,parent)
        self.name = name
        self.values = values
        self._request = self.values.get("request")
        # self.validate = self.values.get("validate")
        self.s = requests.session()

    def values_render_variable(self,values):
        yaml_test = Template(json.dumps(values)).safe_substitute(os.environ)
        values = yaml.safe_load(yaml_test)
        return values

    @allure.step("step:运行测试用例")
    def runtest(self):
        # 运行用例
        values = self.values_render_variable(self.values)
        request_data = values.get("request")
        print(request_data)
        response = self.s.request(**request_data)
        print("\n",response.text)
        #断言
        if values.get("extract"):
            for key, value in values.get("extract").items():
                os.environ[key] = jsonpath.jsonpath(response.json(), value)[0]
        self.assert_response(response,values.get("validate"))

    @allure.step("step:断言")
    def assert_response(self,response,validate):
        # 设置断言
        # import jsonpath
        if validate:
            for i in validate:
                if "eq" in i.keys():
                    yaml_result = i.get("eq")[0]
                    actual_result = jsonpath.jsonpath(response.json(),yaml_result)
                    expect_result = i.get("eq")[1]
                    print("实际结果：%s" % actual_result)
                    print("预期结果：%s" % expect_result)
                    assert actual_result[0] == expect_result


