import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import urllib.parse

# ==========================================================
# 1. CONFIGURACIÓN GENERAL Y ESTILOS
# ==========================================================
st.set_page_config(
    page_title="BogoApts Dashboard V2",
    page_icon="🏢",
    layout="wide"
)

st.markdown("""
<style>
.main { background-color: #0d0d0d; }
[data-testid="stMetricValue"] { font-size: 32px; color: #d6b58e !important; font-weight: 700; }
[data-testid="stMetricLabel"] { color: #f5f5f5 !important; }
h1, h2, h3, p, span { color: #ffffff; font-family: 'Urbanist', sans-serif; }
.stSidebar { background-color: #1a1a1a; border-right: 1px solid #333; }
.stPlotlyChart { border: 1px solid #333; border-radius: 8px; background-color: #1a1a1a; }
</style>
""", unsafe_allow_html=True)

def get_csv_url(sheet_id, sheet_name):
    sheet_enc = urllib.parse.quote(sheet_name)
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_enc}"

def safe_sum(df, column):
    if column in df.columns:
        return pd.to_numeric(df[column].astype(str).str.replace(r'[^\d.-]', '', regex=True), errors='coerce').sum()
    return 0

# ==========================================================
# 2. CONFIGURACIÓN DE DATOS (DATA LAKE)
# ==========================================================
# ¡ID Verificado y corregido con tu enlace exacto!
ID_MAESTRO = "170xDwjP194VX4QgW17lhM4dQyH9qIbMPaI4oXL_RP-I"

url_google = get_csv_url(ID_MAESTRO, "Raw_GoogleAds")
url_meta = get_csv_url(ID_MAESTRO, "Raw_MetaAds")

# ==========================================================
# 3. MÓDULO PRINCIPAL CON EXTRACCIÓN DINÁMICA
# ==========================================================
try:
    with st.spinner('Sincronizando con Data Lake...'):
        df_g = pd.read_csv(url_google).fillna(0)
        df_m = pd.read_csv(url_meta).fillna(0)
        
        df_g.columns = df_g.columns.str.strip()
        df_m.columns = df_m.columns.str.strip()
        
        # Extracción dinámica de clientes de ambas plataformas
        clientes_google = df_g['Account'].unique().tolist() if 'Account' in df_g.columns else []
        clientes_meta = df_m['Account name'].unique().tolist() if 'Account name' in df_m.columns else []
        
        # Unimos las listas, quitamos duplicados y ordenamos alfabéticamente
        todos_los_clientes = sorted(list(set([str(c) for c in clientes_google + clientes_meta if str(c) != '0'])))

    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("## 🏢 BogoApts V2")
        st.markdown("---")
        
        if todos_los_clientes:
            cliente_sel = st.selectbox("Seleccione el Cliente:", options=todos_los_clientes)
        else:
            cliente_sel = st.selectbox("Seleccione el Cliente:", options=["Sin datos"])
            st.warning("No se encontraron clientes en la base de datos.")
        
        st.markdown("---")
        vista_seleccionada = st.radio("Módulo:", options=["Pacing", "ROAS"])

    # --- VISTA PACING ---
    if vista_seleccionada == "Pacing":
        st.title(f"📊 Control de Pauta: {cliente_sel}")
        
        # Filtrado considerando los nombres exactos de las columnas por plataforma
        df_g_cli = df_g[df_g['Account'] == cliente_sel] if 'Account' in df_g.columns else pd.DataFrame()
        df_m_cli = df_m[df_m['Account name'] == cliente_sel] if 'Account name' in df_m.columns else pd.DataFrame()
        
        # Sumamos la inversión (ambos se exportaron como 'Cost')
        gasto_google = safe_sum(df_g_cli, 'Cost')
        gasto_meta = safe_sum(df_m_cli, 'Cost')
        
        total_ejecutado = gasto_google + gasto_meta

        # MÉTRICAS VISUALES
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Inversión Google", f"${gasto_google:,.0f}")
        with c2: st.metric("Inversión Meta", f"${gasto_meta:,.0f}")
        with c3: st.metric("Total Ejecutado", f"${total_ejecutado:,.0f}")
        
        st.divider()
        
        # TABLA CON DETALLE DE CAMPAÑAS
        st.subheader("📝 Detalle de Campañas Automatizado")
        
        # Mostramos Google si hay datos para este cliente
        if not df_g_cli.empty:
            st.markdown("**Google Ads**")
            cols_g = [col for col in ['Date', 'Campaign name', 'Cost'] if col in df_g_cli.columns]
            st.dataframe(df_g_cli[cols_g], use_container_width=True)
            
        # Mostramos Meta si hay datos para este cliente
        if not df_m_cli.empty:
            st.markdown("**Meta Ads**")
            cols_m = [col for col in ['Date', 'Campaign name', 'Cost'] if col in df_m_cli.columns]
            st.dataframe(df_m_cli[cols_m], use_container_width=True)
            
        if df_g_cli.empty and df_m_cli.empty:
            st.info("Este cliente no tiene campañas activas registradas en las plataformas seleccionadas.")

    elif vista_seleccionada == "ROAS":
        st.title("📈 Histórico y ROAS")
        st.info("Módulo en construcción para V2.")

except Exception as e:
    st.error(f"Error crítico en la ejecución: {e}")
    st.info("Verifica que el archivo de Google Sheets permita acceso como lector con el enlace.")
