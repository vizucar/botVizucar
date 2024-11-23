import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import requests
from io import BytesIO
import pyfiglet
from colorama import Fore, Style, init
init(autoreset=True)

def configure_driver():
    """
    Configure le driver Chrome avec les options nécessaires.
    
    Returns:
        webdriver.Chrome: Instance du driver Selenium configurée.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_image_size(image_url):
    response = requests.get(image_url, stream=True, timeout=10)
    if response.status_code != 200:
        print(f"Erreur de téléchargement : {response.status_code}")
        return False
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    return f"{width}x{height}"


def image_has_good_resolution(image_url):
    # Télécharger l'image depuis l'URL
    response = requests.get(image_url, stream=True, timeout=10)
    if response.status_code != 200:
        print(f"Erreur de téléchargement : {response.status_code}")
        return False
    img = Image.open(BytesIO(response.content))
        
    # Vérifier les dimensions de l'image
    width, height = img.size
    return width >= 1280 and height >= 720

def get_car_image_url(driver, car_make, car_model, car_year):
    """
    Recherche et récupère l'URL de l'image d'une voiture sur Google Images.
    
    Args:
        driver (webdriver.Chrome): Le driver Selenium.
        car_make (str): La marque de la voiture.
        car_model (str): Le modèle de la voiture.
        car_year (int): L'année de la voiture.
    
    Returns:
        str: URL de l'image de la voiture si trouvée, sinon None.
    """
    search_url = "https://duckduckgo.com/?q=" + car_make + car_model + str(car_year) + "&kl=us-en&ia=web"
    driver.get(search_url)

    try:
        # Chargement des images
        time.sleep(1)

        ba = driver.find_element(By.XPATH, "//a[text()='Images']")
        ba.click()

        for result in driver.find_elements(By.CSS_SELECTOR, '.js-images-link')[0:0+10]:
            imageURL = result.get_attribute('data-id')
            if imageURL and car_make.lower() in imageURL and car_model.lower() in imageURL and str(car_year) in imageURL:
                if image_has_good_resolution(imageURL):
                    return imageURL
        return None

    except Exception as e:
        print(f"Erreur lors de la récupération de l'image pour {car_make} {car_model}: {e}")
        return None

def search_images_cars(json_file):
    """
    Met à jour le fichier JSON contenant la base de données des voitures avec les URLs des images.
    
    Args:
        json_file (str): Le chemin du fichier JSON contenant les données des voitures.
    """
    with open(json_file, "r") as f:
        cars = json.load(f)

    driver = configure_driver()

    size_cars = len(cars)
    botVizucar = pyfiglet.figlet_format("botVizucar",font="slant")

    print(Fore.RED + Style.BRIGHT + botVizucar.center(60))

    lose = 0
    find = 0
    for i, car in enumerate(cars):
        car_name = f"{car['make']} {car['model']} {car['year']}"
        print("\n+" + ("-" * 58) + "+")
        print(f"Recherche d'image pour : {car_name}".center(60))

        if not car['image_url']:
            print(f"[INFO] Recherche en cours ({i + 1}/{size_cars})...")
            image_url = get_car_image_url(driver, car['make'], car['model'], car['year'])
            image_size = get_image_size(image_url)
            
            if image_url:
                car['image_url'] = image_url
                car['image_size'] = image_size
                find+=1
                print(Fore.GREEN + f"[SUCCESS] Image trouvée pour {car_name} ({find}/{size_cars})")
                print(Fore.WHITE + f"[INFO] Dimensions : {image_size}")
                with open(json_file, "w") as f:
                    json.dump(cars, f, indent=4)
                print(Fore.GREEN + f"[UPDATE] Image mise à jour avec succès.\n")
            else:
                lose+=1
                print(Fore.RED + f"[WARNING] Aucune image trouvée pour {car_name} ({lose}/{size_cars}).\n")
        else:
            find+=1
            print(Fore.YELLOW + f"[SKIP] Image déjà existante pour {car_name}.")
        print("+" + ("-" * 58) + "+\n")

    print("=" * 60)
    print(Style.BRIGHT + " Mise à jour terminée ! ".center(60))
    print("=" * 60)

    driver.quit()
    with open(json_file, "w") as f:
        json.dump(cars, f, indent=4)

if __name__ == "__main__":
    search_images_cars("vizucar-bdd.json")