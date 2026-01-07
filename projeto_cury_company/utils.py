import os
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
import base64

# ==============================================================================
#                               CAMINHOS DO PROJETO
# ==============================================================================

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pasta de logos e imagens
LOGO_DIR = os.path.join(BASE_DIR, "logo")

# Caminhos específicos
LOGO_PATH = os.path.join(LOGO_DIR, "logo.png")
BACKGROUND_PATH = os.path.join(LOGO_DIR, "background.jpg")

# Função utilitária para gerar caminhos
def get_path(*args) -> str:
    """Gera o caminho absoluto a partir da raiz do projeto."""
    return os.path.join(BASE_DIR, *args)


# ==============================================================================
#                               CARGA DOS DADOS
# ==============================================================================

def load_data(folder_path: str, filename: str) -> pd.DataFrame:
    """Carrega um arquivo CSV a partir de um diretório informado."""
    file_path = os.path.join(folder_path, filename)
    return pd.read_csv(file_path)


# ==============================================================================
#                               LIMPEZA DOS DADOS
# ==============================================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza limpeza e padronização do dataframe."""
    
    # Idade do entregador
    df = df[df['Delivery_person_Age'] != 'NaN '].copy()
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(int)

    # Avaliação do entregador
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)

    # Data do pedido
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')

    # Múltiplas entregas
    df = df[df['multiple_deliveries'] != 'NaN '].copy()
    df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)

    # Remoção de espaços em colunas categóricas
    string_columns = [
        'ID', 'Delivery_person_ID', 'Road_traffic_density',
        'Type_of_order', 'Type_of_vehicle', 'Festival', 'City'
    ]
    for col in string_columns:
        df[col] = df[col].str.strip()

    # Remoção de valores inválidos
    df = df[df['City'] != 'NaN']
    df = df[df['Weatherconditions'] != 'conditions NaN']
    df = df[df['Type_of_vehicle'] != 'NaN']

    # Tempo de entrega
    df['Time_taken(min)'] = df['Time_taken(min)'].str.extract(r'(\d+)').astype(int)

    return df


# ==============================================================================
#                               SIDEBAR (STREAMLIT)
# ==============================================================================

def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Cria filtros da sidebar do Streamlit e aplica ao dataframe."""

    # Exibe logo na sidebar
    image = Image.open(LOGO_PATH)
    st.sidebar.image(image, width=120)

    st.sidebar.markdown('# Curry Company')
    st.sidebar.markdown('## Fastest Delivery in Town')
    st.sidebar.markdown('---')

    # Filtro de data
    st.sidebar.markdown('## Selecione uma data')
    date_slider = st.sidebar.slider(
        'Até qual valor',
        value=datetime(2022, 4, 13),
        min_value=datetime(2022, 3, 1),
        max_value=datetime(2022, 3, 31),
        format='DD-MM-YYYY'
    )

    st.sidebar.markdown('---')

    # Filtro de trânsito
    traffic_options = st.sidebar.multiselect(
        'Quais as condições do trânsito',
        ['Low', 'Medium', 'High', 'Jam'],
        default=['Low', 'Medium', 'High', 'Jam']
    )

    st.sidebar.markdown('---')
    st.sidebar.markdown('### Powered by @vitorcampos')

    # Aplicação dos filtros
    df = df[df['Order_Date'] < date_slider]
    df = df[df['Road_traffic_density'].isin(traffic_options)]

    return df


# ==============================================================================
#                               BACKGROUND
# ==============================================================================

def background(image_file: str = BACKGROUND_PATH):
    """Adiciona imagem de fundo ao Streamlit."""
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
#                               CONFIGURAÇÕES PÁGINA HOME
# ==============================================================================

def setup_page(title: str, icon: str):
    """Configura título e ícone da página Streamlit."""
    st.set_page_config(page_title=title, page_icon=icon)

def setup_sidebar(logo_path: str = LOGO_PATH, company_name: str = "Curry Company", slogan: str = "Fastest Delivery in Town"):
    """Configura sidebar da página home."""
    image = Image.open(logo_path)
    st.sidebar.image(image, width=120)
    st.sidebar.markdown(f'# {company_name}')
    st.sidebar.markdown(f'## {slogan}')
    st.sidebar.markdown('---')

def home_text():
    """Exibe conteúdo principal do dashboard."""
    st.write("# Dashboard Curry Company")
    st.markdown("""
    Este dashboard foi desenvolvido para acompanhar as métricas de crescimento da empresa **Curry Company**, cujo modelo de negócio é o de *marketplace*.
    Ele apresenta três visões principais: **Empresa**, **Entregadores** e **Restaurantes**.

    ---

    ### 🧭 Como utilizar o dashboard
    - Utilize o **menu lateral** para navegar entre as diferentes visões disponíveis.
    - Em cada visão, aplique os **filtros interativos** para ajustar a análise conforme o período ou critério desejado.
    - Os gráficos e indicadores são atualizados **automaticamente** de acordo com os filtros selecionados.
    - Para uma análise mais detalhada, explore cada visão de forma individual.

    ---

    ### 🔹 Visão Empresa
    - **Visão Gerencial**: métricas gerais de comportamento
    - **Visão Geográfica**: insights de localização
    - **Visão Tática**: indicadores semanais de crescimento

    ### 🔹 Visão Entregadores
    Acompanhamento dos indicadores semanais de crescimento

    ### 🔹 Visão Restaurantes
    Indicadores semanais de crescimento dos restaurantes

    ---

    ### 🆘 Precisa de ajuda?
    - Time Data Science no Discord  
    - vitorcampomouracosta@gmail.com
    """)