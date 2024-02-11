import json
import scrapy

from jobs_project.items import DynamicItem
import os

class Jobpider(scrapy.Spider):
    name = 'job_spider'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        json_files = ['s01.json', 's02.json']
        cwd = os.getcwd()
        for file in json_files:
            yield scrapy.Request(
                url=f'file://{cwd}/{file}', 
                callback=self.parse_page,
            )

    def parse_page(self, response):
        data = json.loads(response.text)
        for job in data["jobs"]:
            # create fields dynamically
            dynamic_item = DynamicItem(job)
            for key in job.keys():
                dynamic_item[key] = job[key]
                yield {"item": dynamic_item, "type":type(dynamic_item)}