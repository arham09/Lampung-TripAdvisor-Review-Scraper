# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

class TripSpiderSpider(Spider):
    name = 'trip_spider'
    allowed_domains = ['www.tripadvisor.co.id']
    start_urls = ['http://www.tripadvisor.co.id/Attractions-g2301788-Activities-Lampung_Sumatra.html#ATTRACTION_SORT_WRAPPER/']

    def parse(self, response):
        pariwisata = response.xpath('//div[@class="listing_title "]/a/@href').extract()
        for tempat in pariwisata:
            go_url = response.urljoin(tempat)
            # print(go_url + "Success")
            yield Request(go_url, callback=self.parse_review)

    def parse_review(self, response):
        nama = response.xpath('//h1[@class="heading_title"]/text()').extract_first()
        review = response.xpath('//div[@class="wrap"]/div[@class="prw_rup prw_reviews_text_summary_hsx"]/div[@class="entry"]/p/text()').extract()
        for a in review:
            new_review = a.replace("...", "")

            yield {
                "Nama Tempat" : nama,
                "Review" : new_review
            }