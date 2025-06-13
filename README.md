# COMPARATIVO: CHUVA GPM - ALERTA RIO

1- Após ter baixado todos os dados do Alerta Rio e do GPM no período escolhido, é necessário padronizar os dados. Colocar os dados do Alerta Rio no padrão OMM e selecionar os dados do GPM nos locais das estações do Alerta Rio. Utilizando o arquivo de configuração com a *localização das estações* (onde estarão as localizações de todas as estações do Alerta Rio que serão utilizadas), através do script *extrai_dados_GPM_locais_estacoes.py*, você terá os dados do GPM nas localizações exatas das estações do Alerta Rio (você poderá criar seu próprio arquivo de configuração com a localização das estações que você deseja comparar). Os dados serão gerados desta forma: _nomedaestação_GPM.csv_. Assim foram geradas as "Estações do GPM".

2 - Para calcular os percentis e gerar os gráficos com a evolução temporal da precipitação será utilizado o script *calcula_percentil_gera_grafico_v2.py*. Utilizando os dados baixados OU gerados anteriormente, somado ao arquivo de configuração, será feito o cálculo do percentil .99 da cidade e para cada uma das estações de forma individual. Por fim, será gerado um gráfico para cada estação na pasta de saída. Será necessário alterar o script para gerar esses gráficos com os dados do Alerta Rio e depois para o GPM, para que no final possa ser feita a comparação.


3 - Para gerar os mapas interpolados:

  A. Para gerar os mapas com a quantidade de dias com chuva acima de 1 mm registrada para cada estação, seja do Alerta Rio ou do GPM, será necessário contabilizar a quantidade de dias com essa precipitação. Para isso será utilizado o script *quantidade_dias_prec.py*, onde será gerado o arquivo com a quantidade de dias onde houve precipitação em cada estação.

  B. Com o script *gera_mapa_interpolado_GPM.py* serão gerados os diversos mapas, cada um representando um limiar de precipitação. Apesar do nome, esse script pode ser facilmente adaptado para utilizar os dados do Alerta Rio. Importante alterar os títulos das figuras também!

4 - Através do script *calcula_acumulado_mensal_anual.py* serão calculados os acumulados mensais e anuais para as estações (importante fazer para as duas fontes) a fim de se criar gráficos por meio do Excel. Após isso, serão utilizados os scripts que geram os bloxplots comparativos entre os dados diários e mensais. 
