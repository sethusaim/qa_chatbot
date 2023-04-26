#!bin/bash

cd hfcrawl

scrapy crawl huggingface

cd ..

python ingest.py