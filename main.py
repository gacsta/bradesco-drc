# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:10:34 2022

@author: M268701
"""
######################################################################################################
# LIBRARIES

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from glob import glob
import numpy as np
from datetime import date
from datetime import datetime

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

######################################################################################################
# TRATAMENTO DE DADOS

def date_converter(date):
    # if len(date) == 7:
    #     return datetime.strptime(date, '%m/%Y')
    # elif len(date) == 10:
        return datetime.strptime(date, '%m/%Y')

#HISTORICO
file_bh = np.array(glob('base-historica-qtdreneg.csv'))
base_historica = pd.read_csv(file_bh[0], sep=';').reset_index(drop=True)

base_historica['DtBase'] = base_historica['DtBase'].apply(date_converter)

#PROPORÇÕES

    #SEGMENTOS
file_seg = np.array(glob('segmentos.csv'))
segmentos = pd.read_csv(file_seg[0], sep=';').reset_index(drop=True)

segmentos['DtBase'] = segmentos['DtBase'].apply(date_converter)

    #MODALIDADES


    #CANAIS

file_can = np.array(glob('canais.csv'))
canais = pd.read_csv(file_can[0], sep=';').reset_index(drop=True)

canais['DtBase'] = canais['DtBase'].apply(date_converter)

######################################################################################################
app = dash.Dash(__name__)
server = app.server

colors = {
    'background': 'white',
    'graphs': 'black',
    'border': '#BC2943',
    'bradesco': '#CD092F',
    'text': 'black'
}
app.layout = html.Div(id='root', style={'back-ground-color': colors['background'], 'height' : '95vh', 'width' : '98vw'}, children=[

    html.Div(id='cabecalho',
             style={'background-color': colors['background'], 'width': '100%','height' : '32%', 'border-bottom' : '0.6vh solid {}'.format(colors['border'])}, children=[
            html.Img(id='cabecalho_bradesco',
                     src=app.get_asset_url('cabecalho.png'),
                     style={'width': '100%', 'background-color': colors['background']}),

            html.Img(id='datamart-titulo',
                     src=app.get_asset_url('bradesco.webp'),
                     style={'background-color': colors['background'], 'text-align' : 'center', 'position' : 'relative', 'width' : '70%', 'left' : '17%', 'top': '10%', 'height':'25%'}),


            #html.H1('Dashboard Data Mart de Renegociação',
                   # style={'text-align': 'center', 'color': 'black', 'font-family' : 'Diodrum Semibold',
                           #'background-color': colors['background'], 'border-bottom' : '4px solid {}'.format(colors['border']), 'height' : '70px'})
        ]
             ),
    html.Div(id='select-date',
             style={ 'width': '100%', 'height': '8vh', 'background-color': colors['background']},
             children=[
                    dcc.DatePickerRange(id='my-date-picker-range',
                                             style={'position': 'relative', 'left': '2%', 'top': '28%', 'border' : '0.6vh solid {}'.format(colors['border'])},
                                             min_date_allowed=date(2019, 2, 1), max_date_allowed=date(2022, 2, 1),
                                             start_date=date(2021, 2, 1), end_date=date(2022, 2, 1), display_format='MMMM YY'),

             ]
             ),

    html.Div( id = 'analise-historico',
              style={'width' : '61%','height': '70vh', 'background-color': colors['background'], 'float' : 'left', 'position' : 'relative', 'left' : '2%', 'top' : '5%'} ,
              children = [
                    dcc.Graph(id='base_historico' , figure={},
                              style={'border': '4px solid {}'.format(colors['border']), 'height' : '100%'},
                              )
                  ]),

    html.Div(id = 'analise-abertura',
             style = {'float' : 'right', 'width' : '35vw', 'position' : 'relative', 'top' : '5%' },
             children=[
                    html.Div(id='analises-abertas', style ={ 'border': '4px solid {}'.format(colors['border']) } ,children=[
                        dcc.Tabs(id='tabs-abertura', value='tab-1', children=[
                            dcc.Tab(label='Segmentos', value='tab-1'),
                            #dcc.Tab(label='Canais', value='tab-2'),
                            dcc.Tab(label='Modalidades', value='tab-3'),
                        ]),
                        html.Div(id='tabs-conteudo')
                    ])


    ]),

    html.Div(id='analise-canais',
             style={'float': 'left', 'position' : 'relative', 'top': '8vh', 'left' : '2%', 'width' : '59.7vw'},
             children=[
                 html.Div(id='canal', style={'border': '4px solid {}'.format(colors['border'])}, children=[
                        dcc.Tabs(id='tabs-canal', value='tab-a', children=[
                            dcc.Tab(label='Canais', value='tab-a'),
                     ]),
                     html.Div(id='tabs-conteudo-2')
                 ])

             ]),

]
)

@app.callback(Output('base_historico', 'figure'), Input('my-date-picker-range', 'start_date'),
              Input('my-date-picker-range', 'end_date'))

def update_graph(start_date, end_date):
    df = base_historica[(base_historica['DtBase'] >= start_date) & (base_historica['DtBase'] <= end_date)]
    # Plotly Graph
    fig = px.line(df, x='DtBase', y='QtdReneg', markers=True, template = "none")
    fig.update_layout(clickmode = 'event+select')
    fig.update_xaxes(gridcolor='black')
    fig.update_yaxes(gridcolor='black')
    fig.update_traces(line={'color': '#ff0000', 'width': 2}, marker = {'color': '#CD092F', 'size': 12, 'line' : {'width': 2, 'color':'black'}})

    return fig

@app.callback(Output('tabs-conteudo', 'children'),
              Input('tabs-abertura', 'value'),
              Input('base_historico', 'clickData'))


def render_content(tab, clickData):
    #pie plot
    #tables and figs
    # scheme_pie = ['#f3e9f4', '#edc7e2', '#eba2c6', '#ea7ca1', '#e35374', '#e33f5d', '#e02744', '#da0029', '#e40023', '#ed001c', '#f60011', '#ff0000']

    if clickData is not None:
        mes_select = clickData['points'][0]['x']
    else:
        mes_select = segmentos['DtBase'].iloc[0]

    df1 = segmentos[segmentos['DtBase'] == mes_select]
    fig_pie = px.pie(df1, values='QtdReneg', names='Segmento', title='Proporção de renegociações por segmento no mês', color_discrete_sequence=px.colors.sequential.RdBu)
    fig_pie.update_traces(textposition='inside',textinfo='percent+label',marker=dict( line=dict(color='#000000', width=2)))
    fig_pie.update_layout( margin=dict(r=20, l=20, b=10))

    df2 = segmentos[segmentos['DtBase'] == mes_select][['Segmento', 'QtdReneg']]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df2['QtdReneg'],
        y=df2['Segmento'],
        name='Mês Atual',
        text=df2['QtdReneg'],
        marker_color='#CD092F',
        orientation = 'h'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(barmode='group', uniformtext_minsize=5, template = 'none', margin = dict(l = 100, r = 20))


    #tabs
    if tab == 'tab-1':
        return html.Div(children = [
            # html.H3('mes selecionado --> {}'.format(clickData), id = 'Segmentos', style = {'text-align' : 'center'}),

            dcc.Graph(
                figure=fig_bar, style={'height': '70%'}
            ),
            dcc.Graph(
                figure=fig_pie, style={'height': '70%'}
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Proporção das Renegs por Modalidade', style = {'text-align' : 'center'}),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }, style = {'height' : '50vh'}
            ),
            dcc.Graph(
                id='graph-3-tabs-dcc',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [6, 12, 36],
                        'type': 'bar'
                    }]
                }, style = {'height' : '50vh'}
            )
        ])

@app.callback(Output('tabs-conteudo-2', 'children'),
              Input('tabs-canal', 'value'),
              Input('base_historico', 'clickData'))

def render_content(tab_canal, clickData):

    if clickData is not None:
        mes_select = clickData['points'][0]['x']
    else:
        mes_select = segmentos['DtBase'].iloc[0]

    df3 = canais[canais['DtBase'] == mes_select][['CANAL', 'QtdReneg', 'SumVlrAtivo']]
    fig_canal = px.bar(df3, y='QtdReneg', x='CANAL', text='SumVlrAtivo')
    fig_canal.update_traces(textposition='outside', marker_color='#CD092F')
    fig_canal.update_layout(uniformtext_minsize=10, template = 'none', margin = dict(l = 50, r = 20, b = 100))

    # tabs
    if tab_canal == 'tab-a':
        return html.Div(children=[

            dcc.Graph(id = 'graph-canal',
                figure=fig_canal, style = {'height' : '75 %'}
            ),

        ])



if __name__ == '__main__':
    app.run_server(debug=True)
