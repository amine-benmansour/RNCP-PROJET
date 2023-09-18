
from pytrends.request import TrendReq

# Créez une instance de TrendReq
pytrends = TrendReq(hl='fr-FR', tz=0)  # Réglez la langue sur "français" et le fuseau horaire sur UTC (0)

# Spécifiez les mots-clés que vous souhaitez rechercher
prompt = str(input("Entrez votre Recherche Analytics: "))
kw_list = [prompt]
#kw_list = ["ETF Bitcoin"]

# Configurez les paramètres de recherche
periode = str(input("Entrez la periode sous format YYYY-MM-DD YYYY-MM-DD : "))
pytrends.build_payload(kw_list, cat=0, timeframe=periode, geo='', gprop='')

#pytrends.build_payload(kw_list, cat=0, timeframe='2023-01-01 2023-12-31', geo='', gprop='')

# Obtenez les données de tendance
trend_data = pytrends.interest_over_time()

# Affichez les données
print(trend_data)

import matplotlib.pyplot as plt

# Afficher le graphique de tendance de recherche
plt.figure(figsize=(10, 6))  # Définir la taille du graphique
plt.plot(trend_data.index, trend_data[prompt], marker='o', linestyle='-')
plt.title('Tendance de recherche prompt sur la periode')
plt.xlabel('Date')
plt.ylabel('Tendance de recherche')
plt.grid(True)

# Afficher le graphique
plt.show()

import requests
import pandas as pd


url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=250"

# Effectuez une requête GET pour obtenir les données
response = requests.get(url)

# Vérifiez si la requête a réussi
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data['prices'], columns=['Date', 'PrixUSD'])
    
    # Convertissez la colonne 'Date' en format de date
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    
    # Créez un graphique du prix du Bitcoin en USD
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['PrixUSD'], marker='o', linestyle='-')
    plt.title('Prix du Bitcoin en USD (Année 2023)')
    plt.xlabel('Date')
    plt.ylabel('Prix en USD')
    plt.grid(True)
    
    # Affichez le graphique
    plt.show()
else:
    print("Échec de la requête à l'API CoinGecko.")

trend_data.to_csv('GoogleTrend.csv', index = True)
