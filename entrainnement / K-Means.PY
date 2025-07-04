import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# ------------------------------------------------------------
# Étape 1 : Chargement du dataset annoté
# ------------------------------------------------------------
df = pd.read_csv("fcd_data_cleaned.csv")

# ------------------------------------------------------------
# Étape 2 : Sélection des variables pertinentes
# ------------------------------------------------------------
features = ['speed', 'acceleration', 'jerk', 'stopped_time', 'leader_distance', 'gap_time']
X = df[features]          # Variables d'entrée
y_true = df['anomaly']    # Étiquettes (0 = normal, 1 = anomalie) — utilisées uniquement pour l’évaluation

# ------------------------------------------------------------
# Étape 3 : Normalisation des données
# ------------------------------------------------------------
# On standardise les valeurs pour éviter qu'une variable domine le clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ------------------------------------------------------------
# Étape 4 : Application de K-Means avec 2 clusters
# ------------------------------------------------------------
# On demande 2 clusters : un pour les comportements normaux, un pour les anormaux
kmeans = KMeans(n_clusters=2, random_state=42)
y_pred = kmeans.fit_predict(X_scaled)

# ------------------------------------------------------------
# Étape 5 : Réalignement des clusters
# ------------------------------------------------------------
# On suppose que le cluster minoritaire est celui des anomalies.
# Si ce n’est pas le cas, on inverse les 0 et 1.
if sum(y_pred) > len(y_pred) / 2:
    y_pred = [0 if x == 1 else 1 for x in y_pred]

# ------------------------------------------------------------
# Étape 6 : Évaluation (à but d’analyse uniquement, ce modèle reste non supervisé)
# ------------------------------------------------------------
print("🔍 Résultats - K-Means (non supervisé)")
print("Matrice de confusion :")
print(confusion_matrix(y_true, y_pred))

print("\nRapport de classification :")
print(classification_report(y_true, y_pred, digits=4))
