# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 23:50:27 2025

@author: Heloisa
"""

import pandas as pd
import glob
import os
import numpy as np
import matplotlib.pyplot as plt

# Caminho para a pasta dos dados
caminho = r'C:\Users\and_s\Downloads\TEEP\prec_gpm_estacoes'

# Lista dos arquivos CSV
arquivos = glob.glob(os.path.join(caminho, '*.csv'))

# Carrega a tabela de configuração com os nomes das estações
tabela_estacoes = pd.read_excel(
    r'C:\Users\and_s\Downloads\TEEP\configuracao-loc-estacoes.xlsx'
)

# Cria um dicionário para mapear nome do arquivo -> nome da estação
mapa_nome_estacao = dict(
    zip(tabela_estacoes['arquivo'], tabela_estacoes['estação'])
)

# Calcula os percentis
percentil_99_estacoes = {}
todos_dados = []

# Primeiro loop para calcular percentis
for arquivo in arquivos:
    df = pd.read_csv(arquivo, sep=';', encoding='utf-8')

    if 'Precipitacao_mm' in df.columns:
        # Remove NaN e valores menores que 0.9 mm
        dados_precip = df['Precipitacao_mm'].dropna()
        dados_precip = dados_precip[dados_precip >= 0.9]

        p99 = np.percentile(dados_precip, 99)

        nome_arquivo = os.path.basename(arquivo).replace('.csv', '')

        percentil_99_estacoes[nome_arquivo] = p99

        todos_dados.extend(dados_precip.tolist())

# Percentil 99 da cidade
percentil_99_cidade = np.percentile(todos_dados, 99)

# Pasta para salvar os gráficos
pasta_saida = os.path.join(
    r'C:\Users\and_s\Downloads\TEEP', 'graficos_precipitacao_percentil_GPM'
)
os.makedirs(pasta_saida, exist_ok=True)

# Loop para gerar gráficos por estação
for arquivo in arquivos:
    df = pd.read_csv(arquivo, sep=';', encoding='utf-8')

    if {'Data', 'Precipitacao_mm'}.issubset(df.columns):
        nome_arquivo = os.path.basename(arquivo).replace('.csv', '')

        # Pega o nome da estação usando o mapeamento
        nome_estacao = mapa_nome_estacao.get(nome_arquivo, nome_arquivo)

        # Converte a coluna Data para datetime
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

        # Ordena por data
        df = df.sort_values('Data')

        # Dados
        datas = df['Data']
        precip = df['Precipitacao_mm']

        # Percentil da estação
        p99_est = percentil_99_estacoes[nome_arquivo]

        # Faz o gráfico
        plt.figure(figsize=(15, 6))
        plt.bar(datas, precip, color='blue', label='Precipitação diária')

        # Linhas dos percentis
        plt.axhline(p99_est, color='red', linestyle='--',
                    label=f'P99 Estação ({p99_est:.1f} mm)')
        plt.axhline(percentil_99_cidade, color='darkolivegreen',
                    linestyle='-.', label=f'P99 Cidade ({percentil_99_cidade:.1f} mm)')

        # Títulos e labels
        plt.title(f'Precipitação diária - {nome_estacao}', fontsize=14,fontweight='bold')
        plt.ylim(0,275)
        plt.xlabel('Data',fontweight='bold')
        plt.ylabel('Precipitação diária (mm)',fontweight='bold')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        # Melhora no eixo x para datas
        plt.xticks(rotation=45)

        # Salva o gráfico
        caminho_saida = os.path.join(pasta_saida, f'{nome_arquivo}.png')
        plt.tight_layout()
        plt.savefig(caminho_saida, dpi=300)
        plt.close()

        print(f'✅ Gráfico salvo para {nome_estacao}')
    else:
        print(f'⚠️ Arquivo {arquivo} não possui as colunas necessárias.')

print('\n🚀 Todos os gráficos foram gerados e salvos na pasta:')
print(pasta_saida)