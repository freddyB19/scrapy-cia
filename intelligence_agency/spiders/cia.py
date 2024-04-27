import scrapy

# Links Desclassified = //a[starts-with(@href, "collection") and (parent::h2|parent::h3)]/@href
# title = //h1[@class="documentFirstHeading"]/text()
# paragraph = //div[@class="field-item even"]//p[not(@class) and not(@style) and not(child::strong)]/text()

class SpiderCIA(scrapy.Spider):
	name = "cia"
	start_urls = [
		'https://www.cia.gov/readingroom/historical-collections'
	]
	custom_settings = {
		'FEEDS':{
			'./data/cia.json': {
				'format': 'json',
				'encoding': 'utf8',
				'ident': 4
			}
		},
		# 'FEED_EXPORT_ENCODING': 'utf-8'
	}


	def parse_link(self, response, **kwargs):
		if kwargs:
			link = kwargs.get("url")
			title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
			paragraph = response.xpath(
				'//div[@class="field-item even"]//p[not(@class) and not(@style) and not(child::strong)]/text()'
			).get()

		yield {
			'title': title,
			'body': paragraph,
			'link': link,
		}


	def parse(self, response):
		links_desclassified = response.xpath(
			'//a[starts-with(@href, "collection") and (parent::h2|parent::h3)]/@href'
		).getall()

		for link in links_desclassified:
			yield response.follow(
				link, callback = self.parse_link, 
				cb_kwargs = {'url': response.urljoin(link)}
			)