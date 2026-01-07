#=====================================================================================

#                             Imports

#=====================================================================================
import os
import pandas as pd
import re
import plotly.express as px
import streamlit as st
from datetime import datetime
import numpy as np
import matplotlib as plt
#=======================================================================================================


#                           Funções Layout Streamlit


#=======================================================================================================

# kpi cards

def kpi_card(titulo, valor):
    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:12px;
            border-radius:8px;
            background-color:#f5f5f5;
            height:90px;
            display:flex;
            flex-direction:column;
            justify-content:center;
        ">
            <div style="font-size:12px; color:#6c757d; font-weight:bold;">
                {titulo}
            </div>
            <div style="font-size:22px; font-weight:600;">
                {valor}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

#Config design cards:

def config_cards():
    st.markdown(
        "<h1 style='text-align: center;'>Visão Entregadores</h1>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <style>
    .metric-card {
        background-color: #e6f0f5;   /* 👈 mesma cor do Plotly */
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        border-left: 6px solid #4CAF50;

        height: 130px;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .metric-title {
        font-size: 16px;
        font-weight: 700;
        color: #495057;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 32px;
        font-weight: 800;
        color: #212529;
    }

    .metric-good { border-left-color: #2ecc71; }
    .metric-bad  { border-left-color: #e74c3c; }
    .metric-info { border-left-color: #3498db; }
    </style>
    """, unsafe_allow_html=True)


# primeiro card
def entregador_mais_velho(df):
    st.markdown(f"""
        <div class="metric-card metric-info">
            <div class="metric-title">Mais velho</div>
            <div class="metric-value">{df['Delivery_person_Age'].max()}</div>
        </div>
    """, unsafe_allow_html=True)

#segundo card

def entregador_mais_novo(df):
    st.markdown(f"""
        <div class="metric-card metric-info">
            <div class="metric-title">Mais novo</div>
            <div class="metric-value">{df['Delivery_person_Age'].min()}</div>
        </div>
        """, unsafe_allow_html=True)

# terceiro card    
def melhor_veiculo(df):
    st.markdown(f"""
        <div class="metric-card metric-good">
            <div class="metric-title">Melhor veículo</div>
            <div class="metric-value">{df['Vehicle_condition'].max()}</div>
        </div>
        """, unsafe_allow_html=True)
    
# quarto card
def pior_veiculo(df):
    st.markdown(f"""
        <div class="metric-card metric-bad">
            <div class="metric-title">Pior veículo</div>
            <div class="metric-value">{df['Vehicle_condition'].min()}</div>
        </div>
        """, unsafe_allow_html=True)

#primeira tabela
def avaliacao_media_entregador(df):
    st.markdown(
        "<h4 style='text-align: center;'>Avaliação média por entregador</h4>",
        unsafe_allow_html=True
    )

    media_avaliacao = (
        df.groupby("Delivery_person_ID")["Delivery_person_Ratings"]
          .mean()
          .reset_index()
          .rename(columns={
              "Delivery_person_ID": "Entregador",
              "Delivery_person_Ratings": "Avaliação média"
          })
          .sort_values("Avaliação média", ascending=False)
    )

    styled_df = (
        media_avaliacao.style
        # arredondamento VISUAL correto
        .format({"Avaliação média": "{:.2f}"})
        # CORPO DA TABELA → funciona no st.dataframe
        .set_properties(**{
            "background-color": "#e6f0f5",
            "color": "#212529"
        })
        # CABEÇALHO → funciona via set_table_styles
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#e6f0f5"),
                    ("color", "#495057"),
                    ("font-weight", "700")
                ]
            }
        ])
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

#segunda tabela
def avaliacao_media_transito(df: pd.DataFrame):

    st.markdown(
        "<h4 style='text-align: center;'>Avaliação média por condição de trânsito</h4>",
        unsafe_allow_html=True
    )

    media_e_std = (
        df.groupby("Road_traffic_density")["Delivery_person_Ratings"]
        .agg(
            Média="mean",
            Desvio_Padrão="std"
        )
        .reset_index()
        .rename(columns={"Road_traffic_density": "Condição de Trânsito"})
        .round(2)
    )

    styled_df = (
        media_e_std
        .sort_values("Média", ascending=False)
        .style
        .format({
            "Média": "{:.2f}",
            "Desvio_Padrão": "{:.2f}"
        })
        .set_properties(**{
            "background-color": "#e6f0f5",
            "color": "#212529",
            "border-color": "#dee2e6"
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#e6f0f5"),
                    ("color", "#495057"),
                    ("font-weight", "700")
                ]
            }
        ])
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

# terceira tabela (col2)

def avaliacao_por_condicao_climatica(df):

    st.markdown(
        "<h4 style='text-align: center;'>Avaliação média por condição climática</h4>",
        unsafe_allow_html=True
    )

    stats_condicoes_climaticas = (
        df.groupby("Weatherconditions")["Delivery_person_Ratings"]
        .agg(
            Média="mean",
            Desvio_Padrão="std"
        )
        .reset_index()
        .round(2)
    )

    styled_df = (
        stats_condicoes_climaticas
        .sort_values("Média", ascending=False)
        .style
        .format({
            "Média": "{:.2f}",
            "Desvio_Padrão": "{:.2f}"
        })
        .set_properties(**{
            "background-color": "#e6f0f5",
            "color": "#212529",
            "border-color": "#dee2e6"
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#e6f0f5"),
                    ("color", "#495057"),
                    ("font-weight", "700")
                ]
            }
        ])
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    
def top_10_entregadores(df, tipo='rapido'):
    """
    Gera ranking Top 10 de entregadores mais rápidos ou mais lentos (global).
    """

    if tipo == 'rapido':
        agg_func = 'min'
        ascending = True
        titulo = "Entregadores mais rápidos (Top 10)"
    elif tipo == 'lento':
        agg_func = 'max'
        ascending = False
        titulo = "Entregadores mais lentos (Top 10)"
    else:
        st.error("Tipo inválido. Use 'rapido' ou 'lento'.")
        return

    st.markdown(
        f"<h4 style='text-align: center;'>{titulo}</h4>",
        unsafe_allow_html=True
    )

    top_10 = (
        df.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)']
          .agg(agg_func)
          .reset_index()
          .sort_values('Time_taken(min)', ascending=ascending)
          .head(10)
          .rename(columns={
              'City': 'Cidade',
              'Delivery_person_ID': 'Entregador',
              'Time_taken(min)': 'Tempo de Entrega (min)'
          })
    )

    top_10 = top_10[['Entregador', 'Cidade', 'Tempo de Entrega (min)']]
    top_10['Tempo de Entrega (min)'] = top_10['Tempo de Entrega (min)'].round(2)

    styled_df = (
        top_10.style
        # Corpo da tabela
        .set_properties(
            **{
                "background-color": "#e6f0f5",
                "color": "#212529"
            }
        )
        # Cabeçalho
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#e6f0f5"),
                    ("color", "#495057"),
                    ("font-weight", "700")
                ]
            }
        ])
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )
