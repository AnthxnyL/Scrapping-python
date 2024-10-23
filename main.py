from bs4 import BeautifulSoup
import requests 
import csv
import urllib.request
import os, shutil

def scrap_data_product(url_product): 
    url = url_product
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    with open('book.csv', 'a', newline='') as fichier_csv: 
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
        if fichier_csv.tell() == 0:
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
        download_img(book_url, book_title, book_category)



def scrap_category(url_cate): 
    url_category = url_cate
    response = requests.get(url_category)
    soup_category = BeautifulSoup(response.content, 'html.parser')

    products_url = soup_category.select('div.image_container > a')
    for product_url in products_url : 
        url_product = product_url.get('href').replace('../../..', 'https://books.toscrape.com/catalogue')
        scrap_data_product(url_product)
    next_button = soup_category.find(class_='next')

    try:
        if None not in next_button:
            url = next_button.find('a').get('href')
            url_pagination = f'https://books.toscrape.com/catalogue/category/books/fiction_10/{url}'
            scrap_category(url_pagination)
    except: 
        return ['n/a', 'n/a']


def download_img(img_url, img_name, folder_name) :
    path = create_folder_category(folder_name)
    img = img_name.replace(' ', '-')
    file_name = f"{path}/{img.lower()}.jpg"
    urllib.request.urlretrieve(img_url, file_name)

def create_folder_category(folder_name) : 
    parent_dir = "./images"
    directory =  folder_name.replace('\n', "").replace(' ',"")
    path = os.path.join(parent_dir, directory)
    if not os.path.exists(path) : 
        os.mkdir(path)
    return path

def create_directory(): 
    if os.path.isdir("images"):
        shutil.rmtree("images")
    os.mkdir("images")


url_cate = "https://books.toscrape.com/catalogue/category/books/fiction_10/"

create_directory()
scrap_category(url_cate)


