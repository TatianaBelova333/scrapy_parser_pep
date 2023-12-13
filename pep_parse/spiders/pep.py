import re

import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import (PEP_NAME_GRP, PEP_NUM_NAME_SRCH_PATN,
                                PEP_NUM_GRP)


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
        h1_text = response.css('h1.page-title::text').getall()
        complete_text = ''.join(h1_text)

        pep_number_name = re.search(PEP_NUM_NAME_SRCH_PATN, complete_text)
        pep_name = pep_number_name.group(PEP_NAME_GRP)
        pep_number = pep_number_name.group(PEP_NUM_GRP)

        pep_status = response.css(
            'dt:contains("Status") + dd>abbr::text',
        ).get()

        data = {
            'number': pep_number,
            'name': pep_name,
            'status': pep_status,
        }
        yield PepParseItem(data)
