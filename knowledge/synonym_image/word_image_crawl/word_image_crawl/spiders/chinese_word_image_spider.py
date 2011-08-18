#
# -*- coding: utf-8 -*-
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
from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request

class ChineseWordImageSpider(BaseSpider):

    name = "image.google.com_chinese"

    def __init__(self):
        BaseSpider.__init__(self)

        # settings 
        settings.overrides['DOWNLOAD_DELAY'] = 0.2

        # regex object for extracting image url
        self.reobj_image = re.compile(r"http://\S+.gstatic.com[^\"\s]+")

        self.start_urls = [
            # the url should be end with start=xx    
            "http://images.google.com/search?tbm=isch&safe=off&q=美女&start=0"
        ]

        self.num_images_per_page = 20
        self.num_images = 200

    def parse(self, response):
        # if it is an html page
        if "images.google.com" in response.url:
            # extract image urls and send requests
            image_link_list = self.reobj_image.findall(response.body)

            for image_link in image_link_list:
                yield Request(image_link, callback=self.parse)

            # launch more/new searches to google
            start_equal_index = response.url.rindex("=")
            url_without_start = response.url[ :start_equal_index+1]
            new_start = int( response.url[start_equal_index+1: ] ) + self.num_images_per_page

            # invoke more search to the same word
            if new_start<self.num_images: 
                yield Request(url_without_start + str(new_start), callback=self.parse)
            # invoke the search to the new word    
            else:
                pass


        # if it is an image file
        else:
            file_name = "data/" + response.url[response.url.rindex(":")+1: ]
            open(file_name, 'wb').write(response.body)


