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

def get_total_car(json_file):
    with open(json_file, "r") as f:
        cars = json.load(f)
    return len(cars)

def get_total_car_with_image(json_file):
    cars_with_image = 0
    with open(json_file, "r") as f:
        cars = json.load(f)

    for car in cars:
        if car['image_url']:
            cars_with_image+=1
    return cars_with_image

def get_last_car_with_image(json_file):
    last_car = 0
    with open(json_file, "r") as f:
        cars = json.load(f)

    for i,car in enumerate(cars):
        if car['image_url']:
            last_car = i
    return last_car + 1

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
    search_url = "https://duckduckgo.com/?q=" + car_make + car_model + str(car_year) + "&kl=us-en&ia=web&ia=images&iax=images"
    driver.get(search_url)

    try:
        # Chargement des images
        time.sleep(1)

        for result in driver.find_elements(By.CSS_SELECTOR, '.js-images-link')[:20]:
            imageURL = result.get_attribute('data-id')
            if imageURL and (car_make.lower() in imageURL or car_model.lower() in imageURL or str(car_year) in imageURL):
                if image_has_good_resolution(imageURL):
                    return imageURL
        return None

    except Exception as e:
        print(f"Erreur lors de la récupération de l'image pour {car_make} {car_model}: {e}")
        return None

def search_images_cars(json_file, start, end=0):
    """
    Met à jour le fichier JSON contenant la base de données des voitures avec les URLs des images.
    
    Args:
        json_file (str): Le chemin du fichier JSON contenant les données des voitures.
    """
    with open(json_file, "r") as f:
        cars = json.load(f)

    driver = configure_driver()

    size_cars = len(cars)
    if end == 0:
        end = size_cars

    start = start - 1
    end = end - 1

    lose = 0
    find = 0
    while start <= end:
        car_name = f"{cars[start]['make']} {cars[start]['model']} {cars[start]['year']}"
        print("\n+" + ("-" * 58) + "+")
        print(f"Recherche d'image pour : {car_name} ({start+1}/{size_cars})".center(60))

        if not cars[start]['image_url']:
            print(f"[INFO] Recherche en cours...")
            image_url = get_car_image_url(driver, cars[start]['make'], cars[start]['model'], cars[start]['year'])
            
            if image_url:
                image_size = get_image_size(image_url)
                cars[start]['image_url'] = image_url
                cars[start]['image_size'] = image_size
                find+=1
                print(Fore.GREEN + f"[SUCCESS] Image trouvée pour {car_name}, ({find}/{size_cars}) trouvées")
                print(Fore.WHITE + f"[INFO] Dimensions : {image_size}")
                with open(json_file, "w") as f:
                    json.dump(cars, f, indent=4)
                print(Fore.GREEN + f"[UPDATE] Image mise à jour avec succès.")
            else:
                lose+=1
                print(Fore.RED + f"[WARNING] Aucune image trouvée pour {car_name}, ({lose}/{size_cars}) perdus.")
        else:
            find+=1
            print(Fore.YELLOW + f"[SKIP] Image déjà existante pour {car_name}.")
        print("+" + ("-" * 58) + "+\n")
        start+=1

    print("=" * 60)
    print(Style.BRIGHT + " Mise à jour terminée ! ".center(60))
    print("=" * 60)

    driver.quit()
    with open(json_file, "w") as f:
        json.dump(cars, f, indent=4)

if __name__ == "__main__":
    size_cars = get_total_car("vizucar-bdd.json")
    nb_cars_with_image = get_total_car_with_image("vizucar-bdd.json")
    last_car_with_image = get_last_car_with_image("vizucar-bdd.json")

    botVizucar = pyfiglet.figlet_format("botVizucar",font="slant")
    print(Fore.RED + Style.BRIGHT + botVizucar.center(60))
    print(Fore.RED + Style.BRIGHT + "Total cars : " + Fore.WHITE + str(size_cars))
    print(Fore.RED + Style.BRIGHT + "Total cars with image : " + Fore.WHITE + str(nb_cars_with_image))
    print(Fore.RED + Style.BRIGHT + "The number of the last car with image : " + Fore.WHITE + str(last_car_with_image) + '\n')

    while True:
        try:
            start = int(input(f"Give the car number, between 1 and {size_cars}, you want to start with : "))
            if 1 <= start <= size_cars: 
                break 
            else:
                print(Fore.RED + f"Invalide! The number must be between 1 and {size_cars}.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

    response = input(f"\nAre you sure you want to start from car {start} ?[Y/n]")
    while response != "Y" and response != "n":
        response = input("Are you sure you want to start botVizucar ?[Y/n]")
    if response == "Y":
        search_images_cars("vizucar-bdd.json", start)
    else:
        print("exit")