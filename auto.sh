#!/bin/bash
echo "Lancement de la simulation SUMO..."

sumo -c test.sumocfg

echo "Simulation SUMO terminee."
echo "Lancement de visualisation.py..."

python3 visualisation.py

echo "visualisation.py termine."
echo "Lancement de Data_plus.py..."
python3 Data_plus.py

echo "Processus termine."