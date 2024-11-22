import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import requests
from io import BytesIO

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

def image_has_good_resolution(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        if width >= 1280 and height >= 720:
            return True
    return False

def get_car_image_url(driver, car_make, car_model):
    """
    Recherche et récupère l'URL de l'image d'une voiture sur Google Images.
    
    Args:
        driver (webdriver.Chrome): Le driver Selenium.
        car_make (str): La marque de la voiture.
        car_model (str): Le modèle de la voiture.
    
    Returns:
        str: URL de l'image de la voiture si trouvée, sinon None.
    """
    search_url = "https://www.google.com/imghp"
    driver.get(search_url)

    try:
        # Chargement de la page
        time.sleep(2)

        # Récupération de la barre de recherche Google image
        search_box = driver.find_element(By.ID, "APjFqb")

        # Suppression de tous les éléments qui empêche de cliquer sur la barre de recherche
        try:
            overlay = driver.find_element(By.CSS_SELECTOR, "ul.dbXO9")
            driver.execute_script("arguments[0].style.display = 'none';", overlay)
        except Exception as e:
            print("Aucun overlay à supprimer")

        try:
            blocking_div = driver.find_element(By.CLASS_NAME, "yS1nld")
            driver.execute_script("arguments[0].style.display = 'none';", blocking_div)
        except Exception as e:
            print("Aucun div bloquante trouvé")

        try:
            blocking_div = driver.find_element(By.CLASS_NAME, "AG96lb")
            driver.execute_script("arguments[0].style.display = 'none';", blocking_div)
        except Exception as e:
            print("Aucun div bloquante trouvé")

        try:
            blocking_div = driver.find_element(By.CLASS_NAME, "I90TVb")
            driver.execute_script("arguments[0].style.display = 'none';", blocking_div)
        except Exception as e:
            print("Aucun div bloquante trouvé")

        try:
            blocking_div = driver.find_element(By.CLASS_NAME, "IczZ4b")
            driver.execute_script("arguments[0].style.display = 'none';", blocking_div)
        except Exception as e:
            print("Aucun div bloquante trouvé")

        try:
            blocking_div = driver.find_element(By.CLASS_NAME, "QS5gu")
            driver.execute_script("arguments[0].style.display = 'none';", blocking_div)
        except Exception as e:
            print("Aucun div bloquante trouvé")

        try:
            blocking_div = driver.find_element(By.CLASS_NAME, "GzLjMd")
            driver.execute_script("arguments[0].style.display = 'none';", blocking_div)
        except Exception as e:
            print("Aucun div bloquante trouvé")

        try:
            blocking_div = driver.find_element(By.CLASS_NAME, "jw8mI")
            driver.execute_script("arguments[0].style.display = 'none';", blocking_div)
        except Exception as e:
            print("Aucun div bloquant trouvé")

        try:
            blocking_div = driver.find_element(By.CLASS_NAME, "vUd4jb")
            driver.execute_script("arguments[0].style.display = 'none';", blocking_div)
        except Exception as e:
            print("Aucun div bloquante trouvé")

        # Insertion du nom de la voiture dans la barre de recherche
        search_box.click()
        search_box.send_keys(car_model + " " + car_make)
        search_box.send_keys(Keys.RETURN)

        # Chargement des images
        time.sleep(1)

        # Récupération des sites qui contiennent des images de la voiture
        elements_a = driver.find_elements(By.XPATH, f'//a[contains(@href, "{car_make.lower()}")]')
        for a in elements_a:
            try:
                a_href = a.get_attribute('href')
            except Exception as e:
                a_href = None
            if a_href and "google" not in a_href.lower():

                    driver.get(a_href)

                    images = driver.find_elements(By.TAG_NAME, 'img')
                    for img in images:
                        try:
                            image_url = img.get_attribute('src')
                            image_alt = img.get_attribute('alt')
                        except Exception as e:
                            image_url = None
                            image_alt = None
                        
                        if image_url and image_alt:
                            if car_make.lower() in image_alt.lower() or car_model.lower() in image_alt.lower():
                                if image_has_good_resolution(image_url):
                                    return image_url
                        
                            
        print("URL d'image non disponible.")
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'image pour {car_make} {car_model}: {e}")
        return None
    
def update_json_cars_data(json_file):
    """
    Met à jour le fichier JSON contenant la base de données des voitures avec les URLs des images.
    
    Args:
        json_file (str): Le chemin du fichier JSON contenant les données des voitures.
    """
    with open(json_file, "r") as f:
        cars = json.load(f)

    driver = configure_driver()

    size_cars = len(cars)
    i = 0
    j = 0
    for car in cars:
        car_name = car['make'] + " " + car['model']
        print("-"*25)
        print(f"Recherche d'image pour {car_name}...")

        if car['urlimage'] == None:
            image_url = get_car_image_url(driver, car['make'], car['model'])
            if image_url:
                car['urlimage'] = image_url
                i+=1
                print(f"Image trouvée pour {car_name} - {i}/{size_cars}")
                with open(json_file, "w") as f:
                    json.dump(cars, f, indent=4)
                print(f"Mise à jour de l'url pour {car_name}.\n")
            else:
                j+=1
                print(f"Aucune image trouvée pour {car_name} - {j}/{size_cars} image perdu\n")
        else:
            i+=1
            print(f"Image URL déjà existante")
    driver.quit()

    # Sauvegarder les mises à jour dans le fichier JSON
    with open(json_file, "w") as f:
        json.dump(cars, f, indent=4)
    print("Base de données mise à jour.")

if __name__ == "__main__":
    update_json_cars_data("vizucar-bdd.json")