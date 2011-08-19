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
import uuid
import sqlite3

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

        # regex object for extracting image url
        self.reobj_image = re.compile(r"http://\S+.gstatic.com[^\"\s]+")

        self.num_images_per_page = 20
        self.num_images = 20

        # get word list
#        f_word_dict = file(r'SogouLabDic_tab_utf8_linux.dic')
        f_word_dict = file(r'test_dict') 
        self.word_lines = f_word_dict.readlines()

        # create initial url (the url should be end with start=xx)
        self.base_url = "http://images.google.com/search?tbm=isch&safe=off"

        word_line = self.word_lines[0];
        del self.word_lines[0]; 

        self.word = word_line[ : word_line.index("\t")]
        self.start_urls = [self.base_url + "&q=" + self.word + "&start=0"]

    def parse(self, response):
        # if it is an html page
        if "images.google.com" in response.url:
            # extract image urls, record word-image relation and send requests
            image_link_list = self.reobj_image.findall(response.body)

            con = sqlite3.connect('word_image.db3')
            cur = con.cursor()
            for image_link in image_link_list:
                # record word-image relation
                uuid_str = str(uuid.uuid4())
                image = image_link[image_link.rindex(":")+1: ]

                sql = 'INSERT INTO word_image (uuid, word, image) VALUES("%s", "%s", "%s")' % \
                      (uuid_str, self.word, image)

                cur.execute(sql) 
                con.commit()
              
                # send request for the image
                yield Request(image_link, callback=self.parse)

            # update start parameter for next page of images
            start_equal_index = response.url.rindex("=")
            url_without_start = response.url[ :start_equal_index+1]
            new_start = int( response.url[start_equal_index+1: ] ) + self.num_images_per_page

            # invoke more search to the same word
            if new_start < self.num_images: 
                yield Request(url_without_start + str(new_start), callback=self.parse)
            # invoke the search to the new word    
            else:
                if len(self.word_lines): 
                    word_line = self.word_lines[0]
                    del self.word_lines[0]

                    self.word = word_line[ : word_line.index("\t")]
                    print self.word
                    search_word_url = self.base_url + "&q=" + self.word + "&start=0"
                    yield Request(search_word_url, callback=self.parse)

        # if it is an image file
        else:
            file_name = "data/" + response.url[response.url.rindex(":")+1: ]
            open(file_name, 'wb').write(response.body)


