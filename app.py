import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================================
# 1. CONFIGURACIÓN GENERAL Y ESTILOS
# ==========================================================
st.set_page_config(
    page_title="BogoApts Dashboard V2",
    page_icon="🏢",
    layout="wide"
)

estilo_css = """
<style>
.main { background-color: #0d0d0d; }
[data-testid="stMetricValue"] { font-size: 32px; color: #d6b58e !important; font-weight: 700; }
[data-testid="stMetricLabel"] { color: #f5f5f5 !important; }
h1, h2, h3, p, span { color: #ffffff; font-family: 'Georgia', serif; }
.stSidebar { background-color: #1a1a1a; border-right: 1px solid #333; }
.stPlotlyChart { border: 1px solid #333; border-radius: 8px; background-color: #1a1a1a; }
</style>
"""
st.markdown(estilo_css, unsafe_allow_html=True)

# ==========================================================
# 2. MENÚ LATERAL PRINCIPAL
# ==========================================================
with st.sidebar:
    st.markdown("## 🏢 BogoApts V2")
    st.markdown("---")
    
    opciones_menu = {
        "Pacing": "📊 Control de Pauta (Pacing)",
        "ROAS": "📈 Histórico y ROAS"
    }
    
    vista_seleccionada = st.radio(
        "Seleccione el módulo:",
        options=list(opciones_menu.keys()),
        format_func=lambda x: opciones_menu[x]
    )
    st.markdown("---")
    st.caption("Entorno de Desarrollo V2 | Conexión Supermetrics")

# ==========================================================
# 3. MÓDULO 1: CONTROL DE PAUTA (PACING)
# ==========================================================
if vista_seleccionada == "Pacing":
    st.title("🏢 Sistema Inteligente BogoApts: Motor V2")
    
    st.success("✅ El caparazón visual del entorno V2 se ha inicializado con éxito. Estamos listos para conectar la Data Maestra de Supermetrics.")
    
    # Aquí irá la nueva lógica de Pandas para leer tu Data Lake en los próximos pasos
    st.info("Esperando conexión con Google Sheets...")

# ==========================================================
# 4. MÓDULO 2: HISTÓRICO Y ROAS
# ==========================================================
elif vista_seleccionada == "ROAS":
    st.title("📈 Desempeño Histórico y ROAS")
    st.info("El módulo histórico se migrará pronto a esta V2.")
