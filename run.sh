#!/bin/bash
cd jobs_project
scrapy crawl job_spider

cd ..
python query.py

sleep infinity
