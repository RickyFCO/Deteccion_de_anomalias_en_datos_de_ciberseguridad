# Detección de Intrusiones (CIC-IDS2017)

## Descripción General
Este repositorio contiene un análisis exhaustivo del Conjunto de Datos de Evaluación de Detección de Intrusiones (CIC-IDS2017). El Instituto Canadiense de Ciberseguridad (CIC) diseñó este conjunto de datos para el desarrollo y la evaluación de sistemas de detección de intrusiones (IDS). El objetivo principal es mostrar la implementación y comparación de diferentes modelos de aprendizaje automático para tareas de clasificación binaria y multiclase.

📥 **El conjunto de datos se puede obtener [aquí](https://www.unb.ca/cic/datasets/ids-2017.html)**

## Características del Conjunto de Datos

### Tamaño y Composición
- Más de **2,8 millones de instancias** capturadas durante 5 días (del 3 al 7 de julio de 2017)
- Incluye tráfico normal y varios ataques:
  - Fuerza Bruta
  - Heartbleed
  - Botnet
  - DoS
  - DDoS
  - Ataque Web
  - Infiltración
- Conjunto de datos **altamente desequilibrado** con mayoría de registros etiquetados como "benignos"

### Características de los Datos
- **79 columnas** (78 características numéricas + 1 columna categórica 'Etiqueta')
- Características del flujo de red:
  - Duración del flujo
  - Longitud de paquetes
  - Puertos
  - Indicadores
  - Y más

## Contenido

### 🔍 Análisis Exploratorio de Datos (EDA)
- Información detallada sobre estructura y características del dataset
- Visualizaciones que destacan patrones y anomalías

### ⚙️ Preprocesamiento de Datos
- Limpieza de datos y manejo de duplicados/valores faltantes
- Técnicas de optimización de memoria
- Estandarización de datos
- Aplicación de PCA para reducción de dimensionalidad

### 🤖 Modelos de Aprendizaje Automático
Implementación y entrenamiento de:
- Regresión Logística
- Máquinas de Vectores de Soporte (SVM)
- Clasificadores de Bosque Aleatorio
- Árboles de Decisión
- K-Vecinos Más Cercanos (KNN)

### 📊 Evaluación de Desempeño
- Métricas: Precisión, Recall, F1-Score, Matriz de Confusión
- Análisis del impacto del desequilibrio de clases
- Comparación entre clasificación binaria y multiclase

## Características Principales

### 🛠️ Técnicas Implementadas
- **Preprocesamiento**: Estandarización, PCA, SMOTE
- **Modelos**: Clasificación binaria y multiclase
- **Algoritmos**: Regresión Logística, SVM, Random Forest, Decision Trees, KNN
- **Validación**: Validación cruzada para evitar overfitting

### 📈 Métricas de Evaluación
- Precisión (Accuracy)
- Recall (Sensibilidad)
- F1-Score
- Matriz de Confusión
- Análisis comparativo exhaustivo

### 🎯 Objetivo
Proporcionar información valiosa para mejorar la seguridad de red mediante la selección del modelo más adecuado para detección de intrusiones.

---

*Repositorio desarrollado con fines de investigación en ciberseguridad y machine learning*
