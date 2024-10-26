import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from config import *
from run import data_store

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Daily Weather Aggregates"),
    dcc.Dropdown(
        id='city-dropdown',
        options=[
            {'label': city, 'value': city}
            for city in CITIES
        ],
        value='Delhi',  # Default city
        multi=False,
    ),
    dcc.Graph(id='aggregate-graph'),
])

@app.callback(
    Output('aggregate-graph', 'figure'),
    Input('city-dropdown', 'value')
)
def update_graph(selected_city):
    # Fetch daily aggregates from MongoDB for the selected city
    aggregates = data_store.get_all_data(selected_city)
    
    # Convert to DataFrame for easier plotting
    if not aggregates:
        return px.line(title='No data available for the selected city.')
    aggregates = [agg.dict() for agg in aggregates]
    
    df = pd.DataFrame(aggregates)
    print(df)
    
    # Ensure the date is in the correct format
    df['date'] = pd.to_datetime(df['date'])
    
    # Create a line plot for daily aggregates
    fig = px.line(df, x='date', y=['avg_temp', 'max_temp', 'min_temp'],
                  title=f'Daily Weather Aggregates for {selected_city}',
                  labels={'value': 'Temperature (°C)', 'date': 'Date'},
                  markers=True)
    
    fig.update_layout(yaxis_title='Temperature (°C)', xaxis_title='Date')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
