#Como hay ciertos medicamentos de los que los nombres son extraños en estructura
#se me ocurrio realizar que el mismo usuario escriba el medicamento y así se busque este en las 9 farmacias,
#Devolviendo el nombre  con el que esta en esa farmacia y el precio respectivo.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

#configuracion
options=webdriver.ChromeOptions()
options.add_argument('--start-maximized')
service=Service(executable_path="chromedriver.exe")
#Pedir el medicamento:
medicamento_buscar= input("Ingrese Nombre del medicamento: ")
driver = webdriver.Chrome(service=service, options=options)
resultados = []
'''def buscar_en_cada_farmacia(url_farmacia,xpath_buscador,xpath_precios, farmacia):
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)'''
# web
url1="https://www.cruzverde.cl/"
driver.get(url1)

# esperar
wait = WebDriverWait(driver, 10)

########ACEPTAMOS LA UBICACION DADA######
try:
    aceptar_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-secondary')]/span[text()=' Aceptar ']"))
    )
    aceptar_button.click()
    print("Seguimos")
except Exception as e:
    print(f"No se sigue")
##############################################

time.sleep(3)
try:
        #Localizar el buscador
    buscador = wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div/div/div[2]/form/input[2]"))
    )
    buscador.clear()
    buscador.send_keys(medicamento_buscar)

    #esperar
    time.sleep(3)
    nombres = driver.find_elements(By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div[2]/div/div/ml-search-suggestions/section[1]/div[3]/div[2]/div[1]/div[1]/ml-card-product/div/div/div[2]/div[2]/at-link/a/div/span")
    precios = driver.find_elements(By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div[2]/div/div/ml-search-suggestions/section[1]/div[3]/div[2]/div[1]/div[1]/ml-card-product/div/div/div[2]/div[2]/div[2]/ml-price-tag/div[1]/div[1]/span[1]")

    if nombres and precios:
        resultados.append({
            "Farmacia": "Cruz Verde",
            "nombre": nombres[0].text,
            "precio": precios[0].text   
            })
    else:
        resultados.append({
            "Farmacia": "Cruz Verde",
            "nombre":"No encontrado",
            "precio":"-"
        })
except Exception as e:
    print("Problema")
#cerrar el navegador
driver.quit()
df_resultados=pd.DataFrame(resultados)
#print(df_resultados)

driver = webdriver.Chrome(service=service, options=options)
#########################################################################################################
url2 = "https://www.farmaciasahumada.cl/"
driver.get(url2)

#esperar
wait = WebDriverWait(driver, 10)
try:
    aceptar_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="consent-tracking"]/div/div/div[3]/div/button[2]'))
    )
    aceptar_button.click()
    print("Seguimos")
except Exception as e:
    print(f"No se pudo interactuar con el botón")
time.sleep(2)
try:
        #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content-header"]/div/div[2]/div/div/form/input[1]'))
        )
        #buscador.clear()
        #escribir medicamento
        buscador.send_keys(medicamento_buscar)
        #buscador.send_keys(Keys.ENTER)
        #esperar
        time.sleep(4)
        nombres = driver.find_elements(By.XPATH, '/html/body/div[1]/header/nav/div[1]/div/div[2]/div/div/form/div/div/ul/li[2]/ul/li[1]/a/span')
        precios = driver.find_elements(By.XPATH, '/html/body/div[1]/header/nav/div[1]/div/div[2]/div/div/form/div/div/ul/li[2]/ul/li[1]/div/div[1]/div/div/span/span/span')

        if nombres and precios:
            resultados.append({
                "Farmacia": "Farmacia Ahumada",
                "nombre": nombres[0].text,
                "precio": precios[0].text   
            })
        else:
            resultados.append({
                "Farmacia": "Farmacia Ahumada",
                "nombre":"No encontrado",
                "precio":"-"
            })

except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento_buscar}': {e}")
driver.quit()
df_resultados=pd.DataFrame(resultados)
#print(df_resultados)

driver = webdriver.Chrome(service=service, options=options)
#############################################################################################################################
url3 = "https://salcobrand.cl/?srsltid=AfmBOoqV5O5n3vMDh66P2ly8bXMo4r2XxrtH4mqBA7Akmg5PwZGr0kWW"
driver.get(url3)
#Cargar pagina
wait = WebDriverWait(driver, 10)
try:
        #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/div/div[1]/div/div[1]/div/div[2]/div/form/input'))
        )
        #buscador.clear()
        #escribir medicamento
        buscador.send_keys(medicamento_buscar)
        #buscador.send_keys(Keys.ENTER)
        #esperar
        time.sleep(3)
        nombres = driver.find_elements(By.XPATH, '/html/body/div[1]/header/div/div[1]/div/div[1]/div/div[2]/div/form/div/div[2]/div/ul/li[1]/a/div/span[3]')
        precios = driver.find_elements(By.XPATH, '/html/body/div[1]/header/div/div[1]/div/div[1]/div/div[2]/div/form/div/div[2]/div/ul/li[1]/a/div/div/div/span[2]')
        if not precios:
            precios=driver.find_elements(By.XPATH, '/html/body/div[1]/header/div/div[1]/div/div[1]/div/div[2]/div/form/div/div[2]/div/ul/li[1]/a/div/div/span')
        if nombres and precios:  # Verificar que haya al menos un resultado
            resultados.append({
                "Farmacia": "Farmacia Salcobrand",
                "nombre": nombres[0].text,  # Solo el primer resultado
                "precio": precios[0].text   # Solo el primer resultado
            })
        else:
            resultados.append({
                "Farmacia": "Farmacia Salcobrand",
                "nombre":"No encontrado",
                "precio":"-"
            })

except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento_buscar}': {e}")
driver.quit()
df_resultados=pd.DataFrame(resultados)
#print(df_resultados)

driver = webdriver.Chrome(service=service, options=options)
####################################################################################################################################################################
url4 = "https://www.drsimi.cl/"
driver.get(url4)
#Cargar pagina
wait = WebDriverWait(driver, 10)

try:
        #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/section/div/div/div/div[2]/div/div/div[3]/div/div/div/div[1]/label/div/input '))
        )
        #buscador.clear()
        buscador.send_keys(medicamento_buscar)
        #DR.SIMI tiene un formato distinto, no se despliegan los resultados, así que hay que entrar a cada medicamento
        buscador.send_keys(Keys.ENTER)
        #esperar
        time.sleep(5)
        nombres = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/div/div/div/section/a/article/div[2]/h3/span')
        precios = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/div/div/div/section/a/article/div[3]/div/div[2]/span/span/span')
        if nombres and precios:
            resultados.append({
                "Farmacia": "Farmacia Dr.Simi",
                "nombre": nombres[0].text,
                "precio": precios[0].text   
            })
        else:
            resultados.append({
                "Farmacia": "Farmacia Dr.Simi",
                "nombre":"No encontrado",
                "precio":"-"
            })

except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento_buscar}': {e}")
driver.quit()
df_resultados=pd.DataFrame(resultados)
#print(df_resultados)

driver = webdriver.Chrome(service=service, options=options)
#################################### 5 ###################################################33
url5 = "https://www.ecofarmacias.cl/shop/#30fc/classic-initial/"
driver.get(url5)
#Cargar pagina
wait = WebDriverWait(driver, 12)

try:
        #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/div[2]/div/div/div[1]/div/nav/div/div/div[2]/input'))
        )
        buscador.clear()
        #escribir medicamento
        buscador.send_keys(medicamento_buscar)
        #esperar
        time.sleep(3)
        #nombres = driver.find_elements(By.CLASS_NAME, 'dfd-card-title')
        nombres = driver.find_elements(By.XPATH, '/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]')
        #precios = driver.find_elements(By.CLASS_NAME, 'dfd-card-price')
        precios = driver.find_elements(By.XPATH, '/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[3]/div[1]/span')
        if nombres and precios:  # Verificar que haya al menos un resultado
            resultados.append({
                "Farmacia":"EcoFarmacias",
                "nombre": nombres[0].text,  # Solo el primer resultado
                "precio": precios[0].text   # Solo el primer resultado
            })
        else:
            resultados.append({
                "Farmacia": "EcoFarmacias",
                "nombre":"No encontrado",
                "precio":"-"
            })

except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento_buscar}': {e}")
driver.quit()
'''driver = webdriver.Chrome(service=service, options=options)
############################### 6 ###############################################
url6="https://occafarmacia.cl/tienda/"
driver.get(url6)
#Cargar pagina
wait = WebDriverWait(driver, 12)
#########################################################################
try:
    aceptar_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section[3]/div/div/div/section/div/div[2]/div/div/div/div/a'))
    )
    aceptar_button.click()
    print("Manejado exitosamente.")
except Exception as e:
    print(f"No se pudo interactuar con el botón")
try:
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section[3]/div/div/div/section/div/div[2]/div/div/div/div/form/div/input[1]'))
        )
        buscador.clear()
        #escribir medicamento
        buscador.send_keys(medicamento_buscar)
        time.sleep(5)
        #nombre = driver.find_elements(By.CLASS_NAME, 'odd')
        nombre =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[1]/span')
        precio =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[2]/span/ins/span/bdi')
        if not precio:
            precio =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[2]/span/del/span/bdi')
        if nombre and precio:  # Verificar que haya al menos un resultado
            resultados.append({
                "Farmacia": "OccaFarmacia",
                "nombre": nombre[0].text,
                "precio": precio[0].text
            })
        else:
            resultados.append({
                "Farmacia": "OccaFarmacia",
                "nombre":"No encontrado",
                "precio":"-"
            })
except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento_buscar}': {e}")
# Cerrar el navegador
driver.quit()'''
############### RESULTADOS FINALES #############################################
df_resultados = pd.DataFrame(resultados)
print(df_resultados)

    
