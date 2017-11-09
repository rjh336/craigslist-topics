import scrapy
import re
import datetime as dt
	
class CLSpider(scrapy.Spider):
	name = 'cl_spider'
	rotate_user_agent = True
	
	custom_settings = {
		"DOWNLOAD_DELAY": 2,
		"CONCURRENT_REQUESTS_PER_DOMAIN": 3,
		"RANDOMIZE_DOWNLOAD_DELAY":True
		#"HTTPCACHE_ENABLED": True
	}
 
	# start_urls = ["https://newyork.craigslist.org/search/muc",
	# 			  "https://boston.craigslist.org/search/muc",
	# 			  "https://seattle.craigslist.org/search/muc",
	# 			  "https://losangeles.craigslist.org/search/muc",
	# 			  "https://nashville.craigslist.org/search/muc",
	# 			  "https://portland.craigslist.org/search/muc",
	# 			  "https://denver.craigslist.org/search/muc",
	# 			  "https://detroit.craigslist.org/search/muc",
	# 			  "https://sfbay.craigslist.org/search/muc",
	# 			  "https://atlanta.craigslist.org/search/muc",
	# 			  "https://miami.craigslist.org/search/muc",
	# 			  "https://washingtondc.craigslist.org/search/muc",
	# 			  "https://philadelphia.craigslist.org/search/muc",
	# 			  "https://chicago.craigslist.org/search/muc",
	# 			  "https://dallas.craigslist.org/search/muc"]
	start_urls = ['https://raleigh.craigslist.org/search/muc',
				 'https://newjersey.craigslist.org/search/muc',
				 'https://orlando.craigslist.org/search/muc',
				 'https://orangecounty.craigslist.org/search/muc',
				 'https://nh.craigslist.org/search/muc',
				 'https://kansascity.craigslist.org/search/muc',
				 'https://houston.craigslist.org/search/muc',
				 'https://cleveland.craigslist.org/search/muc',
				 'https://lasvegas.craigslist.org/search/muc',
				 'https://sandiego.craigslist.org/search/muc',
				 'https://stlouis.craigslist.org/search/muc',
				 'https://cincinnati.craigslist.org/search/muc',
				 'https://austin.craigslist.org/search/muc',
				 'https://minneapolis.craigslist.org/search/muc',
				 'https://inlandempire.craigslist.org/search/muc',
				 'https://columbus.craigslist.org/search/muc',
				 'https://hudsonvalley.craigslist.org/search/muc',
				 'https://longisland.craigslist.org/search/muc',
				 'https://sanantonio.craigslist.org/search/muc',
				 'https://honolulu.craigslist.org/search/muc',
				 'https://neworleans.craigslist.org/search/muc',
				 'https://phoenix.craigslist.org/search/muc',
				 'https://southjersey.craigslist.org/search/muc',
				 'https://pittsburgh.craigslist.org/search/muc',
				 'https://baltimore.craigslist.org/search/muc',
				 'https://charlotte.craigslist.org/search/muc',
				 'https://providence.craigslist.org/search/muc',
				 'https://cnj.craigslist.org/search/muc',
				 'https://tampa.craigslist.org/search/muc']
	

	def parse(self, response):
		purl = response.request.url
		print("\n", "SCRAPING FROM PAGE: ",purl,"\n")
		for href in response.xpath(
			"//div[@id='sortable-results']/ul/li[@class='result-row']/p/a[@class='result-title hdrlnk']/@href"
			).extract():

			yield scrapy.Request(
				url=href,
				callback=self.parse_post,
				meta={'url': href}
			)

		next_url_path = response.xpath(
			'//span[@class="buttons"]/a[@class="button next"]/@href'
			).extract_first()

		m = re.search(".*craigslist.org",response.request.url)
		root_url = m.group(0)
		next_url = root_url + next_url_path

		yield scrapy.Request(
			url=next_url,
			callback=self.parse
		)

	def parse_post(self, response):

		url = response.request.meta['url']
		print("\n", "SCRAPING FROM POST: ",url,"\n")

		title = response.xpath("//span[@id='titletextonly']//text()").extract_first()
		city = response.xpath("//li[@class='crumb area']/p/a/text()").extract_first()
		body = "".join(response.xpath('//section[@id="postingbody"]//text()').extract())
		gmap_lat = response.xpath("//div[@id='map']//@data-latitude").extract_first()
		gmap_lon = response.xpath("//div[@id='map']//@data-longitude").extract_first()
		gmap_acc = response.xpath("//div[@id='map']//@data-accuracy").extract_first()
		captured = dt.datetime.now()

		yield {'url': url,
		'title': title,
		'city': city,
		'body': body,
		'gmap_lat': gmap_lat,
		'gmap_lon': gmap_lon,
		'gmap_acc': gmap_acc,
		'captured': captured}