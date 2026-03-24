"""
Explorador de Ejercicios de Selectividad - Andalucía
Instrucciones:
  1. Coloca este script y los archivos CSV en la misma carpeta.
  2. Cada CSV debe tener: año, convocatoria, ejercicio, tema, tipo_ejercicio
  3. Ejecuta: streamlit run selectividad_explorer.py
"""

import streamlit as st
import pandas as pd
import glob
import os

# ── Configuración ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Selectividad Andalucía · Explorador",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --bg:      #0f1117;
    --panel:   #171b26;
    --border:  #2a2f3f;
    --accent:  #e8c547;
    --accent2: #5fc4b8;
    --text:    #d4d8e8;
    --muted:   #7a8099;
    --radius:  8px;
}

.stApp { background-color: var(--bg); }

html, body, [class*="css"] {
    font-family: 'Lora', Georgia, serif;
    color: var(--text);
}

section[data-testid="stSidebar"] {
    background: var(--panel);
    border-right: 1px solid var(--border);
}

.main-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: -0.02em;
    margin: 0 0 0.15rem 0;
}
.sub-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.05em;
    margin-bottom: 1.4rem;
}

.filter-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent2);
    margin-bottom: 0.5rem;
}

.metric-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.8rem 1rem;
    text-align: center;
}
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.9rem;
    font-weight: 600;
    color: var(--accent);
    line-height: 1.1;
}
.metric-label {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

.dist-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.73rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent2);
    margin: 0.2rem 0 0.7rem 0;
}
.bar-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.45rem;
    gap: 0.6rem;
}
.bar-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text);
    min-width: 150px;
    max-width: 150px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.bar-track {
    flex: 1;
    height: 7px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
    border-radius: 4px;
}
.bar-count {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    min-width: 22px;
    text-align: right;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str).fillna("")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def tipo_conv(c: str) -> str:
    c = c.lower()
    if "junio" in c:
        return "Junio"
    elif "sept" in c:
        return "Septiembre"
    elif "reserva" in c:
        return "Reserva"
    return c.title()


def build_bars(series: pd.Series, max_items: int = 12) -> str:
    counts = series.value_counts().head(max_items)
    if counts.empty:
        return "<span style='color:var(--muted);font-size:0.75rem'>Sin datos</span>"
    max_val = counts.max()
    rows = []
    for label, cnt in counts.items():
        pct = int(cnt / max_val * 100)
        s = str(label)
        short = (s[:26] + "…") if len(s) > 26 else s
        rows.append(f"""
        <div class="bar-row">
          <span class="bar-label" title="{s}">{short}</span>
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>
          <span class="bar-count">{cnt}</span>
        </div>""")
    return "\n".join(rows)


def metric_card(value, label):
    return (f'<div class="metric-card">'
            f'<div class="metric-value">{value}</div>'
            f'<div class="metric-label">{label}</div>'
            f'</div>')


# ── Sidebar: carga de ficheros ─────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🧪 Cargar datos")
    st.markdown("---")
    uploaded = st.file_uploader(
        "CSV de ejercicios",
        type="csv",
        accept_multiple_files=True,
        help="Columnas: año, convocatoria, ejercicio, tema, tipo_ejercicio",
    )
    st.markdown("---")
    st.markdown(
        '<span style="font-family:\'IBM Plex Mono\',monospace;'
        'font-size:0.68rem;color:#7a8099">'
        'Selectividad Andalucía<br>Explorador v2.0</span>',
        unsafe_allow_html=True,
    )


# ── Carga de datos ─────────────────────────────────────────────────────────────

script_dir = os.path.dirname(os.path.abspath(__file__))
found_csvs = sorted(glob.glob(os.path.join(script_dir, "*.csv")))

dfs, loaded_names = [], []

for path in found_csvs:
    try:
        dfs.append(load_csv(path))
        loaded_names.append(os.path.basename(path))
    except Exception:
        pass

for uf in (uploaded or []):
    try:
        df_up = pd.read_csv(uf, dtype=str).fillna("")
        df_up.columns = [c.strip().lower().replace(" ", "_") for c in df_up.columns]
        dfs.append(df_up)
        loaded_names.append(uf.name)
    except Exception:
        st.warning(f"No se pudo leer «{uf.name}»")

# ── Cabecera (siempre visible) ─────────────────────────────────────────────────

st.markdown('<div class="main-header">Explorador de Ejercicios · Selectividad</div>',
            unsafe_allow_html=True)
st.markdown('<div class="sub-header">Química · Andalucía · Ejercicios resueltos clasificados por tipo</div>',
            unsafe_allow_html=True)

if not dfs:
    st.info("Sube al menos un CSV usando el panel lateral (←).  "
            "Columnas requeridas: año, convocatoria, ejercicio, tema, tipo_ejercicio")
    st.stop()

data = pd.concat(dfs, ignore_index=True)
data["año"] = pd.to_numeric(data["año"], errors="coerce").astype("Int64")
data["_conv_tipo"] = data["convocatoria"].apply(tipo_conv)

# Ficheros activos
files_str = "  ·  ".join(f"📄 {n}" for n in loaded_names)
st.markdown(
    f'<span style="font-family:\'IBM Plex Mono\',monospace;'
    f'font-size:0.72rem;color:var(--accent2)">{files_str}</span>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)


# ── Filtros en la página principal (4 columnas) ────────────────────────────────

st.markdown('<div class="filter-title">🔍 Filtros</div>', unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns(4)

# Tema
temas_disp = sorted(data["tema"].dropna().unique().tolist())
with fc1:
    temas_sel = st.multiselect(
        "Tema",
        options=temas_disp,
        default=temas_disp,
        placeholder="Todos los temas",
        key="f_tema",
    )

# Año — slider de rango cuando hay suficientes valores
años_disp = sorted(int(a) for a in data["año"].dropna().unique())
with fc2:
    if len(años_disp) >= 2:
        año_range = st.select_slider(
            "Año",
            options=años_disp,
            value=(años_disp[0], años_disp[-1]),
            key="f_año",
        )
        años_sel = [a for a in años_disp if año_range[0] <= a <= año_range[1]]
    else:
        años_sel = st.multiselect(
            "Año",
            options=años_disp,
            default=años_disp,
            format_func=str,
            key="f_año_ms",
        )

# Convocatoria
conv_tipos = sorted(data["_conv_tipo"].unique().tolist())
with fc3:
    conv_sel = st.multiselect(
        "Convocatoria",
        options=conv_tipos,
        default=conv_tipos,
        placeholder="Todas",
        key="f_conv",
    )

# Tipo de ejercicio
tipos_disp = sorted(data["tipo_ejercicio"].dropna().unique().tolist())
with fc4:
    tipos_sel = st.multiselect(
        "Tipo de ejercicio",
        options=tipos_disp,
        default=[],
        placeholder="Todos los tipos",
        key="f_tipo",
    )

st.markdown("---")


# ── Filtrado ───────────────────────────────────────────────────────────────────

filtered = data.copy()

if temas_sel:
    filtered = filtered[filtered["tema"].isin(temas_sel)]

if años_sel:
    filtered = filtered[filtered["año"].isin(años_sel)]

if conv_sel:
    filtered = filtered[filtered["_conv_tipo"].isin(conv_sel)]

if tipos_sel:
    filtered = filtered[filtered["tipo_ejercicio"].isin(tipos_sel)]


# ── Métricas ───────────────────────────────────────────────────────────────────

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(metric_card(len(filtered), "Ejercicios"), unsafe_allow_html=True)
with m2:
    st.markdown(metric_card(filtered["año"].nunique(), "Años"), unsafe_allow_html=True)
with m3:
    st.markdown(metric_card(filtered["tema"].nunique(), "Temas"), unsafe_allow_html=True)
with m4:
    st.markdown(metric_card(filtered["tipo_ejercicio"].nunique(), "Tipos distintos"),
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Tabla ──────────────────────────────────────────────────────────────────────

if filtered.empty:
    st.info("Ningún ejercicio coincide con los filtros seleccionados.")
else:
    show = filtered.sort_values(
        ["año", "_conv_tipo", "tema"], ascending=[False, True, True]
    ).reset_index(drop=True)

    display_df = show[["año", "convocatoria", "ejercicio", "tema", "tipo_ejercicio"]].copy()
    display_df["año"] = display_df["año"].apply(
        lambda x: str(int(x)) if pd.notna(x) else "—"
    )
    display_df.columns = ["Año", "Convocatoria", "Ejercicio", "Tema", "Tipo de ejercicio"]

    st.dataframe(
        display_df,
        column_config={
            "Año":               st.column_config.TextColumn(width="small"),
            "Convocatoria":      st.column_config.TextColumn(width="medium"),
            "Ejercicio":         st.column_config.TextColumn(width="medium"),
            "Tema":              st.column_config.TextColumn(width="medium"),
            "Tipo de ejercicio": st.column_config.TextColumn(width="large"),
        },
        use_container_width=True,
        hide_index=True,
        height=min(56 + len(display_df) * 35, 640),
    )

    csv_out = show.drop(columns=["_conv_tipo"], errors="ignore").to_csv(index=False)
    st.download_button(
        label="⬇ Descargar selección como CSV",
        data=csv_out,
        file_name="seleccion_ejercicios.csv",
        mime="text/csv",
    )


# ── Distribuciones ─────────────────────────────────────────────────────────────

if not filtered.empty:
    with st.expander("📊 Distribución de la selección", expanded=False):
        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown('<div class="dist-title">Por tipo de ejercicio</div>',
                        unsafe_allow_html=True)
            st.markdown(build_bars(filtered["tipo_ejercicio"], 12), unsafe_allow_html=True)
        with d2:
            st.markdown('<div class="dist-title">Por convocatoria</div>',
                        unsafe_allow_html=True)
            st.markdown(build_bars(filtered["_conv_tipo"], 6), unsafe_allow_html=True)
        with d3:
            st.markdown('<div class="dist-title">Por año</div>',
                        unsafe_allow_html=True)
            st.markdown(
                build_bars(filtered["año"].dropna().astype(str), 12),
                unsafe_allow_html=True,
            )
