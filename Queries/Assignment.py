import csv
import requests
from bs4 import BeautifulSoup

def get_product_data(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_name = soup.select_one('#productTitle').get_text(strip=True)
    product_price = soup.select_one('.priceBlockBuyingPriceString').get_text(strip=True)
    rating = soup.select_one('.a-icon-star span').get_text(strip=True)
    num_reviews = soup.select_one('#acrCustomerReviewText').get_text(strip=True)

    product_data = {
        'Product URL': product_url,
        'Product Name': product_name,
        'Product Price': product_price,
        'Rating': rating,
        'Number of Reviews': num_reviews,
    }

    product_description = soup.select_one('#productDescription').get_text(strip=True)
    asin = soup.select_one('.prodDetAttrValue').get_text(strip=True)
    manufacturer = soup.select_one('#bylineInfo').get_text(strip=True)

    product_data.update({
        'Description': product_description,
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer,
    })

    return product_data

def scrape_product_listings():
    base_url = 'https://www.amazon.in/s?k=bags&ref=sr_pg_1'
    query_params = {
        'k': 'bags',
        'crid': '2M096C61O4MLT',
        'qid': '1653308124',
        'sprefix': 'ba,aps,283',
        'ref': 'sr_pg_',
    }
    num_pages = 20

    all_product_data = []

    for page in range(1, num_pages + 1):
        query_params['ref'] = f'sr_pg_{page}'
        response = requests.get(base_url, params=query_params)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_links = soup.select('.s-result-item a.a-link-normal.a-text-normal')

        for link in product_links:
            product_url = link['href']
            product_data = get_product_data(product_url)
            all_product_data.append(product_data)
            print(f'Scraped: {product_data["Product Name"]}')

    return all_product_data

def export_to_csv(product_data, filename):
    fieldnames = [
        'Product URL',
        'Product Name',
        'Product Price',
        'Rating',
        'Number of Reviews',
        'Description',
        'ASIN',
        'Product Description',
        'Manufacturer',
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(product_data)

if __name__ == '__main__':
    product_data = scrape_product_listings()
    export_to_csv(product_data, 'amazon_products.csv')

