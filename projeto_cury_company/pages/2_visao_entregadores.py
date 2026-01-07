#=====================================================================================
#                             Imports
#=====================================================================================
import pandas as pd
import streamlit as st
from utils import load_data, clean_data, background, sidebar_filters
from entregadores_utils import (
    entregador_mais_velho, config_cards, entregador_mais_novo,
    melhor_veiculo, pior_veiculo, avaliacao_media_entregador,
    kpi_card, avaliacao_media_transito, avaliacao_por_condicao_climatica,
    top_10_entregadores
)

#======================================================================================
#                           Configuração da Página
#======================================================================================
st.set_page_config(page_title='Visão Entregadores', page_icon='🏍️', layout='wide')

#======================================================================================
#                           Background
#======================================================================================
background()  # já usa BACKGROUND_PATH do utils.py

#======================================================================================
#                           Carga e Limpeza dos Dados
#======================================================================================
# Caminho base do projeto (uma pasta acima da pages/)
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carrega CSV
df1 = load_data(base_dir, "train.csv")
df1 = clean_data(df1)

#======================================================================================
#                           Sidebar com filtros
#======================================================================================
df1 = sidebar_filters(df1)

#======================================================================================
#                           Layout Streamlit - KPIs
#======================================================================================
config_cards()

with st.container():
    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        entregador_mais_velho(df1)
    with col2:
        entregador_mais_novo(df1)
    with col3:
        melhor_veiculo(df1)
    with col4:
        pior_veiculo(df1)

    st.divider()

#======================================================================================
#                           Avaliações
#======================================================================================
with st.container():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        avaliacao_media_entregador(df1)

    with col2:
        avaliacao_media_transito(df1)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        avaliacao_por_condicao_climatica(df1)

#======================================================================================
#                           Top 10 entregadores
#======================================================================================
with st.container():
    col1, col2 = st.columns(2, gap='large')

    with col1:
        top_10_entregadores(df1, tipo='rapido')

    with col2:
        top_10_entregadores(df1, tipo='lento')