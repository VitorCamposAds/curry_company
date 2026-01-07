import streamlit as st
from utils import background, setup_page, setup_sidebar, home_text

# ====================================================
# Configura título e ícone da página
# ====================================================
setup_page("Home", "📈")

# ====================================================
# Define background (usa caminho padrão do utils.py)
# ====================================================
background()  # já usa BACKGROUND_PATH por padrão

# ====================================================
# Configura sidebar
# ====================================================
setup_sidebar()  # já usa LOGO_PATH e textos padrão

# ====================================================
# Exibe conteúdo da página Home
# ====================================================
home_text()