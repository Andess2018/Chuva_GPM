# -*- coding: utf-8 -*-
"""
Created on Fri May 30 18:12:35 2025

@author: Heloisa
"""

import os
import pandas as pd

# Caminho da pasta com os CSVs
pasta = r'C:\Users\and_s\Downloads\TEEP\prec_gpm_estacoes'

# Lista para armazenar os resultados
resultados = []

# Percorre todos os arquivos CSV da pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(pasta, arquivo)
        
        # Lê o CSV
        try:
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
        except:
            df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8')
        
        # Verifica se a coluna 'Precipitacao_mm' existe
        if 'Precipitacao_mm' not in df.columns:
            print(f'Arquivo {arquivo} não possui a coluna "Precipitacao_mm". Pulando.')
            continue
        
        # Conta os dias acima dos limiares
        dias_1 = (df['Precipitacao_mm'] > 1).sum()
        dias_5 = (df['Precipitacao_mm'] > 5).sum()
        dias_10 = (df['Precipitacao_mm'] > 10).sum()
        dias_25 = (df['Precipitacao_mm'] > 25).sum()
        dias_50 = (df['Precipitacao_mm'] > 50).sum()
        dias_100 = (df['Precipitacao_mm'] > 100).sum()
        
        # Nome da estação (pode ser o nome do arquivo sem extensão)
        estacao = os.path.splitext(arquivo)[0]
        
        # Adiciona o resultado na lista
        resultados.append({
            'Estacao': estacao,
            'Dias >1mm': dias_1,
            'Dias >5mm': dias_5,
            'Dias >10mm': dias_10,
            'Dias >25mm': dias_25,
            'Dias >50mm': dias_50,
            'Dias >100mm': dias_100
        })

# Cria um DataFrame com os resultados
df_resultados = pd.DataFrame(resultados)

# Salva em CSV
saida = os.path.join(pasta, 'quantidade_dias_precipitacao.csv')
df_resultados.to_csv(saida, index=False, sep=';')

print(f'Resumo salvo em {saida}')
