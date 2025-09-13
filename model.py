"""
Motor Predictivo para Sistema de Anemia Infantil
MVP - Datatón Exprésate Perú con Datos 2025
Desarrollado por: Dixon Martinez
"""

import pandas as pd
import numpy as np
import json
import os
from typing import Dict, Tuple, List

class ModeloAnemiaInfantil:
    """
    Modelo predictivo de anemia infantil basado en regresión logística optimizada
    AUC: 0.800 - Nivel de excelencia internacional
    """
    
    def __init__(self, modelo_path: str = "modelo_params.json"):
        """
        Inicializa el modelo cargando parámetros desde archivo JSON
        """
        self.modelo_path = modelo_path
        self.params = self._cargar_parametros()
        self.auc_score = self.params['auc_score']
        self.coeficientes = self.params['coeficientes']
        self.threshold = self.params['threshold_optimizado']
        
        # Mapeo de departamentos peruanos
        self.departamentos_nombres = {
            1: 'Amazonas', 2: 'Áncash', 3: 'Apurímac', 4: 'Arequipa', 5: 'Ayacucho',
            6: 'Cajamarca', 7: 'Callao', 8: 'Cusco', 9: 'Huancavelica', 10: 'Huánuco',
            11: 'Ica', 12: 'Junín', 13: 'La Libertad', 14: 'Lambayeque', 15: 'Lima',
            16: 'Loreto', 17: 'Madre de Dios', 18: 'Moquegua', 19: 'Pasco', 20: 'Piura',
            21: 'Puno', 22: 'San Martín', 23: 'Tacna', 24: 'Tumbes', 25: 'Ucayali'
        }
        
        print(f"✅ Modelo inicializado - AUC: {self.auc_score}")
        
    def _cargar_parametros(self) -> dict:
        """Carga parámetros del modelo desde archivo JSON"""
        try:
            with open(self.modelo_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo {self.modelo_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar JSON en {self.modelo_path}")
    
    def _crear_variables_derivadas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Crea variables derivadas necesarias para el modelo
        """
        df_procesado = df.copy()
        
        # Variables de interacción críticas
        df_procesado['quintil_x_rural'] = df['quintil'] * df['area_rural']
        
        # Primera infancia vulnerable (variable top-2)
        df_procesado['primera_infancia_vulnerable'] = (
            (df['grupo_edad'] <= 1) * (6 - df['quintil']) * 0.1
        )
        
        # Edad por vulnerabilidad
        df_procesado['edad_x_vulnerabilidad'] = (
            df['grupo_edad'] * (6 - df['quintil']) * 0.05
        )
        
        # Riesgo departamental usando mapeos del JSON o valores por defecto
        try:
            dept_alto_riesgo = self.params['mapeos']['departamentos_alto_riesgo']
            dept_bajo_riesgo = self.params['mapeos']['departamentos_bajo_riesgo']
        except (KeyError, TypeError):
            # Valores por defecto si no están en el JSON
            dept_alto_riesgo = [16, 21, 8, 9, 5, 25]  # Loreto, Puno, Cusco, Huancavelica, Ayacucho, Ucayali
            dept_bajo_riesgo = [15, 11, 4, 7]  # Lima, Ica, Arequipa, Callao
        
        df_procesado['departamento_riesgo'] = df['departamento'].apply(
            lambda x: 2 if x in dept_alto_riesgo else (0 if x in dept_bajo_riesgo else 1)
        )
        
        # Cobertura de programas
        df_procesado['cobertura_programas'] = (
            df['programa_juntos'] * 2 + df['programa_qaliwarma'] * 1.5
        )
        
        return df_procesado
    
    def obtener_nombre_departamento(self, codigo_dept: int) -> str:
        """
        Convierte código de departamento a nombre
        """
        return self.departamentos_nombres.get(codigo_dept, f"Departamento {codigo_dept}")
    
    def predecir_probabilidad(self, datos_nino: Dict) -> float:
        """
        Predice probabilidad de anemia para un niño individual
        """
        # Convertir dict a DataFrame para procesamiento
        df = pd.DataFrame([datos_nino])
        df_procesado = self._crear_variables_derivadas(df)
        
        # Calcular score lineal
        score_lineal = self.coeficientes['intercept']
        
        for variable, coef in self.coeficientes.items():
            if variable != 'intercept' and variable in df_procesado.columns:
                score_lineal += coef * df_procesado[variable].iloc[0]
        
        # Aplicar función logística
        probabilidad = 1 / (1 + np.exp(-score_lineal))
        
        return min(max(probabilidad, 0.05), 0.85)  # Límites realistas
    
    def clasificar_riesgo(self, probabilidad: float) -> Tuple[str, str, str]:
        """
        Clasifica el riesgo basado en umbrales optimizados
        Retorna: (categoria, descripcion, color)
        """
        if probabilidad >= 0.65:
            return "Alto", "Intervención inmediata requerida", "#e74c3c"
        elif probabilidad >= 0.45:
            return "Medio", "Monitoreo intensivo y prevención", "#f39c12"
        elif probabilidad >= 0.25:
            return "Bajo", "Seguimiento rutinario", "#3498db"
        else:
            return "Muy Bajo", "Población de referencia", "#2ecc71"
    
    def procesar_poblacion(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Procesa dataset completo y genera predicciones poblacionales
        """
        # Crear variables derivadas
        df_procesado = self._crear_variables_derivadas(df)
        
        # Calcular probabilidades para toda la población
        probabilidades = []
        
        for idx, row in df_procesado.iterrows():
            datos_nino = row.to_dict()
            prob = self.predecir_probabilidad(datos_nino)
            probabilidades.append(prob)
        
        # Agregar resultados al DataFrame
        df_resultado = df.copy()
        df_resultado['probabilidad_anemia'] = probabilidades
        df_resultado['score_riesgo'] = [int(p * 100) for p in probabilidades]
        
        # Clasificar riesgo
        clasificaciones = [self.clasificar_riesgo(p) for p in probabilidades]
        df_resultado['categoria_riesgo'] = [c[0] for c in clasificaciones]
        df_resultado['descripcion_riesgo'] = [c[1] for c in clasificaciones]
        df_resultado['color_riesgo'] = [c[2] for c in clasificaciones]
        
        # Agregar nombres de departamentos
        if 'departamento' in df_resultado.columns:
            df_resultado['departamento_nombre'] = df_resultado['departamento'].apply(
                self.obtener_nombre_departamento
            )
        
        return df_resultado
    
    def generar_metricas_poblacion(self, df_resultado: pd.DataFrame) -> Dict:
        """
        Genera métricas de impacto poblacional
        """
        total_ninos = len(df_resultado)
        
        # Distribución por riesgo
        distribucion_riesgo = df_resultado['categoria_riesgo'].value_counts()
        
        # Niños prioritarios (Alto + Medio)
        ninos_prioritarios = distribucion_riesgo.get('Alto', 0) + distribucion_riesgo.get('Medio', 0)
        
        # Métricas de impacto
        metricas = {
            'total_ninos': total_ninos,
            'prevalencia_estimada': df_resultado['probabilidad_anemia'].mean() * 100,
            'ninos_alto_riesgo': distribucion_riesgo.get('Alto', 0),
            'ninos_medio_riesgo': distribucion_riesgo.get('Medio', 0),
            'ninos_prioritarios': ninos_prioritarios,
            'porcentaje_focalizacion': (ninos_prioritarios / total_ninos) * 100,
            'casos_prevenibles_estimados': int(ninos_prioritarios * 0.25),  # 25% efectividad
            'distribucion_riesgo': distribucion_riesgo.to_dict()
        }
        
        return metricas

# Clase auxiliar para carga de datos
class CargadorDatos:
    """
    Utilidades para cargar y validar datasets
    """
    
    @staticmethod
    def cargar_dataset(filepath: str) -> pd.DataFrame:
        """Carga dataset desde CSV"""
        try:
            df = pd.read_csv(filepath)
            print(f"✅ Dataset cargado: {len(df)} registros, {df.shape[1]} variables")
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo {filepath}")
        except Exception as e:
            raise Exception(f"Error al cargar dataset: {str(e)}")
    
    @staticmethod
    def validar_variables_requeridas(df: pd.DataFrame, variables_requeridas: List[str]) -> bool:
        """Valida que el dataset tenga las variables necesarias"""
        variables_faltantes = set(variables_requeridas) - set(df.columns)
        
        if variables_faltantes:
            print(f"⚠️ Variables faltantes: {variables_faltantes}")
            return False
        
        print("✅ Todas las variables requeridas están presentes")
        return True
