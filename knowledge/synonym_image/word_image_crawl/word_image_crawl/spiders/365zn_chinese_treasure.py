#
# -*- coding: utf-8 -*-
#
# Fetch chinese treasures from www.365zn.com/fyc 
#
# @author Zhenhua Cai <czhedu@gmail.com>
# @date   2011-08-24
# 
# Below is an example of word list page link 
#     http://www.365zn.com/fyc/fyc_c.htm
#
# And here is an example of word page link
#     http://www.365zn.com/fyc/htm/22322.htm
#

import re
import uuid
import sqlite3
import urlparse

from scrapy import log
from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request

class znChineseTreasureSpider(BaseSpider):

    name = "www.365zn.com_fyc"

    def __init__(self):
        BaseSpider.__init__(self)

        # settings 
        settings.overrides['DOWNLOAD_DELAY'] = 0
        settings.overrides['LOG_FILE'] = "scrapy.log"
        settings.overrides['LOG_STDOUT'] = True
        settings.overrides['DOWNLOAD_TIMEOUT'] = 180
        settings.overrides['RETRY_TIMES'] = 10

        # base url of all the pages
        self.base_url = "http://www.365zn.com/fyc/"

        # regex objects 

        # example: <a href="fyc_h.htm"
        self.reobj_word_list_page = re.compile(r"fyc_\w+.htm")

        # example: <a href=htm/11474.htm title='把持'>
        self.reobj_word_and_page = re.compile(r"href=\S+\s+title='[^']+'")  

        # 【同义词】 <font color=blue>胸有成竹&nbsp;&nbsp;心中有数&nbsp;&nbsp;稳操胜券</font>
        self.reobj_synonym = re.compile(r"【同义词】\W+<font color=blue>([^<]*)</font>") 
        
        # 【反义词】 <font color=red>心中无数&nbsp;&nbsp;手忙脚乱</font>
        self.reobj_antonym = re.compile(r"【反义词】\W+<font color=red>([^<]*)</font>") 

        # chinese character(s)
#        self.reobj_chinese = re.compile(r"[\u4e00-\u9fa5]+")
        self.reobj_chinese = re.compile(r"[\x80-\xff]+")

    def start_requests(self):
        '''Called only once in the initialization of spider'''
        return [ Request("http://www.365zn.com/fyc/fyc_A.htm", callback=self.parse_word_list_page) ]

    def parse_word_list_page(self, response): 
        '''Parse page of word list'''
        # normalize html of response page
        html = response.body.decode("gb18030").encode("utf-8")

        # get all the fragments of word and page
        # <a href=htm/11474.htm title='把持'>
        word_and_page_list = self.reobj_word_and_page.findall(html)

        # process all the fragments of word and page
        for word_and_page in word_and_page_list: 
            print word_and_page
            word_page = word_and_page[word_and_page.index("htm"):
                                      word_and_page.rindex("htm")+3
                                     ]
            word = word_and_page[word_and_page.index("'")+1: 
                                 word_and_page.rindex("'")
                                ]

            print "word_page: " + word_page + " word: " + word

            # send request for the word
            yield Request(self.base_url+word_page, 
                          callback=self.parse_word_page,
                          meta={'word': word}
                         )

        # get all the fragments of word list page
        # <a href="fyc_h.htm"
        word_list_list = self.reobj_word_list_page.findall(html)

        # process all the fragments of word list
        for word_list in word_list_list:
            yield Request(self.base_url+word_list, callback=self.parse_word_list_page)

    def parse_word_page(self, response): 
        '''Parse page of word'''
        # normalize html of response page
        html = response.body.decode("gb18030").encode("utf-8")

        # get word
        word = response.meta['word']

        print "parse word page of: " + word

        # search synonym and antonym fragments
        synonym_fragment = self.reobj_synonym.search(html)
        antonym_fragment = self.reobj_antonym.search(html)

        synonym_str = ""
        antonym_str = ""

        if synonym_fragment:
            for synonym in self.reobj_chinese.findall( synonym_fragment.group(1) ):
                synonym_str += synonym + ","

        if len(synonym_str) > 0:
            synonym_str = synonym_str[ : len(synonym_str)-1]

        if antonym_fragment:     
            for antonym in self.reobj_chinese.findall( antonym_fragment.group(1) ): 
                antonym_str += antonym + ","

        if len(antonym_str) > 0:
            antonym_str = antonym_str[ : len(antonym_str)-1]

        print "word: " + word + " synonyms: " + synonym_str + " antonyms: " + antonym_str

        # open database
        con = sqlite3.connect('chinese_treasures.sqlite')
        cur = con.cursor()

        # record word, synonyms and antonyms
        uuid_str = str(uuid.uuid4())

        sql = 'INSERT INTO chinese_treasures (uuid, word, synonym, antonym) ' + \
              'VALUES("%s", "%s", "%s", "%s")' % (uuid_str, word, synonym_str, antonym_str)

        cur.execute(sql) 
        con.commit()

