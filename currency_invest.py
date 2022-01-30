import requests
import json
import pandas as pd
import numpy as np
from datetime import timedelta, date
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chart_studio.plotly as py


class currency_invest:
    def __init__(self,s_date,perc_gbp,perc_usd):
        self.s_date = s_date
        self.e_date = str(date.fromisoformat(s_date) + timedelta(days=30))
        self.perc_gbp = perc_gbp
        self.perc_usd = perc_usd
        self.perc_chf = 1 - perc_gbp - perc_usd
        self.init_val = 1000
        self.codes = ['gbp', 'usd', 'chf']
        self.colors = ['rgb(188,210,238)', 'rgb(162,181,205)', 'rgb(110,123,139)', 'rgb(0,139,139)']


    def analyse(self):

        data = pd.DataFrame()
        for i in self.codes:
            data_init = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/' +
                                        i + '/' + self.s_date + '/' + self.e_date + '/?format=json')
            data[i] = pd.DataFrame.from_dict(json.loads(data_init.text)['rates'])['mid']
        data['daty'] = pd.DataFrame.from_dict(json.loads(data_init.text)['rates'])['effectiveDate']

        data_0 = {self.codes[0]: (self.perc_gbp * self.init_val) / data.iloc[0, 0],
                  self.codes[1]: (self.perc_usd * self.init_val) / data.iloc[0, 1],
                  self.codes[2]: (self.perc_chf * self.init_val) / data.iloc[0, 2]}

        data_final = data.iloc[:, :3] * data_0.values()
        data_final['wallet'] = round(data_final.sum(1), 2)
        data_final['daty'] = pd.DataFrame.from_dict(json.loads(data_init.text)['rates'])['effectiveDate']
        data_final.iloc[:, :3] = data_final.iloc[:, :3].round(2)
        return data_final

    def plot_percentages(self, invest_data):

        labels = [i.upper() for i in self.codes]

        plot_perc = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

        plot_perc.add_trace(go.Pie(labels=labels, values=[self.perc_gbp, self.perc_usd, self.perc_chf]), 1, 1)

        plot_perc.add_trace(go.Pie(labels=labels, values=[invest_data.iloc[-1, 0] / invest_data.iloc[-1, 3],
                                                          invest_data.iloc[-1, 1] / invest_data.iloc[-1, 3],
                                                          invest_data.iloc[-1, 2] / invest_data.iloc[-1, 3]]), 1, 2)
        plot_perc.update_layout(
            title_text="Porównanie procentowego udziału poszczególnych składowych watości portfela inwestycyjnego",
            title_font=dict(size=18),
            legend=dict(font=dict(family="Arial", size=15)),
            annotations=[dict(text='Początek<br>inwestycji', x=0.17, y=0.5, font_size=16, showarrow=False),
                         dict(text='Koniec<br>inwestycji', x=0.83, y=0.5, font_size=16, showarrow=False)])

        plot_perc.update_traces(textinfo='percent', textfont_size=20, hole=.4, hoverinfo="label+percent",
                                marker=dict(colors=self.colors[:3]))
        return plot_perc


    def plot_values(self, invest_data):
        labels = ['Wartość inwestycji w GBP', 'Wartość inwestycji w USD', 'Wartość inwestycji w CHF',
                  'Wartość portfela inwestycyjnego']
        labels_init_end = ['Początkowa/końcowa wartość<br>inwestycji w GBP',
                           'Początkowa/końcowa wartość<br>inwestycji w USD',
                           'Początkowa/końcowa wartość<br>inwestycji w CHF',
                           'Początkowa/końcowa wartość<br>portfela inwestycyjnego']

        mode_size = [6, 6, 6, 8]
        line_size = [2, 2, 2, 3]

        x_data = np.vstack((invest_data.iloc[:, 4].to_numpy(),) * 4)
        y_data = invest_data.iloc[:, :4].transpose().to_numpy()

        plot_values = go.Figure()
        for i in range(0, 4):
            plot_values.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                                     name=labels[i],
                                     line=dict(color=self.colors[i], width=line_size[i]),
                                     connectgaps=True,
                                     hovertemplate='Data: %{x}' + '<br>Wartość: %{y} PLN<extra></extra>',
                                     ))
            plot_values.add_trace(go.Scatter(
                x=[x_data[i][0], x_data[i][-1]],
                y=[y_data[i][0], y_data[i][-1]],
                name=labels_init_end[i],
                mode='markers',
                marker=dict(color=self.colors[i], size=mode_size[i]),
                hovertemplate='Data: %{x}' + '<br>Wartość: %{y} PLN<extra></extra>',
        ))
        plot_values.update_layout(
            title_text="Zmiana wartości inwestycji w czasie",
            title_font=dict(size=20),
            xaxis=dict(
                title='Oś czasu inwestycji',
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickangle=45,
                tickfont=dict(
                    family='Arial',
                    size=14,
                    color='rgb(82, 82, 82)')
            ),
            yaxis=dict(
                title='Wartość [PLN]',
                linecolor='rgb(204, 204, 204)',
                linewidth=1.7,
                tickfont=dict(
                    family='Arial',
                    size=14,
                    color='rgb(82, 82, 82)')
            ),
            plot_bgcolor='white',
            legend = dict(
                font=dict(
                    size=14)
            )
        )
        plot_values.update_xaxes(tickformat='%d.%m.%Y', nticks=20),
        plot_values.update_yaxes(nticks=10)

        return plot_values