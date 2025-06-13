import os
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Caminhos
dados_dir = r"C:\Users\and_s\Downloads\TEEP\sat"  # pasta base onde tem as subpastas dos anos
shapefile_path = r"C:\Users\and_s\Downloads\TEEP\RJ_Municipios_2024\Limite_de_Bairros.shp"
saida_dir = r"C:\Users\and_s\Downloads\TEEP\GPM_anual_mapas"  # pasta para salvar as imagens

# Cria pasta de saída caso não exista
os.makedirs(saida_dir, exist_ok=True)

# Carrega shapefile do município do Rio de Janeiro
rio = gpd.read_file(shapefile_path)
rio = rio.to_crs("EPSG:4326")  # garantir CRS certo

def somar_precipitacao_anual(ano):
    pasta_ano = os.path.join(dados_dir, str(ano))
    if not os.path.exists(pasta_ano):
        print(f"Pasta do ano {ano} não existe. Pulando.")
        return None

    arquivos = sorted([os.path.join(pasta_ano, f) for f in os.listdir(pasta_ano) if f.lower().endswith((".nc", ".nc4"))])

    if not arquivos:
        print(f"0 arquivos encontrados para o ano {ano}")
        return None

    acumulado = None

    for arq in arquivos:
        ds = xr.open_dataset(arq)
        chuva = ds['precipitation'].squeeze().transpose('lat', 'lon')
        chuva = chuva.rio.write_crs("EPSG:4326", inplace=False)
        chuva = chuva.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=False)

        if acumulado is None:
            acumulado = chuva
        else:
            acumulado += chuva

    return acumulado

def plotar_chuva_zoom(chuva, municipio, ano):
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_title(f"Precipitação anual {ano}", fontsize=14)

    vmin = 800       # valor mínimo da escala (ajuste conforme necessário)
    vmax = 1800       # valor máximo da escala (ajuste conforme necessário)
    cmap = 'YlGnBu'    # colormap

    im = chuva.plot(
        ax=ax,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        cbar_kwargs={
            'label': 'Precipitação acumulada (mm)',
            'shrink': 0.7,
            'aspect': 30,
            'pad': 0.02
        },
        transform=ccrs.PlateCarree(),
        add_labels=False 
    )

    municipio.boundary.plot(ax=ax, edgecolor='Black', linewidth=1)

    minx, miny, maxx, maxy = municipio.total_bounds
    ax.set_extent([minx, maxx, miny, maxy], crs=ccrs.PlateCarree())

    ax.coastlines()

    # Salva a figura antes de mostrar
    plt.savefig(os.path.join(saida_dir, f"precipitacao_{ano}.png"), bbox_inches='tight', dpi=150)
    plt.show()
    plt.close(fig)  # libera memória

# Loop para processar todos os anos
for ano in range(2010, 2025):
    print(f"Processando o ano {ano}...")
    try:
        chuva_ano = somar_precipitacao_anual(ano)
        if chuva_ano is None:
            print(f"Nenhum dado para o ano {ano}, pulando...")
            continue

        plotar_chuva_zoom(chuva_ano, rio, ano)

    except Exception as e:
        print(f"Erro no ano {ano}: {e}")
