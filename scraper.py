import csv
import requests
from bs4 import BeautifulSoup

def extraer_datos_libros():
    # URL de una página web pública diseñada específicamente para practicar scraping
    url = "https://books.toscrape.com/"
    
    # Definir un User-Agent para simular una petición desde un navegador web real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"[START] Conectando a {url}...")
    
    try:
        # Realizar la petición HTTP a la página
        response = requests.get(url, headers=headers, timeout=15)
        
        # Verificar si la página respondió correctamente (Código 200)
        if response.status_code == 200:
            print("[INFO] Conexión establecida. Procesando código HTML...")
            
            # Parsear el contenido HTML de la página con BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontrar todos los contenedores de libros en el catálogo
            libros = soup.find_all('article', class_='product_pod')
            
            lista_libros = []
            
            # Iterar sobre cada libro encontrado para extraer su información
            for libro in libros:
                # Extraer el título del atributo 'title' dentro de la etiqueta <a>
                titulo = libro.h3.a['title'].strip()
                
                # Extraer el precio buscando la clase 'price_color' y limpiar el texto
                precio = libro.find('p', class_='price_color').text.strip()
                # Remover caracteres extraños de la moneda (mantener solo número y símbolo)
                precio_limpio = precio.replace("Â", "") 
                
                # Guardar en un diccionario organizado
                lista_libros.append({
                    "title": titulo,
                    "price": precio_limpio
                })
            
            # Guardar los datos recolectados en un archivo CSV formateado
            guardar_en_csv(lista_libros)
            
        else:
            print(f"[ERROR] No se pudo acceder a la página. Código de estado: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Ocurrió un fallo inesperado durante el rastreo: {e}")

def guardar_en_csv(datos):
    nombre_archivo = "datos_libros_scraped.csv"
    columnas = ["title", "price"]
    
    try:
        with open(nombre_archivo, mode='w', encoding='utf-8', newline='') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader() # Escribir los encabezados de columna
            escritor.writerows(datos) # Escribir todas las filas de datos
            
        print(f"[ÉXITO] Datos extraídos correctamente y guardados en '{nombre_archivo}'.")
        print(f"Se procesaron un total de {len(datos)} registros de forma automatizada.")
        
    except IOError:
        print("[ERROR] Error al intentar escribir el archivo CSV resultante.")

if __name__ == "__main__":
    extraer_datos_libros()