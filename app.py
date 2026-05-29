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
ID_MAESTRO = "1Qkw-Fi3tLvY68maHxJOmHlX9sx0kOvNg-150YRE42W0"

url_google = get_csv_url(ID_MAESTRO, "Raw_GoogleAds")
url_meta = get_csv_url(ID_MAESTRO, "Raw_MetaAds")

# ==========================================================
# 3. MENÚ LATERAL
# ==========================================================
with st.sidebar:
    st.markdown("## 🏢 BogoApts V2")
    st.markdown("---")
    
    cliente_sel = st.selectbox(
        "Seleccione el Cliente:",
        options=["BogoApts_CO", "Otro_Cliente_Prueba"]
    )
    
    st.markdown("---")
    vista_seleccionada = st.radio(
        "Módulo:",
        options=["Pacing", "ROAS"]
    )

# ==========================================================
# 4. MÓDULO PACING
# ==========================================================
if vista_seleccionada == "Pacing":
    st.title(f"📊 Control de Pauta: {cliente_sel}")
    
    try:
        with st.spinner('Sincronizando con Data Lake...'):
            df_g = pd.read_csv(url_google).fillna(0)
            df_m = pd.read_csv(url_meta).fillna(0)
            
            # Limpieza básica de nombres de columnas (quita espacios al principio y al final)
            df_g.columns = df_g.columns.str.strip()
            df_m.columns = df_m.columns.str.strip()
            
            # MODO DEBUG: Si no encuentra la columna, imprime lo que está viendo
            if 'Account name' not in df_g.columns and 'Account name' not in df_m.columns:
                st.warning("⚠️ No se encontró la columna 'Account name'. Esto es lo que Python está leyendo desde Google Sheets:")
                st.write("**Columnas detectadas en Google Ads:**", df_g.columns.tolist())
                st.write("**Columnas detectadas en Meta Ads:**", df_m.columns.tolist())
                st.stop() # Detiene la ejecución aquí para que podamos ver el mensaje
                
            # FILTRADO DINÁMICO POR CLIENTE
            df_g_cli = df_g[df_g['Account name'] == cliente_sel] if 'Account name' in df_g.columns else pd.DataFrame()
            df_m_cli = df_m[df_m['Account name'] == cliente_sel] if 'Account name' in df_m.columns else pd.DataFrame()
            
            # CÁLCULOS DE INVERSIÓN
            gasto_google = safe_sum(df_g_cli, 'Cost') if 'Cost' in df_g_cli.columns else safe_sum(df_g_cli, 'Amount spent')
            gasto_meta = safe_sum(df_m_cli, 'Amount spent')
            
            total_ejecutado = gasto_google + gasto_meta

        # VISUALIZACIÓN DE MÉTRICAS TOP
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Inversión Google", f"${gasto_google:,.0f}")
        with c2: st.metric("Inversión Meta", f"${gasto_meta:,.0f}")
        with c3: st.metric("Total Ejecutado", f"${total_ejecutado:,.0f}")
        
        st.divider()
        
        # TABLA DE DETALLE
        st.subheader("📝 Detalle de Campañas Automatizado")
        cols_g = [col for col in ['Date', 'Campaign name', 'Cost', 'Amount spent'] if col in df_g_cli.columns]
        if not cols_g: cols_g = df_g_cli.columns.tolist()
        st.dataframe(df_g_cli[cols_g], use_container_width=True)

    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.info("Asegúrate de que el archivo de Google Sheets tenga el acceso compartido (Cualquiera con el enlace puede ver).")

elif vista_seleccionada == "ROAS":
    st.title("📈 Histórico y ROAS")
    st.info("Módulo en construcción para V2.")
