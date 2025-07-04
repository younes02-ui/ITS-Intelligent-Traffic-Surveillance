import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------
# Étape 1 : Chargement du dataset
# ------------------------------------------------------------
df = pd.read_csv("/Users/younes/Desktop/5 anomalies/projet/fcd_data_cleaned.csv")

# ------------------------------------------------------------
# Étape 2 : Sélection des variables explicatives et de la cible
# ------------------------------------------------------------
features = ['speed', 'acceleration', 'jerk', 'stopped_time', 'leader_distance', 'gap_time']
X = df[features]
y = df['anomaly']

# ------------------------------------------------------------
# Étape 3 : Normalisation des données
# ------------------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ------------------------------------------------------------
# Étape 4 : Séparation entraînement/test
# ------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# ------------------------------------------------------------
# Étape 5 : Entraînement du modèle Random Forest
# ------------------------------------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ------------------------------------------------------------
# Étape 6 : Prédictions et évaluation
# ------------------------------------------------------------
y_pred = model.predict(X_test)

print("🔍 Résultats - Random Forest (supervisé)")
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

print("\nRapport de classification :")
print(classification_report(y_test, y_pred, digits=4))


# ------------------------------------------------------------
# Étape 7 : Visualisation de l’importance des variables
# ------------------------------------------------------------
importances = model.feature_importances_
plt.figure(figsize=(8, 5))
sns.barplot(x=importances, y=features)
plt.title("Importance des variables - Random Forest")
plt.xlabel("Importance")
plt.ylabel("Variables")
plt.tight_layout()
plt.show()
