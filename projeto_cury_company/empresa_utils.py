#=====================================================================================

#                             Imports

#=====================================================================================
import pandas as pd
import streamlit as st
from datetime import datetime
import os
import pandas as pd
import re
import plotly.express as px
import streamlit as st
from datetime import datetime
import numpy as np
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from haversine import haversine, Unit


#=====================================================================================

#                           Visão Empresa

#=====================================================================================

def entregas_dia(df):
    # Texto centralizado
    st.markdown(
        "<h3 style='text-align: center;'>Quantidade de Entregas por dia</h3>",
        unsafe_allow_html=True
    )

    qtde_entregas_dia = (
        df.groupby('Order_Date')['ID']
          .count()
          .reset_index(name='Quantidade de pedidos')
          .sort_values('Order_Date')
    )

    fig = px.bar(
        qtde_entregas_dia,
        x='Order_Date',
        y='Quantidade de pedidos',
        labels={'Order_Date': 'Data', 'Quantidade de pedidos': 'Quantidade de pedidos'},
        hover_data={'Order_Date': '|%d/%m/%Y', 'Quantidade de pedidos': True}
    )

    mediana_diaria = qtde_entregas_dia['Quantidade de pedidos'].median()
    fig.add_hline(
        y=mediana_diaria,
        line_dash='dash',
        annotation_text='Mediana diária',
        annotation_position='top left'
    )

    fig.update_layout(
        bargap=0.15,
        margin=dict(t=70, l=40, r=40, b=60),
        plot_bgcolor='#e6f0f5',
        paper_bgcolor='#e6f0f5'
    )
    fig.update_xaxes(tickformat='%d/%m/%Y', tickangle=-45)
    fig.update_yaxes(title='Quantidade de pedidos')

    st.plotly_chart(fig, use_container_width=True)

def pedidos_cidades_trafego(df):
    # 2. Quantidade de pedidos por cidade e tipo de tráfego
    st.markdown(
        "<h5 style='text-align: center;'>Pedidos por Tráfego e por Cidade</h4>",
        unsafe_allow_html=True
    )
    
    with st.container():
        pedidos_cidade_trafego = (
            df.groupby(['City', 'Road_traffic_density'])['ID']
            .count()
            .reset_index(name='Quantidade de pedidos')
        )

        # Escala logarítmica para melhorar visibilidade de valores baixos
        pedidos_cidade_trafego['Pedidos (log)'] = np.log1p(
            pedidos_cidade_trafego['Quantidade de pedidos']
        )

        fig2 = px.density_heatmap(
            pedidos_cidade_trafego,
            x='City',
            y='Road_traffic_density',
            z='Pedidos (log)',
            color_continuous_scale='Blues',
            labels={
                'City': 'Cidade',
                'Road_traffic_density': 'Tráfego',
                'Pedidos (log)': 'Pedidos (escala log)'
            },
            hover_data={
                'Quantidade de pedidos': True
            }
        )

        # Centralizando o título de forma profissional e aplicando fundo azul acinzentado
        fig2.update_layout(
            margin=dict(t=70, l=40, r=40, b=60),
            plot_bgcolor='#e6f0f5',   # fundo azul acinzentado clarinho
            paper_bgcolor='#e6f0f5'
        )

        st.plotly_chart(fig2, use_container_width=True)

def pedidos_densidade_trafego(df):
    # Título centralizado em Markdown
    st.markdown(
        "<h5 style='text-align: center;'>Entregas por Tráfego</h4>",
        unsafe_allow_html=True
    )

    # Agrupar pedidos por densidade de tráfego
    pedidos_trafego = (
        df.groupby('Road_traffic_density')['ID']
          .count()
          .reset_index(name='Pedidos')
    )

    # Renomear coluna para melhor UX
    pedidos_trafego.rename(
        columns={'Road_traffic_density': 'Densidade de Tráfego'},
        inplace=True
    )

    # Calcular percentual (com proteção contra divisão por zero)
    total_pedidos = pedidos_trafego['Pedidos'].sum()
    if total_pedidos > 0:
        pedidos_trafego['Percentual'] = (
            pedidos_trafego['Pedidos'] / total_pedidos
        ) * 100
    else:
        pedidos_trafego['Percentual'] = 0

    # Ordenar do maior para o menor (melhora leitura)
    pedidos_trafego = pedidos_trafego.sort_values(
        by='Pedidos',
        ascending=False
    )

    # Paleta de cores semântica
    color_map = {
        'Low': '#2ecc71',
        'Medium': '#f1c40f',
        'High': '#e67e22',
        'Jam': '#e74c3c'
    }

    # Criar gráfico de donut (sem título)
    fig = px.pie(
        pedidos_trafego,
        values='Pedidos',
        names='Densidade de Tráfego',
        color='Densidade de Tráfego',
        color_discrete_map=color_map,
        hole=0.4
    )

    # Ajustar rótulos e hover (UX)
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate=(
            '<b>%{label}</b><br>'
            'Pedidos: %{value}<br>'
            'Percentual: %{percent:.1%}'
            '<extra></extra>'
        )
    )

    # Ajustes de layout (removendo título interno)
    fig.update_layout(
        legend_title_text='Densidade de Tráfego',
        margin=dict(t=20, b=20, l=20, r=20),
        plot_bgcolor='#e6f0f5',   # fundo azul acinzentado clarinho
        paper_bgcolor='#e6f0f5'
    )

    # Exibir gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)


def volume_semanal_pedidos(df):
    
    st.markdown(
        "<h3 style='text-align: center;'>Volume semanal de pedidos</h3>",
        unsafe_allow_html=True
    )

    qtde_pedidos_semana = (
        df.groupby('Week_of_the_year')['ID']
          .count()
          .reset_index(name='Pedidos por Semana')
    )

    fig4 = px.line(
        qtde_pedidos_semana,
        x='Week_of_the_year',
        y='Pedidos por Semana',
        markers=True,
        labels={
            'Week_of_the_year': 'Semana do ano',
            'Pedidos por Semana': 'Número de pedidos'
        },
        color_discrete_sequence=['#1f77b4']  # azul consistente
    )

    # Fundo azul acinzentado e margens
    fig4.update_layout(
        plot_bgcolor='#e6f0f5',
        paper_bgcolor='#e6f0f5',
        margin=dict(t=60, b=40, l=40, r=40)
    )

    # Grades mais visíveis
    fig4.update_xaxes(showgrid=True, gridcolor='#cccccc', gridwidth=1)
    fig4.update_yaxes(showgrid=True, gridcolor='#cccccc', gridwidth=1)

    st.plotly_chart(fig4, use_container_width=True)

def media_pedidos_entregador_semanal(df):
    st.markdown(
        "<h3 style='text-align: center;'>Média de pedidos por entregador (semanal)</h3>",
        unsafe_allow_html=True
    )

    # Pedidos por semana
    pedidos_semana = (
        df.groupby('Week_of_the_year')['ID']
          .count()
          .reset_index(name='Pedidos')
    )

    # Entregadores únicos por semana
    entregadores_semana = (
        df.groupby('Week_of_the_year')['Delivery_person_ID']
          .nunique()
          .reset_index(name='Entregadores')
    )

    # Média de pedidos por entregador
    juncao_dfs = pd.merge(pedidos_semana, entregadores_semana, on='Week_of_the_year')
    juncao_dfs['Pedidos por Entregador'] = juncao_dfs['Pedidos'] / juncao_dfs['Entregadores']

    fig = px.line(
        juncao_dfs,
        x='Week_of_the_year',
        y='Pedidos por Entregador',
        markers=True,
        labels={
            'Week_of_the_year': 'Semana do ano',
            'Pedidos por Entregador': 'Pedidos médios'
        },
        color_discrete_sequence=['#1f77b4']  # azul consistente
    )

    # Fundo azul acinzentado e margens
    fig.update_layout(
        plot_bgcolor='#e6f0f5',
        paper_bgcolor='#e6f0f5',
        margin=dict(t=60, b=40, l=40, r=40)
    )

    # Grades mais visíveis
    fig.update_xaxes(showgrid=True, gridcolor='#cccccc', gridwidth=1)
    fig.update_yaxes(showgrid=True, gridcolor='#cccccc', gridwidth=1)

    st.plotly_chart(fig, use_container_width=True)



def mapa_cidades(df):
    # Localização central (mediana) por cidade e tráfego
    st.markdown(
            """
            <div style="text-align: center;">
                <h3>Cidades</h3>
            </div>
            """,
            unsafe_allow_html=True
    )
    mediana = (
        df.groupby(['City', 'Road_traffic_density'])[
            ['Delivery_location_latitude', 'Delivery_location_longitude']
        ]
        .median()
        .reset_index()
    )

    # Criar mapa base
    mapa = folium.Map()

    # Adicionar marcadores
    for _, location_info in mediana.iterrows():
        popup_html = f"""
        <b>Cidade:</b> {location_info['City']}<br>
        <b>Tráfego:</b> {location_info['Road_traffic_density']}<br>
        <b>Latitude:</b> {location_info['Delivery_location_latitude']:.5f}<br>
        <b>Longitude:</b> {location_info['Delivery_location_longitude']:.5f}
        """

        folium.Marker(
            location=[
                location_info['Delivery_location_latitude'],
                location_info['Delivery_location_longitude']
            ],
            popup=popup_html,
            tooltip=location_info['City']
        ).add_to(mapa)

    # Renderizar no Streamlit
    folium_static(mapa, width=1024, height=600)