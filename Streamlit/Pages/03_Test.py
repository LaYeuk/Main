import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion
import streamlit as st



# Fonction pour télécharger et préparer les données d'une action
def get_stock_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period="1y", interval="1d")  # Historique sur 1 an, intervalle journalier
    df = df.reset_index()  # Réinitialiser l'index pour avoir la colonne "Date"
    return df

# Liste des symboles boursiers
symbols = ["IDIA.SW", "NESN.SW", "GEBN.SW"]

# Générer un graphique par symbole
for symbol in symbols:
    df = get_stock_data(symbol)

    # Création du graphique financier pour chaque action
    fig = go.Figure(data=[
        go.Candlestick(
            x=df['Date'],        # Axe X : Date
            open=df['Open'],     # Valeurs d'ouverture
            high=df['High'],     # Valeurs hautes
            low=df['Low'],       # Valeurs basses
            close=df['Close'],   # Valeurs de clôture
            name=symbol          # Nom de l'action
        )
    ])

    # Personnalisation du graphique
    fig.update_layout(
        title=f'Graphique financier pour {symbol}',
        xaxis_title='Date',
        yaxis_title='Prix',
        xaxis_rangeslider_visible=True,  # Ajoute un sélecteur de plage d'axe X spécifique
        template='plotly_dark'           # Thème sombre
    )

    # Affichage du graphique pour chaque action
    fig

# Activer le mode interactif pour Matplotlib
ion()

# Télécharger les données de clôture pour les 3 titres
tickers = ["IDIA.SW", "NESN.SW", "GEBN.SW"]
data = yf.download(tickers, period="1y", interval="1d")["Close"]

# Calcul des rendements journaliers
returns = data.pct_change().dropna()

# Poids équipondérés
weights = np.array([1 / 3, 1 / 3, 1 / 3])

# Simulation de la frontière efficiente
num_portfolios = 5000
results = np.zeros((3, num_portfolios))

for i in range(num_portfolios):
    # Générer des poids aléatoires
    random_weights = np.random.random(len(tickers))
    random_weights /= np.sum(random_weights)

    # Calcul du rendement et du risque pour le portefeuille simulé
    portfolio_return = np.dot(returns.mean(), random_weights) * 252
    portfolio_volatility = np.sqrt(np.dot(random_weights.T, np.dot(returns.cov() * 252, random_weights)))
    sharpe_ratio = portfolio_return / portfolio_volatility

    # Stocker les résultats
    results[0, i] = portfolio_volatility
    results[1, i] = portfolio_return
    results[2, i] = sharpe_ratio

# Extraction des résultats
volatility, portfolio_returns, sharpe_ratios = results

# Trouver le portefeuille avec le meilleur ratio de Sharpe
max_sharpe_idx = sharpe_ratios.argmax()
max_sharpe_volatility = volatility[max_sharpe_idx]
max_sharpe_return = portfolio_returns[max_sharpe_idx]

# Trouver le portefeuille avec le plus faible risque
min_volatility_idx = volatility.argmin()
min_volatility = volatility[min_volatility_idx]
min_volatility_return = portfolio_returns[min_volatility_idx]

# Tracer la frontière efficiente
graph=plt.figure(figsize=(10, 6))
plt.scatter(volatility, portfolio_returns, c=sharpe_ratios, cmap="viridis", marker="o", s=10, alpha=0.7)
plt.colorbar(label="Ratio de Sharpe")
plt.scatter(max_sharpe_volatility, max_sharpe_return, color="r", marker="*", s=200, label="Max Sharpe Ratio")
plt.scatter(min_volatility, min_volatility_return, color="b", marker="*", s=200, label="Min Volatility")
plt.title("Frontière efficiente du portefeuille")
plt.xlabel("Volatilité (Risque)")
plt.ylabel("Rendement attendu")
plt.legend()
plt.grid()
plt.show()

st.pyplot(graph)

max_sharpe_return



