import scrapy
import json
import os
from csv import DictWriter

try:
	os.remove('openrice_data.json')
except OSError:
	pass

class OpenriceSpider(scrapy.Spider):
	name = 'openrice'
	allowed_domains = ['www.openrice.com']

	def start_requests(self):
		headers = {
			# 'accept-encoding': 'gzip, deflate, sdch, br',
			# 'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
			# 'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
			# 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			# 'cache-control': 'max-age=0',
		}
		file = open('openrice_urls.txt', "r")
		limit = 1200
		x = 1
		for line in file:
			if x > limit:
				break;
			x += 1
			# if the url includes a chinese character which we cannot read, skip that url
			if "%E" in line:
			 	#print("ERROR: CHINESE URL. Skipping: " + line)
				continue;
			else:
				pass#print("Scraping: " + line);

		 	yield scrapy.Request(url=line.strip(), headers=headers, callback=self.parse)

	def parse(self, response):
		restaurant_data = {}
		address = []
		reviews = []

		# below line extracts a script node from the beginning of the html that includes lots of useful informtation
		raw_data = response.xpath('//*[@id="global-container"]/main/script[1]/text()').extract()

		try:
		    os.remove('temp.json')
		except OSError:
		    pass

		# this stores that information into a new file as a json
		with open('temp.json', 'w') as outfile:
			data_array = []
			for x in raw_data:
				if not x.isspace():
					x = x.strip().encode('utf-8')
					data_array.append(x)
					#print(x);
					outfile.write(x)
			outfile.close();

		# this immediately opens up that newly created file to read it back in as a json
		with open('temp.json') as json_data:
			data = json.load(json_data)
			latitude = data['geo']['latitude']
			address.append(latitude)
			longitude = data['geo']['longitude']
			address.append(longitude)
			price_range = data['priceRange'].encode('utf-8').lower()
			district = data['address']['addressLocality'].encode('utf-8').lower()
			name = data['name'].encode('utf-8').lower()
			json_data.close()

		#The above functions work well, but theres still some data that we have to strip from the rest of the page:

		cuisine = response.xpath('//*[@id="global-container"]/main/div[2]/div[1]/div[1]/div/section/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]//text()').extract()
		cuisine_array = []
		for x in cuisine:
			if not x.isspace():
				cuisine_array.append(x.strip().encode('utf-8').lower())


		rating = response.xpath('//*[@id="global-container"]/main/div[2]/div[1]/div[1]/div/section/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/text()').extract_first()
		#print(rating)
		good_reviews = response.xpath('//*[@id="global-container"]/main/div[2]/div[1]/div[2]/section/div[2]/div[2]/text()').extract_first()
		reviews.append(str(good_reviews).encode('utf-8'))
		ok_reviews = response.xpath('//*[@id="global-container"]/main/div[2]/div[1]/div[2]/section/div[2]/div[4]/text()').extract_first()
		reviews.append(str(ok_reviews).encode('utf-8'))
		bad_reviews = response.xpath('//*[@id="global-container"]/main/div[2]/div[1]/div[2]/section/div[2]/div[6]/text()').extract_first()
		reviews.append(str(bad_reviews).encode('utf-8'))

		url = response.url
		#print(url)

		[x.encode('utf-8') for x in cuisine_array]

		restaurant_data['name'] = name
		restaurant_data['cuisine'] = cuisine_array
		restaurant_data['price_range'] = price_range
		restaurant_data['address'] = address
		restaurant_data['rating'] = rating
		restaurant_data['reviews'] = reviews
		restaurant_data['district'] = district
		restaurant_data['url'] = url

	 	with open('openrice_data.json', 'a') as outfile:
			if os.path.getsize('openrice_data.json') == 0:
				outfile.write("[")
			else:
				outfile.seek(-1,os.SEEK_END)
		 		outfile.truncate()
				outfile.write(",")
			json.dump(restaurant_data, outfile, indent=4)
			outfile.write("]")

		try:
		    os.remove('temp.json')
		except OSError:
		    pass
