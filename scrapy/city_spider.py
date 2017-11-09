import scrapy
	
class CLCSpider(scrapy.Spider):
	name = 'cities'
	
	custom_settings = {
		"DOWNLOAD_DELAY": 3,
		"CONCURRENT_REQUESTS_PER_DOMAIN": 3,
		"HTTPCACHE_ENABLED": True
	}
 
	
	start_urls = ["https://www.craigslist.org/about/sites"]
	

	def parse(self, response):
		cities = response.xpath("/html/body/article/section/div[3]/div/ul/li/a/@href").extract()
		for city in cities:
			city_url = city + "d/musicians/search/muc"
			yield scrapy.Request(
				url=city_url,
				callback=self.parse_page
			)

	def parse_page(self, response):

		url = response.url
		active_posts = response.xpath("//span[@class='totalcount']//text()").extract_first()
		
		yield {'url': url, 'active_posts': active_posts}