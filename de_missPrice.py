from cred2 import url,consumer_key,consumer_secret
from woocommerce import API
import random
import time
import string

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
    
            if product['regular_price'] == '13.50':
                missing_price_items.append({'id': product['id'], 'product_name': product['name']})
        # breakpoint()

        current_page += 1


print(missing_price_items)