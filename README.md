# Book Scraper

Ce projet est un scraper de livres qui extrait des informations sur les livres à partir du site [Books to Scrape](https://books.toscrape.com/). Le programme génère des graphiques pour visualiser les données extraites.

## Prérequis

Assurez-vous d'avoir Python 3.x installé sur votre machine. Vous pouvez télécharger Python à partir de [python.org](https://www.python.org/downloads/).

## Installation

1. Clonez ce dépôt sur votre machine locale :

    ```sh
    git clone https://github.com/votre-utilisateur/book-scraper.git
    cd book-scraper
    ```

2. Créez un environnement virtuel (optionnel mais recommandé) :

    ```sh
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances nécessaires :

    ```sh
    pip install -r requirements.txt
    ```

## Dépendances

Le fichier `requirements.txt` contient toutes les dépendances nécessaires pour exécuter le programme. Voici les principales bibliothèques utilisées :

- `requests`
- `beautifulsoup4`
- `matplotlib`

## Utilisation

1. Assurez-vous que vous êtes dans le répertoire du projet et que votre environnement virtuel est activé (si vous en utilisez un).

2. Exécutez le programme :

    ```sh
    python main.py
    ```

3. Le programme va scraper les données des livres à partir du site [Books to Scrape](https://books.toscrape.com/), générer des fichiers CSV pour chaque catégorie, et afficher des graphiques pour visualiser les données.

## Structure du Projet

- `main.py`: Le script principal qui contient le code de scraping et de génération des graphiques.
- `requirements.txt`: Le fichier contenant les dépendances nécessaires.
- `csv/`: Le répertoire où les fichiers CSV seront stockés.
- `images/`: Le répertoire où les images des livres seront téléchargées.