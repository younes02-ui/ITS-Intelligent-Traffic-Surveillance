import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_gradient_boosting():
    df = pd.read_csv("entrainnement/fcd_data_normalized_cleaned.csv")
    features = ['speed', 'acceleration', 'jerk', 'stopped_time', 'leader_distance', 'gap_time']
    X = df[features]
    y = df['anomaly']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, stratify=y, random_state=42
    )

    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report_text = classification_report(y_test, y_pred, digits=4)

    console.print(Panel.fit(
        "[bold cyan]🎯 Modèle 2 : Gradient Boosting Classifier[/bold cyan]\n\n"
        "[bold white]Rapport de classification :[/bold white]\n\n"
        f"[white]{report_text}[/white]",
        title="📊 Résultats du modèle",
        border_style="magenta"
    ))
