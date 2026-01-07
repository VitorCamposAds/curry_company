#======================================================================================
#                             Imports
#======================================================================================
import pandas as pd
import streamlit as st
from utils import load_data, clean_data, background, sidebar_filters
from restaurantes_utils import (
    entregadores_unicos_cadastrados, kpi_card, distancia_media_entregas,
    media_entregas_festival, media_entregas_sem_festival, std_com_festival,
    std_entregas_sem_festival, plot_tempo_medio_por_cidade,
    mediaTempo_Cidade_Trafego, pizza, sunburst
)

#======================================================================================
#                           Configuração da Página
#======================================================================================
st.set_page_config(page_title='Visão Restaurantes', page_icon='🍽️', layout='wide')

#======================================================================================
#                           Background
#======================================================================================
background()  # já usa BACKGROUND_PATH do utils.py

#======================================================================================
#                           Título da Página
#======================================================================================
st.markdown("<h1 style='text-align:center;'>Visão Restaurantes</h1>", unsafe_allow_html=True)
st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

#======================================================================================
#                           Carga e Limpeza dos Dados
#======================================================================================
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df1 = load_data(base_dir, "train.csv")
df1 = clean_data(df1)

#======================================================================================
#                           Sidebar com filtros
#======================================================================================
df1 = sidebar_filters(df1)

#======================================================================================
#                           Layout - Cards
#======================================================================================
with st.container():
    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        entregadores_unicos_cadastrados(df1)
    with col2:
        distancia_media_entregas(df1)
    with col3:
        media_entregas_festival(df1)

st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

with st.container():
    col4, col5, col6 = st.columns(3, gap='large')
    with col4:
        media_entregas_sem_festival(df1)
    with col5:
        std_com_festival(df1)
    with col6:
        std_entregas_sem_festival(df1)

#======================================================================================
#                           Layout - Gráficos
#======================================================================================
with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        plot_tempo_medio_por_cidade(df1)
    with col2:
        mediaTempo_Cidade_Trafego(df1)

with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        pizza(df1)
    with col2:
        sunburst(df1)