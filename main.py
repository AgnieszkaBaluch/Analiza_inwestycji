
from currency_invest import currency_invest
import dash
from dash import dcc
from dash import html

#paramery: data rozpoczecia inwestycji, % inwestycji GBP i % inwestycji USD
inwestycja = currency_invest('2018-10-15', 0.4, 0.3)
dane = inwestycja.analyse()

app = dash.Dash(__name__)
colors = {
    'text': '#607B8B',
    'textbis': '#707070'
}
app.layout = html.Div([

    html.H1(children='Analiza inwestycji walutowej',
    style = {
                'textAlign': 'left',
                'color': colors['text'],
                'fontSize': '48px',
                'font-family': 'Arial'
    }),

    html.Div(
        [
            html.P(
                """Prezentowana analiza dotyczy 30-dniowej inwestycji kwoty tysiąca złotych 
                w trzy waluty: funta szterlinga, dolara amerykańskiego i franka szwajcarskiego. 
                Do jej przeprowadzenia wykorzystano dane udsotępniane przez Narodowy Bank Polski,
                dotyczące średnich kursow walut obcych (tabele A)."""

            )
        ],
        style={
            'width': '30%',
            'display': 'inline-block',
            'margin-top': '100px',
            'height': '45vh',
            'font-family': 'Arial',
            'fontSize': '18px',
            'color': colors['textbis'],
        },
    ),

    dcc.Graph(id="perc_plot", figure=inwestycja.plot_percentages(dane),
              style={'width': '70%', 'float': 'right',
                     'display': 'inline-block'}),

    dcc.Graph(id='value_plot', figure=inwestycja.plot_values(dane),
              style={'width': '160vh', 'height': '110vh'}),

])

app.run_server(debug=True)



