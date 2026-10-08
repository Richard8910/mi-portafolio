import csv
import psycopg2
from psycopg2 import sql

# 1. Configuración de conexión a tu base de datos local de PostgreSQL
DB_PARAMS = {
    "host": "localhost",
    "database": "tu_base_de_datos",  # Cambia por el nombre de tu DB
    "user": "postgres",              # Cambia por tu usuario
    "password": "tu_password"        # Cambia por tu contraseña
}

def crear_tabla_si_no_existe(cursor):
    """Crea una tabla de ejemplo para almacenar datos de empresas de tecnología"""
    query = """
    CREATE TABLE IF NOT EXISTS tech_companies (
        id SERIAL PRIMARY KEY,
        company_name VARCHAR(100) UNIQUE,
        technology_used VARCHAR(150),
        country VARCHAR(50)
    );
    """
    cursor.execute(query)
    print("[INFO] Tabla 'tech_companies' verificada/creada exitosamente.")

def procesar_y_guardar_csv(file_path):
    """Lee un archivo CSV e inserta los datos de forma masiva en PostgreSQL"""
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # Asegurar que la estructura exista
        crear_tabla_si_no_existe(cursor)
        
        # Abrir y leer el archivo CSV
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            insert_query = """
            INSERT INTO tech_companies (company_name, technology_used, country)
            VALUES (%s, %s, %s)
            ON CONFLICT (company_name) DO UPDATE 
            SET technology_used = EXCLUDED.technology_used;
            """
            
            registros_insertados = 0
            for row in csv_reader:
                # Extraer y limpiar los datos del renglón
                nombre = row['company_name'].strip()
                tecnologia = row['technology_used'].strip()
                pais = row['country'].strip()
                
                # Ejecutar inserción protegiendo contra inyección SQL
                cursor.execute(insert_query, (nombre, tecnologia, pais))
                registros_insertados += 1
                
        # Confirmar los cambios en la base de datos (Commit)
        conn.commit()
        print(f"[ÉXITO] Pipeline completado. Se procesaron {registros_insertados} registros.")

    except Exception as error:
        print(f"[ERROR] Ocurrió un fallo en el pipeline: {error}")
        if conn:
            conn.rollback() # Deshacer cambios si hubo error
            
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Ejecución del script
if __name__ == "__main__":
    # Nota: Requiere que tengas un archivo llamado 'empresas.csv' en la misma carpeta
    # Con las columnas: company_name, technology_used, country
    print("[START] Iniciando pipeline de datos...")
    procesar_y_guardar_csv("empresas.csv")