import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt


def app():

    st.title('Modelo')
    
    st.write('A previsão de preços de petróleo representa um desafio significativo devido à sua alta variância e inconstância. Essa volatilidade é influenciada por uma miríade de fatores, incluindo eventos geopolíticos, variações na oferta e demanda, e flutuações econômicas globais. Para enfrentar esse desafio, utilizamos a abordagem de séries temporais, um método poderoso e amplamente utilizado para análise e previsão de dados sequenciais ao longo do tempo.')

    st.write('Foram utilizados, para esta previsão, os dados históricos de preços (em R$) desde 2009, conforme o gráfico a seguir:')

    DATA_FINAL_TREINO = '11-01-2023'
    indice = "BZ=F"
    inicio = "2009-01-01"
    dados_acao = yf.download(indice, inicio)
    df_cotacoes = pd.DataFrame({indice: dados_acao['Close']})
    df = df_cotacoes
    df.index.name = 'ds'
    df.rename(columns={'BZ=F': 'y'}, inplace=True)
    treino = df.loc[df.index < DATA_FINAL_TREINO]
    teste = df.loc[df.index >= DATA_FINAL_TREINO]
    
    df_treino_teste = df_cotacoes.copy()
    df_treino_teste['Conjunto de treinamento'] = treino
    df_treino_teste['Conjunto de teste'] = teste
    df_treino_teste = df_treino_teste[['Conjunto de treinamento', 'Conjunto de teste']]

    def adiciona_periodos(df):
        df = df.copy()
        df['dia_do_ano'] = df.index.dayofyear
        df['dia_do_mes'] = df.index.day
        df['dia_da_semana'] = df.index.dayofweek
        df['trimestre'] = df.index.quarter
        df['mes'] = df.index.month
        df['ano'] = df.index.year
        df['semana_do_ano'] = df.index.isocalendar().week
        return df

    df = adiciona_periodos(df)
    treino = adiciona_periodos(treino)
    teste = adiciona_periodos(teste)

    PERIODOS = ['dia_do_ano', 'dia_do_mes', 'dia_da_semana', 'trimestre', 'mes', 'ano', 'semana_do_ano']
    Y = 'y'

    X_treino = treino[PERIODOS]
    Y_treino = treino[Y]

    X_teste = teste[PERIODOS]
    Y_teste = teste[Y]

    reg = xgb.XGBRegressor(base_score=0.5,
                        booster='gbtree',
                        objective='reg:tweedie',
                        max_depth=3,
                        learning_rate=1.5)
    reg.fit(X_treino, Y_treino,
            eval_set=[(X_treino, Y_treino), (X_teste, Y_teste)],
            verbose=100)

    relevancia_periodos = pd.DataFrame(data=reg.feature_importances_,
                index=reg.feature_names_in_,
                columns=['relevancia'])

    df_cotacoes.rename(columns={'y': 'Valor por barril (R$)'}, inplace=True)
    df_cotacoes['Período'] = df_cotacoes.index
    st.line_chart(df_cotacoes, x='Período', y='Valor por barril (R$)')
    
    st.subheader('Conjunto de Dados e Preparo')
    st.write('Dada a natureza volátil dos preços do petróleo, uma atenção especial foi dedicada ao preparo dos conjuntos de dados de treinamento e teste. O conjunto de treinamento foi substancialmente maior que o de teste. Essa decisão foi baseada na necessidade de fornecer ao modelo uma quantidade significativa de dados históricos para capturar os padrões complexos e as tendências subjacentes aos preços do petróleo.')
    
    df_treino_teste['Período'] = df_treino_teste.index
    st.line_chart(df_treino_teste, x='Período', y=['Conjunto de treinamento', 'Conjunto de teste'])
    
    st.subheader('Abordagem de Séries Temporais')
    st.write('A escolha da abordagem de séries temporais para este problema foi baseada em várias razões fundamentais. Primeiramente, os preços do petróleo são inerentemente sequenciais, com cada valor dependente dos valores anteriores, o que torna a análise temporal particularmente apropriada. As séries temporais permitem modelar as dependências e autocorrelações dentro dos dados, capturando tanto padrões de curto prazo quanto tendências de longo prazo.')

    teste['resultado'] = reg.predict(X_teste)
    df = df.merge(teste[['resultado']], how='left', left_index=True, right_index=True)
    ax = df['y'].plot(figsize=(18, 6))
    df['resultado'].plot(ax=ax, style='-')
    plt.legend(['Dados', 'Previsões'])
    ax.set_title('Petróleo')

    mape = mean_absolute_percentage_error(df.loc[df.index > DATA_FINAL_TREINO]['y'], df.loc[df.index > DATA_FINAL_TREINO]['resultado'])

    st.subheader('Resultados')
    
    df = df[['y', 'resultado']]
    df.rename(columns={'y': 'Dados', 'resultado': 'Previsão'}, inplace=True)
    df['Período'] = df.index
    
    st.line_chart(df, x='Período', y=['Dados', 'Previsão'])
    st.text(f'MAPE: {mape*100:.3f}%')
    
    st.write('Os resultados da previsão foram satisfatórios. O modelo conseguiu capturar com precisão as tendências gerais e algumas flutuações significativas dos preços do petróleo. A avaliação do desempenho foi realizada utilizando a métrica MAPE (Erro Percentual Absoluto Médio).')
    
    st.subheader('Conclusão')
    
    st.write('A previsão de preços do petróleo é inerentemente complexa devido à sua alta variabilidade. No entanto, a abordagem de séries temporais demonstrou ser uma ferramenta eficaz para esse desafio. A utilização de um conjunto de treinamento extenso, em comparação ao conjunto de teste reduzido, permitiu ao modelo aprender melhor os padrões históricos dos preços. Os resultados satisfatórios reforçam a viabilidade de utilizar técnicas avançadas de séries temporais para previsões econômicas, oferecendo insights valiosos para investidores e formuladores de políticas.')