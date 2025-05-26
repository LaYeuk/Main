import streamlit as st
import pandas as pd
import altair as alt
from Layout import couleurs

# Afficher le logo au tout début de la sidebar
st.image("Streamlit/Identité visuelle - Logo GIP (ID 41903).svg", use_container_width=True)






# Titre principal
st.title("Analyse de la police d'assurance")

# Section : Entrée des données techniques avec mise en forme des taux en %
st.sidebar.header("Données techniques")
prime_epargne = st.sidebar.number_input("Prime épargne annuelle (CHF)", min_value=0, step=100, value=2700)
prime_risque = st.sidebar.number_input("Prime risque annuelle (CHF)", min_value=0, step=100, value=1500)
debut_annee = st.sidebar.number_input("Année de début", min_value=1900, step=1, value=2018)
fin_annee = st.sidebar.number_input("Année de fin", min_value=1900, step=1, value=2056)

# Sliders : valeur décimale manipulée mais affichée en pourcentage
taux_technique = st.sidebar.slider("Taux d'intérêt technique (%)",
                                    min_value=0.0, max_value=10.0, step=0.01, value=1.05, format="%.2f%%")

taux_revenu = st.sidebar.slider("Taux profil revenu (%)",
                                 min_value=0.0, max_value=10.0, step=0.01, value=3.00, format="%.2f%%")

taux_equilibree = st.sidebar.slider("Taux profil équilibré (%)",
                                    min_value=0.0, max_value=10.0, step=0.01, value=5.00, format="%.2f%%")

taux_action = st.sidebar.slider("Taux profil actions (%)",
                                 min_value=0.0, max_value=10.0, step=0.01, value=7.00, format="%.2f%%")





# Calcul du nombre d'années
annees = list(range(debut_annee, fin_annee + 1))

# Initialisation des colonnes du tableau
data = {
    "Année": annees,
    "Prime épargne": [prime_epargne] * len(annees),
    "Prime risque + admin": [prime_risque] * len(annees),
    "Total": [prime_epargne + prime_risque] * len(annees),
    "Prime épargne cumulée": [],
    "Prime risque cumulée": [],
    "Total cumulée": [],
    "Prime épargne avec intérêt": [],
    "Profil revenu": [],
    "Profil équilibré": [],
    "Profil actions": [],
    "Coût d'opportunité": []
}

# Calculs dynamiques
cumul_epargne = 0
cumul_risque = 0
cumul_total = 0

# Pour stocker les versements année par année
versements_epargne = []
versements_total = []

for i, annee in enumerate(annees):
    cumul_epargne += prime_epargne
    cumul_risque += prime_risque
    cumul_total += prime_epargne + prime_risque

    # Ajout des versements de l'année
    versements_epargne.append(prime_epargne)
    versements_total.append(prime_epargne + prime_risque)

    # Calcul de l'intérêt composé sur chaque versement
    epargne_avec_interet = sum([
        montant * ((1 + (taux_technique/100)) ** (i - j))
        for j, montant in enumerate(versements_epargne)
    ])

    profil_eq = sum([
        montant * ((1 + (taux_equilibree/100)) ** (i - j))
        for j, montant in enumerate(versements_total)
    ])

    profil_rev = sum([
        montant * ((1 + (taux_revenu/100)) ** (i - j))
        for j, montant in enumerate(versements_total)
    ])

    profil_act = sum([
        montant * ((1 + (taux_action/100)) ** (i - j))
        for j, montant in enumerate(versements_total)
    ])

    # Ajout des résultats dans le tableau
    data["Prime épargne cumulée"].append(cumul_epargne)
    data["Prime risque cumulée"].append(cumul_risque)
    data["Total cumulée"].append(cumul_total)
    data["Prime épargne avec intérêt"].append(epargne_avec_interet)
    data["Profil équilibré"].append(profil_eq)
    data["Profil revenu"].append(profil_rev)
    data["Profil actions"].append(profil_act)
    data["Coût d'opportunité"].append(profil_act - epargne_avec_interet)


# Création du DataFrame
df = pd.DataFrame(data)

# Création d'une copie formatée pour l'affichage (évite d'altérer les données numériques)
df_formatted = df.copy()

# Application du formatage : colonnes sans "Année"
df_formatted = df_formatted.applymap(
    lambda x: f"{int(x):,}".replace(",", "'") if isinstance(x, (int, float)) else x
)

# Gestion spécifique de la colonne 'Année', supprimer le séparateur
if "Année" in df_formatted.columns:
    df_formatted["Année"] = df["Année"].astype(int)



# Affichage interactif des résultats
st.subheader("Tableau généré")
st.dataframe(df_formatted, use_container_width=True)


# Affichage graphique interactif
st.subheader("Graphique de l'évolution des colonnes")


# Création du graphique avec Altair
df_melted = df.melt(id_vars=["Année"], value_vars=["Prime épargne avec intérêt", "Profil équilibré","Profil revenu","Profil actions"],
                    var_name="Type", value_name="Valeur")
type_categories = df_melted["Type"].unique()  # Récupération des catégories pour "Type"


chart = alt.Chart(df_melted).mark_line().encode(
    x=alt.X("Année:O", title="Année"),
    y=alt.Y("Valeur:Q", title="Montant (CHF)"),
    color=alt.Color("Type:N",
                    title="Type",
                    scale=alt.Scale(domain=list(type_categories), range=couleurs)),

    tooltip=["Année", "Type", "Valeur"]
).properties(
    title=f"Évolution de 'Prime épargne avec intérêt' et 3 profils",
    width=800,
    height=400
).configure_title(
    fontSize=18,
    anchor="start"
)

st.altair_chart(chart, use_container_width=True)

