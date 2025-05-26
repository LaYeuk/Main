import yfinance as yf

# Télécharger les données uniquement pour NESN en 2024
data_nesn = yf.download("NESN.SW", start="2024-01-01", end="2024-12-31")
print(data_nesn["Close"])
