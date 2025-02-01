from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re
#ESTA FARMACIA NO TIENE INFORMACION DEL LABORATORIO O MARCA...
def normalizar(nombre):
    nombre = re.sub(r'\(.*?\)', '', nombre)
    # Eliminar espacios extra al inicio y al final
    nombre = nombre.strip()
    return nombre
def farmaciaIquique(excel):
    #Leer medicamentos desde el archivo Excel
    df_medicamentos = excel
    #medicamentos=df_medicamentos['CLEANED_DENOMINACION'].dropna(axis=0)
    lista = df_medicamentos['Nombre'].tolist()  # Asegúrate de que la columna se llame "Medicamento"
    #print(medicamentos)
    extra=[""]+lista
    lista_medicamentos=extra
    #print(lista_medicamentos)
    ##Configuramos el navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    #Cambia la ruta al driver según tu sistema operativo
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    #Abrir la web de la farmacia
    url = "http://unisag.cormudesi.cl/unisag/servicios/farmacia_comunal/consultor/view/consulta_medicamento.php"
    driver.get(url)
    #Cargar pagina
    wait = WebDriverWait(driver, 10)
    #########################################################################
    resultados =[]
    for medicamento in lista_medicamentos:
        try:
            #Localizar el buscador
            buscador = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[2]/div[2]/div/div/div[2]/label/input'))
            )
            buscador.clear()
        #escribir medicamento
            medicamento_sinlab=normalizar(medicamento)
            buscador.send_keys(medicamento_sinlab)
            time.sleep(3)
            #nombre = driver.find_elements(By.CLASS_NAME, 'odd')
            nombre = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]')
            precio = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/table/tbody/tr[1]/td[8]')
        
            if nombre and precio:  # Verificar que haya al menos un resultado
                resultados.append({
                    "medicamento_buscado": medicamento_sinlab,
                    "nombre en Farmacia comunal Iquique": nombre[0].text,  # Solo el primer resultado
                    "precio en Farmacia comunal Iquique": precio[0].text   # Solo el primer resultado
                })
            else:
                resultados.append({
                    "medicamento_buscado": medicamento_sinlab,
                    "nombre en Farmacia comunal Iquique":"No encontrado",
                    "precio en Farmacia comunal Iquique":"-"
                })
        except Exception as e:
            print(f"Error al buscar el medicamento '{medicamento}': {e}")
    # Cerrar el navegador
    driver.quit()
    # Convertir los resultados a un DataFrame
    df_resultados = pd.DataFrame(resultados)
    df_resultados=df_resultados.drop(df_resultados.index[0])
    return df_resultados
