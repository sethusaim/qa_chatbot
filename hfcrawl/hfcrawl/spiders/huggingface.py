import os
from urllib.parse import urljoin

import scrapy
from html2text import HTML2Text


class HuggingfaceSpider(scrapy.Spider):
    name = "huggingface"

    allowed_domains = ["huggingface.co"]

    start_urls = ["http://huggingface.co/docs/diffusers/index"]

    def __init__(self, *args, **kwargs):
        super(HuggingfaceSpider, self).__init__(*args, **kwargs)

        if not os.path.exists("output"):
            os.makedirs("output")

        self.converter = HTML2Text()

        self.converter.ignore_links = True

        self.converter.ignore_images = True

        self.converter.ignore_emphasis = True

        self.converter.ignore_tables = True

        self.converter.body_width = 0

    def parse(self, response):
        """
        This is a Python function that parses a web page's response, replaces a specific string, saves the
        parsed text to a file, and recursively calls itself to parse other pages.

        Args:
          response: The response object contains the data that was received after making a request to a
        website. It includes the HTML content, headers, status code, and other information related to the
        response.
        """
        text = self.converter.handle(response.body.decode())

        text = text.replace("<|endoftext|>", " ")

        text.strip()

        url = response.url.strip("/")

        filename = f"output/{hash(url)}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        for link in response.xpath("//a/@href"):
            href = link.get()

            if href.startswith("/docs/diffusers"):
                url = urljoin(response.url, href)

                yield scrapy.Request(url, callback=self.parse)
