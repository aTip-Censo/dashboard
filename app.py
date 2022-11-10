from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import psycopg2
import os

app = Dash(__name__)

server = app.server

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

# criando o gráfico
fig = px.bar(df, x="companyName", y="qtd_answers", color="companyName", barmode="group",
       labels={
            'companyName': 'Empresa',
            'qtd_answers': 'Quantidade de Respostas'
        })
opcoes = list(df2['companyName'].unique())
opcoes.append("Todas as Empresas")

app.layout = html.Div(children=[
    html.H1(children='Dashboard'),

    html.Div(children='''
        Dashboard gerado através dos formularios de cada empresa.
    '''),

    html.Div(id="texto"),

    dcc.Dropdown(opcoes, value='Todas as Empresas', id='lista_dashboard'),

    dcc.Graph(
        id='grafico_dashboard',
        figure=fig
    )
])

@app.callback(
    Output('grafico_dashboard', 'figure'),
    Input('lista_dashboard', 'value')
)
def update_output(value):
    if value == "Todas as Empresas":
        fig = px.bar(df, x="companyName", y="qtd_answers", color="companyName", barmode="group",         
        labels={
            'companyName': 'Empresa',
            'qtd_answers': 'Quantidade de Respostas'
        })
    else:
        tabela_filtrada = df2.loc[df2['companyName']==value, :]
        fig = px.bar(tabela_filtrada, x="answer", y="appointments", color="questionName", barmode="group",
        labels={
            'questionName': 'Pergunta',
            'appointments': 'Quantidade',
            'answer': 'Resposta'
        },
        height=550
)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)