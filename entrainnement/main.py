from rich.console import Console
from rich.panel import Panel
from gradient_boosting_model import run_gradient_boosting 
from random_forest_model import run_random_forest
import matplotlib.pyplot as plt


# Initialiser la console Rich
console = Console()

console.print(Panel.fit("🚦 [bold cyan]Détection d'anomalies dans un système de transport intelligent[/bold cyan]",
                        title="🧠 Projet IA - ITS", border_style="blue"))

# Lancer le premier modèle
console.print("\n[bold yellow]▶️ Lancement du modèle Random Forest...[/bold yellow]")
run_random_forest()

# Lancer le deuxième modèle
console.print("\n[bold yellow]▶️ Lancement du modèle Gradient Boosting...[/bold yellow]")
run_gradient_boosting()

console.print("\n[bold green]✅ Exécution complète des modèles. Rapport terminé.[/bold green]")

models = ["Random Forest", "Gradient Boosting"]
f1_scores = [0.9924, 0.9924]
recalls = [1.0, 1.0]
precisions = [0.9924, 1.0]

x = range(len(models))

plt.figure(figsize=(8, 5))
plt.bar(x, precisions, width=0.2, label="Precision", align='center')
plt.bar([i + 0.2 for i in x], recalls, width=0.2, label="Recall", align='center')
plt.bar([i + 0.4 for i in x], f1_scores, width=0.2, label="F1-Score", align='center')
plt.xticks([i + 0.2 for i in x], models)
plt.title("Comparaison des modèles supervisés")
plt.ylabel("Score")
plt.ylim(0.8, 1.05)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
