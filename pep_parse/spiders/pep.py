import re
from pep_parse.settings import (PEP_NAME_GROUP, PEP_NUMBER_NAME_SRCH_PATN,
                                PEP_NUMBER_GROUP)

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Parse all PEP documentation links from the main page."""
        num_idx_section = response.css('#numerical-index')
        all_pep_links = num_idx_section.css('a[href^="pep-"]')

        for pep_link in all_pep_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        """
        Parse PEP document number, title and status
        from each PEP documentation page.

        """
        h1 = response.css('h1.page-title::text').get()
        pep_num_name_pattern = PEP_NUMBER_NAME_SRCH_PATN

        pep_number_name = re.search(pep_num_name_pattern, h1)
        pep_name = pep_number_name.group(PEP_NAME_GROUP)
        pep_number = pep_number_name.group(PEP_NUMBER_GROUP)

        pep_status = response.css(
            'dt:contains("Status") + dd>abbr::text',
        ).get()

        data = {
            'number': pep_number,
            'name': pep_name,
            'status': pep_status,
        }
        yield PepParseItem(data)
