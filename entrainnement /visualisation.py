import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Chargement des données nettoyées
df = pd.read_csv("/Users/younes/Desktop/5 anomalies/projet/fcd_data_normalized_cleaned.csv")

# S'assurer que 'anomaly' est bien de type catégorie
df['anomaly'] = df['anomaly'].astype(int)

# Configuration des graphes
sns.set(style="whitegrid")

# 1. Distribution de la vitesse (speed)
plt.figure(figsize=(10, 5))
sns.kdeplot(data=df[df['anomaly'] == 0], x='speed', label='Normal', fill=True)
sns.kdeplot(data=df[df['anomaly'] == 1], x='speed', label='Anomalie', fill=True, color="red")
plt.title("Distribution de la vitesse selon l’anomalie")
plt.xlabel("Vitesse (m/s)")
plt.ylabel("Densité")
plt.legend()
plt.tight_layout()
plt.show()

# 2. Distribution de l’accélération
plt.figure(figsize=(10, 5))
sns.kdeplot(data=df[df['anomaly'] == 0], x='acceleration', label='Normal', fill=True)
sns.kdeplot(data=df[df['anomaly'] == 1], x='acceleration', label='Anomalie', fill=True, color="red")
plt.title("Distribution de l’accélération selon l’anomalie")
plt.xlabel("Accélération (m/s²)")
plt.ylabel("Densité")
plt.legend()
plt.tight_layout()
plt.show()
