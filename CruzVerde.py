from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Leer medicamentos desde el archivo Excel
def Farmacia1(excel):
    df_medicamentos = excel
    lista = df_medicamentos['Nombre'].tolist()
    extra= [""] + lista
    lista_medicamentos = extra
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    # web
    url = "https://www.cruzverde.cl/"
    driver.get(url)

    # esperar
    wait = WebDriverWait(driver, 10)

    ########ACEPTAMOS LA UBICACION DADA######
    try:
        aceptar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-secondary')]/span[text()=' Aceptar ']"))
        )
        aceptar_button.click()
        print("Pop-up manejado exitosamente.")
    except Exception as e:
        print(f"No se pudo interactuar con el botón: {e}")
    ##############################################

    resultados = []
    # buscar medicamento por medicamento
    for medicamento in lista_medicamentos:
        try:
            #Localizar el buscador
            buscador = wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div/div/div[2]/form/input[2]"))
            )
            buscador.clear()
            buscador.send_keys(medicamento)

            #esperar
            time.sleep(3)
            nombres = driver.find_elements(By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div[2]/div/div/ml-search-suggestions/section[1]/div[3]/div[2]/div[1]/div[1]/ml-card-product/div/div/div[2]/div[2]/at-link/a/div/span")
            precios = driver.find_elements(By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div[2]/div/div/ml-search-suggestions/section[1]/div[3]/div[2]/div[1]/div[1]/ml-card-product/div/div/div[2]/div[2]/div[2]/ml-price-tag/div[1]/div[1]/span[1]")
            laboratorios=driver.find_elements(By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div[2]/div/div/ml-search-suggestions/section[1]/div[3]/div[2]/div[1]/div/ml-card-product/div/div/div[2]/div[2]/div[1]")
            if nombres and precios:  # Verificar que haya al menos un resultado
                resultados.append({
                    "medicamento_buscado": medicamento,
                    "nombre Cruz Verde": nombres[0].text,
                    "precio Cruz Verde": precios[0].text,
                    "laboratorio": laboratorios[0].text
                })
            else:
                resultados.append({
                    "medicamento_buscado": medicamento,
                    "nombre Cruz Verde":"No encontrado",
                    "precio Cruz Verde":"-",
                    "laboratorio":"-"
                })

        except Exception as e:
            print(f"Error al buscar el medicamento '{medicamento}': {e}")

    #cerrar el navegador
    driver.quit()
    df_resultados = pd.DataFrame(resultados)
    df_resultados=df_resultados.drop(df_resultados.index[0])
    #df_resultados.to_excel("RESULTADO Cruz Verde.xlsx", index=False)
    return df_resultados
    


