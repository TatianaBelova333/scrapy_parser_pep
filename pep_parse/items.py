import scrapy


class PepParseItem(scrapy.Item):
    """Item for parsing PEP documentation."""
    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
