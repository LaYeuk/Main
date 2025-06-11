import streamlit as st
import pandas as pd
import altair as alt
from Layout import couleurs
from datetime import datetime


# Afficher le logo au tout début de la sidebar
with st.sidebar:
    st.image("Streamlit/Identité visuelle - Logo GIP (ID 41903).svg", use_container_width=True)






# Titre principal
st.title("Analyse de la police d'assurance ")

#Ajout espace
st.markdown("<br><br><br>", unsafe_allow_html=True)


# Section : Entrée des données techniques avec mise en forme des taux en %

prime_epargne = st.sidebar.number_input("Prime épargne annuelle (CHF)", min_value=0, step=100, value=2700)
prime_risque = st.sidebar.number_input("Prime risque annuelle (CHF)", min_value=0, step=100, value=1500)


# Calcul du montant total de la prime
montant_total_prime = prime_epargne + prime_risque
st.sidebar.write(f"### Total: {montant_total_prime:,.2f} CHF")

# Affichage dans la sidebar
st.sidebar.header("Paramètres techniques")

debut_annee = st.sidebar.number_input("Année de début", min_value=1900, step=1, value=2018)
fin_annee = st.sidebar.number_input("Année de fin", min_value=1900, step=1, value=2056)
capital_assure = st.sidebar.number_input("Capital assuré", min_value=50000, step=10000, value=100000)




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

# Récupération de l'année actuelle
annee_actuelle = datetime.now().year

# Récupération de la "Prime épargne cumulée" pour l'année en cours
if annee_actuelle in df["Année"].values:
    prime_epargne_cumulee_actuelle = df.loc[df["Année"] == annee_actuelle, "Prime épargne cumulée"].values[0]
else:
    prime_epargne_cumulee_actuelle = 0

# Affichage d'une métrique au-dessus du tableau des calculs
#Tableau pour les metrics

a, b, c = st.columns(3)

a.metric("Année actuelle", annee_actuelle)
c.metric("Prime de risque & admin", f"{prime_risque:,.0f} CHF", help="Montant total épargné jusqu'à l'année actuelle")
b.metric("",""
   )

#Ajout espace
st.markdown("<br>", unsafe_allow_html=True)
d, e, f = st.columns(3)

d.metric("Capital assuré en cas de décès", f"{capital_assure:,.0f} CHF", help="Montant assuré en cas de décès")
e.metric("Valeur de rachat estimée", f"{prime_epargne_cumulee_actuelle:,.0f} CHF", help="À vérifier avec votre assureur")
f.metric(
    "Montant que vous assurez actuellement",
    f"{capital_assure - prime_epargne_cumulee_actuelle:,.0f} CHF",
    help="Différence entre le capital assuré et l'épargne cumulée"
)

#Ajout espace
st.markdown("<br>", unsafe_allow_html=True)
j, k, l = st.columns(3)

j.metric("Coût d'opportunité profil revenu", f"{profil_rev- prime_epargne_cumulee_actuelle:,.0f} CHF")
k.metric("Coût d'opportunité profil équilibré", f"{profil_eq- prime_epargne_cumulee_actuelle:,.0f} CHF")
l.metric("Coût d'opportunité profil action", f"{profil_act- prime_epargne_cumulee_actuelle:,.0f} CHF")



#Ajout espace
st.markdown("<br><br><br>", unsafe_allow_html=True)

# Affichage interactif des résultats
st.subheader("Détails des calculs")
#Ajout espace
st.markdown("<br>", unsafe_allow_html=True)

st.dataframe(df_formatted, use_container_width=True)





#Ajout espace
st.markdown("<br><br><br>", unsafe_allow_html=True)

# Affichage graphique interactif
st.subheader("Évolution de votre capital")
#Ajout espace
st.markdown("<br>", unsafe_allow_html=True)

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
    title=f"Comparaison entre votre police et une solution investie",
    width=800,
    height=400
).configure_title(
    fontSize=18,
    anchor="start"
)

st.altair_chart(chart, use_container_width=True)

