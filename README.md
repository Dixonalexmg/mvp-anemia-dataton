# 🩸 MVP Sistema Predictivo de Anemia Infantil

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mvp-anemia-dataton.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AUC Score](https://img.shields.io/badge/AUC-0.800-green.svg)](https://mvp-anemia-dataton.streamlit.app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**🏆 Datatón Exprésate Perú con Datos 2025 | Desarrollado por Dixon Martinez**

---

## 🎯 **DEMO EN VIVO**
### 👉 **[ACCEDER AL SISTEMA](https://mvp-anemia-dataton.streamlit.app)** 👈

*Sistema operacional 24/7 - Acceso inmediato desde cualquier dispositivo*

---

## 📊 **MÉTRICAS DE IMPACTO**

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| 🎯 **Precisión** | **AUC 0.800** | Excelencia internacional |
| 👶 **Casos Analizados** | **1,000 niños** | Dataset ENDES 2024 |
| 🚨 **Alto Riesgo** | **18 casos (1.8%)** | Intervención inmediata |
| ⚠️ **Riesgo Medio** | **254 casos (25.4%)** | Monitoreo intensivo |
| 🎯 **Eficiencia** | **27.2% focalización** | vs 100% intervención universal |
| 💊 **Impacto** | **68 casos prevenibles** | Proyección con 25% efectividad |

---

## 🧠 **TECNOLOGÍA E INNOVACIÓN**

### **🤖 Motor Predictivo**
- **Algoritmo**: Regresión Logística Optimizada con Feature Engineering
- **Variables**: 8 predictores + 3 interacciones epidemiológicas críticas
- **Datos**: ENDES 2024 (Encuesta Nacional de Salud Familiar)
- **Validación**: Threshold optimizado (0.45) para balance precisión-recall

### **🏗️ Arquitectura**
Frontend: Streamlit Dashboard
Backend: Python ML Pipeline
Deploy: Streamlit Cloud
Data: ENDES CSV + JSON Model Parameters
Visualizations: Plotly Interactive Charts


### **🗺️ Cobertura Territorial**
- **25 departamentos** del Perú con nombres reales
- **Clasificación de riesgo** por contexto epidemiológico:
  - Alto riesgo: Loreto, Puno, Cusco, Huancavelica, Ayacucho, Ucayali
  - Bajo riesgo: Lima, Ica, Arequipa, Callao

---

## 🎮 **FUNCIONALIDADES**

### **📊 Dashboard Poblacional**
- Análisis de 1,000 casos en tiempo real
- KPIs operacionales con métricas de impacto
- Visualizaciones interactivas (distribución de riesgo, análisis por quintil)
- Lista exportable de casos prioritarios (CSV download)

### **👶 Evaluación Individual**
- Formulario intuitivo con datos del niño
- Predicción instantánea de probabilidad de anemia
- Clasificación de riesgo (Alto/Medio/Bajo/Muy Bajo)
- Gauge visual + recomendaciones específicas
- Mapeo de 25 departamentos peruanos

---

## 📈 **RESULTADOS TÉCNICOS**

### **🎯 Performance del Modelo**
- **AUC-ROC**: 0.800 (Nivel de excelencia internacional)
- **Precisión**: 80.0%
- **F1-Score**: 0.747
- **Especificidad**: 85%

### **🔬 Variables Más Importantes**
1. **quintil_x_rural** (14.3%) - Interacción pobreza-ruralidad
2. **primera_infancia_vulnerable** (11.0%) - 0-23 meses en pobreza
3. **edad_x_vulnerabilidad** (10.0%) - Edad por vulnerabilidad socioeconómica

### **📊 Distribución de Casos**
- **Muy Bajo Riesgo**: 33.9% (339 casos)
- **Bajo Riesgo**: 38.9% (389 casos)
- **Riesgo Medio**: 25.4% (254 casos)
- **Alto Riesgo**: 1.8% (18 casos)

---

## 🌟 **IMPACTO SOCIAL**

### **🎯 Focalización Inteligente**
El sistema identifica **272 casos prioritarios** (27.2% de la población), permitiendo:
- **Eficiencia 4x mayor** vs intervención universal
- **Recursos optimizados** para máximo impacto
- **Intervención temprana** en casos críticos

### **💊 Casos Prevenibles**
- **68 casos de anemia** prevenibles estimados
- **Proyección nacional**: ~2,797 casos prevenibles (extrapolando a 3.2M niños)
- **ROI estimado**: $15 invertidos por cada $100 en tratamiento evitado

### **🏥 Aplicabilidad MINSA**
- **Variables disponibles** en registros existentes
- **Interface lista** para personal de salud
- **Exportación de listas** para intervención territorial
- **Escalabilidad nacional** inmediata

---

## 🚀 **INSTALACIÓN Y USO**

### **⚡ Acceso Inmediato**
🌐 Demo Online: https://mvp-anemia-dataton.streamlit.app


### **💻 Instalación Local**
Clonar repositorio
git clone https://github.com/Dixonalexmg/mvp-anemia-dataton.git
cd mvp-anemia-dataton

Instalar dependencias
pip install -r requirements.txt

Ejecutar aplicación
streamlit run app.py


### **📁 Estructura del Proyecto**

mvp-anemia-dataton/
├── app.py # Dashboard principal Streamlit
├── model.py # Motor predictivo con AUC 0.800
├── modelo_params.json # Parámetros del modelo entrenado
├── requirements.txt # Dependencias Python
├── data/
│ └── endes_muestra.csv # Dataset de muestra (1,000 casos)
└── README.md # Documentación completa


---

## 🏆 **RECONOCIMIENTOS**

### **🎖️ Datatón Exprésate Perú con Datos 2025**
**Proyecto desarrollado para el Datatón Nacional de Políticas Públicas con Datos**

### **👨‍💻 Desarrollador**
**Dixon Martinez** - Cientifico de datos y IA entusiasta.
- LinkedIn: https://www.linkedin.com/in/dixon-martinez09/
- Email: dixonalexmg@gmail.com

### **🤝 Metodología**
- **AI-Assisted Development** con documentación transparente
- **Feature Engineering** epidemiológicamente validado
- **User-Centered Design** para personal de salud pública

---

## 📄 **CITAS Y REFERENCIAS**

### **📚 Fuentes de Datos**
- ENDES 2024 - Instituto Nacional de Estadística e Informática (INEI)
- Ministerio de Salud del Perú (MINSA) - Guías de anemia infantil

### **🔬 Metodología Técnica**
- Regresión Logística con regularización L2
- Feature engineering basado en literatura epidemiológica
- Validación cruzada k-fold para robustez del modelo

---

## 🎯 **PRÓXIMOS PASOS**

### **🚀 Escalabilidad Inmediata**
- [ ] Integración con sistemas MINSA
- [ ] API REST para consultas masivas  
- [ ] Dashboard gerencial para tomadores de decisión
- [ ] Alertas automáticas para casos críticos

### **📊 Mejoras Continuas**
- [ ] Incorporación de variables clínicas adicionales
- [ ] Modelo ensemble para mayor precisión
- [ ] Análisis predictivo temporal (forecasting)
- [ ] Integración con mapas geográficos en tiempo real

---

**⭐ Si este proyecto te parece valioso, dale una estrella en GitHub ⭐**

---

*Desarrollado con 💖 para mejorar la salud infantil en el Perú 🇵🇪*
