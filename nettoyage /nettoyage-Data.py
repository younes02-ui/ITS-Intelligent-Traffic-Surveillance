import pandas as pd
import numpy as np

# Chargement des données normalisées
df = pd.read_csv("/Users/younes/Desktop/5 anomalies/projet/fcd_data_normalized.csv")

# 1. Suppression des doublons
df.drop_duplicates(inplace=True)

# 2. Suppression des lignes avec NaN dans les colonnes critiques
colonnes_critiques = ['speed', 'acceleration', 'jerk', 'leader_distance', 'gap_time']
df.dropna(subset=colonnes_critiques, inplace=True)

# 3. Conversion explicite en float (par sécurité)
cols_to_float = ['speed', 'acceleration', 'jerk', 'stopped_time', 'leader_distance', 'gap_time']
df[cols_to_float] = df[cols_to_float].apply(pd.to_numeric, errors='coerce')

# 4. Filtrage minimal après normalisation
# Toutes les colonnes sont censées être entre 0 et 1 (MinMaxScaler)
# On filtre uniquement les valeurs vraiment hors bornes par erreur
for col in cols_to_float:
    df = df[(df[col] >= 0) & (df[col] <= 1)]

# 5. Réinitialisation des index
df.reset_index(drop=True, inplace=True)

# 6. Sauvegarde
df.to_csv("fcd_data_normalized_cleaned.csv", index=False)

print("✅ Données normalisées nettoyées avec succès.")
print(f"🔢 Nombre de lignes finales : {len(df)}")
print("📄 Fichier exporté : fcd_data_normalized_cleaned.csv")
