from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import re
#FUNCION PARA HACER EL NOMBRE SIN LABORATORIO, YA QUE DR.SIMI NO TIENE TAN BUEN BUSCADOR :V
def normalizar(nombre):
        nombre = re.sub(r'\(.*?\)', '', nombre)
        # Eliminar espacios extra al inicio y al final
        nombre = nombre.strip()
        return nombre
def farmacia4(excel):
    #Leer medicamentos desde el archivo Excel
    df_medicamentos = excel
    lista = df_medicamentos['Nombre'].tolist()
    #print(medicamentos)
    extra=[""]+lista
    lista_medicamentos=extra
    #print(lista_medicamentos)
    #configuracion del navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    #url
    url = "https://www.drsimi.cl/"
    driver.get(url)
    #Cargar pagina
    wait = WebDriverWait(driver, 10)
    #########################################################################
    resultados =[]
    # Iterar por cada medicamento en la lista
    for medicamento in lista_medicamentos:
        try:
            #Localizar el buscador
            buscador = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/section/div/div/div/div[2]/div/div/div[3]/div/div/div/div[1]/label/div/input '))
            )
            buscador.clear()
            medicamento_sinlab=normalizar(medicamento)
            buscador.send_keys(medicamento_sinlab)
            #DR.SIMI tiene un formato distinto, no se despliegan los resultados, así que hay que entrar a cada medicamento
            buscador.send_keys(Keys.ENTER)
            #esperar
            time.sleep(5)
            nombres = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/div/div/div/section/a/article/div[2]/h3/span')
            precios = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/div/div/div/section/a/article/div[3]/div/div[2]/span/span/span')
            #NO ES NECESARIO EL LABORATORIO PORQUE VIENE EN EL NOMBRE
            if nombres and precios:
                resultados.append({
                    "medicamento_buscado": medicamento_sinlab,
                    "nombre en Dr.Simi": nombres[0].text,
                    "precio en Dr.Simi": precios[0].text   
                })
            else:
                resultados.append({
                    "medicamento_buscado": medicamento_sinlab,
                    "nombre en Dr.Simi":"No encontrado",
                    "precio en Dr.Simi":"-"
                })

        except Exception as e:
            print(f"Error al buscar el medicamento '{medicamento}': {e}")
    driver.quit()
    # Convertir resultados a DataFrame
    df_resultados = pd.DataFrame(resultados)
    df_resultados=df_resultados.drop(df_resultados.index[0])
    return df_resultados
