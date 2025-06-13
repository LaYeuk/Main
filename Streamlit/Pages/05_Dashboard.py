import pandas as pd
import pyodbc
from great_tables import GT
import streamlit as st

# Configurer la chaîne de connexion avec vos informations
connection_string = (
    "DRIVER={Progress OpenEdge 12.2 Driver};"
    "HOSTNAME=10.0.0.4;"  # Adresse du serveur
    "PORT=12508;"  # Port de la base de données
    "DATABASE=Concept;"  # Nom de la base de données
    "UID=gip;"  # Nom d'utilisateur
    "PWD=Gip2025!;"  # Mot de passe
)

try:
    # Établir une connexion avec gestionnaire de contexte
    with pyodbc.connect(connection_string) as conn:
        # Corriger la requête SQL avec la syntaxe spécifique à Progress OpenEdge
        query = """
        SELECT *
        FROM PUB.cpsValuatLine
        FETCH FIRST 30 ROWS ONLY
        """

        # Charger les données dans un DataFrame
        df = pd.read_sql(query, conn)

        # Afficher un aperçu des données
        print(df.head())

except pyodbc.Error as e:
    # Afficher l'erreur en cas de problème de connexion ou d'exécution SQL
    print(f"Erreur ODBC : {e}")
except Exception as ex:
    # Gérer toute autre exception
    print(f"Erreur générale : {ex}")



st.dataframe(df)


