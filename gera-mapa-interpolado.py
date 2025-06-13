

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import Rbf
import contextily as ctx
import os

# Carregar os dados
csv_path = r'C:\Users\and_s\Downloads\resultado_regressoes.csv'  # Altere se necessário
dados_chuva = pd.read_csv(csv_path, sep=';', encoding='latin1')

# Corrigir vírgulas decimais e converter para float
dados_chuva['Regressao_mm_por_decada'] = dados_chuva['Regressao_mm_por_decada'].str.replace(',', '.').astype(float)


shape_bairros = gpd.read_file(r'C:\Users\and_s\Downloads\RJ_Municipios_2024\Limite_de_Bairros.shp')

# Converter coordenadas para numéricas
dados_chuva['latitude'] = dados_chuva['latitude'].str.replace(',', '.').astype(float)
dados_chuva['longitude'] = dados_chuva['longitude'].str.replace(',', '.').astype(float)

output_dir = os.path.join(os.path.dirname(csv_path), 'mapas_limiares_v2')
os.makedirs(output_dir, exist_ok=True)

# Criar GeoDataFrame para as estações
estacoes = gpd.GeoDataFrame(
    dados_chuva,
    geometry=gpd.points_from_xy(dados_chuva.longitude, dados_chuva.latitude),
    crs=4326
).to_crs(shape_bairros.crs)

# Função para criar mapa interpolado
def criar_mapa_interpolado(coluna, titulo):
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plotar o shapefile dos bairros
    shape_bairros.plot(ax=ax, color='none', edgecolor='black', alpha=0.3)
    
    # Preparar dados para interpolação
    x = estacoes.geometry.x.values
    y = estacoes.geometry.y.values
    z = estacoes[coluna].astype(float).values
    
    # Criar grid para interpolação
    xmin, ymin, xmax, ymax = shape_bairros.total_bounds
    grid_x, grid_y = np.mgrid[xmin:xmax:500j, ymin:ymax:500j]
    
    # Interpolação usando Radial Basis Function
    rbf = Rbf(x, y, z, function='linear')
    grid_z = rbf(grid_x, grid_y)
    
    # Criar máscara para área fora dos bairros
    pontos_grid = gpd.points_from_xy(grid_x.flatten(), grid_y.flatten())
    mask = shape_bairros.geometry.unary_union.contains(pontos_grid)
    grid_z[~mask.reshape(grid_x.shape)] = np.nan
    
    # Plotar a interpolação
    im = ax.imshow(grid_z.T, extent=(xmin, xmax, ymin, ymax), origin='lower',
                  cmap='RdBu', alpha=0.7, vmin=-1, vmax=1)
    
    # Barra de cores
    cbar = fig.colorbar(im, ax=ax, shrink=0.5)
    cbar.set_label('Variação mm/década', fontweight='bold')
    
    # Plotar as estações
    estacoes.plot(ax=ax, color='red', markersize=50, alpha=0.7)
    for idx, row in estacoes.iterrows():
        ax.text(row.geometry.x, row.geometry.y, 
                f"{row[coluna]:.2f} mm",
                fontsize=8, ha='center', va='bottom', color='black',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # Mapa de fundo
    # ctx.add_basemap(ax, crs=shape_bairros.crs)
    
    # Configurações
    ax.set_title('Variação mm/década', fontweight='bold')
    ax.set_axis_off()

    plt.tight_layout()
    output_path = os.path.join(output_dir, f'mapa_{titulo.replace(">","maior_que").replace(" ", "_")}.png')
    plt.savefig(output_path, dpi=300)
    plt.show()

criar_mapa_interpolado('Regressao_mm_por_decada', 'Variação de Chuva (mm/década)')