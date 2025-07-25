import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# === Étape 1 : Chargement du fichier nettoyé ===
fichier_entree = "fcd_data_augmented.csv"
df = pd.read_csv(fichier_entree)

# === Étape 2 : Définition des colonnes à normaliser ===
colonnes_a_normaliser = ['speed', 'acceleration', 'jerk', 'stopped_time', 'leader_distance', 'gap_time']

# === Étape 3 : Application du MinMaxScaler ===
scaler = MinMaxScaler()
df_normalized = df.copy()
df_normalized[colonnes_a_normaliser] = scaler.fit_transform(df[colonnes_a_normaliser])

# === Étape 4 : Sauvegarde du fichier normalisé ===
fichier_sortie = "fcd_data_normalized.csv"
df_normalized.to_csv(fichier_sortie, index=False)

print("✅ Normalisation terminée avec succès.")
print(f"📄 Fichier généré : {fichier_sortie}")
print(f"🔢 Colonnes normalisées : {colonnes_a_normaliser}")
