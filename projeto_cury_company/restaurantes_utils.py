#======================================================================================

#                             Imports

#======================================================================================
import os
import pandas as pd
import re
import plotly.express as px  # Corrigido o 'as px'
import streamlit as st
from datetime import datetime
import numpy as np
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from haversine import haversine, Unit  # Não precisa importar o módulo inteiro 'haversine' novamente
from utils import (load_data, clean_data, load_data,
                   background, sidebar_filters)



# função única para todos os cards
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
    

#====================================================================================

#                           Sidebar streamlit

#====================================================================================

# primeiro card
def entregadores_unicos_cadastrados(df):
    entregadores_unicos = df['Delivery_person_ID'].nunique()
    kpi_card("Entregadores Únicos cadastrados", entregadores_unicos)
    
# segundo card
def distancia_media_entregas(df):
    cols = [
        'Restaurant_latitude',
        'Restaurant_longitude',
        'Delivery_location_latitude',
        'Delivery_location_longitude'
    ]

    df['distance_km'] = df[cols].apply(
        lambda x: haversine(
            (x['Restaurant_latitude'], x['Restaurant_longitude']),
            (x['Delivery_location_latitude'], x['Delivery_location_longitude']),
            unit=Unit.KILOMETERS
        ),
        axis=1
    ).round(2)

    media_distancia = df['distance_km'].mean().round(2)
    kpi_card("Distância Média (km) das Entregas", media_distancia)

# terceiro card
def media_entregas_festival(df):
    festivais = df.loc[df['Festival'] == 'Yes', :]
    tempo_medio_festival = (
            festivais
            .groupby('Festival')['Time_taken(min)']
            .mean()
            .round(2)
            .iloc[0]
        )
    kpi_card("Tempo Médio das Entregas com Festival", tempo_medio_festival)

#quarto card
def media_entregas_sem_festival(df):
    festivais = df.loc[df['Festival'] == 'No', :]
    tempo_medio_sem_festival = (
                festivais
                .groupby('Festival')['Time_taken(min)']
                .mean()
                .round(2)
                .iloc[0]
            )

    kpi_card("Tempo Médio das Entregas sem Festival", tempo_medio_sem_festival)

# quinto card
def std_com_festival(df):
    festivais = df.loc[df['Festival'] == 'Yes', :]
            
    std_com_festival = (
        festivais
        .groupby('Festival')['Time_taken(min)']
            .std()
            .round(2)
            .iloc[0]
        )
    kpi_card("Desvio Padrão das Entregas com Festival", std_com_festival)

# sexto card
def std_entregas_sem_festival(df):
    # Filtra os registros sem festival
    festivais = df.loc[df['Festival'] == 'No', :]
    # Calcula o desvio padrão do tempo de entrega
    std_sem_festival = (
        festivais
        .groupby('Festival')['Time_taken(min)']
        .std()
        .round(2)
        .iloc[0]
    )

    # Exibe o KPI
    kpi_card("Desvio Padrão das Entregas sem Festival", std_sem_festival)

#gráfico de barra com error
def plot_tempo_medio_por_cidade(df):
    # Calcula média e desvio padrão por cidade
    st.markdown('<h4 style="text-align: center;">Média de tempo e Desvio Padrão por cidade</h4>', unsafe_allow_html=True)
    mean_std = (
        df
        .groupby('City')['Time_taken(min)']
        .agg(
            Media_Tempo='mean',
            Desvio_Padrao='std'
        )
        .reset_index()
        .round(2)
    )

    # Renomeia coluna
    mean_std = mean_std.rename(columns={'City': 'Cidade'})

    # Cria gráfico de barras com erro
    fig = px.bar(
        mean_std,
        x='Cidade',
        y='Media_Tempo',
        error_y='Desvio_Padrao',
        labels={
            'Media_Tempo': 'Tempo médio (min)',
            'Cidade': 'Cidade'
        }
    )

    # Configura hover e aparência das barras de erro
    fig.update_traces(
        error_y=dict(
            color='black',   # barrinha preta
            thickness=2,     # espessura da linha
            width=6          # largura do “cap”
        ),
        hovertemplate=
            '<b>Cidade:</b> %{x}<br>' +
            '<b>Tempo médio:</b> %{y} min<br>' +
            '<b>Desvio padrão:</b> %{customdata[0]} min',
        customdata=mean_std[['Desvio_Padrao']]
    )

    # Layout do gráfico com cores de fundo
    fig.update_layout(
        yaxis_title='Tempo (min)',
        xaxis_title='Cidade',
        plot_bgcolor='#e6f0f5',   # fundo do gráfico
        paper_bgcolor='#e6f0f5'   # fundo da área inteira
    )

    # Exibe no Streamlit
    st.plotly_chart(fig, use_container_width=True)

#tabela   
def mediaTempo_Cidade_Trafego(df):
    st.markdown('<h4 style="text-align: center;">Cidade e Densidade de Tráfego por Tipo de Pedido</h4>', unsafe_allow_html=True)
    # Agrupa por Cidade e Tipo de Pedido, calculando média e desvio padrão
    mean_std_2 = (
        df.groupby(['City', 'Type_of_order'])['Time_taken(min)']
          .agg(Media='mean', Desvio_Padrao='std')
          .reset_index()
          .round(2)
    )

    # Renomeia colunas
    mean_std_2 = mean_std_2.rename(columns={
        'City': 'Cidade',
        'Type_of_order': 'Tipo de Pedido'
    })

    # Constrói tabela HTML manualmente para Streamlit
    tabela_html = "<table style='border-collapse: collapse; width: 100%;'>"
    
    # Cabeçalho
    tabela_html += "<thead>"
    tabela_html += "<tr>"
    for col in mean_std_2.columns:
        tabela_html += (
            f"<th style='background-color:#cce0eb; color:black; border:1px solid black; "
            f"padding:5px; text-align:center;'>{col}</th>"
        )
    tabela_html += "</tr></thead>"

    # Linhas da tabela
    tabela_html += "<tbody>"
    for _, row in mean_std_2.iterrows():
        tabela_html += "<tr>"
        for val in row:
            tabela_html += (
                f"<td style='background-color:#e6f0f5; color:black; border:1px solid black; "
                f"padding:5px; text-align:center;'>{val}</td>"
            )
        tabela_html += "</tr>"
    tabela_html += "</tbody></table>"

    st.markdown(tabela_html, unsafe_allow_html=True)
    
def pizza(df):
    st.markdown('<h4 style="text-align: center;">Distância Média de Entrega por Cidade</h4>', unsafe_allow_html=True)
    distancia_cidades = (df
                            .groupby('City', as_index=False)['distance_km']
                            .mean())
    idx_min = distancia_cidades['distance_km'].idxmin()
    pull = [0] * len(distancia_cidades)
    pull[idx_min] = 0.25

    cores = ['#1f77b4', '#2ca02c', '#9467bd', '#17becf', '#ff7f0e', '#8c564b']

    fig1 = px.pie(
                    distancia_cidades,
                    values='distance_km',
                    names='City',
                    color_discrete_sequence=cores,
                    height=400,
                )
    fig1.update_traces(pull=pull, rotation=360, textinfo='label+percent')

    # Adiciona cores de fundo
    fig1.update_layout(
        plot_bgcolor='#e6f0f5',   # fundo da área do gráfico
        paper_bgcolor='#e6f0f5'   # fundo da área total do gráfico
    )

    st.plotly_chart(fig1, use_container_width=True)
#sunburst
def sunburst(df):
    st.markdown('<h4 style="text-align: center;">Tempo Médio Cidade e Densidade de Tráfego</h4>', unsafe_allow_html=True)   
    means_std_3 = (df.groupby(['City', 'Road_traffic_density'])['Time_taken(min)']
                     .agg(Média='mean', Desvio_Padrão='std')
                     .reset_index()
                     .round(2)
                  )

    means_std_3 = means_std_3.rename(columns={
        'City': 'Cidade',
        'Road_traffic_density': 'Densidade de Tráfego',
        'Time_taken(min)': 'Tempo gasto'
    })

    fig2 = px.sunburst(
        means_std_3,
        path=['Cidade', 'Densidade de Tráfego'],
        values='Média',
        color='Desvio_Padrão',
        color_continuous_scale='RdBu_r',
        hover_data={
            'Média': True,
            'Desvio_Padrão': True
        },
        height=400
    )

    # Layout: fundo + título (mesmo padrão do gráfico de pizza)
    fig2.update_layout(
                        paper_bgcolor='#e6f0f5',
                        plot_bgcolor='#e6f0f5',
                      )

    st.plotly_chart(fig2, use_container_width=True)





    