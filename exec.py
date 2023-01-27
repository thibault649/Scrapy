from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from sig.spiders.quotes_spider import IndexSpider

spider = IndexSpider()

settings = get_project_settings()
configure_logging(settings)

runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(IndexSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished
