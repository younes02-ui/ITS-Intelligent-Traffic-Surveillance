# 🧠 ITS - Intelligent Traffic Surveillance

Ce projet vise à détecter automatiquement les **anomalies** dans un système de transport intelligent en se basant sur des données FCD (Floating Car Data).

## 🚦 Objectifs
- Détection supervisée des comportements anormaux des véhicules.
- Visualisation des résultats par réduction de dimension (PCA).
- Dashboard interactif pour l’analyse en temps réel.

## 📂 Contenu du projet

- `models/`
  - `random_forest_model.py` : Classification avec Random Forest.
  - `gradient_boosting_model.py` : Classification avec Gradient Boosting.
- `dashboard/`
  - Application web pour visualiser les anomalies détectées.
- `main.py` : Point d’entrée pour exécuter et comparer les deux modèles.
- `data/fcd_data_normalized_cleaned.csv` : Données utilisées.

## 📊 Résultats

Les deux modèles affichent une excellente performance :
- **Précision** : >99%
- **Recall anomalies** : ~84.6%
- **Visualisation PCA** : Affichage clair des points anormaux

## 🖥️ Dashboard
Accès via `dashboard_ITS.py` (Streamlit ou Flask).
Permet de visualiser :
- Statistiques globales
- Anomalies détectées en temps réel
- Données filtrables

## 🚀 Lancement rapide

```bash
pip install -r requirements.txt
python main.py
# ou
streamlit run dashboard/dashboard_ITS.py
