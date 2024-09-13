import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

# Función para cargar modelos de alarma (simulado)
def load_alarm_models():
    return {
        "Simple Moving Average": lambda data: data['Close'].rolling(window=20).mean(),
        "Bollinger Bands": lambda data: {
            'upper': data['Close'].rolling(window=20).mean() + 2 * data['Close'].rolling(window=20).std(),
            'lower': data['Close'].rolling(window=20).mean() - 2 * data['Close'].rolling(window=20).std()
        }
    }

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div([
    html.H1("Dashboard de Monitoreo de Acciones"),
    dcc.Input(id='stock-input', type='text', placeholder='Ingrese símbolo de acción'),
    dcc.Graph(id='stock-graph'),
    html.Div(id='alarm-output')
])

# Callback para actualizar el gráfico y las alarmas
@app.callback(
    [Output('stock-graph', 'figure'),
     Output('alarm-output', 'children')],
    [Input('stock-input', 'value')]
)
def update_graph(stock_symbol):
    if not stock_symbol:
        return dash.no_update, dash.no_update

    # Obtener datos de la acción
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Crear gráfico
    figure = {
        'data': [go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close']
        )],
        'layout': {
            'title': f'Gráfico de velas de {stock_symbol}'
        }
    }

    # Verificar alarmas
    alarm_models = load_alarm_models()
    alarms = []
    for model_name, model_func in alarm_models.items():
        result = model_func(stock_data)
        if isinstance(result, pd.Series):
            if stock_data['Close'].iloc[-1] > result.iloc[-1]:
                alarms.append(f"Alarma {model_name}: Precio por encima del umbral")
        elif isinstance(result, dict):
            if stock_data['Close'].iloc[-1] > result['upper'].iloc[-1]:
                alarms.append(f"Alarma {model_name}: Precio por encima de la banda superior")
            elif stock_data['Close'].iloc[-1] < result['lower'].iloc[-1]:
                alarms.append(f"Alarma {model_name}: Precio por debajo de la banda inferior")

    return figure, html.Ul([html.Li(alarm) for alarm in alarms])

if __name__ == '__main__':
    app.run_server(debug=True)