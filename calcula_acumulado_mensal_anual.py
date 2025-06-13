# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 13:17:46 2025

@author: Heloisa
"""

import pandas as pd
import os

# Caminho dos arquivos diários já gerados
pasta_diarios = r'C:\Users\and_s\Downloads\TEEP\prec_gpm_estacoes'
arquivos = [f for f in os.listdir(pasta_diarios) if f.endswith('_GPM.csv')]

# Caminhos de saída
saida_mensal = r'C:\Users\and_s\Downloads\TEEP\chuva_mensal_GPM'
saida_anual = r'C:\Users\and_s\Downloads\TEEP\chuva_anual_GPM'
os.makedirs(saida_mensal, exist_ok=True)
os.makedirs(saida_anual, exist_ok=True)

for arquivo in arquivos:
    print(f'Processando {arquivo}...')

    # Ler o arquivo diário
    caminho = os.path.join(pasta_diarios, arquivo)
    df = pd.read_csv(caminho, sep=';')

    # Converter a coluna de data
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

    # Adicionar colunas de mês e ano
    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month

    # Agrupar por ano e mês para calcular acumulado mensal
    mensal = df.groupby(['Ano', 'Mes'])['Precipitacao_mm'].sum().reset_index()
    mensal['Precipitacao_mm'] = mensal['Precipitacao_mm'].round(2)

    # Agrupar por ano para acumulado anual
    anual = df.groupby('Ano')['Precipitacao_mm'].sum().reset_index()
    anual['Precipitacao_mm'] = anual['Precipitacao_mm'].round(2)

    # Salvar arquivos
    nome_base = arquivo.replace('_GPM.csv', '')
    caminho_saida_mensal = os.path.join(saida_mensal, f'{nome_base}_chuva_mensal_GPM.csv')
    caminho_saida_anual = os.path.join(saida_anual, f'{nome_base}_chuva_anual_GPM.csv')

    mensal.to_csv(caminho_saida_mensal, index=False, sep=';')
    anual.to_csv(caminho_saida_anual, index=False, sep=';')

    print(f'Arquivos salvos: {nome_base}_chuva_mensal_GPM.csv e {nome_base}_chuva_anual_GPM.csv')

print('Cálculo de acumulados concluído!')