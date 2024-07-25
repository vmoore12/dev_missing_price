from cred2 import url,consumer_key,consumer_secret
from woocommerce import API
import random
import time
import string
import csv

woo_api = API(
    url=url,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    wp_api=True,
    version='wc/v3'

)

per_page = 100
current_page = 1
count = 0
skipped_items =[]
missing_price_items = []
while True:
        payload = {
            "per_page": per_page,
            "page": current_page, #Note: this show the specific page you want to see now
        }

        all_products = woo_api.get('products', params=payload).json()
        if not all_products:
                break 
        
        for product in all_products:
            if product['type'] != 'simple':
                s_name = product['name'] +',' + product['type']
                skipped_items.append(s_name)
                continue
    
            if product['regular_price'] <= '1.00':
                missing_price_items.append({'id': product['id'], 'product_name': product['name'], 'product_price': product['price']})
        # breakpoint()

        current_page += 1


fieldnames = ['id', 'name', 'price']

with open('missing_price.csv', 'w', newline='') as f:
      writer = csv.DictWriter(f, fieldnames=fieldnames)

      writer.writeheader()
      for item in missing_price_items:
         data  = {
              'id': item['id'],
              'name': item['product_name'],
              'price': item['product_price'] 
         }
         writer.writerow(data)

