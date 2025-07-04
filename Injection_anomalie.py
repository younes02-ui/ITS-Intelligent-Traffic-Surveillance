# === Anomalies Injection (SUMO + TraCI) ===

import traci
import sumolib
import pandas as pd
import numpy as np
import os

os.environ["SUMO_HOME"] = "/opt/homebrew/Cellar/sumo/1.18.0/share/sumo"
sumo_binary = "sumo-gui"
sumo_config = "test.sumocfg"
simulation_step_duration = 1.0

traci.start([
    sumo_binary,
    "-c", sumo_config,
    "--log", "sumo_run.log",
    "--message-log", "sumo_message.log",
    "--error-log", "sumo_error.log",
    "--verbose"
])

step = 0
anomaly_ids = {"v_neg_speed", "v_burst", "v_stop", "v_zigzag","v_ghost"}
anomalies_triggered = {vid: False for vid in anomaly_ids}
anomalies_active = {vid: False for vid in anomaly_ids}
simulation_data = []

print("\U0001F6A6 Simulation démarrée...")

burst_route = ["308158679#2", "ET01", "456581921#0", "S03", "315255842#0"]

while step < 1000:
    try:
        traci.simulationStep()
    except traci.exceptions.TraCIException as e:
        print(f"[Erreur TraCI à t={step}] : {e}")
        break

    vehicle_ids = traci.vehicle.getIDList()

    # 🔒 Empêche tous les véhicules sauf v_burst de changer de voie
    for vid in vehicle_ids:
        try:
            if vid == "v_burst":
                traci.vehicle.setLaneChangeMode(vid, 1621)
            elif traci.vehicle.getRoute(vid) == burst_route:
                traci.vehicle.setLaneChangeMode(vid, 512)
        except:
            pass

    # Anomalie v_neg_speed
    if "v_neg_speed" in vehicle_ids and not anomalies_triggered["v_neg_speed"] and step >= 5:
        try:
            traci.vehicle.slowDown("v_neg_speed", 0.9, 1000.0)
            traci.vehicle.setColor("v_neg_speed", (255, 0, 0, 255))
            anomalies_triggered["v_neg_speed"] = True
            anomalies_active["v_neg_speed"] = True
            print(f"[Anomalie] v_neg_speed ralenti et colorié à t={step}")
        except:
            anomalies_triggered["v_neg_speed"] = True

    # Anomalie v_burst : vitesse lente puis accélération
    if "v_burst" in vehicle_ids and step == 92:
        try:
            traci.vehicle.setColor("v_burst", (255, 165, 0, 255))
            traci.vehicle.setSpeedMode("v_burst", 0)
            traci.vehicle.setSpeed("v_burst", 3.0)
        except:
            pass

    if "v_burst" in vehicle_ids and step == 120 and not anomalies_triggered["v_burst"]:
        try:
            traci.vehicle.setSpeed("v_burst", 15.0)
            traci.vehicle.setColor("v_burst", (255, 165, 0, 255))
            anomalies_triggered["v_burst"] = True
            anomalies_active["v_burst"] = True
            print(f"[Anomalie] v_burst accélère brutalement à t={step}")
        except:
            pass

    # Anomalie v_stop
    if "v_stop" in vehicle_ids and step < 108:
        try:
            traci.vehicle.setColor("v_stop", (128, 0, 128, 255))
        except:
            pass

    if "v_stop" in vehicle_ids and not anomalies_triggered["v_stop"] and step >= 108:
        try:
            traci.vehicle.setSpeed("v_stop", 0)
            anomalies_triggered["v_stop"] = True
            anomalies_active["v_stop"] = True
            print(f"[Anomalie] v_stop arrêt complet à t={step}")
        except:
            pass

    # Anomalie v_zigzag
    if "v_zigzag" in vehicle_ids and 45 <= step <= 200 and step % 3 == 0:
        try:
            edge = traci.vehicle.getRoadID("v_zigzag")
            lane_count = traci.edge.getLaneNumber(edge)
            if lane_count > 1:
                current_lane = traci.vehicle.getLaneIndex("v_zigzag")
                new_lane = (current_lane + 1) % lane_count
                traci.vehicle.changeLane("v_zigzag", new_lane, 2.0)
                traci.vehicle.setColor("v_zigzag", (0, 255, 255, 255))
                anomalies_active["v_zigzag"] = True
                anomalies_triggered["v_zigzag"] = True
                print(f"[Anomalie] v_zigzag change vers voie {new_lane} à t={step}")
        except:
            pass

            # Anomalie v_ghost (voiture fantôme téléportée au milieu du trajet)
    if "v_ghost" in vehicle_ids:
     try:
        # Une seule téléportation à t >= 65
        if not anomalies_triggered["v_ghost"] and step >= 65:
            lane_id = "39456620#1_0"  # ← Vérifie que ce lane ID existe dans net.xml
            pos = 20.0  # Position sur la voie
            traci.vehicle.moveTo("v_ghost", lane_id, pos)
            traci.vehicle.setSpeedMode("v_ghost", 0b00000)  # Ignorer collisions
            anomalies_triggered["v_ghost"] = True
            anomalies_active["v_ghost"] = True
            print(f"[Anomalie] v_ghost téléporté à {lane_id} à t={step}")

        # Couleur grise persistante pour l'effet "fantôme"
        traci.vehicle.setColor("v_ghost", (160, 160, 160, 255))

     except traci.exceptions.TraCIException as e:
        print(f"[Erreur v_ghost à t={step}] : {e}")
        anomalies_triggered["v_ghost"] = True

            





    # Collecte des données
    for vid in vehicle_ids:
        try:
            pos = traci.vehicle.getPosition(vid)
            is_anomalous = int(anomalies_active.get(vid, False))
            simulation_data.append({
                "time": step,
                "vehicle_id": vid,
                "x": pos[0],
                "y": pos[1],
                "speed": traci.vehicle.getSpeed(vid),
                "angle": traci.vehicle.getAngle(vid),
                "lane": traci.vehicle.getLaneID(vid),
                "pos": traci.vehicle.getLanePosition(vid),
                "anomaly": is_anomalous
            })
        except:
            continue

    step += 1

if traci.isLoaded():
    traci.close()

print("\u2705 Simulation SUMO terminée.")

os.makedirs("output", exist_ok=True)
df = pd.DataFrame(simulation_data)
df.to_csv("output/fcd_output.csv", index=False)
print("\U0001F4BE Données enregistrées dans output/fcd_output.csv")
