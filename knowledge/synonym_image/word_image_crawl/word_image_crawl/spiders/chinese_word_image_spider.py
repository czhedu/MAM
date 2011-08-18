#
# Fetch images from google search engine 
#
# @author Zhenhua Cai <czhedu@gmail.com>
# @date   2011-08-18
# 
# Below is an example of image link in google server
#     data-src="http://t3.gstatic.com/images?q=tbn:ANd9GcQzA4FrQnpyiUbdTXzXpxCrzXSYjcq29Ds8c6MwI9KQV2FmilZH"
#
# About google image searching api 
#     http://www.codeproject.com/KB/IP/google_image_search_api.aspx
#

import re
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.http import Request

class ChineseWordImageSpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)
        self.reobj_image = re.compile(r"http://\S+.gstatic.com[^\"\s]+")

    name = "image.google.com_chinese"
    start_urls = [
        "http://images.google.com/search?tbm=isch&q=apple&start=0"

#        "http://images.google.com/search?tbm=isch&q=girl",
#        "http://images.google.com/search?tbm=isch&q=man",
#        "http://images.google.com/search?tbm=isch&q=woman",
#        "http://images.google.com/search?tbm=isch&q=apple"
    ]

    def parse(self, response):
        if "images.google.com" in response.url:
            image_link_list = self.reobj_image.findall(response.body)

            for image_link in image_link_list:
                yield Request(image_link, callback=self.parse)

        else:
            file_name = "data/" + response.url[response.url.rindex(":")+1:]
            open(file_name, 'wb').write(response.body)


