import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import os

# Specifica il percorso completo del file CSV
csv_file_path = '/path/to/your/european_capitals_weather.csv'

# Verifica se il file esiste
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"File non trovato: {csv_file_path}")

# Caricamento dei dati dal file CSV
try:
    df = pd.read_csv(csv_file_path)
    print("Dati caricati dal CSV:")
    print(df.head())
except Exception as e:
    print(f"Errore durante il caricamento del CSV: {e}")

# Connessione al database MySQL
try:
    conn = mysql.connector.connect(
        user='your_username',
        password='your_password',
        host='localhost',
        database='weather_data',
        auth_plugin='mysql_native_password'  # Utilizza il plugin mysql_native_password
    )
    cursor = conn.cursor()

    # Inserimento dei dati nella tabella MySQL
    for _, row in df.iterrows():
        try:
            cursor.execute(
                """
                INSERT INTO weather (city, date, max_temp, min_temp)
                VALUES (%s, %s, %s, %s)
                """,
                (row['city'], row['date'], row['max_temp'], row['min_temp'])
            )
            print(f"Record inserito: {row['city']}, {row['date']}, {row['max_temp']}, {row['min_temp']}")
        except Exception as e:
            print(f"Errore durante l'inserimento del record: {e}")
    
    # Commit delle transazioni
    conn.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Errore di accesso")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database non esiste")
    else:
        print(err)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
