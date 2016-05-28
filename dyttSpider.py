# coding=utf-8

import requests
import re
import base64

class spider(object):
    def __init__(self):
        print '开始爬取内容。。。'

#getsource用来获取网页源代码
    def getsource(self,url):
        get_html = requests.get(url)
        get_html.encoding = "gb2312"
        return get_html.text

#changepage用来生产不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('list_23_(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('list_23_\d+','list_23_%s'%i,url,re.S)
            page_group.append(link)
        return page_group

#geteverymovie用来抓取每部电影的信息
    def geteverymovie(self,source):
        everymovie = re.findall('<b>(.*?)</b>',source,re.S)
        return everymovie

# url2Thunder用来转化成迅雷下载地址
    def url2Thunder(self, url):
        url = 'AA' + url + 'ZZ'
        # print type(url)
        url = base64.b64encode(url.encode("utf-8"))
        url = 'thunder://' + url
        # print url
        return url

#geteverymovieinfo用来抓取每部电影的url和title信息
    def geteverymovieinfo(self,everymovie):
        domain = 'http://www.ygdy8.net'
        info = {}
        info['title'] = re.search('>(.*?)</a>',everymovie,re.S).group(1).encode("utf-8")
        info['url'] = domain+re.search('href="(.*?)" class',everymovie,re.S).group(1).encode("utf-8")
        # print info['title'] +' '+ info['url']
        #获取每部电影的下载地址
        print info['url']
        html = self.getsource(info['url'])
        url = re.search('bgcolor="#fdfddf"><a href="(.*?)">',html,re.S)
        # print type(self.url2Thunder(url))
        #有些没有下载地址需要做出判断
        if url is not None:
            info['thunder'] = self.url2Thunder(url.group(1))
        else:
            info['thunder'] = ''
        return info

#saveinfo用来保存结果到info.txt文件中
    def saveinfo(self,movieDownloadInfo):
        f = open('info.txt','a')
        for each in movieDownloadInfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('url:' + each['url'] + '\n')
            f.writelines('thunder:' + each['thunder'] + '\n')
            f.writelines('\n')
        f.close()

if __name__ == '__main__':

    movieDownloadInfo = []
    url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_1.html'
    # url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_30.html'
    moviespider = spider()
    html = moviespider.getsource(url)
    # 获得要爬的页数
    pagecount = re.findall('>(.*?)</option>', html, re.S)[-1]
    # print pagecount
    all_links = moviespider.changepage(url,int(pagecount))
    # all_links = moviespider.changepage(url,1)
    for link in all_links:
        print '正在处理页面：' + link
        html = moviespider.getsource(link)
        everymovie = moviespider.geteverymovie(html)
        for each in everymovie:
            info = moviespider.geteverymovieinfo(each)
            movieDownloadInfo.append(info)
            print info
    moviespider.saveinfo(movieDownloadInfo)