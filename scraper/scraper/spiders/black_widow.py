import scrapy, time
from scraper.scraper.items import ScraperItem


class RehabSpider(scrapy.Spider):
   name = "rehabs"
   allowed_domains = ["addictioncenter.com"]
   start_urls = ["https://www.addictioncenter.com/"]

   states = ['arizona', 'alabama', 'alaska', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'florida','georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas','kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan','minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new-hampshire','new-york', 'new-jersey', 'new-mexico', 'north-carolina', 'north-dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode-island','south-carolina', 'south-dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west-virginia', 'wisconsin', 'wyoming','guam', 'puerto-rico', 'us-pacific-islands', 'us-virgin-islands', 'washington-dc']
 
   def parse(self, response):
       for state in self.states:
         for href in response.css(r" a[href*='https://www.addictioncenter.com/rehabs/{}']::attr(href)".format(state)).getall():
            url = response.urljoin(href)
            req = scrapy.Request(url, callback=self.parse_urls, cb_kwargs=dict(state=state))
            time.sleep(3)
            yield req

   def parse_urls(self, response, state):
      for href in response.css(r" a[href*='https://www.addictioncenter.com/rehabs/{}']::attr(href)".format(state)).getall():
         url = response.urljoin(href)
         data = {}
         data['urls'] = url
         req = scrapy.Request(url, callback=self.parse_data, cb_kwargs=dict(state=state))
         yield req
   
   def parse_data(self, response, state):
      for text in response.css('html').getall():
         data = ScraperItem()
         data['name'] = response.css("h1.PageHero__title::text").get()
         data['address'] = response.css("h3.PageHero__address span::text").get()
         data['phone'] = response.css("a.phone-number::text").get()
         data['website'] = response.css("a.PageHero__btn::attr(href)").get()
         data['description'] =  response.css("div.Rehab__section__inner>p::text").get()

         yield data