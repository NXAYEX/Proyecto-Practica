from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
def farmacia2(excel):
        df_medicamentos = excel
        #medicamentos=df_medicamentos['CLEANED_DENOMINACION'].dropna(axis=0)
        lista= df_medicamentos['Nombre'].tolist()  
        #print(medicamentos)
        extra= [""] + lista
        lista_medicamentos = extra

        #print(lista_medicamentos)

        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

        url = "https://www.farmaciasahumada.cl/"
        driver.get(url)

        #esperar
        wait = WebDriverWait(driver, 10)
        try:
            aceptar_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="consent-tracking"]/div/div/div[3]/div/button[2]'))
            )
            aceptar_button.click()
            print("Pop-up manejado exitosamente.")
        except Exception as e:
            print(f"No se pudo interactuar con el botón: {e}")

        #########################################################################
        resultados =[]
        # Buscamos medicamento por medicamento
        for medicamento in lista_medicamentos:
            try:
                #Localizar el buscador
                buscador = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="content-header"]/div/div[2]/div/div/form/input[1]'))
                )
                buscador.clear()
                #escribir medicamento
                buscador.send_keys(medicamento)
                buscador.send_keys(Keys.ENTER)
                #SI APARECE ALTIRO LA BUSQUEDA
                time.sleep(4)
                nombres = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[3]/a')
                precios = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[4]/span/span/span')
                laboratorios=driver.find_elements(By.XPATH,"/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[2]/span")
                if nombres and precios:
                    resultados.append({
                        "medicamento_buscado": medicamento,
                        "nombre en Ahumada": nombres[0].text,  #solo el primer resultado
                        "precio Ahumada": precios[0].text,
                        "laboratorios": laboratorios[0].text
                        })
                else:
                    quieres_decir = wait.until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/p[2]/a'))
                        )
                    quieres_decir.click()
                    time.sleep(4)
                    nombres = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[3]/a')
                    precios = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[4]/span/span/span')
                    laboratorios=driver.find_elements(By.XPATH,"/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[2]/span")
                    if nombres and precios:
                        resultados.append({
                        "medicamento_buscado": medicamento,
                        "nombre en Ahumada": nombres[0].text,  #solo el primer resultado
                        "precio Ahumada": precios[0].text,
                        "laboratorios": laboratorios[0].text
                        })
                    else:
                        resultados.append({
                        "medicamento_buscado": medicamento,
                        "nombre en Ahumada":"No encontrado",
                        "precio Ahumada":"-",
                        "laboratorios":"-"
                        })

            except Exception as e:
                print(f"Error al buscar el medicamento '{medicamento}': {e}")
        driver.quit()
        # Convertir resultados a DataFrame
        df_resultados = pd.DataFrame(resultados)
        df_resultados=df_resultados.drop(df_resultados.index[0])
        return df_resultados


