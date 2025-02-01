from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
#NADA QUE CANBIAR PORQUE EN EL NOMBRE VIENE LA INFO, OSEA NO HAY MUCHA INFORMACION DEL LABORATORIO :c
def farmacia5(excel):
    #Leer medicamentos desde el archivo Excel
    df_medicamentos = excel
    lista = df_medicamentos['Nombre'].tolist()
    extra=[""]+lista
    lista_medicamentos=extra
    #print(lista_medicamentos)
    # Configuración de Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    # Cambia la ruta al driver según tu sistema operativo
    service = Service(executable_path="chromedriver.exe")

    # Inicia el navegador
    driver = webdriver.Chrome(service=service, options=options)

    # Abrir la página de la farmacia
    url = "https://www.ecofarmacias.cl/shop/#30fc/classic-initial/"
    driver.get(url)
    #Cargar pagina
    wait = WebDriverWait(driver, 12)
    # Diccionario para almacenar los resultados
    #########################################################################
    resultados =[]
    # Iterar por cada medicamento en la lista
    for medicamento in lista_medicamentos:
        try:
            #Localizar el buscador
            buscador = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/div[2]/div/div/div[1]/div/nav/div/div/div[2]/input'))
            )
            buscador.clear()
            #escribir medicamento
            buscador.send_keys(medicamento)
            #esperar
            time.sleep(3)
            #nombres = driver.find_elements(By.CLASS_NAME, 'dfd-card-title')
            nombres = driver.find_elements(By.XPATH, '/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]')
            #precios = driver.find_elements(By.CLASS_NAME, 'dfd-card-price')
            precios = driver.find_elements(By.XPATH, '/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[3]/div[1]/span')
            if nombres and precios:  # Verificar que haya al menos un resultado
                resultados.append({
                    "medicamento_buscado": medicamento,
                    "nombre en EcoFarmacias": nombres[0].text,  # Solo el primer resultado
                    "precio en EcoFarmacias": precios[0].text   # Solo el primer resultado
                })
            else:
                resultados.append({
                    "medicamento_buscado": medicamento,
                    "nombre en EcoFarmacias":"No encontrado",
                    "precio en EcoFarmacias":"-"
                })

        except Exception as e:
            print(f"Error al buscar el medicamento '{medicamento}': {e}")
    driver.quit()
    # Convertir resultados a DataFrame
    df_resultados = pd.DataFrame(resultados)
    df_resultados=df_resultados.drop(df_resultados.index[0])
    return df_resultados