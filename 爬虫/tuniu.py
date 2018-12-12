from requests_html import HTMLSession
import os
import time
import re
import json


# 创建连接对象
session = HTMLSession()

# 获取所有的请求列表
response = session.get("http://www.tuniu.com/wenda/")
all_elements = response.html.xpath("//div[2]/div[2]/ul/li/a")
all_name_url_list = [
    (i.xpath("./a/@href")[0], i.xpath("./a/@title")[0]) for i in all_elements]
print(all_name_url_list)


now_path = os.getcwd()
# 创建tuniu文件夹并且换路径
tuniu_path = now_path + os.path.sep + "tuniu"
if not os.path.exists(tuniu_path):
    os.mkdir(tuniu_path)
    os.chdir(tuniu_path)
else:
    os.chdir(tuniu_path)


class TuNiu(object):
    """
    功能：爬去途牛网站问答信息
    返回数据类型：数据类型为json
    内容：分为已回答和未回答问题
    response:请求返回的数据
    parse：解析数据
    save：存储信息
    run:启动程序
    """

    def __init__(self, No_answer_base_url, with_answer_base_url):
        self.No_answer_base_url = No_answer_base_url
        self.with_answer_base_url = with_answer_base_url
        self.base_urls = [self.No_answer_base_url, self.with_answer_base_url]

    def response(self, url):
        res = session.get(url)
        json_data = res.json()
        return json_data

    def parse(self, json_data):
        data = json_data.get("data")
        list_ = data.get("list")
        return list_

    def save(self, data, name):
        file_path = tuniu_path + os.path.sep + name
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        for need_data in data:
            # 构造所需数据
            question = need_data.get('questionContent').strip()
            tags = need_data.get("tagNames")
            text = "{0}    {1}".format(question, "    ".join(tags))
            file_name = str(int(time.time()*1000))
            file_name = file_name + ".txt"
            with open(file_path + os.path.sep + file_name, "w", encoding="utf-8") as f:
                f.write(text)

            answer = need_data.get('answerContent')
            city = need_data.get('destinationCity')
            # 构造json
            json_dict = {"question": question,
                         "answer": answer, "tags": tags, "city": city}
            jsonData = json.dumps(json_dict, ensure_ascii=False) + "\n"
            with open(tuniu_path + os.path.sep + "tuniu.json", "a", encoding="utf-8") as f:
                f.write(jsonData)

    def run(self, name, tag):
        """
        d: {"pageSize":20,"pageNumber":2,"cityCode":"","tags":[38],"timestamp":"1528359223836"}
        c: {"ct":100}
        _: 1528359236872
        """
        pageSize = 9999
        pageNumber = 1
        tags = tag
        timestamp = int(time.time()*1000)
        _ = timestamp + 1300
        for base_url in self.base_urls:
            # 构造url
            url = base_url.format(pageSize, pageNumber, tags, timestamp, _)
            # 发送请求
            json_data = self.response(url)
            if not json_data:
                break
            # 解析数据
            data = self.parse(json_data)
            if not data:
                break
            # 存储数据
            self.save(data, name)


if __name__ == "__main__":
    No_answer_base_url = "http://www.tuniu.com/papi/wenda/index/getNoAnswerQa?d=%7B%22pageSize%22%3A{0}%2C%22pageNumber%22%3A{1}%2C%22cityCode%22%3A%22%22%2C%22tags%22%3A%5B{2}%5D%2C%22timestamp%22%3A%22{3}%22%7D&c=%7B%22ct%22%3A100%7D&_={4}"
    with_answer_base_url = "http://www.tuniu.com/papi/wenda/index/getHomeQaFromEs?d=%7B%22pageSize%22%3A{0}%2C%22pageNumber%22%3A{1}%2C%22cityCode%22%3A%22%22%2C%22tags%22%3A%5B{2}%5D%2C%22timestamp%22%3A%22{3}%22%7D&c=%7B%22ct%22%3A100%7D&_={4}"
    # 实例化对象
    tuniu = TuNiu(No_answer_base_url, with_answer_base_url)
    for tup in all_name_url_list:
        url, name = tup
        tag = re.search(r"\d+", url).group()
        print(name, tag)
        tuniu.run(name, tag)
    tuniu.run("热门", '')
