import pandas as pd
import re
#Obtencion de nombres y cantidades de medicamentos
#cargar el archivo excel
def convertir(archivo):
    #archivo = 'Medicamentos FOM - copia.xlsx'
    #borrar las primeras 266 filas que estan extrañas
    #df_medicamentos= pd.read_excel(archivo, skiprows=266)
    df_medicamentos=pd.read_excel(archivo) 
    #df_medicamentos=archivo
    df_medicamentos.columns=['Descripcion_Producto','Laboratorio','Valor_Propio']
    # Función para normalizar nombres conservando las cantidades
    def normalizar_nombre(nombre):
        # Conservar cantidades (mg, %, etc.) y eliminar palabras innecesarias
        nombre = re.sub(r'\b(?:COMP|CAPS|CM|BE|X|SO|FCO|GTS|%)\b', '', nombre, flags=re.IGNORECASE)  # Eliminar palabras comunes
        nombre = re.sub(r'\s+', ' ', nombre).strip()
        return nombre

    # Crear un nuevo DataFrame para almacenar los resultados tipo Nombre_medicamento (Laboratorio)
    df = pd.DataFrame(columns=['Nombre','Valor_Propio'])

    #Procesar cada fila del DataFrame original
    for i in range(len(df_medicamentos)):
        descripcion_actual = df_medicamentos.loc[i, 'Descripcion_Producto']
        laboratorio_actual = df_medicamentos.loc[i, 'Laboratorio']
        valor_lote= df_medicamentos.loc[i, 'Valor_Propio']
        
        # Normalizar la descripción del producto (conservando cantidades)
        descripcion_normalizada = normalizar_nombre(descripcion_actual)
        
        # Si hay laboratorio, añadirlo al nombre
        if pd.notna(laboratorio_actual):
            nombre = f"{descripcion_normalizada} ({laboratorio_actual})"
            valor=f"{valor_lote}"
        else:
            # Si no hay laboratorio, usar el principio activo
            nombre = f"{descripcion_normalizada}"
            valor=f"{valor_lote}"

        
        # Agregar el nombre al nuevo DataFrame
        df.loc[i, 'Nombre'] = nombre
        df.loc[i, 'Valor_Propio']=valor
    return df
    # Mostrar el DataFrame resultante
#m=convertir('MEDICAMENTOS-Prueba.xlsx')
    
#Excel
    
    ###################