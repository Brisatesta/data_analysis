import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

# Connessione al database MySQL
try:
    conn = mysql.connector.connect(
        user='brisatesta',
        password='pswd>',
        host='localhost',
        database='weather_data',
        auth_plugin='pswd>'  # Utilizza il plugin mysql_native_password
    )

    # Query per estrarre i dati dal database
    query = "SELECT city, date, max_temp, min_temp FROM weather"
    df = pd.read_sql(query, conn)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Errore di accesso")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database non esiste")
    else:
        print(err)
finally:
    if 'conn' in locals():
        conn.close()


# Funzione per l'analisi di regressione
def regression_analysis(df, column, title, filename):
    df['year'] = pd.to_datetime(df['date']).dt.year
    X = df[['year']]
    y = df[column]

    model = LinearRegression()
    model.fit(X, y)

    # Predizione
    y_pred = model.predict(X)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Dati reali')
    plt.plot(X, y_pred, color='red', label='Linea di regressione')
    plt.xlabel('Anno')
    plt.ylabel(column)
    plt.title(title)
    plt.legend()

    # Salva il grafico come file immagine
    plt.savefig(filename)
    plt.close()
    print(f'Grafico salvato come {filename}')


# Crea una cartella per salvare i grafici se non esiste
output_dir = '/home/dario/Statistiche/meteo'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Analisi per ogni gruppo di temperature
for city in df['city'].unique():
    city_df = df[df['city'] == city]

    for month, day in [(1, 15), (7, 15)]:
        subset_df = city_df[(pd.to_datetime(city_df['date']).dt.month == month) &
                            (pd.to_datetime(city_df['date']).dt.day == day)]

        if not subset_df.empty:
            filename_max = os.path.join(output_dir, f'{city}_max_temp_{day}_{month}.png')
            filename_min = os.path.join(output_dir, f'{city}_min_temp_{day}_{month}.png')

            regression_analysis(subset_df, 'max_temp', f'Temperatura massima a {city} il {day} {month}', filename_max)
            regression_analysis(subset_df, 'min_temp', f'Temperatura minima a {city} il {day} {month}', filename_min)

print("Analisi completata e grafici salvati nella cartella 'regression_plots'")
