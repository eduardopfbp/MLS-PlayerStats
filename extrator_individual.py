import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página
url = "https://fbref.com/pt/partidas/6b8eefb5/Inter-Miami-Real-Salt-Lake-2024Fevereiro21-Major-League-Soccer"

# Faz a requisição para a página
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Função para extrair os dados de uma tabela
def extrair_tabela(rows):
    headers = []
    data = []
    
    for row in rows:
        # Ignora as linhas com a classe "over_header"
        if 'over_header' in row.get('class', []):
            continue
        
        # Verifica se a linha é de cabeçalho ou de dados
        cols = row.find_all(['th', 'td'])
        if len(headers) == 0:  # Primeira linha após "over_header" será o cabeçalho
            headers = [col.get_text(strip=True) for col in cols]
        else:  # Demais linhas são dados
            data.append([col.get_text(strip=True) for col in cols])
    
    # Cria o DataFrame
    return pd.DataFrame(data, columns=headers)

# Encontra todos os containers de tabelas
table_containers = soup.select('div.table_container')

# Lista para armazenar as tabelas extraídas
tabelas = []

# Itera sobre cada container e extrai a tabela
for i, container in enumerate(table_containers):
    rows = container.find_all('tr')
    tabela = extrair_tabela(rows)
    
    # Tenta pegar o título da tabela
    titulo = container.find_previous(['h2', 'h3', 'caption'])
    if titulo:
        nome_tabela = titulo.get_text(strip=True)
    else:
        nome_tabela = f"Tabela {i+1}"  # Caso não tenha título, cria um nome padrão
    
    # Adiciona a tabela com o nome associado
    tabelas.append((nome_tabela, tabela))
# Agora as tabelas estão armazenadas na lista `tabelas`, onde cada item é uma tupla (nome_tabela, DataFrame)

tabelas_desejadas = [tabelas[0]]  # Primeiro DataFrame
if len(tabelas) > 7:
    tabelas_desejadas.append(tabelas[7])  # Oitavo DataFrame

df1 = tabelas_desejadas[0][1]  # Primeiro DataFrame
df2 = tabelas_desejadas[1][1]  # Oitavo DataFrame

# Concatena os dois DataFrames
df_concatenado = pd.concat([df1, df2], ignore_index=True) 