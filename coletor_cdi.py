import csv
import json
import os
import time
from datetime import datetime
from random import uniform
from sys import argv

import pandas as pd
import requests
import seaborn as sns

# URL da API do Banco Central para obter a taxa CDI
API_URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

# Função para buscar a taxa CDI na API
def obter_taxa_cdi():
    try:
        resposta = requests.get(url=API_URL)
        resposta.raise_for_status()
    except requests.HTTPError as erro_http:
        print("Erro HTTP ao acessar a API. Continuando.")
        return None
    except Exception as erro:
        print("Erro geral ao acessar a API. Parando a execução.")
        raise erro
    else:
        return json.loads(resposta.text)[-1]['valor']

# Função para criar e gravar o arquivo CSV com os dados da taxa CDI
def criar_csv():
    taxa_cdi = obter_taxa_cdi()

    for _ in range(10):
        timestamp_atual = datetime.now()
        data_formatada = timestamp_atual.strftime('%Y/%m/%d')
        hora_formatada = timestamp_atual.strftime('%H:%M:%S')
        taxa = float(taxa_cdi) + (uniform(-0.5, 0.5))

        # Verifica se o arquivo CSV existe; caso contrário, cria com cabeçalho
        if not os.path.isfile('./dados_cdi.csv'):
            with open('./dados_cdi.csv', mode='w', encoding='utf-8') as arquivo:
                arquivo.write('data,hora,taxa\n')

        # Adiciona os dados ao CSV
        with open('./dados_cdi.csv', mode='a', encoding='utf-8') as arquivo:
            arquivo.write(f'{data_formatada},{hora_formatada},{taxa}\n')

        time.sleep(1)

    print("Arquivo CSV gerado com sucesso.")

# Função para gerar um gráfico e salvar como imagem PNG
def plotar_grafico(nome_imagem):
    dataframe = pd.read_csv('./dados_cdi.csv')

    # Criando o gráfico de linha
    grafico = sns.lineplot(x=dataframe['hora'], y=dataframe['taxa'])
    grafico.set_xticklabels(labels=dataframe['hora'], rotation=90)
    grafico.get_figure().savefig(f"{nome_imagem}.png")
    print(f"Gráfico salvo como {nome_imagem}.png")

# Função principal para executar todas as tarefas
def executar():
    if len(argv) < 2:
        print("Por favor, informe o nome do gráfico como argumento.")
        return

    nome_imagem = argv[1]

    # Cria o CSV com os dados da taxa CDI
    criar_csv()

    # Gera o gráfico com o nome fornecido
    plotar_grafico(nome_imagem)

if __name__ == "__main__":
    executar()
