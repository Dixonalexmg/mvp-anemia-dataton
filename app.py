"""
Dashboard MVP - Sistema Predictivo de Anemia Infantil
Datatón Exprésate Perú con Datos 2025
Desarrollado por: Dixon Martinez
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from model import ModeloAnemiaInfantil, CargadorDatos
import os

# Configuración de página
st.set_page_config(
    page_title="MVP Anemia Infantil - Datatón 2025",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .high-risk { border-left-color: #e74c3c !important; }
    .medium-risk { border-left-color: #f39c12 !important; }
    .low-risk { border-left-color: #3498db !important; }
    .very-low-risk { border-left-color: #2ecc71 !important; }
</style>
""", unsafe_allow_html=True)

# Función para cargar datos con caché
@st.cache_data
def cargar_datos_demo():
    """Carga datos de demostración"""
    try:
        filepath = "data/endes_muestra.csv"
        if not os.path.exists(filepath):
            st.error(f"❌ No se encontró el archivo {filepath}")
            st.info("📝 Asegúrate de que el archivo esté en la carpeta 'data/'")
            return None
        
        cargador = CargadorDatos()
        df = cargador.cargar_dataset(filepath)
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        return None

# Función principal
def main():
    # Header principal
    st.title("🩸 Sistema Predictivo de Anemia Infantil")
    st.subheader("MVP - Datatón Exprésate Perú con Datos 2025")
    
    # Información del modelo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🤖 **Modelo**: Regresión Logística Optimizada")
    with col2:
        st.info("📊 **Precisión**: AUC 0.800 (Excelencia Internacional)")
    with col3:
        st.info("👨‍💻 **Desarrollado por**: Dixon Martinez")
    
    # Sidebar para configuración
    st.sidebar.header("⚙️ Configuración del Sistema")
    
    # Inicializar modelo
    try:
        modelo = ModeloAnemiaInfantil()
        st.sidebar.success("✅ Modelo cargado correctamente")
    except Exception as e:
        st.sidebar.error(f"❌ Error al cargar modelo: {str(e)}")
        st.error("⚠️ No se pudo cargar el modelo. Verifica que 'modelo_params.json' esté en la carpeta raíz.")
        st.stop()
    
    # Cargar datos
    df = cargar_datos_demo()
    if df is None:
        st.stop()
    
    # Opciones en sidebar
    modo_operacion = st.sidebar.selectbox(
        "🎯 Modo de Operación",
        ["📊 Análisis Poblacional", "👶 Evaluación Individual"]
    )
    
    if modo_operacion == "📊 Análisis Poblacional":
        mostrar_analisis_poblacional(modelo, df)
    else:
        mostrar_evaluacion_individual(modelo)

def mostrar_analisis_poblacional(modelo, df):
    """Muestra análisis poblacional completo"""
    
    st.header("📊 Análisis Poblacional - Datos ENDES 2024")
    
    # Procesamiento con spinner
    with st.spinner("🔄 Procesando análisis poblacional..."):
        df_resultado = modelo.procesar_poblacion(df)
        metricas = modelo.generar_metricas_poblacion(df_resultado)
    
    # KPIs principales
    st.subheader("🎯 Métricas Clave del Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "👶 Niños Analizados",
            f"{metricas['total_ninos']:,}",
            delta="Dataset ENDES 2024"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card high-risk">', unsafe_allow_html=True)
        st.metric(
            "🚨 Alto Riesgo",
            f"{metricas['ninos_alto_riesgo']:,}",
            delta=f"{(metricas['ninos_alto_riesgo']/metricas['total_ninos']*100):.1f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card medium-risk">', unsafe_allow_html=True)
        st.metric(
            "⚠️ Riesgo Medio",
            f"{metricas['ninos_medio_riesgo']:,}",
            delta=f"{(metricas['ninos_medio_riesgo']/metricas['total_ninos']*100):.1f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "🎯 Focalización",
            f"{metricas['porcentaje_focalizacion']:.1f}%",
            delta=f"{metricas['casos_prevenibles_estimados']:,} casos prevenibles"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualizaciones
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribución de riesgo
        st.subheader("📊 Distribución de Riesgo")
        
        distribucion = pd.DataFrame(list(metricas['distribucion_riesgo'].items()), 
                                  columns=['Categoría', 'Cantidad'])
        
        colores = {'Alto': '#e74c3c', 'Medio': '#f39c12', 'Bajo': '#3498db', 'Muy Bajo': '#2ecc71'}
        distribucion['Color'] = distribucion['Categoría'].map(colores)
        
        fig_pie = px.pie(
            distribucion, 
            values='Cantidad', 
            names='Categoría',
            color='Categoría',
            color_discrete_map=colores,
            title="Distribución de Niveles de Riesgo"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Análisis por quintil
        st.subheader("💰 Análisis por Quintil Socioeconómico")
        
        analisis_quintil = df_resultado.groupby('quintil_label').agg({
            'probabilidad_anemia': 'mean',
            'score_riesgo': 'mean'
        }).reset_index()
        
        fig_bar = px.bar(
            analisis_quintil,
            x='quintil_label',
            y='probabilidad_anemia',
            title="Prevalencia Promedio por Quintil",
            labels={'probabilidad_anemia': 'Probabilidad de Anemia', 'quintil_label': 'Quintil'},
            color='probabilidad_anemia',
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(yaxis=dict(tickformat='.1%'))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tabla de casos prioritarios
    st.subheader("🚨 Casos Prioritarios Identificados")
    
    casos_prioritarios = df_resultado[
        df_resultado['categoria_riesgo'].isin(['Alto', 'Medio'])
    ].sort_values('probabilidad_anemia', ascending=False)
    
    # Mostrar solo primeros 20 casos
    st.dataframe(
        casos_prioritarios.head(20)[['HHID', 'quintil_label', 'area_label', 
                                   'grupo_edad_label', 'score_riesgo', 
                                   'categoria_riesgo', 'descripcion_riesgo']],
        use_container_width=True
    )
    
    # Botón de descarga
    csv = casos_prioritarios.to_csv(index=False)
    st.download_button(
        label="📥 Descargar Lista Completa de Casos Prioritarios",
        data=csv,
        file_name="casos_prioritarios_anemia.csv",
        mime="text/csv"
    )

def mostrar_evaluacion_individual(modelo):
    """Interfaz para evaluación de casos individuales"""
    
    st.header("👶 Evaluación Individual de Riesgo")
    
    st.info("💡 Ingresa los datos de un niño para obtener su evaluación de riesgo personalizada")
    
    # Formulario de entrada
    with st.form("evaluacion_individual"):
        col1, col2 = st.columns(2)
        
        with col1:
            quintil = st.selectbox("💰 Quintil de Riqueza", 
                                 options=[1, 2, 3, 4, 5],
                                 format_func=lambda x: f"Q{x} ({'Más pobre' if x==1 else 'Más rico' if x==5 else 'Medio' if x==3 else ''})"
                                )
            
            area_rural = st.selectbox("🏘️ Área de Residencia",
                                    options=[0, 1],
                                    format_func=lambda x: "Rural" if x==1 else "Urbano"
                                   )
            
            grupo_edad = st.selectbox("👶 Grupo de Edad",
                                    options=[0, 1, 2, 3, 4],
                                    format_func=lambda x: ["0-11m", "12-23m", "24-35m", "36-47m", "48-59m"][x]
                                   )
            
            departamentos_nombres = {
                1: 'Amazonas', 2: 'Áncash', 3: 'Apurímac', 4: 'Arequipa', 5: 'Ayacucho',
                6: 'Cajamarca', 7: 'Callao', 8: 'Cusco', 9: 'Huancavelica', 10: 'Huánuco',
                11: 'Ica', 12: 'Junín', 13: 'La Libertad', 14: 'Lambayeque', 15: 'Lima',
                16: 'Loreto', 17: 'Madre de Dios', 18: 'Moquegua', 19: 'Pasco', 20: 'Piura',
                21: 'Puno', 22: 'San Martín', 23: 'Tacna', 24: 'Tumbes', 25: 'Ucayali'
            }
            
            departamento = st.selectbox("🗺️ Departamento",
                                      options=list(range(1, 26)),
                                      format_func=lambda x: departamentos_nombres[x]
                                     )
        
        with col2:
            electricidad = st.selectbox("⚡ Acceso a Electricidad",
                                      options=[0, 1],
                                      format_func=lambda x: "Sí" if x==1 else "No"
                                     )
            
            agua_potable = st.selectbox("💧 Acceso a Agua Potable",
                                      options=[0, 1], 
                                      format_func=lambda x: "Sí" if x==1 else "No"
                                     )
            
            programa_juntos = st.selectbox("🤝 Programa Juntos",
                                         options=[0, 1],
                                         format_func=lambda x: "Beneficiario" if x==1 else "No beneficiario"
                                        )
            
            programa_qaliwarma = st.selectbox("🍎 Programa Qali Warma",
                                            options=[0, 1],
                                            format_func=lambda x: "Beneficiario" if x==1 else "No beneficiario"
                                           )
        
        # Botón de evaluación
        submitted = st.form_submit_button("🔍 Evaluar Riesgo", use_container_width=True)
        
        if submitted:
            # Crear diccionario con datos del niño
            datos_nino = {
                'quintil': quintil,
                'area_rural': area_rural,
                'grupo_edad': grupo_edad,
                'departamento': departamento,
                'electricidad': electricidad,
                'agua_potable': agua_potable,
                'programa_juntos': programa_juntos,
                'programa_qaliwarma': programa_qaliwarma
            }
            
            # Realizar predicción
            with st.spinner("🤖 Procesando evaluación..."):
                probabilidad = modelo.predecir_probabilidad(datos_nino)
                categoria, descripcion, color = modelo.clasificar_riesgo(probabilidad)
                score = int(probabilidad * 100)
            
            # Mostrar resultados
            st.success("✅ Evaluación completada")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Probabilidad de Anemia", f"{probabilidad:.1%}")
            
            with col2:
                st.metric("🎯 Score de Riesgo", f"{score}/100")
            
            with col3:
                st.markdown(f'<div style="color: {color}; font-weight: bold; font-size: 1.2em;">🚨 Riesgo: {categoria}</div>', 
                          unsafe_allow_html=True)
            
            # Recomendación
            st.info(f"💡 **Recomendación**: {descripcion}")
            
            # Gráfico de gauge
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Score de Riesgo"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 25], 'color': "#2ecc71"},
                        {'range': [25, 45], 'color': "#3498db"},
                        {'range': [45, 65], 'color': "#f39c12"},
                        {'range': [65, 100], 'color': "#e74c3c"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)

if __name__ == "__main__":
    main()
