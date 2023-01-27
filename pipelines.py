# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.files import FilesPipeline

# To get your settings from (settings.py):
from scrapy.utils.project import get_project_settings

import zipfile
import os

class SigPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        url = item['file_urls']
        file_names = item['file_names']
        yield scrapy.Request(url=url, meta={'file_names': file_names})

    def file_path(self, request, response=None, info=None, *, item=None):
        file_names = request.meta['file_names']
        return file_names

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        #print("file paths: ", file_paths)
        settings = get_project_settings()
        output_path = settings.get('FILES_STORE') + '\\' + file_paths[0]
        #print("output path: ", output_path)
        with zipfile.ZipFile(output_path, 'r') as zip_ref:
            zip_ref.extractall(output_path[:output_path.rfind('.')])
        os.remove(output_path)
        return item
