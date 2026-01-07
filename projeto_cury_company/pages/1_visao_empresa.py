#======================================================================================
#                             Imports
#======================================================================================
import os
import pandas as pd
import streamlit as st
from utils import load_data, clean_data, background, sidebar_filters
from empresa_utils import (
    entregas_dia, pedidos_cidades_trafego, pedidos_densidade_trafego,
    volume_semanal_pedidos, media_pedidos_entregador_semanal, mapa_cidades
)

#======================================================================================
#                           Configuração da Página
#======================================================================================
st.set_page_config(page_title='Visão Empresa', page_icon='📊', layout='wide')

#======================================================================================
#                           Background
#======================================================================================
background()  # usa BACKGROUND_PATH do utils.py

#======================================================================================
#                           Título da Página
#======================================================================================
st.markdown("<h1 style='text-align: center;'>Visão Empresa</h1>", unsafe_allow_html=True)

#======================================================================================
#                           Carga e Limpeza dos Dados
#======================================================================================
# Caminho base do projeto
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carrega CSV corretamente
df1 = load_data(base_dir, "train.csv")
df1 = clean_data(df1)

#======================================================================================
#                           Filtros Sidebar
#======================================================================================
df1 = sidebar_filters(df1)

#======================================================================================
#                           Layout Streamlit
#======================================================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        entregas_dia(df1)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            pedidos_cidades_trafego(df1)
        with col2:
            pedidos_densidade_trafego(df1)

with tab2:
    # Garantir coluna da semana
    if 'Week_of_the_year' not in df1.columns:
        df1['Week_of_the_year'] = df1['Order_Date'].dt.isocalendar().week

    with st.container():
        volume_semanal_pedidos(df1)

    with st.container():
        media_pedidos_entregador_semanal(df1)

with tab3:
    with st.container():
        mapa_cidades(df1)
