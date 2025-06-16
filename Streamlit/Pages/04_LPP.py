import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# 1. Charger les données depuis le fichier CSV (par exemple : 'chemin/vers/data.csv')
df = pd.read_csv(r"Streamlit/Datas/Suisse_ Produit Intérieur Brut (2023).csv")  # Remplacez par le chemin du fichier sur votre ordinateur

# Vérifier les premières lignes du tableau pour confirmer son contenu
print(df.head())

# S'assurer que 'observation date' est interprété comme un objet datetime
df['Variable observation date'] = df['Variable observation date'].astype(str).str[-4:].astype(int)

# Filtrer seulement les données depuis 1985
df = df[df['Variable observation date'] >= 1985]


# Conversion des valeurs en milliards
df['Variable observation value'] = df['Variable observation value'] / 1e9


# Créer le graphique
plt.figure(figsize=(10, 6))
plt.plot(df['Variable observation date'], df['Variable observation value'], linestyle='-', color='#00CFFF', label='Valeurs Observées')

# Personnalisation de l'axe des X : afficher une graduation tous les 5 ans
plt.xticks(ticks=df['Variable observation date'][::5], labels=df['Variable observation date'][::5], rotation=45)  # Affiche les années sans jour ni mois


# Personnalisation de l'axe des Y : afficher les nombres en milliards
ax = plt.gca()  # Obtenir l'objet de l'axe actuel
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x)}'))  # Format en milliards avec une décimale



# Ajouter des titres et des étiquettes
plt.title("Évolution du PIB Suisse (en milliards)", fontsize=16)
plt.xlabel("Année", fontsize=12)
plt.ylabel("PIB Suisse (en milliards)", fontsize=12)
plt.xticks(rotation=45)  # Rotation (si nécessaire)

# Ajouter une grille et une légende

plt.legend()

# Afficher le graphique
plt.show()

###########################################################################################

# Extraire l'année à partir des 4 derniers caractères de 'Variable observation date'
df['Variable observation date'] = df['Variable observation date'].astype(str).str[-4:].astype(int)

# Filtrer seulement les données depuis 1985
df = df[df['Variable observation date'] >= 1985]


# Calcul de la variation annuelle en pourcentage par rapport à la valeur précédente
df['Variation annuelle'] = df['Variable observation value'].pct_change()

# Calcul géométrique cumulée
# (1 + variation annuelle) cumulée, puis on soustrait 1 pour revenir au total géométrique
df['Variation cumulée géométrique'] = (1 + df['Variation annuelle']).cumprod() - 1

# Convertir en pourcentage
df['Variation cumulée géométrique'] *= 100

# Tracer le graphique des pourcentages cumulés géométriquement
plt.plot(df['Variable observation date'], df['Variation cumulée géométrique'], linestyle='-', color='#00CFFF', marker='o', label='Variation cumulée géométrique (%)')

# Ajouter une échelle logarithmique à l'axe Y
plt.yscale('log')

# Ajouter des titres et étiquettes
plt.title("Variation cumulée géométrique (%) (échelle logarithmique)", fontsize=16)
plt.xlabel("Années", fontsize=12)
plt.ylabel("Variation cumulée (log scale)", fontsize=12)

# Ajouter une ligne horizontale pour référence (0 % de variation)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)

# Ajouter une légende
plt.legend()

# Afficher le graphique
plt.show()

###########################################################################################

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Télécharger les données historiques du SMI depuis Yahoo Finance
# Le ticker officiel pour le SMI est "^SSMI"
smi_data = yf.download("^SSMI", start="1990-01-01", end="2023-12-31", progress=False)

# Vérifier les premières lignes du dataframe chargé
print(smi_data.head())

# Tracer la courbe des valeurs de clôture
plt.figure(figsize=(12, 6))
plt.plot(smi_data.index, smi_data['Close'], color='#00CFFF', label='SMI Close')


# Ajouter des titres et étiquettes
plt.title("Évolution de la clôture du SMI (Swiss Market Index) depuis 1985", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Indice de clôture (Close)", fontsize=12)

# Ajouter une grille et une légende

plt.legend()

# Afficher le graphique
plt.show()


##########################################################################################

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Télécharger les données historiques du SMI depuis Yahoo Finance
# Le ticker officiel pour le SMI est "^SSMI"
dfcp = pd.read_excel(r"Streamlit/Datas/Alloc Caisse de pension SQN Tuto.xlsx")
dfcp = dfcp.iloc[::-1].reset_index(drop=True)

dfcp['Unnamed: 0'] = pd.to_datetime(dfcp['Unnamed: 0'])
# Définir 'Unnamed: 0' comme index
dfcp.set_index('Unnamed: 0', inplace=True)





plt.figure(figsize=(12, 6))
# Tracer la colonne 'PF 1'
plt.plot(dfcp.index, dfcp['PF 1'], color='#00CFFF', label='Allocation 20% actions')
# Ajouter l'annotation pour la valeur finale de PF 1
plt.text(dfcp.index[-1], dfcp['PF 1'].iloc[-1], f'{dfcp["PF 1"].iloc[-1]:.2f}',
         color='#00CFFF', fontsize=12, fontweight='bold', va='center')



# Tracer la colonne 'PF 2'
plt.plot(dfcp.index, dfcp['PF 2'], color="#01282B", label='Allocation 40% actions')
# Ajouter l'annotation pour la valeur finale de PF 2
plt.text(dfcp.index[-1], dfcp['PF 2'].iloc[-1], f'{dfcp["PF 2"].iloc[-1]:.2f}',
         color="#01282B", fontsize=12, fontweight='bold', va='center')

# Tracer la colonne 'Min LPP'
plt.plot(dfcp.index, dfcp['Min LPP'], color="#DDD8C4", label='Taux min LPP')
# Ajouter l'annotation pour la valeur finale de PF 2
plt.text(dfcp.index[-1], dfcp['Min LPP'].iloc[-1], f'{dfcp["Min LPP"].iloc[-1]:.2f}',
         color="#DDD8C4", fontsize=12, fontweight='bold', va='center')


# Ajouter une légende
plt.legend()

# Ajouter des titres et des étiquettes
plt.title("Comparatif allocation 20% en actions vs 40% en actions et Taux Min LPP", fontsize=16)




# Afficher le graphique
plt.show()

