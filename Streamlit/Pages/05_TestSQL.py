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



   gt_table = (
     GT(df) # Prend les 10 premières lignes pour l'exemple
        .tab_header(
            title="Exemple de Tableau Great Tables",
            subtitle=html("Données de <b>qualité de l'air</b>"),
        )
        .fmt_number(
            columns=["o3", "co", "no2"],
            decimals=2
        )
        .tab_source_note(
            source_note="Source: great_tables.data.sza"
        )
    )
    return gt_table

st.set_page_config(layout="wide")
st.title("Intégration de Great Tables avec Streamlit")

st.write("Voici un exemple de tableau créé avec `great_tables` et affiché dans Streamlit :")

# Générez le tableau Great Tables
my_gt_table = create_great_table()

# Convertissez le tableau Great Tables en HTML brut
gt_html = my_gt_table.as_raw_html()

# Affichez le HTML dans Streamlit
# Il est crucial de définir unsafe_allow_html=True pour permettre l'affichage du HTML.
st.write(gt_html, unsafe_allow_html=True)

st.write("---")
st.write("Vous pouvez personnaliser le tableau avec toutes les fonctionnalités de `great_tables`.")

