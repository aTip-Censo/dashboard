import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
TB_NAME = os.environ.get("TB_NAME")
TB_NAME2 = os.environ.get("TB_NAME2")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

df = pd.read_sql_query("select * from {}".format(TB_NAME), con=conn)

df2 = pd.read_sql_query("select * from {}".format(TB_NAME2), con=conn)

dash.register_page(__name__)

fig = px.pie(df, values="qtd_answers", names="companyName", 
             title='Dashboard', hover_data=['companyName']) 

opcoes = list(df2['questionName'].unique())
opcoes.append("Todas as Empresas")

layout = html.Div(children=[
    html.H1(children='Dashboard'),

    html.Div(children='''
        Dashboard gerado através dos formularios de cada empresa.
    '''),

    html.Div(id="texto"),

    dcc.Dropdown(opcoes, value='Todas as Empresas', id='lista_pie'),

    dcc.Graph(
        id='grafico_pie',
        figure=fig
    )
])

@callback(
    Output('grafico_pie', 'figure'),
    Input('lista_pie', 'value')
)
def update_output(value):
    if value == "Todas as Empresas":
        fig = px.pie(df, values="qtd_answers", names="companyName", 
             title=value, hover_data=['companyName']) 
    else:
        tabela_filtrada = df2.loc[df2['questionName']==value, :]
        fig = px.pie(tabela_filtrada, values="appointments", names="answer", title=value, hover_data=['questionName'],
)
    return fig