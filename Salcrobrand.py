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
def farmacia3(excel):
    #Leer medicamentos desde el archivo Excel
    df_medicamentos = excel
    #medicamentos=df_medicamentos['CLEANED_DENOMINACION'].dropna(axis=0)
    lista = df_medicamentos['Nombre'].tolist()  # Asegúrate de que la columna se llame "Medicamento"
    #print(medicamentos)
    extra=[""]+lista
    lista_medicamentos=extra
    #Funcion para quitar el laboratorio ya que en salcobrand no da resultados
    def normalizar(nombre):
        nombre = re.sub(r'\(.*?\)', '', nombre)
        # Eliminar espacios extra al inicio y al final
        nombre = nombre.strip()
        return nombre
        
    #Configuración
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://salcobrand.cl/?srsltid=AfmBOoqV5O5n3vMDh66P2ly8bXMo4r2XxrtH4mqBA7Akmg5PwZGr0kWW"
    driver.get(url)
    #Cargar pagina
    wait = WebDriverWait(driver, 10)
    # Diccionario para almacenar los resultados
    #########################################################################
    resultados =[]
    # Iterar por cada medicamento en la lista
    for medicamento in lista_medicamentos:
        try:
            #Localizar el buscador
            buscador = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/div/div[1]/div/div[1]/div/div[2]/div/div/form/input'))
            )
            buscador.clear()
            medicamento_sin_lab=normalizar(medicamento)
            #escribir medicamento
            buscador.send_keys(medicamento_sin_lab)
            #esperar
            time.sleep(3)
            nombres = driver.find_elements(By.CLASS_NAME, 'product-name')
            precios = driver.find_elements(By.CLASS_NAME, 'product-price normal-price')
            laboratorios=driver.find_elements(By.CLASS_NAME,'product-brand')
            if not precios:
                precios=driver.find_elements(By.CLASS_NAME, 'offer-price__strikethrough')
            if nombres and precios:  # Verificar que haya al menos un resultado
                resultados.append({
                    "medicamento_buscado": medicamento_sin_lab,
                    "nombre Salcobrand": nombres[0].text,  # Solo el primer resultado
                    "precio Salcobrand": precios[0].text,
                    "laboratorios":laboratorios[0].text
                })
            else:
                resultados.append({
                    "medicamento_buscado": medicamento_sin_lab,
                    "nombre Salcobrand":"No encontrado",
                    "precio Salcobrand":"-",
                    "laboratorios":"-"
                })

        except Exception as e:
            print(f"Error al buscar el medicamento '{medicamento}': {e}")
    driver.quit()
    # Convertir resultados a DataFrame
    df_resultados = pd.DataFrame(resultados)
    df_resultados=df_resultados.drop(df_resultados.index[0])
    return df_resultados