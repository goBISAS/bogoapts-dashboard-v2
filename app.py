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

# Estilos visuales Dark & Gold
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

# --- FUNCIONES DE CONEXIÓN ---
def get_csv_url(sheet_id, sheet_name):
    sheet_enc = urllib.parse.quote(sheet_name)
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_enc}"

def safe_sum(df, column):
    if column in df.columns:
        return pd.to_numeric(df[column].str.replace(r'[^\d.-]', '', regex=True), errors='coerce').sum()
    return 0

# ==========================================================
# 2. CONFIGURACIÓN DE DATOS (DATA LAKE)
# ==========================================================
# ID de tu archivo "Data Maestra - Supermetrics"
ID_MAESTRO = "1Qkw-Fi3tLvY68maHxJOmHlX9sx0kOvNg-150YRE42W0" # Verifica que este sea el ID correcto

# URLs de las pestañas crudas de Supermetrics
url_google = get_csv_url(ID_MAESTRO, "Raw_GoogleAds")
url_meta = get_csv_url(ID_MAESTRO, "Raw_MetaAds")

# ==========================================================
# 3. MENÚ LATERAL
# ==========================================================
with st.sidebar:
    st.markdown("## 🏢 BogoApts V2")
    st.markdown("---")
    
    # Lista de clientes (En el futuro esto puede ser dinámico leyendo la columna 'Account name')
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
        # Carga de datos crudos
        with st.spinner('Sincronizando con Data Lake...'):
            df_g = pd.read_csv(url_google).fillna(0)
            df_m = pd.read_csv(url_meta).fillna(0)
            
            # FILTRADO DINÁMICO POR CLIENTE
            # Nota: Ajusta 'Account name' si en tu Sheets el nombre de la columna es diferente
            df_g_cli = df_g[df_g['Account name'] == cliente_sel]
            df_m_cli = df_m[df_m['Account name'] == cliente_sel]
            
            # CÁLCULOS DE INVERSIÓN (Ajustar nombres de columnas según tu Sheets)
            # Google usa 'Cost' usualmente, Meta usa 'Amount spent'
            gasto_google = df_g_cli['Cost'].sum() if 'Cost' in df_g_cli.columns else 0
            gasto_meta = df_m_cli['Amount spent'].sum() if 'Amount spent' in df_m_cli.columns else 0
            
            total_ejecutado = gasto_google + gasto_meta

        # VISUALIZACIÓN DE MÉTRICAS TOP
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Inversión Google", f"${gasto_google:,.0f}")
        with c2: st.metric("Inversión Meta", f"${gasto_meta:,.0f}")
        with c3: st.metric("Total Ejecutado", f"${total_ejecutado:,.0f}")
        
        st.divider()
        
        # TABLA DE DETALLE
        st.subheader("📝 Detalle de Campañas Automatizado")
        cols_mostrar = ['Date', 'Campaign name', 'Cost'] if 'Cost' in df_g_cli.columns else ['Date', 'Campaign name']
        st.dataframe(df_g_cli, use_container_width=True)

    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.info("Asegúrate de que el archivo de Google Sheets tenga el acceso compartido (Cualquiera con el enlace puede ver).")

elif vista_seleccionada == "ROAS":
    st.title("📈 Histórico y ROAS")
    st.info("Módulo en construcción para V2.")

**Pasos a seguir:**
1. Borra todo el contenido de tu archivo `app.py` en GitHub.
2. Pega este nuevo código.
3. **Muy importante:** Asegúrate de que tu archivo de Google Sheets "Data Maestra" esté compartido como **"Cualquier persona con el enlace puede ver"** para que Streamlit pueda entrar sin contraseñas.
4. Espera a que Streamlit Cloud se actualice automáticamente.

¡Confírmame cuando logres ver los números de inversión (Google y Meta) en tu Dashboard de Streamlit! Si sale algún error, no te preocupes, revisaremos los nombres de las columnas.

Tu presentación y tu app están en marcha. ¿Qué te parece el avance?
