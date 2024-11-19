import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

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
        time.sleep(0.25)

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
        search_box.send_keys(car_model + car_make)
        search_box.send_keys(Keys.RETURN)

        # Chargement des images
        time.sleep(1)

        # Récupération de l'url de la première image
        image_elements = driver.find_elements(By.TAG_NAME, 'img')
        for img in image_elements:
            alt_text = img.get_attribute('alt')
            if alt_text and car_make.lower() in alt_text.lower():
                image_url = img.get_attribute('src')
                if image_url:
                    return image_url
                else:
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
        print(f"Recherche d'image pour {car_name}...")

        image_url = get_car_image_url(driver, car['make'], car['model'])
        if image_url:
            car['urlimage'] = image_url
            i+=1
            print(f"Image trouvée pour {car_name} - {i}/{size_cars}\n")
        else:
            j+=1
            print(f"Aucune image trouvée pour {car_name} - {j}/{size_cars} image perdu\n")

    driver.quit()

    # Sauvegarder les mises à jour dans le fichier JSON
    with open(json_file, "w") as f:
        json.dump(cars, f, indent=4)
    print("Base de données mise à jour.")

if __name__ == "__main__":
    update_json_cars_data("vehicles-model.json")