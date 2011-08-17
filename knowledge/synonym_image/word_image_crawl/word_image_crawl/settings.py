# Scrapy settings for word_image_crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'word_image_crawl'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['word_image_crawl.spiders']
NEWSPIDER_MODULE = 'word_image_crawl.spiders'
DEFAULT_ITEM_CLASS = 'word_image_crawl.items.WordImageCrawlItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

