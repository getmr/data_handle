from requests_html import HTMLSession, etree
import re
import os
import time
import pymongo


# 连接mongodb数据库
client = pymongo.MongoClient("117.78.35.174", 27017)
# 连接lvmama
db = client.lvmama


session = HTMLSession()


# 获得所有的请求列表
response = session.get("http://www.lvmama.com/lvyou/wenda/")
all_elements = response.html.xpath("//div[2]/div/div/a|//div[3]/div/div/a")
print(all_elements)
all_links_pls = [(i.xpath("./a/@href")[0], i.xpath("./a/text()")[0]) for i in all_elements]
print(all_links_pls)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

_path = os.getcwd()
lm_path = _path + os.path.sep + 'LvMama'
if not os.path.exists(lm_path):
    os.mkdir(lm_path)
    os.chdir(lm_path)
# 切换工作目录
else:
    os.chdir(lm_path)


class LvMama(object):
    """
    获得驴妈妈问答的所有问题及分类
    parse：解析数据
    response：请求数据返回的对象
    save：储存信息
    run：启动程序
    """
    def __init__(self, hot_base_url, new_base_url):
        self.hot_base_url = hot_base_url
        self.new_base_url = new_base_url
        self.base_urls = [self.hot_base_url, self.new_base_url]
        self.file = open("/Users/zhangjintao/Desktop/lvmama.txt")

    def response(self, url):
        res = session.get(url)
        # 解析数据
        json_data = res.json()
        # 获得html
        html = json_data.get("data")
        return html

    def parse(self, data):
        print(data, type(data))
        # 构造xpath对象
        html_xpath = etree.HTML(data)
        # 获得对象列表
        element_list = html_xpath.xpath("//li")
        return element_list

    def save(self, data, page_num):
        for i in data:
            # print(i.xpath("./p/span/text()")[0], i.xpath("./p/a/text()")[0],i.xpath("./div/a/text()"))
            path = os.getcwd()
            # 构造存储的样本
            tags = i.xpath("./div/a/text()")
            tags.pop(0)
            text = "{0}    {1}    {2}".format(i.xpath("./p/span/text()")[0],i.xpath("./p/a/text()")[0], "    ".join(tags))

            # 构造mongodb的数据
            mongo_dict = {"palce": i.xpath("./p/span/text()")[0], "message": text, "tag": "    ".join(tags)}
            print("mongodb:", mongo_dict)
            # 写入mongodb的lvmama数据库
            # db.lvmama.insert(mongo_dict)
            self.file.write(pymongo)
            print(text)
            with open(path + os.path.sep + str(page_num), "w", encoding="utf-8") as f:
                f.write(text)
            page_num += 1
        return page_num

    def __del__(self):
        self.file.close()
        
    def run(self, num, pl):
        pl = re.sub(r'/', '', pl)
        pl_path = lm_path + os.path.sep + pl
        if not os.path.exists(pl_path):
            os.mkdir(pl_path)
            os.chdir(pl_path)
        else:
            os.chdir(pl_path)
        # 构造请求url
        file_num = 0
        for base_url in self.base_urls:
            page_num = 1
            while True:
                time.sleep(1)
                start_url = base_url.format(num, page_num)
                # 发起请求，返回数据
                res_data = self.response(start_url)
                if not res_data:
                    break
                # 解析数据
                data = self.parse(res_data)
                if not data:
                    break
                # 存储数据
                file_num = self.save(data, file_num)
                page_num += 1


if __name__ == '__main__':
    base_hot_url = "http://www.lvmama.com/qa-web/lvyou/wenda/ajaxGetNextPageList?keyId={0}&page={1}&pageSize=10&listType=DEST&showType=HOT"
    base_new_url = "http://www.lvmama.com/qa-web/lvyou/wenda/ajaxGetNextPageList?keyId={0}&page={1}&pageSize=10&listType=DEST&showType=NEW"
    lvMama = LvMama(base_hot_url, base_new_url)
    for link in all_links_pls[0:32]:
        print(link[0])
        num = re.search(r"(\d+)", link[0]).group(1)
        pl = link[1]
        print(num, pl)
        lvMama.run(num, pl)
    base_hot_url1 = "http://www.lvmama.com/qa-web/lvyou/wenda/ajaxGetNextPageList?keyId={0}&page={1}&pageSize=10&listType=TAG&showType=HOT"
    base_new_url1 = "http://www.lvmama.com/qa-web/lvyou/wenda/ajaxGetNextPageList?keyId={0}&page={1}&pageSize=10&listType=TAG&showType=NEW"
    lvMama = LvMama(base_hot_url, base_new_url)
    for link in all_links_pls[32:]:
        print(link[0])
        num = re.search(r"(\d+)", link[0]).group(1)
        pl = link[1]
        print(num, pl)
        lvMama.run(num, pl)

