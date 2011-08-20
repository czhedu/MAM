#
# -*- coding: utf-8 -*-
#
# Fetch images from google search engine 
#
# @author Zhenhua Cai <czhedu@gmail.com>
# @date   2011-08-20
# 
# Below is an example of image link in google server
#     data-src="http://t3.gstatic.com/images?q=tbn:ANd9GcQzA4FrQnpyiUbdTXzXpxCrzXSYjcq29Ds8c6MwI9KQV2FmilZH"
#
# About google image searching api 
#     http://www.codeproject.com/KB/IP/google_image_search_api.aspx
#

import re
import uuid
import sqlite3
import urlparse

from scrapy import log
from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request

class ChineseWordImageSpider(BaseSpider):

    name = "image.google.com_chinese"

    def __init__(self):
        BaseSpider.__init__(self)

        # settings 
        settings.overrides['DOWNLOAD_DELAY'] = 0
        settings.overrides['LOG_FILE'] = "scrapy.log"
        settings.overrides['LOG_STDOUT'] = True
        settings.overrides['DOWNLOAD_TIMEOUT'] = 180
        settings.overrides['RETRY_TIMES'] = 10

        self.num_images_per_page = 20
        self.num_images = 60

        # base url for image searching
        self.base_url = "http://images.google.com/search?tbm=isch&safe=off"

        # regex object for extracting image url
        self.reobj_image = re.compile(r"http://\S+.gstatic.com[^\"\s]+")

        # initialize start_urls
        self.fill_start_urls()

    def fill_start_urls(self):
        '''Append more urls in start urls'''
#        f_word_dict = file(r'SogouLabDic_tab_utf8_linux.dic')
        f_word_dict = file(r'temp.dic') 
        word_lines = f_word_dict.readlines()
        f_word_dict.close()

        for word in word_lines:
#            word = word_line[ : word_line.index("\t")]
            start = 0 
            while start < self.num_images:
                self.start_urls.append( self.base_url + 
                                        "&q=" + word + 
                                        "&start=" + str(start)
                                      )
                start += self.num_images_per_page

    def parse(self, response):
        # if it is an html page
        if "images.google.com" in response.url:
            # get word
            query = urlparse.urlparse(response.url).query
            word = urlparse.parse_qs(query)["q"][0].decode("utf-8")

            # extract image urls 
            image_link_list = self.reobj_image.findall(response.body)

            # open database
            con = sqlite3.connect('word_image.db3')
            cur = con.cursor()

            # send requests for all the images and record word-image relation
            for image_link in image_link_list:
                # get image name
                image_name = image_link[image_link.rindex(":")+1: ]

                # record word-image relation
                uuid_str = str(uuid.uuid4())

                sql = 'INSERT INTO word_image (uuid, word, image) VALUES("%s", "%s", "%s")' % \
                      (uuid_str, word, image_name)

                cur.execute(sql) 
                con.commit()

                # send request for the image
                yield Request(image_link, callback=self.parse)

        # if it is an image file, save it
        else:
            # save image file
            image_name = response.url[response.url.rindex(":")+1: ]
            open("data/" + image_name, 'wb').write(response.body)

