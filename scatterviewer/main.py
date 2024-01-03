import json
import dash
import flask
from flask import Flask, send_from_directory
from dash import dcc, html, Input, Output, State, callback_context
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from plotly.graph_objs import Scatter3d, Layout

# Step 1: Load JSON Data
with open('sample_data.json', 'r') as file:
    data = json.load(file)

# Step 2: Feature Extraction
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([item['content'] for item in data])

# Step 3: Clustering
num_clusters = 5  # choose the number of clusters
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

# Step 4: Dimensionality Reduction
pca = PCA(n_components=3)
coords = pca.fit_transform(tfidf_matrix.toarray())

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Initial JSON display
initial_json_display = html.Pre(json.dumps(data, indent=2), style={'overflowY': 'scroll', 'height': '600px'})

app.layout = html.Div([
    dcc.Graph(
        id='3d-clustering-plot',
        figure={
            'data': [Scatter3d(
                x=coords[:, 0], y=coords[:, 1], z=coords[:, 2],
                mode='markers',
                marker=dict(size=5, color=clusters, colorscale='Viridis', opacity=0.8),
                text=[item['name'] for item in data],
                customdata=[item['name'] for item in data]
            )],
            'layout': Layout(title='3D Clustering Plot')
        },
        style={'width': '50%', 'height': '100%', 'display': 'inline-block'}
    ),
    html.Div(
        id='display-area',
        children=initial_json_display,
        style={'width': '50%', 'display': 'inline-block'}
    ),
    html.Button('Close PDF', id='close-button', style={'display': 'none'})
])

@server.route('/pdfs/<path:filename>')
def serve_pdf(filename):
    return flask.send_from_directory('pdfs', filename)

@app.callback(
    Output('display-area', 'children'),
    [Input('3d-clustering-plot', 'clickData'), Input('close-button', 'n_clicks')],
    [State('display-area', 'children')]
)
def update_display_area(clickData, close_clicks, current_display):
    ctx = callback_context

    if not ctx.triggered:
        return initial_json_display

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == '3d-clustering-plot':
        if clickData:
            filename = clickData['points'][0]['customdata']
            print("Filename clicked:", filename)  # Debug print
            pdf_path = f'/pdfs/{filename}'
            print("PDF path:", pdf_path)  # Debug print
            return html.Div([
                html.Button('Close PDF', id='close-button', style={'display': 'block'}),
                html.Iframe(src=pdf_path, style={'width': '100%', 'height': '600px'})
            ])
        else:
            return initial_json_display

    elif button_id == 'close-button':
        return initial_json_display

    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)