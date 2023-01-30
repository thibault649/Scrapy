import scrapy
from sig.items import ZipfilesItem

# To get your settings from (settings.py):
from scrapy.utils.project import get_project_settings

import os
from datetime import datetime

class IndexSpider(scrapy.Spider):
    name = "quotes"

    custom_settings = {
        'DOWNLOAD_TIMEOUT': '3600',
    }

    def start_requests(self):
        start_url = 'https://cadastre.data.gouv.fr/datasets/cadastre-etalab'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        #title = response.css('h1.nova-legacy-e-text::text').get()
        #title = response.css('li.nova-legacy-e-list__item::text').get()
        date = response.css('h5.jsx-184752799::text').getall()[1]
        #print('dates: ', date)
        months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
        months_number = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

        date_day = date.split(' ')[0]
        date_month = date.split(' ')[1]
        date_year = date.split(' ')[2]
        if date_day.isdigit():
            if int(date_day) < 10:
                date_day_converted = '0' + str(date_day)
            else:
                date_day_converted = str(date_day)
        else:
            date_day_converted = '01'
        date_month_converted = months_number[months.index(date_month)]
        new_date = datetime.strptime(date_day_converted + '-' + date_month_converted + '-' + str(date_year), '%d-%m-%Y')
        #date = date_day_converted + ' ' + date.split(' ')[1] + ' ' + date.split(' ')[2]
        #print("test_date : ", datetime.strptime(date, '%d %b %Y'))
        print("Last vintage: ", new_date.strftime("%d-%m-%Y"))
        
        """

        settings = get_project_settings()
        output_path = settings.get('FILES_STORE')
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        count = 0
        for entry in os.scandir(output_path):
            #print(entry.name)
            if '01' in entry.name:
                m_time = os.path.getmtime(entry.path)
                file_date = datetime.fromtimestamp(m_time)
                #print("file date: ", file_date.strftime("%d-%m-%Y"))
                break
            else:
                count += 1
        #print(count)
        if count == len(os.listdir(output_path)):
            href = [href for href in response.css('a::attr(href)').getall() if 'cadastre' in href and 'shp' in href and 'departement' in href][0]
            #print("link founded: ", href)
            yield scrapy.Request(url=href, callback=self.parse_next_page)
        else:
            if file_date < new_date:
                href = [href for href in response.css('a::attr(href)').getall() if 'cadastre' in href and 'shp' in href and 'departement' in href][0]
                #print("link founded: ", href)
                yield scrapy.Request(url=href, callback=self.parse_next_page)
            else:
                print('latest version already downloaded')

    def parse_next_page(self, response):
        list_href = response.css('a::attr(href)').getall()[1:]
        #print("list href: ", list_href)
        for href2 in list_href:
            if href2 == '01/':
                yield scrapy.Request(url=response.request.url+href2, callback=self.parse_download_page)

    def parse_download_page(self, response):
        file_url_list = response.css('a::attr(href)').getall()[1:]
        for file_name in file_url_list:
            file_url = response.urljoin(file_name)
            #print(file_url)
            #print(file_name)
            item = ZipfilesItem()
            item['file_urls'] = file_url
            item['file_names'] = file_name
            print('file: ' + file_name[:file_name.rfind('.')])
            yield item
            
     """
