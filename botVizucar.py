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
        time.sleep(2)

        # Récupération de la barre de recherche Google image
        search_box = driver.find_element(By.ID, "APjFqb")

        if not search_box.is_displayed():
            print("La barre de recherche n'est pas visible.")
        else:
            print("La barre de recherche est visible.")

        # Suppression de tous les éléments qui empêche de cliquer sur la barre de recherche
        try:
            overlays = driver.find_elements(By.CSS_SELECTOR, "ul.dbXO9")
            for overlay in overlays:
                driver.execute_script("arguments[0].style.display = 'none';", overlay)
            print("Overlays supprimés.")
        except Exception as e:
            print(f"Aucun overlay à supprimer : {e}")

        try:
            blocking_divs = driver.find_elements(By.CLASS_NAME, "yS1nld")
            for div in blocking_divs:
                driver.execute_script("arguments[0].style.display = 'none';", div)
            print("Divs bloquantes supprimés.")
        except Exception as e:
            print(f"Aucun div bloquante trouvé : {e}")

        try:
            blocking_divs = driver.find_elements(By.CLASS_NAME, "AG96lb")
            for div in blocking_divs:
                driver.execute_script("arguments[0].style.display = 'none';", div)
            print("Divs bloquantes supprimés.")
        except Exception as e:
            print(f"Aucun div bloquante trouvé : {e}")

        try:
            blocking_divs = driver.find_elements(By.CLASS_NAME, "I90TVb")
            for div in blocking_divs:
                driver.execute_script("arguments[0].style.display = 'none';", div)
            print("Divs bloquantes supprimés.")
        except Exception as e:
            print(f"Aucun div bloquante trouvé : {e}")

        try:
            blocking_divs = driver.find_elements(By.CLASS_NAME, "IczZ4b")
            for div in blocking_divs:
                driver.execute_script("arguments[0].style.display = 'none';", div)
            print("Divs bloquantes supprimés.")
        except Exception as e:
            print(f"Aucun div bloquante trouvé : {e}")

        try:
            blocking_divs = driver.find_elements(By.CLASS_NAME, "QS5gu")
            for div in blocking_divs:
                driver.execute_script("arguments[0].style.display = 'none';", div)
            print("Divs bloquantes supprimés.")
        except Exception as e:
            print(f"Aucun div bloquante trouvé : {e}")

        try:
            blocking_divs = driver.find_elements(By.CLASS_NAME, "GzLjMd")
            for div in blocking_divs:
                driver.execute_script("arguments[0].style.display = 'none';", div)
            print("Divs bloquantes supprimés.")
        except Exception as e:
            print(f"Aucun div bloquante trouvé : {e}")

        try:
            blocking_divs = driver.find_elements(By.CLASS_NAME, "jw8mI")
            for div in blocking_divs:
                driver.execute_script("arguments[0].style.display = 'none';", div)
            print("Divs bloquantes supprimés.")
        except Exception as e:
            print(f"Aucun div bloquant trouvé : {e}")

        try:
            blocking_divs = driver.find_elements(By.CLASS_NAME, "vUd4jb")
            for div in blocking_divs:
                driver.execute_script("arguments[0].style.display = 'none';", div)
            print("Divs bloquantes supprimés.")
        except Exception as e:
            print(f"Aucun div bloquante trouvé : {e}")

        # Insertion du nom de la voiture dans la barre de recherche
        search_box.click()
        search_box.send_keys(car_model + car_make)
        search_box.send_keys(Keys.RETURN)

        # Chargement des images
        time.sleep(2) 

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

        print(f"Aucune image trouvée correspondant au nom de la voiture {car_make} {car_model}.")
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'image pour {car_make} {car_model}: {e}")
        return None