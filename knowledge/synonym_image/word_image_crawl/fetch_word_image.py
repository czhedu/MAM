#
# -*- coding: utf-8 -*-
#
# Run the spider repeatly for the whole dictionary 
#
# @author Zhenhua Cai <czhedu@gmail.com>
# @date   2011-08-20
#

import random
import subprocess

f_word_dict = file(r'SogouLabDic_tab_utf8_linux.dic')
word_lines = f_word_dict.readlines()
f_word_dict.close()

while word_lines:
    i_word = 0
    max_word_num = random.randint(10, 30)

    f_temp_dict = file('temp.dic', "w")
    f_temp_dict.truncate(0)

    while i_word < max_word_num and word_lines:
        word_line = word_lines.pop(0)
        word = word_line[ : word_line.index("\t")]
        f_temp_dict.write(word+"\n")

        i_word += 1
        print "searching word: " + word

    f_temp_dict.close()

    # run the spider
    subprocess.Popen(['scrapy', 'crawl', 'image.google.com_chinese']).wait()

