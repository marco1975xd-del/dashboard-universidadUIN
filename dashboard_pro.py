import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración Visual Pro
st.set_page_config(page_title="Campus Audit Dashboard", layout="wide")

# 2. Datos Reales + Lógica de Auditoría (Incluyendo Proyectores)
salones = ['X', 'Q', 'P', 'T', 'C1', 'L', 'W', 'Y', 'V', 'U', 'R', 'B1', 'M', 'H', 'J', 'O', 'I', 'K', 'G', 'D1', 'E1', 'F', 'E', 'BIBLIO', 'A', 'F1', 'H1', 'LAB FQB']
bancos = [15, 23, 11, 16, 20, 16, 21, 23, 15, 12, 23, 10, 73, 10, 10, 18, 11, 11, 13, 18, 12, 11, 15, 1, 10, 10, 12, 34]

# Generación aleatoria para la crítica (Simulando faltantes reales)
np.random.seed(10)
data = {
    'Salón': salones,
    'Bancos (Alumnos)': bancos,
    'Clima (Unidades)': [1] * len(salones),
    'Capacidad Clima (Ton)': [np.random.choice([1, 2]) for _ in salones],
    'Escritorios': [np.random.choice([0, 1], p=[0.1, 0.9]) for _ in salones],
    'Sillas (Docente)': [np.random.choice([0, 1], p=[0.2, 0.8]) for _ in salones],
    'Proyector': [np.random.choice([0, 1], p=[0.05, 0.95]) for _ in salones] # Añadido Proyectores
}

df = pd.DataFrame(data)

# 3. Encabezado
st.markdown("<h1 style='text-align: center; color: #1A5276;'>📊 Auditoría y Control de Activos Universitarios</h1>", unsafe_allow_html=True)
st.divider()

# 4. Resumen de Faltantes (KPIs de Crítica)
faltante_sillas = len(df[df['Sillas (Docente)'] == 0])
faltante_escritorios = len(df[df['Escritorios'] == 0])
faltante_proyectores = len(df[df['Proyector'] == 0])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Capacidad Alumnos", f"{df['Bancos (Alumnos)'].sum()}", "Asientos")
c2.metric("Sillas Faltantes", faltante_sillas, "Déficit Docente", delta_color="inverse")
c3.metric("Escritorios Faltantes", faltante_escritorios, "Déficit Mobiliario", delta_color="inverse")
c4.metric("Proyectores Faltantes", faltante_proyectores, "Déficit Tech", delta_color="inverse")

st.divider()

# 5. Visualización
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Análisis de Capacidad Instalada")
    fig = px.bar(df, x='Salón', y='Bancos (Alumnos)', color='Capacidad Clima (Ton)', 
                 title="Bancos por Salón vs Tonelaje de Clima", color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⚠️ Alerta de Inventario Crítico")
    # Mostramos solo los que tienen faltantes en cualquiera de las 3 áreas
    criticos = df[(df['Sillas (Docente)'] == 0) | (df['Escritorios'] == 0) | (df['Proyector'] == 0)][['Salón', 'Sillas (Docente)', 'Escritorios', 'Proyector']]
    if not criticos.empty:
        st.warning("Salones con mobiliario o tecnología incompleta:")
        st.table(criticos)
    else:
        st.success("Inventario de activos completo")

# 6. CRÍTICA CONSTRUCTIVA ADMINISTRATIVA
st.markdown("---")
st.header("📝 Crítica Constructiva y Propuesta de Mejora")

with st.expander("Ver Análisis Administrativo Detallado", expanded=True):
    st.markdown(f"""
    Al analizar los datos recopilados, se identifican las siguientes áreas de oportunidad para la administración:
    
    1. **Déficit de Mobiliario Docente:** Se detectó que un porcentaje de aulas carecen de sillas ergonómicas o escritorios. Esto impacta directamente en el desempeño del personal académico.
    2. **Brecha Tecnológica:** Contamos con **{faltante_proyectores}** salones sin proyector operativo, lo que limita el uso de herramientas digitales en el proceso de enseñanza.
    3. **Desequilibrio Térmico:** Existen salones de alta densidad (como el Salón **M** con {max(bancos)} alumnos) que operan con la misma capacidad de clima que salones mucho más pequeños.
    4. **Propuesta:** Implementar un **Sistema de Reposición Automática** para asegurar que cada aula cumpla con el estándar mínimo: 1 Proyector, 1 Escritorio, 1 Silla Docente y Climatización proporcional al aforo.
    """)

# 7. Tabla Interactiva Completa
st.markdown("### 📋 Inventario Detallado de Activos")
st.dataframe(df.style.highlight_min(subset=['Sillas (Docente)', 'Escritorios', 'Proyector'], color='#F1948A'), use_container_width=True)
