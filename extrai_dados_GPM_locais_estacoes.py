# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 16:17:49 2025

@author: and_s
"""

import os
import xarray as xr
import pandas as pd
import numpy as np

# --- CONFIGURAÇÕES ---
dir_base = r'C:\Users\and_s\Downloads\TEEP\sat'
arquivo_estacoes = r'C:\Users\and_s\Downloads\TEEP\configuracao-loc-estacoes.xlsx'
saida_dir = r'C:\Users\and_s\Downloads\TEEP\prec_gpm_estacoes'
os.makedirs(saida_dir, exist_ok=True)

# !!! PASSO MAIS IMPORTANTE !!!
# Verifique a unidade 'units' nos metadados do seu arquivo.
# Se for 'mm/hr' ou 'mm h-1', use 24.0.
# Se for 'mm', 'mm/day' ou 'kg m-2' (equivalente a mm), use 1.0.
FATOR_CONVERSAO = 1.0 # Altere para 24.0 se a unidade for mm/hr

# Nome da variável de precipitação
VARIAVEL_PREC = 'precipitation'

# --- INÍCIO DO SCRIPT ---
print(f"Usando FATOR_CONVERSAO = {FATOR_CONVERSAO}")

# Leitura mais direta e segura das coordenadas
try:
    df_estacoes = pd.read_excel(arquivo_estacoes, decimal=',')
    df_estacoes = df_estacoes[['arquivo', 'estação', 'latitude', 'longitude']]
except Exception as e:
    print(f"Erro ao ler arquivo de estações: {e}")
    exit()

dados_estacoes = {nome: [] for nome in df_estacoes['estação']}

for ano in range(2010, 2024):
    pasta_ano = os.path.join(dir_base, str(ano))
    if not os.path.isdir(pasta_ano):
        continue

    # Filtro de arquivo mais genérico para .nc ou .nc4
    arquivos_nc = sorted([f for f in os.listdir(pasta_ano) if f.endswith(('.nc', '.nc4', '.nc4.nc4'))])
    print(f'\nProcessando ano {ano} com {len(arquivos_nc)} arquivos...')

    for arq in arquivos_nc:
        caminho_arq = os.path.join(pasta_ano, arq)

        try:
            # Usar 'with' garante que o arquivo será fechado automaticamente
            with xr.open_dataset(caminho_arq) as ds:
                # 1. Corrigir e ordenar longitudes do GPM, se necessário
                if np.any(ds['lon'] > 180):
                    ds = ds.assign_coords(lon=(((ds['lon'] + 180) % 360) - 180))
                    ds = ds.sortby('lon') # Essencial para o .sel() funcionar bem

                # 2. Extrair data do nome do arquivo
                nome = os.path.basename(arq)
                data_str = nome.split('.')[4].split('-')[0]
                data = pd.to_datetime(data_str, format='%Y%m%d')

                # 3. Iterar pelas estações e extrair dados com .sel()
                for _, linha in df_estacoes.iterrows():
                    estacao = linha['estação']
                    lat0, lon0 = linha['latitude'], linha['longitude']
                    
                    try:
                        # Método idiomático do xarray para selecionar o ponto mais próximo
                        ponto_proximo = ds[VARIAVEL_PREC].sel(lat=lat0, lon=lon0, method='nearest')
                        
                        # Extrair o valor e aplicar o fator de conversão
                        valor_bruto = ponto_proximo.item(0) # .item(0) para pegar o primeiro valor se houver dim de tempo
                        valor_final = np.nan if np.isnan(valor_bruto) else valor_bruto * FATOR_CONVERSAO

                    except (KeyError, IndexError) as e:
                        print(f"Aviso: Não foi possível extrair dados para {estacao} no arquivo {arq}. Erro: {e}")
                        valor_final = np.nan

                    dados_estacoes[estacao].append({
                        'Data': data,
                        'Precipitacao_mm': valor_final
                    })
        except Exception as e:
            print(f"Erro ao abrir ou processar o arquivo {arq}: {e}")
            continue

# Salvar arquivos CSV por estação
print('\nSalvando os dados...')
for estacao, dados in dados_estacoes.items():
    if not dados:
        print(f"Nenhum dado processado para a estação: {estacao}")
        continue
    
    df = pd.DataFrame(dados)
    df.sort_values('Data', inplace=True)
    nome_seguro = "".join(c if c.isalnum() or c in " _-" else "_" for c in estacao)
    caminho_saida = os.path.join(saida_dir, f'{nome_seguro}_GPM.csv')
    
    df.to_csv(
        caminho_saida,
        index=False,
        sep=';',
        float_format='%.2f',
        date_format='%d/%m/%Y'
    )
    print(f'Dados salvos para a estação: {estacao}')

print('\nProcessamento concluído!')