import pandas as pd
import numpy as np
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


fcd_path = 'output/fcd_output.csv'  # ✅ Le fichier généré avec la colonne "anomaly"
routes_path = 'random_routes.rou.xml'
net_path = 'E3.net.xml'

def parse_routes(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    data = []
    for veh in root.findall('vehicle'):
        veh_id = veh.attrib['id']
        depart = float(veh.attrib.get('depart', 0))
        route = veh.find('route')
        edges = route.attrib.get('edges', '') if route is not None else ''
        data.append({'vehicle_id': veh_id, 'depart': depart, 'edges': edges})
    return pd.DataFrame(data)

def parse_net(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    edge_records = []
    for edge in root.findall('edge'):
        edge_id = edge.attrib['id']
        for lane in edge.findall('lane'):
            rec = {
                'edge_id': edge_id,
                'lane_id': lane.attrib['id'],
                'length': float(lane.attrib.get('length', 0)),
                'lane_speed': float(lane.attrib.get('speed', 0)),
                'shape': lane.attrib.get('shape', '')
            }
            edge_records.append(rec)
    return pd.DataFrame(edge_records)

def compute_leader_distance(group, df_all):
    group = group.sort_values('time')
    distances = []
    for _, row in group.iterrows():
        same_time = df_all[
            (df_all['time'] == row['time']) &
            (df_all['vehicle_id'] != row['vehicle_id']) &
            (df_all['lane'] == row['lane'])
        ]
        if not same_time.empty:
            same_time = same_time.copy()
            same_time['distance'] = np.sqrt((same_time['x'] - row['x'])**2 + (same_time['y'] - row['y'])**2)
            min_dist = same_time['distance'].min()
            distances.append(min_dist)
        else:
            distances.append(np.nan)
    group['leader_distance'] = distances
    return group

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)

    # ✅ Lecture directe du fichier CSV contenant la colonne anomaly
    fcd_df = pd.read_csv(fcd_path)
    if fcd_df.empty:
        print("⚠️ fcd_output.csv est vide.")
        exit()

    routes_df = parse_routes(routes_path)
    net_df = parse_net(net_path)

    df = fcd_df.copy()  # Contient déjà "anomaly"
    df = df.merge(routes_df, on='vehicle_id', how='left')
    df = df.merge(net_df, left_on='lane', right_on='lane_id', how='left')

    df['time'] = df['time'].astype(float)
    df['speed'] = df['speed'].astype(float)

    df = df.sort_values(by=['vehicle_id', 'time'])

    df['acceleration'] = df.groupby('vehicle_id')['speed'].diff() / df.groupby('vehicle_id')['time'].diff()
    df['jerk'] = df.groupby('vehicle_id')['acceleration'].diff() / df.groupby('vehicle_id')['time'].diff()
    df['stopped'] = (df['speed'] == 0).astype(int)
    df['stopped_time'] = df.groupby('vehicle_id')['stopped'].cumsum()
    df = df.groupby('vehicle_id').apply(lambda g: compute_leader_distance(g, df)).reset_index(drop=True)
    df['gap_time'] = df['leader_distance'] / df['speed'].replace(0, np.nan)

    df.to_csv('output/all_data_enriched.csv', index=False)
    print("✅ Données enrichies enregistrées avec la colonne anomaly.")

# 1) Trajectoire (x,y) de tous les véhicules, en pointillés pour les anomalies
plt.figure()
for vid, g in df.groupby('vehicle_id'):
    # normal vs anomalous
    normal = g[g['anomaly'] == 0]
    ana    = g[g['anomaly'] == 1]
    plt.plot(normal['x'], normal['y'], linestyle='-', linewidth=0.5)
    if not ana.empty:
        plt.plot(ana['x'], ana['y'], linestyle='--', linewidth=1)
plt.title("Trajectoires des véhicules (-- = anomalie)")
plt.xlabel("x")
plt.ylabel("y")
plt.axis('equal')
plt.tight_layout()
plt.savefig("output/trajectoires.png")
plt.close()

# 2) Série temporelle de la vitesse moyenne par instant, et part d'anomalies
time_summary = df.groupby('time').agg({
    'speed': 'mean',
    'anomaly': 'mean'
}).reset_index()

plt.figure()
plt.plot(time_summary['time'], time_summary['speed'])
plt.title("Vitesse moyenne (toutes voitures)")
plt.xlabel("Temps")
plt.ylabel("Vitesse moyenne")
plt.tight_layout()
plt.savefig("output/vitesse_moyenne.png")
plt.close()

plt.figure()
plt.plot(time_summary['time'], time_summary['anomaly'])
plt.title("Proportion de véhicules en anomalie au cours du temps")
plt.xlabel("Temps")
plt.ylabel("Proportion anomalie")
plt.tight_layout()
plt.savefig("output/part_anomalies.png")
plt.close()

# 3) Histogramme des gap_time
plt.figure()
plt.hist(df['gap_time'].dropna(), bins=50)
plt.title("Distribution des temps de gap")
plt.xlabel("gap_time")
plt.ylabel("Effectif")
plt.tight_layout()
plt.savefig("output/histogramme_gap_time.png")
plt.close()

print("✅ Graphiques générés dans le dossier output/ :")
print("   - trajectoires.png")
print("   - vitesse_moyenne.png")
print("   - part_anomalies.png")
print("   - histogramme_gap_time.png")
