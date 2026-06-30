import os
from playwright.sync_api import sync_playwright

def extraer_textos_de_pagina(url):
    print(f"-> Paso 1: Abriendo navegador para visitar {url}")
    
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()
        
        # Vamos a la página y esperamos a que el banco termine de cargar todo
        pagina.goto(url, wait_until="networkidle")
        print("-> Paso 2: Página cargada. Extrayendo información...")
        
        # Sacamos todos los textos crudos de párrafos y títulos
        textos_crudos = pagina.locator('p, h1, h2, h3, li').all_inner_texts()
        navegador.close()
        
    # Limpiamos los textos
    textos_limpios = []
    for texto in textos_crudos:
        texto = texto.strip()
        # Solo guardamos si el fragmento tiene más de 25 caracteres
        if len(texto) > 25:
            textos_limpios.append(texto)
            
    return textos_limpios

def guardar_en_archivo(textos, nombre_archivo):
    # Nos aseguramos de que la carpeta 'data' exista, si no, pues que la crea
    os.makedirs('data', exist_ok=True)
    ruta = os.path.join('data', nombre_archivo)
    
    print(f"-> Paso 3: Guardando {len(textos)} fragmentos de texto en {ruta}")
    
    with open(ruta, 'w', encoding='utf-8') as archivo:
        for texto in textos:
            # Escribimos el texto y agregamos dos saltos de línea para separarlos
            archivo.write(texto + "\n\n")

# Ejecuicion
if __name__ == "__main__":
    # Definimos las variables
    url_objetivo = "https://www.bbva.com.co/personas/productos/tarjetas/credito.html"
    archivo_salida = "bbva_tarjetas.txt"
    
    # Llamamos a la función de extraer
    mis_textos = extraer_textos_de_pagina(url_objetivo)
    
    # Llamamos a la función de guardar
    if len(mis_textos) > 0:
        guardar_en_archivo(mis_textos, archivo_salida)
        print("-> ¡Proceso terminado con éxito!")
    else:
        print("-> Cuidado: No se encontró texto para extraer.")