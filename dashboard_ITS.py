import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import webbrowser
import os


# Charger les données
df = pd.read_csv("entrainnement/fcd_data_normalized_cleaned.csv")

# Initialisation de l'application Dash avec thème dark Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Dashboard ITS – Anomalies de Trafic"

# Layout avec Navbar + KPIgit status

app.layout = dbc.Container([
 dbc.Navbar(
    dbc.Container([
        dbc.Row([
            # Logo IA à gauche
            dbc.Col(html.Img(
                src="https://cdn-icons-png.flaticon.com/512/4712/4712104.png",
                height="50px"
            ), width="auto"),

            # Titre centré
            dbc.Col(html.Div([
                html.H3("ITS – Intelligent Traffic Surveillance", className="text-white text-center fw-bold mb-0")
            ]), width=True, className="d-flex justify-content-center align-items-center")
        ], align="center", className="w-100")
    ], fluid=True),
    color="dark",
    dark=True,
    className="mb-4 shadow-sm p-3"
)
,
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de véhicules", className="card-title"),
                html.H2(df['vehicle_id'].nunique(), className="card-text")
            ])
        ], color="primary", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("% d'anomalies", className="card-title"),
                html.H2(f"{round(df['anomaly'].mean() * 100, 2)} %", className="card-text")
            ])
        ], color="danger", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Vitesse moyenne", className="card-title"),
                html.H2(f"{round(df['speed'].mean() * 3.6, 2)} km/h", className="card-text")  # conversion en km/h
            ])
        ], color="info", inverse=True), width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Sélectionner un véhicule :"),
            dcc.Dropdown(
                id='vehicle-dropdown',
                options=[{'label': v, 'value': v} for v in sorted(df['vehicle_id'].unique())],
                value=sorted(df['vehicle_id'].unique())[0],
                style={'color': 'black'}
            )
        ], width=6),

        dbc.Col([
            html.Label("Sélectionner une variable :"),
            dcc.Dropdown(
                id='variable-dropdown',
                options=[
                    {'label': 'Vitesse (speed)', 'value': 'speed'},
                    {'label': 'Accélération (acceleration)', 'value': 'acceleration'},
                    {'label': 'Jerk', 'value': 'jerk'},
                    {'label': 'Distance au leader', 'value': 'leader_distance'},
                    {'label': 'Gap time', 'value': 'gap_time'}
                ],
                value='speed',
                style={'color': 'black'}
            )
        ], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-time-series'), width=12)
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-histogram'), width=6),
        dbc.Col(dcc.Graph(id='graph-boxplot'), width=6)
    ]),

html.Footer([
    html.P("© 2025 — Réalisé par Younes Boudjella & Chihab Eddine Cherif", className="mb-0"),
    html.Small("Université du Québec en Outaouais – Projet synthèse ITS", className="text-muted")
], className="text-center mt-5 text-light bg-dark py-3")
], fluid=True)

# Callback des graphiques
@app.callback(
    Output('graph-time-series', 'figure'),
    Output('graph-histogram', 'figure'),
    Output('graph-boxplot', 'figure'),
    Input('vehicle-dropdown', 'value'),
    Input('variable-dropdown', 'value')
)
def update_graphs(selected_vehicle, selected_variable):
    df_vehicle = df[df['vehicle_id'] == selected_vehicle]

    fig1 = px.line(df_vehicle, x='time', y=selected_variable,
                   title=f'Évolution de {selected_variable} pour {selected_vehicle}',
                   markers=True,
                   template="plotly_dark")

    fig2 = px.histogram(df, x=selected_variable, color='anomaly',
                        barmode='overlay', nbins=60,
                        title=f'Distribution de {selected_variable} selon les anomalies',
                        template="plotly_dark")

    fig3 = px.box(df, x='anomaly', y=selected_variable, color='anomaly',
                  title=f'{selected_variable} : comparaison normal / anomalie',
                  labels={'anomaly': 'Anomalie (0 = non, 1 = oui)'},
                  template="plotly_dark")

    return fig1, fig2, fig3

# Lancement auto
if __name__ == '__main__':
    if not os.environ.get("RENDER"):
        webbrowser.open_new("http://127.0.0.1:8050/")
    app.run(debug=True, host="0.0.0.0", port=10000)
