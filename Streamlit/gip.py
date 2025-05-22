import streamlit as st
import pandas as pd
import altair as alt



#ajout des colonnes
col1, col2= st.columns(2)

with col1:
    st.image("Streamlit/Identité visuelle - Logo GIP (ID 41903).svg")


with col2:
    # Titre principal de la page
    st.title("Dashboard GIP")



# Titre principal
st.title("Analyse de la police d'assurance")

# Section : Entrée des données techniques
st.sidebar.header("Données techniques")
prime_epargne = st.sidebar.number_input("Prime épargne annuelle (CHF)", min_value=0, step=100, value=2700)
prime_risque = st.sidebar.number_input("Prime risque annuelle (CHF)", min_value=0, step=100, value=1500)
debut_annee = st.sidebar.number_input("Année de début", min_value=1900, step=1, value=2018)
fin_annee = st.sidebar.number_input("Année de fin", min_value=1900, step=1, value=2056)
taux_technique = st.sidebar.number_input("Taux d'intérêt technique (%)", min_value=0.0, step=0.01, value=0.02)
taux_equilibree = st.sidebar.number_input("Taux profil équilibré (%)", min_value=0.0, step=0.01, value=0.03)
taux_revenu = st.sidebar.number_input("Taux profil revenu (%)", min_value=0.0, step=0.01, value=0.05)
taux_action = st.sidebar.number_input("Taux profil actions (%)", min_value=0.0, step=0.01, value=0.07)

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
    "Profil équilibré": [],
    "Profil revenu": [],
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
        montant * ((1 + taux_technique) ** (i - j))
        for j, montant in enumerate(versements_epargne)
    ])

    profil_eq = sum([
        montant * ((1 + taux_equilibree) ** (i - j))
        for j, montant in enumerate(versements_total)
    ])

    profil_rev = sum([
        montant * ((1 + taux_revenu) ** (i - j))
        for j, montant in enumerate(versements_total)
    ])

    profil_act = sum([
        montant * ((1 + taux_action) ** (i - j))
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

# Affichage interactif des résultats
st.subheader("Tableau généré")
st.dataframe(df, use_container_width=True)

with st.expander("Télécharger les données au format CSV"):
    csv_data = df.to_csv(index=False)
    st.download_button(label="Télécharger le fichier CSV", data=csv_data, file_name="analyse_assurance.csv",
                       mime="text/csv")

st.write("Réajustez les données dans la barre latérale pour générer un tableau personnalisé.")



# Affichage graphique interactif
st.subheader("Graphique de l'évolution des colonnes")
colonne_choisie = st.selectbox(
    "Choisissez une colonne à comparer avec 'Prime épargne avec intérêt':",
    ["Profil équilibré", "Profil revenu", "Profil actions"]
)

# Création du graphique avec Altair
df_melted = df.melt(id_vars=["Année"], value_vars=["Prime épargne avec intérêt", colonne_choisie],
                    var_name="Type", value_name="Valeur")
chart = alt.Chart(df_melted).mark_line().encode(
    x=alt.X("Année:O", title="Année"),
    y=alt.Y("Valeur:Q", title="Montant (CHF)"),
    color="Type:N",
    tooltip=["Année", "Type", "Valeur"]
).properties(
    title=f"Évolution de 'Prime épargne avec intérêt' et '{colonne_choisie}'",
    width=800,
    height=400
).configure_title(
    fontSize=18,
    anchor="start"
)

st.altair_chart(chart, use_container_width=True)
st.write("Vous pouvez choisir une colonne différente à comparer à partir du menu déroulant.")

