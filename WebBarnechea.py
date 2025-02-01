from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re
#Obtencion de nombres y cantidades de medicamentos
#grupo 1: nombre + cantidad:
'''
df = pd.read_excel("Intermediación 2025_Farmacia Rodoviario.xlsx")
#regex
def clean_denominacion(denominacion):
    match = re.match(r'((^[A-Z]+.[a-zA-Z]*)\s*(\d*|\d*,\d*)\s*(MG|UI|ML))', denominacion)
    #{match.group(1).strip()} {match.group(2).strip()}= BILASTINA 20 MG BILASTINA
    if match:
        return f"{match.group(1).strip()}"

#aplicamos la funcion a la columna que queremos
df['CLEANED_DENOMINACION'] = df['DENOMINACION'].apply(clean_denominacion)
#guardamos en un dataframe que ocuparemos más adelante
cleaned_df = df[['DENOMINACION', 'CLEANED_DENOMINACION']]
#los que no hacen match(osea tienen un nombre con una estructura más compleja de texto)
no_match_df = df[df['CLEANED_DENOMINACION'].isna()]
m = len(no_match_df)
# Exporta o muestra los resultados
#print(f"Número de filas sin coincidencia: {m}")
#print(no_match_df[['DENOMINACION','DENOMINACIONAMPL']])
#pasamos a excel a los que no hacen match:
#no_match_df[['DENOMINACION','DENOMINACIONAMPL']].to_excel('Medicamentos_con_nombres_complejos2.xlsx',index=False)
cleaned_df.to_excel('Nombres_medicamentos.xlsx', index=False)
###################

#Configuramos el navegador
driver=webdriver.Chrome()
url="https://farmaciacomunalonline.cl/Consultor?farmacia=lobarnechea"
driver.get(url)
#asegurarse de que la página cargue completamente
time.sleep(3)
html=driver.page_source
soup = BeautifulSoup(html, "html.parser")

#Los datos de la pag web que estamos revisando esta en una tabla con id:grdDatos
tabla=soup.find("table", {"id": "grdDatos"})
medicamentos=tabla.find_all("tr")
medicamentos_data=[]

# Iterar sobre las filas y extraer los datos
for fila in medicamentos:
    columnas= fila.find_all("td")
    #debemos extraer el texto de la tabla
    datos= [columna.get_text(strip=True) for columna in columnas] 
    if datos:
        medicamentos_data.append(datos)

# Cerrar el driver
driver.quit()

# Paso 3: Comparar con CLEANED_DENOMINATION
resultados = []

# Iterar sobre los medicamentos extraídos
for medicamento in medicamentos_data:
    #nombre_medicamento = medicamento[3] 
    nombre_medicamento = medicamento[2]  
    #precio = medicamento[-2]
    precio = medicamento[-3]
    #print(precio)
    #Verificar si el medicamento está en CLEANED_DENOMINACION
    resultados.append({'nombre': nombre_medicamento, 'precio': precio})
#print(resultados)
###########'''
def normalizar(nombre):
    nombre = re.sub(r'\(.*?\)', '', nombre)
    # Eliminar espacios extra al inicio y al final
    nombre = nombre.strip()
    return nombre
def farmaciaBar(excel):
    df_medicamentos=excel
    #medicamentos=df_excel['CLEANED_DENOMINACION'].dropna(axis=0)
    #nombres en una lista
    lista = df_medicamentos['Nombre'].tolist()  # Asegúrate de que la columna se llame "Medicamento"
    #print(medicamentos)
    extra=[""]+lista
    lista_medicamentos=extra
    ''' VALPARAISO
    #Normalizar una cadena (sin espacios extras, todo en mayúsculas)
    def normalizar(cadena):
        if isinstance(cadena, float) or cadena is None:
            return ""  # Devuelve una cadena vacía si no es texto
        return str(cadena).replace(" ", "").upper()

    #Crear un diccionario para buscar por nombre normalizado
    medicamentos_farmacia = {normalizar(item['nombre']): item['precio'] for item in resultados}

    #Comparar y obtener precios
    precios_encontrados=[]

    for medicamento in nombres_excel:
        nombre_normalizado = normalizar(medicamento)
        precio = medicamentos_farmacia.get(nombre_normalizado, "No disponible")  # Busca el precio o devuelve 'No disponible'
        precios_encontrados.append({'medicamento': medicamento, 'precio': precio})

    '''
    '''def normalizar(cadena):
        if isinstance(cadena, float) or cadena is None:
            return ""
        cadena = str(cadena).upper()
        # Mantener solo la estructura "Nombre + número + MG/UI/ML"
        cadena = re.sub(r'[^\w\s]', '', cadena)  # Eliminar caracteres especiales
        cadena = re.sub(r'(X\s\d+\s.*|VALOR.*|RECETA.*)', '', cadena)  # Eliminar textos extra como "X 60 CAPS."
        cadena = re.sub(r'\sBE$', '', cadena)  # Elimina " BE" solo si está al final
        cadena = re.sub(r'\s+', ' ', cadena).strip()  # Quitar espacios extra
        return cadena

    # Normalizar los nombres del Excel
    #nombres_excel_normalizados = [normalizar(nombre) for nombre in nombres_excel]

    # Crear un diccionario para buscar medicamentos por nombre normalizado
    medicamentos_farmacia = {
        normalizar(item['nombre']): item['precio']
        for item in resultados
    }
    print(medicamentos_farmacia)
    # Comparar y obtener precios
    precios_encontrados = []

    for medicamento in nombres_excel:
        if medicamento:  # Verificar que el nombre no esté vacío
            precio = medicamentos_farmacia.get(medicamento, "No disponible")  # Busca el precio o devuelve 'No disponible'
        else:
            precio = "No disponible"
        precios_encontrados.append({'Medicamento': medicamento, 'Precio Barnechea': precio})
    ##############################################################
    print(precios_encontrados)
    # Convertir el resultado en un DataFrame y guardarlo como Excel
    df_resultados = pd.DataFrame(precios_encontrados)
    print(df_resultados)'''
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    #Cambia la ruta al driver según tu sistema operativo
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    #Abrir la web de la farmacia
    url="https://farmaciacomunalonline.cl/Consultor?farmacia=lobarnechea"
    driver.get(url)
    #Cargar pagina
    wait = WebDriverWait(driver, 10)
    #########################################################################
    resultados =[]
    for medicamento in lista_medicamentos:
        try:
            #Localizar el buscador
            buscador = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'js-kioskboard-input'))
            )
            buscador.clear()
        #escribir medicamento
            medicamento_sinlab=normalizar(medicamento)
            buscador.send_keys(medicamento_sinlab)
            buscar_boton = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[3]/button[1]'))
                    )
            buscar_boton.click()
            time.sleep(2)
            #nombre = driver.find_elements(By.CLASS_NAME, 'odd')
            nombre = driver.find_elements(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr/td[3]')
            precio = driver.find_elements(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr/td[10]')
            laboratorios=driver.find_elements(By.XPATH,'/html/body/div/div/div/div[2]/div[2]/div/div[3]/table/tbody/tr/td[11]')
        
            if nombre and precio:  # Verificar que haya al menos un resultado
                resultados.append({
                    "medicamento_buscado": medicamento_sinlab,
                    "nombre en Barnechea": nombre[0].text,
                    "Valor referencial venta Barnechea": precio[0].text,
                    "laboratorios": laboratorios[0].text
                })
            else:
                resultados.append({
                    "medicamento_buscado": medicamento_sinlab,
                    "nombre en Barnechea":"No encontrado",
                    "Valor referencial venta Barnechea":"-",
                    "laboratorios":"-"
                })
        except Exception as e:
            print(f"Error al buscar el medicamento '{medicamento}': {e}")
    # Cerrar el navegador
    driver.quit()
    df_resultados = pd.DataFrame(resultados)
    df_resultados=df_resultados.drop(df_resultados.index[0])
    return df_resultados