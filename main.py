from bs4 import BeautifulSoup
import requests 
import csv

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

with open('book.csv', 'w', newline='') as fichier_csv: 
    column_name=[
        "product_page_url",
        "universal_product_code",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ]
    writer = csv.DictWriter(fichier_csv, fieldnames=column_name)
    writer.writeheader()

    table_data = soup.select('tr > td')

    book_upc = table_data[0].text
    book_price_exclude = table_data[2].text
    book_price_include = table_data[3].text
    book_available = table_data[5].text.split()[2].replace('(', '')
    book_title = soup.find('h1').text
    book_img = soup.find('img').get('src').replace('../..', 'https://books.toscrape.com')
    book_category = soup.select('ul.breadcrumb > li')[2].text
    book_description = soup.find_all('p')[3].text
    book_url = url 
    book_rating = soup.find(class_='star-rating').get('class')[1]
    

    dict = {
        "product_page_url": book_url,
        "universal_product_code": book_upc,
        "title": book_title,
        "price_including_tax": book_price_include,
        "price_excluding_tax": book_price_exclude,
        "number_available": book_available,
        "product_description": book_description,
        "category": book_category,
        "review_rating": book_rating,
        "image_url": book_img
    }
    writer.writerow(dict)
    
