import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import urllib.request
import requests
from PIL import Image
from io import BytesIO

st.title('Variação do Preço por Barril do Petróleo Bruto Brent (FOB)')
# st.write('# Dados')

opcoes_abas = ['Explicação Tech Challenge 4', 'Projeto Final']
aba_selecionada = st.sidebar.selectbox('Escolha uma aba', opcoes_abas)

if aba_selecionada == 'Explicação Tech Challenge 4':
    st.write('# Explicação Tech Challenge 4')
    paragraphs = [
        "Você foi contratado(a) para uma consultoria, e seu trabalho envolve analisar os dados de preço do petróleo Brent, que pode ser encontrado no site do Ipea.",
        "Essa base de dados histórica envolve duas colunas: data e preço (em dólares).",
        "Um grande cliente do segmento pediu para que a consultoria desenvolvesse um dashboard interativo e que gere insights relevantes para tomada de decisão.",
        "Além disso, solicitaram que fosse desenvolvido um modelo de Machine Learning para fazer o forecasting do preço do petróleo e um modelo de Deploy (nesse caso estarei usando o Streamlit).",
        "",
        "Dentro do Streamlit há duas abas: a primeira explicando o Tech Challenge e a segunda com os Dados do Projeto",
        "",
    ]

    for paragraph in paragraphs:
        st.write(paragraph)
    st.write('Clique [aqui](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view) para acessar os dados do IPEA')
    st.write('Clique [aqui](https://www.youtube.com/watch?v=lsGS1SKqSrY) para acessar o link de como foi feito o projeto, no youtube')
    st.write("Clique [aqui](https://github.com/gustafarsoares23/Tech-Challenge-4/tree/main) e acesse todo o conteúdo do trabalho no GitHub")

elif aba_selecionada == 'Projeto Final':
    st.write('# Projeto Final')

    st.write('## Preço do Petróleo')
    paragraphs = [
        "Análise da Flutuação do Preço do Petróleo ao Longo do Tempo.",
        "Este estudo examina a dinâmica do preço do petróleo em diferentes períodos. É possível ajustar as datas de referência e observar a tabela e o gráfico correspondentes à variação do preço conforme a data selecionada."
    ]

    for paragraph in paragraphs:
        st.write(paragraph)

    # Carregar o arquivo Excel usando pandas
    df = pd.read_csv("https://raw.githubusercontent.com/gustafarsoares23/Tech-Challenge-4/main/base_preco_petroleo.csv", sep=';', encoding='latin1')

    # Exibir os dados no Streamlit

    data_inicial_padrao = pd.to_datetime('1987-05-20').date()
    data_final_padrao = pd.to_datetime('2024-05-13').date()

    data_inicial = st.date_input("Data Inicial", value=data_inicial_padrao, min_value=data_inicial_padrao)
    data_final = st.date_input("Data Final", value=data_final_padrao, max_value=pd.to_datetime('2024-05-13').date())

    # Modificando o Nome das Colunas
    df.rename(columns={'Data': 'data', 'Preço do Petróleo': 'preco'}, inplace=True)
    df['preco'] = df['preco'].str.replace(',', '.')
    df['preco'] = df['preco'].astype(float)
    df['data'] = pd.to_datetime(df['data']).dt.date

    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] <= data_final)]

    st.write(df_filtrado)

    x = df_filtrado['data']
    y = df_filtrado['preco']

    plt.plot(df_filtrado['data'], df_filtrado['preco'], marker='o')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.title('Preço ao longo dos anos')
    # plt.show()  # Removido porque st.pyplot será usado

    st.pyplot(plt)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.write('## Prevendo o valor do barril de Petróleo com Prophet')
    paragraphs = [
        "Para prever os valores do barril do Petróleo dos próximos 30 dias eu estudei alguns modelos tradicionais de Machine Learning, como Média Móvel, Arima e também um modelo robusto, o Prophet.",
        "A melhor previsão, entre eles, foi do Prophet, com um MAPE de 15%.",
        "Mas não satisfeito com a previsão, eu estudei mais sobre as flutuações de preço do petróleo e percebi que, em várias datas, e por um período curto de tempo, o preço aumentou ou diminuiu abruptamente, por questões climáticas ou geopolíticas.",
        "Acontece que, essas variações grandes, mas de períodos curtos, interferem muito no modelo de previsão.",
        "Então eu resolvi, ao invés de usar dados desde 1987, usar apenas dados de 2023 e 2024 para previsão do modelo.",
        "Logo, consegui um modelo Prophet Melhor, com MAPE 3%, conforme gráficos abaixo:"
    ]

    for paragraph in paragraphs:
        st.write(paragraph, format='markdown')

    url_predicao = "https://github.com/gustafarsoares23/Tech-Challenge-4/raw/main/Prophet_previsao_2023_2024.png"
    st.image(url_predicao, use_column_width=True, caption="Gráfico de Predição")

    st.write('Fonte: Código Python disponível no Github')
    st.write('Clique [aqui](https://github.com/gustafarsoares23/Tech-Challenge-4/blob/main/Tech_Challenge_4_Machine_Learning_Pre%C3%A7o_do_Petr%C3%B3leo.ipynb)')

    st.markdown("<hr>", unsafe_allow_html=True)

    st.write('<hr>', unsafe_allow_html=True)
    st.write('### Tabela com as previsões dos próximos 30 dias')

    paragraphs = [
        'Na tabela abaixo, você pode ver a previsão dos valores para os próximos 30 dias:'
    ]

    for paragraph in paragraphs:
        st.write(paragraph, format='markdown')

    url_tabelapredicao = 'https://github.com/gustafarsoares23/Tech-Challenge-4/raw/main/tabela%20previs%C3%A3o.png'
    st.image(url_tabelapredicao, use_column_width=True, caption='Tabela com Predição dos Valores')

    st.markdown("<hr>", unsafe_allow_html=True)

    st.write('## Dashboard Power Bi')
    paragraphs = [
        'O Dashboard abaixo mostra as variações do preço do petróleo ao longo dos anos e também explica as variações.',
        'Para acessar todos os recursos, recomendo clicar no link e baixar o arquivo do Power Bi.'
    ]

    for paragraph in paragraphs:
        st.write(paragraph)

    img_url = "https://raw.githubusercontent.com/gustafarsoares23/Tech-Challenge-4/main/Dashboard_Power%20BI.png"

    st.image(img_url, use_column_width=True, caption="Foto do Dashboard Power Bi")

    st.write('Clique [aqui](https://github.com/gustafarsoares23/Tech-Challenge-4/blob/main/An%C3%A1lise%20Pre%C3%A7o%20do%20Petr%C3%B3leo.pbix) para abrir o arquivo Power BI no Github')

    st.markdown("<hr>", unsafe_allow_html=True)

image_url = 'https://raw.githubusercontent.com/gustafarsoares23/Tech-Challenge-4/main/foto%20capa.jpg'

response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

st.image(image,
         width=85,
         output_format='PNG',
         use_column_width=True,
)

st.markdown('<p class="footer"> Tech Challenge 4 - Gustavo Silveira Soares - Grupo 90</p)', unsafe_allow_html=True)
