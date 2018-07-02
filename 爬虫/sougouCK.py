from requests_html import HTMLSession
import os, re
print(os.getcwd())
os.chdir("/Users/zhangjintao/Desktop/喜马拉雅爬虫/搜狗词库")

class SouGciK(object):
    def __init__(self):
        self.start_url = "https://pinyin.sogou.com/dict/cate/index/"
        self.base_url = "https://pinyin.sogou.com/dict/cate/index/{}/default/{}"

    def reponse(self, url):
        session = HTMLSession()
        res = session.get(url)
        return res

    def parse_data(sefl, data):
        html = data.html
        elements = html.xpath('//*[@id="dict_detail_list"]/div/div[1]/div/a')
        dl_url_list = [("https://pinyin.sogou.com" + i.xpath('./a/@href')[0], i.xpath('./a/text()')[0]) for i in elements]
        # print(dl_url_list)
        return dl_url_list

    def save(self, data, name):
        with open(name + '.scel', 'wb') as f:
            f.write(data)

    def run(self):
        # 发起请求
        res = self.reponse(self.start_url)
        html = res.html
        element = html.xpath('//*[@id="city_list_show"]/table/tbody/tr/td/div/a/@href')
        num_list = [re.search(r'\d+', i).group() for i in element]
        print(num_list)
        # 构造url
        page = 1
        for num in num_list:
            url = self.base_url.format(num, page)
            print(url)
            res = self.reponse(url)
            dl_url_list = self.parse_data(res)
            print(dl_url_list)
            for tup in dl_url_list:
                # print(tup)
                if re.search(r'信息精选', tup[1]):
                    print(tup[0], tup[1])
                    nm = re.search(r'\d+', tup[0]).group()
                    res = self.reponse(tup[0])
                    html = res.html
                    print(nm)
                    xpt = '//a[@id="dict_{}"]/@href'.format(nm)
                    print(xpt)
                    print(html.xpath(xpt))
                    dw_url = "https:" + html.xpath(xpt)[0]
                    res_data = self.reponse(dw_url)
                    content = res_data.content
                    self.save(content, tup[1])


if __name__ == "__main__":
    sougou = SouGciK()
    sougou.run()