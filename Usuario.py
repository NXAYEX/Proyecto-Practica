import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from io import BytesIO
from Nombres import convertir
from CruzVerde import Farmacia1
from Ahumada import farmacia2
from Salcrobrand import farmacia3
from DrSimi import farmacia4
from Ecofarmacias import farmacia5
from WebBarnechea import farmaciaBar
from WebIquique import farmaciaIquique
from OccaFarmacia import farmacia6
#configuracion

def cruzVerde(medicamento):
    options=webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service=Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    resultados = []
    url1="https://www.cruzverde.cl/"
    driver.get(url1)
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
    time.sleep(3)
    try:
            #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div/div/div[2]/form/input[2]"))
        )
        buscador.clear()
        buscador.send_keys(medicamento)

        #esperar
        time.sleep(4)
        nombres = driver.find_elements(By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div[2]/div/div/ml-search-suggestions/section[1]/div[3]/div[2]/div[1]/div[1]/ml-card-product/div/div/div[2]/div[2]/at-link/a/div/span")
        precios = driver.find_elements(By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div[2]/div/div/ml-search-suggestions/section[1]/div[3]/div[2]/div[1]/div[1]/ml-card-product/div/div/div[2]/div[2]/div[2]/ml-price-tag/div[1]/div[1]/span[1]")
        laboratorios=driver.find_elements(By.XPATH, "/html/body/app-root/app-page/div[1]/div/header/or-header/or-navbar/nav/div/div[2]/div/div/ml-search-suggestions/section[1]/div[3]/div[2]/div[1]/div/ml-card-product/div/div/div[2]/div[2]/div[1]")
        if nombres and precios:
            resultados.append({
            "Farmacia": "Cruz Verde",
            "nombre": nombres[0].text,
            "precio": precios[0].text,
            "laboratorio": laboratorios[0].text
            })
        else:
            resultados.append({
            "Farmacia": "Cruz Verde",
            "nombre":"No encontrado",
            "precio":"-",
            "laboratorio":"-"
        })
    except Exception as e:
        print("Problema")
    driver.quit()
    df_resultados=pd.DataFrame(resultados)
    return df_resultados
def Ahumada(medicamento):
    options=webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service=Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    resultados = []
    url2 = "https://www.farmaciasahumada.cl/"
    driver.get(url2)

    #esperar
    wait = WebDriverWait(driver, 10)
    try:
        aceptar_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="consent-tracking"]/div/div/div[3]/div/button[2]')))
        aceptar_button.click()
        print("Seguimos")
    except Exception as e:
        print(f"No se pudo interactuar con el botón")
    time.sleep(2)
    try:
        #Localizar el buscador
        buscador = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-header"]/div/div[2]/div/div/form/input[1]')))
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
                "Farmacia": "Farmacia Ahumada",
                "nombre": nombres[0].text,  #solo el primer resultado
                "precio": precios[0].text,
                "laboratorio": laboratorios[0].text
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
                "Farmacia": "Farmacia Ahumada",
                "nombre": nombres[0].text,  #solo el primer resultado
                "precio": precios[0].text,
                "laboratorio": laboratorios[0].text
                })
            else:
                resultados.append({
                "Farmacia": "Farmacia Ahumada",
                "nombre":"No encontrado",
                "precio":"-",
                "laboratorio":"-"
                })
    except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento}': {e}")
    driver.quit()
    df_resultados=pd.DataFrame(resultados)
    return df_resultados
def Salcobrand(medicamento):
    options=webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service=Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    resultados = []
    url3 = "https://salcobrand.cl/?srsltid=AfmBOoqV5O5n3vMDh66P2ly8bXMo4r2XxrtH4mqBA7Akmg5PwZGr0kWW"
    driver.get(url3)
    #Cargar pagina
    wait = WebDriverWait(driver, 10)
    try:
        #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/div/div[1]/div/div[1]/div/div[2]/div/div/form/input'))
        )
        buscador.clear()
        #escribir medicamento
        buscador.send_keys(medicamento)
        #esperar
        time.sleep(3)
        nombres = driver.find_elements(By.CLASS_NAME, 'product-name')
        precios = driver.find_elements(By.CLASS_NAME, 'product-price normal-price')
        laboratorios=driver.find_elements(By.CLASS_NAME,'product-brand')
        if not precios:
            precios=driver.find_elements(By.CLASS_NAME, 'offer-price__strikethrough')
        if nombres and precios:  # Verificar que haya al menos un resultado
            resultados.append({
                "Farmacia": "Salcobrand",
                "nombre": nombres[0].text,  # Solo el primer resultado
                "precio": precios[0].text,
                "laboratorio":laboratorios[0].text
            })
        else:
            resultados.append({
                "Farmacia": "Salcobrand",
                "nombre":"No encontrado",
                "precio":"-",
                "laboratorio":"-"
            })

    except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento}': {e}")
    driver.quit()
    df_resultados=pd.DataFrame(resultados)
    return df_resultados
def dr_simi(medicamento):
    options=webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service=Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    url4 = "https://www.drsimi.cl/"
    driver.get(url4)
    #Cargar pagina
    wait = WebDriverWait(driver, 10)
    resultados = []
    try:
        #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/section/div/div/div/div[2]/div/div/div[3]/div/div/div/div[1]/label/div/input '))
        )
        buscador.clear()
        buscador.send_keys(medicamento)
        #DR.SIMI tiene un formato distinto, no se despliegan los resultados, así que hay que entrar a cada medicamento
        buscador.send_keys(Keys.ENTER)
        #esperar
        time.sleep(5)
        nombres = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/div/div/div/section/a/article/div[2]/h3/span')
        precios = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[3]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/div/div/div/section/a/article/div[3]/div/div[2]/span/span/span')
        #NO ES NECESARIO EL LABORATORIO PORQUE VIENE EN EL NOMBRE
        if nombres and precios:
            resultados.append({
                "Farmacia":"Dr.Simi",
                "nombre": nombres[0].text,
                "precio": precios[0].text,
                "laboratorio":"en el nombre"   
            })
        else:
            resultados.append({
                "Farmacia":"Dr.Simi",
                "nombre":"No encontrado",
                "precio":"-",
                "laboratorio":"-"
            })

    except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento}': {e}")
    driver.quit()
    df_resultados=pd.DataFrame(resultados)
    return df_resultados
def Ecofarmacia(medicamento):
    st.info("EcoFarmacia no tiene la marca bien reconocida, por lo cual es medio dificil, se recomienda solo poner formato 'laboratorio'+'medicamento' o simplemente 'medicamento', de esa manera es más probable obtener una busqueda correcta, y la marca(laboratorio) suele aparecer en el nombre")
    options=webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service=Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    url5 = "https://www.ecofarmacias.cl/shop/#30fc/classic-initial/"
    driver.get(url5)
    #Cargar pagina
    wait = WebDriverWait(driver, 8)
    resultados=[]
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
                "Farmacia": "EcoFarmacias",
                "nombre": nombres[0].text,
                "precio": precios[0].text   
            })
        else:
            resultados.append({
                "Farmacia": "EcoFarmacias",
                "nombre":"No encontrado",
                "precio":"-"
            })

    except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento}': {e}")
    driver.quit()
    df_resultados=pd.DataFrame(resultados)
    return df_resultados
def occaFarmacia(medicamento):
    st.info("OccaFarmacia no tiene muchos medicamentos, en realidad tiene muy pocos, y su buscador es extraño...y tarda en buscar")
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service=Service(executable_path="chromedriver.exe")
    driver=webdriver.Chrome(service=service, options=options)
    #Abrir la web de la farmacia
    url6="https://occafarmacia.cl/tienda/"
    driver.get(url6)
    resultados =[]
    #Cargar pagina
    wait = WebDriverWait(driver, 10)
    #### boton
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
        buscador.send_keys(medicamento)
        time.sleep(5)
        #nombre = driver.find_elements(By.CLASS_NAME, 'odd')
        nombre =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[1]/span')
        precio =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[2]/span/ins/span/bdi')
        if not precio:
            precio =driver.find_elements(By.XPATH, '/html/body/div[11]/a/div/div[2]/span/del/span/bdi')
        if nombre and precio:  # Verificar que haya al menos un resultado
            resultados.append({
                "Farmacia": "Occafarmacia",
                "nombre": nombre[0].text,  # Solo el primer resultado
                "precio": precio[0].text   # Solo el primer resultado
            })
        else:
            resultados.append({
                "Farmacia": "Occafarmacia",
                "nombre":"No encontrado",
                "precio":"-"
            })
    except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento}': {e}")
    # Cerrar el navegador
    driver.quit()
    df_resultados = pd.DataFrame(resultados)
    return df_resultados
def Iquique(medicamento):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    url = "http://unisag.cormudesi.cl/unisag/servicios/farmacia_comunal/consultor/view/consulta_medicamento.php"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    #########################################################################
    resultados =[]
    try:
        #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[2]/div[2]/div/div/div[2]/label/input'))
        )
        buscador.clear()
    #escribir medicamento
        buscador.send_keys(medicamento)
        time.sleep(3)
        #nombre = driver.find_elements(By.CLASS_NAME, 'odd')
        nombre = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/table/tbody/tr[1]/td[1]')
        precio = driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/table/tbody/tr[1]/td[8]')
        comprimidos= driver.find_elements(By.XPATH, '/html/body/div/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/table/tbody/tr[1]/td[6]')
        if nombre and precio:  # Verificar que haya al menos un resultado
            resultados.append({
                "Farmacia":"Farmacia comunal Iquique",
                "nombre": nombre[0].text+" ("+comprimidos[0].text+")",
                "precio": precio[0].text  
            })
        else:
            resultados.append({
                "Farmacia":"Farmacia comunal Iquique",
                "nombre":"No encontrado",
                "precio":"-"
            })
    except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento}': {e}")
    # Cerrar el navegador
    driver.quit()
    df_resultados = pd.DataFrame(resultados)
    return df_resultados

def Barnechea(medicamento):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    url="https://farmaciacomunalonline.cl/Consultor?farmacia=lobarnechea"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    resultados =[]
    try:
        #Localizar el buscador
        buscador = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-kioskboard-input'))
        )
        buscador.clear()
    #escribir medicamento
        buscador.send_keys(medicamento)
        buscar_boton = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[3]/button[1]'))
                )
        buscar_boton.click()
        time.sleep(4)
        #nombre = driver.find_elements(By.CLASS_NAME, 'odd')
        nombre = driver.find_elements(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr/td[3]')
        precio = driver.find_elements(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr/td[10]')
        laboratorios=driver.find_elements(By.XPATH,'/html/body/div/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr/td[11]')
        if nombre and precio:  # Verificar que haya al menos un resultado
            resultados.append({
                "Farmacia":"Farmacia comunal Barnechea",
                "nombre": nombre[0].text,
                "precio": precio[0].text,
                "laboratorio": laboratorios[0].text
            })
        else:
            resultados.append({
                "Farmacia":"Farmacia comunal Barnechea",
                "nombre":"No encontrado",
                "precio":"-",
                "laboratorio":"-"
            })
    except Exception as e:
        print(f"Error al buscar el medicamento '{medicamento}': {e}")
    driver.quit()
    df_resultados = pd.DataFrame(resultados)
    return df_resultados

st.set_page_config(page_title='APP medicamentos',page_icon="smile", layout="wide")
def main():
    st.title("Buscador automático de medicamentos")
    menu=["Busqueda individual","Busqueda por excel"]
    eleccion= st.sidebar.selectbox("Menú", menu)
    if eleccion=="Busqueda individual":
        st.text(f"Recuerda escribir el nombre del medicamento correctamente")
        opciones = st.multiselect(
            'Selecciona las farmacias en las que quieres buscar',
            ['Cruz Verde','Ahumada','Salcobrand','Dr.Simi','EcoFarmacia','OccaFarmacia','Comunal Barnechea','Comunal Iquique']
        )
        medicamento=st.text_input("Ingresa el nombre del medicamento que buscas")
        if medicamento!="":
            dataframes=[]
            if 'Cruz Verde' in opciones:
                df_cruzverde=cruzVerde(medicamento)
                dataframes.append(df_cruzverde)
            if 'Ahumada' in opciones:
                df_ahumada=Ahumada(medicamento)
                dataframes.append(df_ahumada)
            if 'Salcobrand' in opciones:    
                df_salcobrand=Salcobrand(medicamento)
                dataframes.append(df_salcobrand)
            if 'Dr.Simi' in opciones:
                df_drsimi=dr_simi(medicamento)
                dataframes.append(df_drsimi)
            if 'EcoFarmacia' in opciones:
                df_ecofarmacias=Ecofarmacia(medicamento)
                dataframes.append(df_ecofarmacias)
            if 'OccaFaramacia' in opciones:
                df_occafarmacia=occaFarmacia(medicamento)
                dataframes.append(df_occafarmacia)
            if 'Comunal Barnechea' in opciones:
                df_barnechea=Barnechea(medicamento)
                dataframes.append(df_barnechea)
            if 'Comunal Iquique' in opciones:
                df_iquique=Iquique(medicamento)
                dataframes.append(df_iquique)
            if dataframes:
                final=pd.concat(dataframes,axis=0)
                #final=pd.concat([df_cruzverde,df_ahumada,df_salcobrand,df_drsimi,df_ecofarmacias,df_occafarmacia,df_barnechea,df_iquique], axis=0)
                #st.dataframe(buscar)
                st.dataframe(final)
            else:
                ("No se seleccionaron Farmacias")
    if eleccion=="Busqueda por excel":
        st.subheader("Buscar varios medicamentos automaticamente")
        st.info("Debes subir un archivo excel (.xlsx) en el que tenga las columnas 'Descripción Producto', 'Laboratorio' y 'Valor Lote' para que todo funcione correctamente.")
        archivo=st.file_uploader("Subir archivo", type=["xlsx"])
        if archivo is not None:
            detalles_archivo={
                "nombre_Archivo":archivo.name,
                "tipo_archivo":archivo.type,
                "tamaño":archivo.size
            }
            #st.write(detalles_archivo)
            if detalles_archivo['tipo_archivo']=="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df=archivo
            else:
                df=pd.DataFrame()
            st.info("Para facilidad de busqueda, se convierte el excel dado a: ")
            df_excel=convertir(df)
            st.dataframe(df_excel)
        farmacia=st.selectbox(
            'Selecciona las farmacia en la que quieres buscar los medicamentos',
            ['Cruz Verde','Ahumada','Salcobrand','Dr.Simi','EcoFarmacias','Comunal Barnechea','Comunal Iquique','OccaFarmacia']
        )
        if st.button("Hacer busqueda"):
            if farmacia =='Cruz Verde':
                resultado = Farmacia1(df_excel)
                output= BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Sheet1')
                st.dataframe(resultado)
                #boton descarga:
                st.download_button(
                    label="Descargar como Excel",
                    data=output.getvalue(),
                    file_name='Resultado-CruzVerde.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            if farmacia == 'Ahumada':
                resultado = farmacia2(df_excel)
                output= BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Sheet1')
                st.dataframe(resultado)
                #boton descarga:
                st.download_button(
                    label="Descargar como Excel",
                    data=output.getvalue(),
                    file_name='Resultado-Ahumada.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            if farmacia == 'Salcobrand':
                resultado = farmacia3(df_excel)
                output= BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Sheet1')
                st.dataframe(resultado)
                #boton descarga:
                st.download_button(
                    label="Descargar como Excel",
                    data=output.getvalue(),
                    file_name='Resultado-Salcobrand.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            if farmacia == 'Dr.Simi':
                resultado = farmacia4(df_excel)
                output= BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Sheet1')
                st.dataframe(resultado)
                #boton descarga:
                st.download_button(
                    label="Descargar como Excel",
                    data=output.getvalue(),
                    file_name='Resultado-Dr-Simi.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            if farmacia == 'EcoFarmacias':
                resultado = farmacia5(df_excel)
                output= BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Sheet1')
                st.dataframe(resultado)
                #boton descarga:
                st.download_button(
                    label="Descargar como Excel",
                    data=output.getvalue(),
                    file_name='Resultado-EcoFarmacias.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            if farmacia == 'Comunal Barnechea':
                resultado = farmaciaBar(df_excel)
                output= BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Sheet1')
                st.dataframe(resultado)
                #boton descarga:
                st.download_button(
                    label="Descargar como Excel",
                    data=output.getvalue(),
                    file_name='Resultado-ComunalBarnechea.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            if farmacia == 'Comunal Iquique':
                resultado = farmaciaIquique(df_excel)
                output= BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Sheet1')
                st.dataframe(resultado)
                #boton descarga:
                st.download_button(
                    label="Descargar como Excel",
                    data=output.getvalue(),
                    file_name='Resultado-Comunal-Iquique.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            if farmacia == 'OccaFarmacia':
                st.warning("Esta farmacia no tiene mucha variedad, no tienen casi nada... además de que su buscador es deficiente, por lo que se recomienda mejor buscar INDIVIDUALMENTE en esta farmacia")
                resultado = farmacia6(df_excel)
                output= BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    resultado.to_excel(writer, index=False, sheet_name='Sheet1')
                st.dataframe(resultado)
                #boton descarga:
                st.download_button(
                    label="Descargar como Excel",
                    data=output.getvalue(),
                    file_name='Resultado-OccaFarmacia.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )


if __name__=='__main__':
    main()