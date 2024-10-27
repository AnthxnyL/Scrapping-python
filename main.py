from bs4 import BeautifulSoup
import requests 
import csv
import urllib.request
import os, shutil
import matplotlib.pyplot as plt
import re

# Scrappe les données d'un produit spécifique à partir de son URL
def scrap_data_product(url_product): 
    # Récupère l'URL du produit
    url = url_product
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extrait le nom de la catégorie du produit à partir de la barre de navigation
    category_name = soup.select('ul.breadcrumb > li')[2].text.replace('\n', "").replace(' ',"").lower()

    # Ouvre (ou crée) un fichier CSV pour la catégorie spécifique en mode ajout
    with open(f'./csv/book_{category_name}.csv', 'a', newline='') as fichier_csv: 
        # Définition des noms de colonnes pour le fichier CSV
        column_name = [
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

        # Écrit l'en-tête du fichier CSV si le fichier est vide
        if fichier_csv.tell() == 0:
            writer.writeheader()

        # Extrait les données du produit à partir de la table HTML
        table_data = soup.select('tr > td')
        book_upc = table_data[0].text
        book_price_exclude = table_data[2].text
        book_price_include = table_data[3].text
        book_available = table_data[5].text.split()[2].replace('(', '')
        
        # Extrait d'autres informations sur le produit
        book_title = soup.find('h1').text
        book_img = soup.find('img').get('src').replace('../..', 'https://books.toscrape.com')
        book_category = soup.select('ul.breadcrumb > li')[2].text
        book_description = soup.find_all('p')[3].text
        book_url = url 
        book_rating = soup.find(class_='star-rating').get('class')[1]

        # Crée un dictionnaire avec les données du produit
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
        
        # Écrit les données du produit dans le fichier CSV
        writer.writerow(dict)
        
        # Télécharge l'image du produit
        download_img(book_url, book_title, book_category)


# Scrappe les données de tous les produits dans une catégorie spécifique
def scrap_category(url_cate): 
    # Initialise l'URL de la catégorie
    url_category = url_cate
    
    # Envoie une requête HTTP GET à l'URL de la catégorie
    response = requests.get(url_category)
    
    # Parse le contenu HTML de la réponse avec BeautifulSoup
    soup_category = BeautifulSoup(response.content, 'html.parser')
    
    # Sélectionne tous les liens des produits dans la catégorie
    products_url = soup_category.select('div.image_container > a')
    
    # Pour chaque produit trouvé, construit l'URL complète et scrape les données du produit
    for product_url in products_url: 
        url_product = product_url.get('href').replace('../../..', 'https://books.toscrape.com/catalogue')
        scrap_data_product(url_product)
    
    # Trouve le bouton "next" pour la pagination
    next_button = soup_category.find(class_='next')

    try:
        # Si un bouton "next" est trouvé, construit l'URL de la page suivante et appelle récursivement la fonction
        if next_button is not None:
            url = next_button.find('a').get('href')
            # Utilise une expression régulière pour supprimer la partie de l'URL qui change
            url_pagination = re.sub(r'(index\.html|page-\d+\.html)$', '', url_category) + url
            scrap_category(url_pagination)
    except Exception as e: 
        # En cas d'exception, affiche un message d'erreur et retourne une liste contenant 'n/a'
        print(f"An error occurred: {e}")
        return ['n/a', 'n/a']
    

# Permet de télécharger une image à partir d'une URL et de l'enregistrer dans un fichier spécifié
def download_img(img_url, img_name, folder_name):
    # Crée le dossier pour la catégorie si nécessaire et obtient le chemin du dossier
    path = create_folder_category(folder_name)
    
    # Nettoie le nom de l'image en remplaçant les caractères spéciaux par des tirets ou en les supprimant
    img = img_name.replace(' ', '-').replace('/', '-').replace(':', '').replace('?', '').replace('!', '').replace(';', '').replace(',', '').replace('.', '').replace('\'', '').replace('\"', '')
    
    # Construit le nom complet du fichier avec le chemin et le nom de l'image en minuscules
    file_name = f"{path}/{img.lower()}.jpg"
    
    # Télécharge l'image depuis l'URL et l'enregistre dans le fichier spécifié
    urllib.request.urlretrieve(img_url, file_name)

# Crée un dossier pour une catégorie spécifique si nécessaire et retourne le chemin du dossier
def create_folder_category(folder_name):
    # Définit le répertoire parent où les images seront stockées
    parent_dir = "./images"
    
    # Nettoie le nom du dossier en supprimant les sauts de ligne et les espaces
    directory = folder_name.replace('\n', "").replace(' ', "")
    
    # Construit le chemin complet du dossier
    path = os.path.join(parent_dir, directory)
    
    # Crée le dossier s'il n'existe pas déjà
    if not os.path.exists(path):
        os.mkdir(path)
    
    # Retourne le chemin du dossier
    return path

# Crée les répertoires nécessaires pour stocker les fichiers CSV et les images
def create_directory():
    # Vérifie si le dossier "images" existe et le supprime s'il existe
    if os.path.isdir("images"):
        shutil.rmtree("images")
    
    # Crée un nouveau dossier "images"
    os.mkdir("images")

    # Vérifie si le dossier "csv" existe et le supprime s'il existe
    if os.path.isdir("csv"):
        shutil.rmtree("csv")
    
    # Crée un nouveau dossier "csv"
    os.mkdir("csv")

# PERMET DE SCRAPPER LE SITE WEB
def scrap_website(): 
    # Initialise l'URL du site web
    url_website = "https://books.toscrape.com/"
    
    # Envoie une requête HTTP GET à l'URL du site web
    response = requests.get(url_website)
    
    # Parse le contenu HTML de la réponse avec BeautifulSoup
    soup_website = BeautifulSoup(response.content, 'html.parser')

    # Sélectionne tous les liens des catégories dans le menu de navigation
    category_links = soup_website.select('ul.nav-list > li > ul > li > a')
    
    # Pour chaque lien de catégorie trouvé, construit l'URL complète et scrape la catégorie
    for link in category_links: 
        link_category = url_website + link.get('href')
        scrap_category(link_category)

# Crée les répertoires nécessaires pour stocker les fichiers CSV et les images
create_directory()

# Lance le processus de scraping du site web
scrap_website()


# Calcule le nombre de livres dans une catégorie spécifique
def counter_book(category_name):
    # Initialise le compteur de livres à 0
    sum = 0
    
    # Ouvre le fichier CSV correspondant à la catégorie en mode lecture
    with open(f'./csv/book_{category_name}.csv', 'r', newline='') as fichier_csv: 
        # Crée un lecteur CSV pour lire le fichier
        reader = csv.DictReader(fichier_csv)
        
        # Compte le nombre de lignes dans le fichier CSV (chaque ligne représente un livre)
        sum = len(list(reader))
        
        # Retourne le nombre de livres dans la catégorie
        return sum


# Calcule le prix moyen des livres dans une catégorie spécifique
def calculate_average_price(category_name):
    # Initialise une liste pour stocker les prix
    prices = []
    
    # Nom de la colonne contenant les prix dans le fichier CSV
    price_column_name = "price_excluding_tax"
    
    # Ouvre le fichier CSV correspondant à la catégorie en mode lecture
    with open(f'./csv/book_{category_name}.csv', 'r', newline='', encoding='utf-8') as csvfile:
        # Crée un lecteur CSV pour lire le fichier
        reader = csv.DictReader(csvfile)
        
        # Parcourt chaque ligne du fichier CSV
        for row in reader:
            # Extrait le prix de la colonne spécifiée et supprime le symbole de la livre sterling
            price_str = row[price_column_name].replace('£', '').strip()
            try:
                # Convertit le prix en flottant et l'ajoute à la liste des prix
                price = float(price_str)
                prices.append(price)
            except ValueError:
                # Affiche un message d'erreur si la conversion échoue
                print(f"Invalid price value: {price_str}")
    
    # Calcule la moyenne des prix si la liste des prix n'est pas vide
    if prices:
        average_price = sum(prices) / len(prices)
        # Retourne la moyenne arrondie à deux décimales
        return round(average_price, 2)
    else:
        # Retourne None si la liste des prix est vide
        return None

# Crée un diagramme en barres horizontal avec les prix moyens et les noms de catégories renommés
def diagramme_barre(average_prices_all, list_category): 
    # Crée une nouvelle figure et un axe pour le graphique
    fig, ax = plt.subplots()
    
    # Crée un diagramme en barres horizontal avec les prix moyens et les catégories
    ax.barh(list_category, average_prices_all)
    
    # Définit l'étiquette de l'axe des x
    ax.set_xlabel('Prix moyen')
    
    # Définit l'étiquette de l'axe des y
    ax.set_ylabel('Catégorie')
    
    # Définit le titre du graphique
    ax.set_title('Prix moyen par catégorie')
    
    # Affiche le graphique
    plt.show()

# Crée un graphique en camembert avec les sommes totales et les noms de catégories renommés
def pie_chart(sum, labels):
    # Crée une nouvelle figure et un axe pour le graphique en camembert
    fig1, ax1 = plt.subplots()
    
    # Crée un graphique en camembert avec les données fournies
    ax1.pie(sum, labels=labels, autopct='%1.1f%%', startangle=90)
    
    # Assure que le graphique est dessiné en cercle (égalise les axes)
    ax1.axis('equal')
    
    # Affiche le graphique
    plt.show()



# PERMET DE RECUPERER LES CATEGORIES
def get_categories(url):
    # Envoie une requête HTTP GET à l'URL fournie
    response = requests.get(url)
    
    # Parse le contenu HTML de la réponse avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialise une liste pour stocker les noms des catégories
    categories = []
    
    # Sélectionne tous les éléments <a> qui contiennent les liens vers les catégories
    category_elements = soup.select('ul.nav-list > li > ul > li > a')
    
    # Pour chaque élément de catégorie trouvé, extrait et nettoie le nom de la catégorie
    for element in category_elements:
        category_name = element.text.strip()
        categories.append(category_name)
    
    # Retourne la liste des noms de catégories
    return categories



# POUR LANCER LE PROGRAMME

# URL de la page contenant les catégories
url = "https://books.toscrape.com/"

# Récupère la liste des catégories à partir de l'URL
list_category = get_categories(url)

# Initialise les listes pour stocker les sommes totales, les prix moyens et les noms de catégories renommés
total_sum = []
average_prices_all = []
rename_category = []

# Parcourt chaque catégorie dans la liste des catégories
for category in list_category:
    # Remplace les espaces par des chaînes vides et convertit le nom de la catégorie en minuscules
    category = category.replace(' ', '').lower()
    
    # Ajoute le nom de la catégorie renommé à la liste rename_category
    rename_category.append(category)
    
    # Compte le nombre de livres dans la catégorie et ajoute le total à la liste total_sum
    total_sum.append(counter_book(category))
    
    # Calcule le prix moyen des livres dans la catégorie
    average_price = calculate_average_price(category)
    
    # Si le prix moyen est calculé, l'ajoute à la liste average_prices_all, sinon ajoute 0
    if average_price is not None:
        average_prices_all.append(average_price)
    else:
        average_prices_all.append(0)

# Crée un graphique en camembert avec les sommes totales et les noms de catégories renommés
pie_chart(total_sum, rename_category)

# Crée un diagramme en barres horizontal avec les prix moyens et les noms de catégories renommés
diagramme_barre(average_prices_all, rename_category)

