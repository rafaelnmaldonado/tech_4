import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def app():

    st.title('Visualização dos dados')
    st.write('Para que o leitor possa ter a melhor experiência de visualização, dividimos essa etapa em dois tipos de dados: "Recorte longo de 15 anos" e "Ano selecionado. Esta última sessão aparecerá ao final da página, somente se o usuário selecionar um ano no menu abaixo."')


    indice = "BZ=F"
    inicio = "2009-01-01"
    dados_acao = yf.download(indice, inicio) 
    df_cotacoes = pd.DataFrame({indice: dados_acao['Close']}).reset_index()
    df_cotacoes.columns = ['Date', indice]
    df_cotacoes['Date'] = df_cotacoes['Date'].dt.strftime('%Y-%m-%d')
    df_cotacoes = df_cotacoes.rename(columns={'BZ=F': 'Valor por barril'})
    df_cotacoes = df_cotacoes.rename(columns={'Date': 'Periodo'})


    st.subheader('Recorte ao longo de 15 anos')

    st.write('Escolhemos compartilhar os dados de duas formas: tabelas e gráficos. As tabelas foram uma escolha mais voltada a praticidade, pensando na agilidade com que nosso usuário poderia, por exemplo, verificar quantas vezes o menor preço do barril se repetiu ao longo de um ano. Já os gráficos de linha provêm a clareza necessária para analizarmos temporalmente, as quedas e altas de uma commodity que a todo momento tem seu preço afetado pela política e economia.')
    st.write('Separamos alguns momentos dos últimos anos para analisar com mais detalhes: ')
    st.write('- **2010 a 2014 - Os altos preços da guerra:** Em 2010 se inícia uma alta no preço do petróleo do tipo BRENT que atinge o seu pico em abril de 2011. Essa alta está diretamente ligada a Primavera Árabe, momento histórico no qual vários conflitos armados se iniciaram em países do Oriente Médio, afetando, consequentemente, a produção de petróleo dessa região.  ')
    st.write('- **2015 e 2016 - O começo de uma queda vertiginosa:** Em 2015 se inicia uma caída histórica no preço do barril, por conta do crescimento da exploração de xisto nos EUA. Essa movimento de baixa culmina em 2016, nesse ano a oferta do barril de petróleo ao redor do mundo foi maior que a sua demanda, fazendo com que a cotação do barril atingisse o seu valor mais baixo desde 2003, $27.88.')
    st.write('- **2020 - As consequências avassaladoras da pandemia:**  Apesar dos números impressionantes de 2015 e 2016, o preço mais baixo do  barril de petróleo foi registrado em 2020, chegando a 19 dólares. Esse preço foi  decorrência da pandêmia de COVID-19 que fez com que as pessoas se isolassem em suas casas, resultando assim em uma diminuição drástica do uso de combustíveis fósseis ao redor do globo e, consequentemente, na diminuição da demanda de petróleo em todo o planeta.  ')
    st.write('- **2021 e 2022 - Retomada dos preços:** Com as tensões políticas se intensificando entre os países ligados a OTAN, o valor do barril começa a subir a partir de 2021, alcançando o valor de $86. Já em 2022, o preço do barril chega a uma alta histórica com a invasão do território ucraniano pela Rússia, que resultou na suspensão do petróleo russo para os países europeus. ')
    st.write('- **2024 - Situações políticas instáveis e preços promissores:** Em 2024 o preço do petróleo vem apresentando valores(já bateu $88), devido ao aumento da produção industrial da China e a guerra entra Israel e HAMAS que gera um clima de instabilidade entre os países da Opep(Organização dos Países Exportadores de Petróleo) ')


    col1, col2 = st.columns(2)

    col1.dataframe(df_cotacoes)

    df_cotacoes['Periodo'] = pd.to_datetime(df_cotacoes['Periodo'])


    fig = px.line(df_cotacoes,
                x="Periodo",
                y="Valor por barril",
                )
    col2.plotly_chart(fig, use_container_width=True, height=500, width=2000)



    st.subheader("Recorte ano selecionado")
    st.write('Sabemos que depois de olhar o gráfico completo, talvez você sinta curiosidade em entender o que aconteceu em determinado ano, por isso lhe damos a opção de visualizar os preços do barril de petróleo tipo BRENT em um ano específico,então é só escolher um ano e se aprofundar nos dados:')

    unique_years = df_cotacoes['Periodo'].dt.year.unique()
    selected_year = st.selectbox("Selecione o ano:", unique_years, format_func=lambda x: str(x))
    filtered_df = df_cotacoes[df_cotacoes['Periodo'].dt.year == selected_year]


    if(selected_year) > 0:

        col1, col2 = st.columns(2)

        filtered_df['Periodo'] = filtered_df['Periodo'].dt.strftime('%Y-%m-%d')


        fig = px.line(filtered_df,
                    x="Periodo",
                    y="Valor por barril",
                    )

        col2.plotly_chart(fig, use_container_width=True, height=500, width=2000)

        col1.dataframe(filtered_df)