# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

class TripSpider(Spider):
    name = 'trip'
    allowed_domains = ['www.tripadvisor.co.id']
    start_urls = ['http://www.tripadvisor.co.id/Attractions-g2301788-Activities-Lampung_Sumatra.html#ATTRACTION_SORT_WRAPPER/']

    def parse(self, response):
        pariwisata = response.xpath('//div[@class="listing_title "]/a/@href').extract()
        for tempat in pariwisata:
            go_url = response.urljoin(tempat)
            # print(go_url + "Success")
            yield Request(go_url, callback=self.parse_link)

    def parse_link(self, response):
        link_review = response.xpath('//div[@class="quote"]/a/@href').extract_first()
        go_url = response.urljoin(link_review)
        # print(go_url + " Success Broh")
        yield Request(go_url, callback=self.parse_review)

    def parse_review(self, response):
        nama = response.xpath('//div[@class="surContent"]/a/text()').extract_first()
        box = response.xpath('//div[@class="reviewSelector"]/div[@class="review hsx_review is-multiline is-mobile inlineReviewUpdate provider0"]')
        for data in box:
            review = data.xpath('.//div[@class="mainContent"]/div[@class="innerBubble"]/div[@class="wrap"]/div[@class="prw_rup prw_reviews_text_summary_hsx"]/div[@class="entry"]/p/text()').extract()
            user = data.xpath('.//div[@class="leftMemberInfo"]/div[@class="prw_rup prw_reviews_member_info_hsx"]/div[@class="member_info"]/div[@class="memberOverlayLink"]/div["username mo"]/span/text()').extract_first()
            rating = data.xpath('.//div[@class="mainContent"]/div[@class="innerBubble"]/div[@class="wrap"]/div[@class="rating reviewItemInline"]/span/@class').extract_first()

            review_fix = ''.join(map(str, review))
            rating_raw = rating.replace("ui_bubble_rating bubble_", "")
            rating_fix = rating_raw.replace("0", "")

            yield {
                "Nama" : nama,
                "User" : user,
                "Isi" : review_fix,
                "Rating" : rating_fix

            }

        next_url = response.xpath('//a[@class="nav next taLnk "]/@href').extract_first()
        absolute_url = "https://www.tripadvisor.co.id" + next_url
        #next_url_fix = response.urljoin(absolute_url)
        print(absolute_url + " Success")
        yield Request(url=absolute_url, callback=self.parse_review)
        
        