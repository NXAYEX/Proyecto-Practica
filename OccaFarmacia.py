from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
#ESTA FARMACIA EN REALIDAD TIENE MUY POCOS PRODUCTOS, 
def farmacia6(excel):
    df_medicamentos =excel
    #medicamentos=df_medicamentos['CLEANED_DENOMINACION'].dropna(axis=0) #son 655
    lista = df_medicamentos['Nombre'].tolist()  # Asegúrate de que la columna se llame "Medicamento"
    extra=[""]+lista
    lista_medicamentos=extra
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service=Service(executable_path="chromedriver.exe")
    driver=webdriver.Chrome(service=service, options=options)
    #Abrir la web de la farmacia
    url="https://occafarmacia.cl/tienda/"
    driver.get(url)
    #Cargar pagina
    wait = WebDriverWait(driver, 10)
    #########################################################################
    try:
        aceptar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section[3]/div/div/div/section/div/div[2]/div/div/div/div/a'))
        )
        aceptar_button.click()
        print("Manejado exitosamente.")
    except Exception as e:
        print(f"No se pudo interactuar con el botón")
    resultados =[]
    for medicamento in lista_medicamentos:
        try:
            buscador = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section[3]/div/div/div/section/div/div[2]/div/div/div/div/form/div/input[1]'))
            )
            buscador.clear()
            #escribir medicamento
            buscador.send_keys(medicamento)
            time.sleep(3)
            #nombre = driver.find_elements(By.CLASS_NAME, 'odd')
            nombre =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[1]/span')
            precio =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[2]/span/ins/span/bdi')
            if not precio:
                precio =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[2]/span/del/span/bdi')
            if nombre and precio:  # Verificar que haya al menos un resultado
                resultados.append({
                    "medicamento_buscado": medicamento,
                    "nombre en OccaFarmacia": nombre[0].text,  # Solo el primer resultado
                    "precio en OccaFarmacia": precio[0].text   # Solo el primer resultado
                })
            else:
                resultados.append({
                    "medicamento_buscado": medicamento,
                    "nombre en OccaFarmacia":"No encontrado",
                    "precio en OccaFarmacia":"-"
                })
        except Exception as e:
            print(f"Error al buscar el medicamento '{medicamento}': {e}")
    # Cerrar el navegador
    driver.quit()
    # Convertir los resultados a un DataFrame
    df_resultados = pd.DataFrame(resultados)
    df_resultados=df_resultados.drop(df_resultados.index[0])
    return df_resultados
