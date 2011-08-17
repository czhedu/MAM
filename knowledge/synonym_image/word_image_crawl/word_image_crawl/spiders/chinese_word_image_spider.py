import re
from scrapy import log
from scrapy.spider import BaseSpider

class ChineseWordImageSpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)
#        self.reobj_image = re.compile(r"data-src=\"(http:[^\"\s]+)\"\s+")
        self.reobj_image = re.compile(r"gstatic.com")

    name = "image.google.com_chinese"
    start_urls = [
        "http://images.google.com/search?tbm=isch&q=girl",
        "http://images.google.com/search?tbm=isch&q=man",
        "http://images.google.com/search?tbm=isch&q=woman",
        "http://images.google.com/search?tbm=isch&q=apple"
    ]

    def parse(self, response):
        if "images.google.com" in response.url:
#            print response.body
            query_image_result = self.reobj_image.search(response.body)
#            query_image_result = self.reobj_image.findall("http://www.gstatic.com")
            print query_image_result

        else:
            file_name = response.url[response.url.rindex():]
            print file_name
#            open(file_name, 'wb').write(response.body)

# data-src="http://t3.gstatic.com/images?q=tbn:ANd9GcQzA4FrQnpyiUbdTXzXpxCrzXSYjcq29Ds8c6MwI9KQV2FmilZH"

#        filename = response.url.split("/")[-2]
#        open(filename, 'wb').write(response.body)

