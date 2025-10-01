# Deteccion_de_anomalias_en_datos_de_ciberseguridad
*Detección de intrusiones (CIC-IDS2017)
Descripción general
Este repositorio contiene un análisis exhaustivo del Conjunto de Datos de Evaluación de Detección de Intrusiones (CIC-IDS2017). El Instituto Canadiense de Ciberseguridad (CIC) diseñó este conjunto de datos para el desarrollo y la evaluación de sistemas de detección de intrusiones (IDS). El objetivo principal de este repositorio es mostrar la implementación y la comparación de diferentes modelos de aprendizaje automático para tareas de clasificación binaria y multiclase. El conjunto de datos se puede obtener aquí .

Características del conjunto de datos
Tamaño y composición
Se capturaron más de 2,8 millones de instancias durante 5 días (del 3 al 7 de julio de 2017).
Incluye tráfico normal y varios ataques: Fuerza Bruta, Heartbleed, Botnet, DoS, DDoS, Ataque Web e Infiltración.
Un conjunto de datos altamente desequilibrado con una mayoría de registros etiquetados como "benignos" (tráfico normal).
Características de los datos
79 columnas con 78 características numéricas y una columna 'Etiqueta' categórica.
Las características incluyen características del flujo de red, como duración del flujo, longitud de paquetes, puertos, indicadores y más.
Contenido
Características de los conjuntos de datos y análisis exploratorio de datos (EDA)
Información detallada sobre la estructura y las características del conjunto de datos y un EDA que resalta patrones y anomalías mediante visualizaciones.
Preprocesamiento de datos
Pasos tomados para limpiar los datos, manejar duplicados y valores faltantes, técnicas de optimización de memoria, estandarización de datos y aplicación de PCA para hacer que el conjunto de datos sea adecuado para el análisis.
Modelos de aprendizaje automático
Implementación y entrenamiento de diversos modelos de aprendizaje automático, incluyendo regresión logística, máquinas de vectores de soporte, clasificadores de bosque aleatorio, árboles de decisión y k-vecinos más cercanos. Se exploran clasificaciones binarias y multiclase.
Evaluación y discusión del desempeño
Se presentan métricas de evaluación como la precisión, la recuperación, la puntuación F1 y la matriz de confusión para cada modelo. Se analiza el impacto del desequilibrio de clases en el rendimiento del modelo.
Características principales
Uso de técnicas de preprocesamiento de datos, incluyendo estandarización para lograr uniformidad, análisis de componentes principales (PCA) para reducción de dimensionalidad y técnica de sobremuestreo de minorías sintéticas (SMOTE) para equilibrar la distribución de clases.
Implementa modelos de clasificación binarios y multiclase.
Utiliza algoritmos de aprendizaje automático que incluyen regresión logística, máquina de vectores de soporte (SVM), bosque aleatorio, árboles de decisión y K vecinos más cercanos (KNN).
Utiliza un conjunto de datos del mundo real para entrenamiento y pruebas.
Uso de validación cruzada para garantizar que los modelos no estén sobreajustados.
Proporciona un análisis exhaustivo y comparaciones de los diferentes algoritmos de clasificación.
Incluye métricas de evaluación del desempeño, como precisión, recuperación, exactitud, puntuación F1, matriz de confusión y más.
Ofrece información para mejorar la seguridad de la red seleccionando el modelo más adecuado*
