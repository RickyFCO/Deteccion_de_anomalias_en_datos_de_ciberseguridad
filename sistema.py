# src/sistema.py - CLASE PRINCIPAL DEL SISTEMA (VERSIÓN FINAL)
import os
import time
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import json

class SistemaDeteccionAnomalias:
    def __init__(self):
        self.resultados = {}
        # El preprocesador se definirá dinámicamente
        self.preprocessor = None

    def cargar_y_dividir_datos(self):
        """Carga el dataset y lo divide en conjuntos de entrenamiento y prueba (70/30)"""
        print("\n📂 CARGANDO Y DIVIDIENDO DATASET...")
        try:
            df = pd.read_csv('data/dataset_ciberseguridad.csv')
            print(f"✅ Dataset cargado: {df.shape[0]:,} registros")
            
            # Separar características (X) y etiqueta (y)
            X = df.drop(columns=['label', 'attack_type'])
            y = df['label']
            
            # Dividir 70% para entrenamiento, 30% para prueba
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=None, stratify=y
            )
            print(f"   - Conjunto de entrenamiento: {X_train.shape[0]:,} registros")
            print(f"   - Conjunto de prueba: {X_test.shape[0]:,} registros")
            return X_train, X_test, y_train, y_test
        except FileNotFoundError:
            print("❌ ERROR: No se encontró 'data/dataset_ciberseguridad.csv'")
            return None, None, None, None

    def definir_y_ajustar_preprocesador(self, X_train):
        """Define y ajusta el pipeline de preprocesamiento (One-Hot Encoding y Scaler)"""
        print("\n⚙️ DEFINIENDO Y AJUSTANDO PREPROCESADOR...")
        
        # Identificar columnas numéricas y categóricas
        numeric_features = X_train.select_dtypes(include=np.number).columns.tolist()
        categorical_features = ['protocol_type', 'service', 'flag']
        
        # Crear el transformador de columnas
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ],
            remainder='passthrough' # Mantiene otras columnas si las hubiera
        )
        
        # Ajustar el preprocesador SOLO con los datos de entrenamiento
        self.preprocessor.fit(X_train)
        print("✅ Preprocesador ajustado con One-Hot Encoding y StandardScaler.")

    def aplicar_preprocesamiento(self, X):
        """Aplica el preprocesador ya ajustado a un conjunto de datos"""
        return self.preprocessor.transform(X)

    def optimizar_y_entrenar_modelos(self, X_train_proc, y_train):
        """Usa Grid Search para encontrar los mejores hiperparámetros y entrena los modelos"""
        print("\n🤖 OPTIMIZANDO Y ENTRENANDO MODELOS CON GRID SEARCH...")
        
        # --- Isolation Forest ---
        print("   - Optimizando Isolation Forest...")
        t_if = time.time()
        
        # Parámetros a probar para Isolation Forest
        params_if = {
            'contamination': [0.01, 0.05, 0.1],
            'n_estimators': [100, 200]
        }
        # random_state=None hace que el modelo no sea determinista
        grid_if = GridSearchCV(
            IsolationForest(random_state=None),
            param_grid=params_if,
            cv=3,              # 3-fold cross-validation
            scoring='f1',      # Optimizar para F1-Score
            n_jobs=-1          # Usar todos los procesadores
        )
        grid_if.fit(X_train_proc, y_train)
        
        print(f"   ✅ Mejor F1-Score encontrado: {grid_if.best_score_:.4f}")
        print(f"   ✅ Mejores parámetros: {grid_if.best_params_}")
        
        # Guardar el mejor modelo encontrado
        self.modelos = {'IsolationForest': grid_if.best_estimator_}
        print(f"   ✅ Isolation Forest optimizado y entrenado en {time.time() - t_if:.2f} segundos.")
        
        # --- DBSCAN (Nota de la metodología) ---
        print("\n   - Entrenando DBSCAN (sin Grid Search)...")
        print("     (Nota: DBSCAN no es apto para Grid Search por su naturaleza de clustering.")
        print("      Se entrena con parámetros fijos como benchmark).")
        t_db = time.time()
        self.modelos['DBSCAN'] = DBSCAN(eps=3.0, min_samples=10)
        self.modelos['DBSCAN'].fit(X_train_proc)
        print(f"   ✅ DBSCAN entrenado en {time.time() - t_db:.2f} segundos.")

    def evaluar_modelos(self, X_test_proc, y_test):
        """Evalúa los modelos en el conjunto de prueba"""
        print("\n📊 EVALUANDO MODELOS EN EL CONJUNTO DE PRUEBA...")
        
        for nombre, modelo in self.modelos.items():
            print(f"--- {nombre} ---")
            
            # Predecir en el conjunto de prueba
            pred_raw = modelo.fit_predict(X_test_proc)
            predicciones = np.where(pred_raw == -1, 1, 0)
            
            # Calcular métricas
            f1 = f1_score(y_test, predicciones)
            precision = precision_score(y_test, predicciones)
            recall = recall_score(y_test, predicciones)
            cm = confusion_matrix(y_test, predicciones)
            
            # Calcular curva ROC y AUC
            # Para Isolation Forest, usamos decision_function. DBSCAN no lo tiene.
            if hasattr(modelo, 'decision_function'):
                scores = modelo.decision_function(X_test_proc)
                # Invertimos el score, ya que IF da valores más bajos a las anomalías
                fpr, tpr, _ = roc_curve(y_test, -scores)
                roc_auc = auc(fpr, tpr)
            else:
                fpr, tpr, roc_auc = None, None, None

            self.resultados[nombre] = {
                'f1_score': f1, 'precision': precision, 'recall': recall,
                'confusion_matrix': cm.tolist(), 'anomalias_detectadas': int(np.sum(predicciones)),
                'fpr': fpr.tolist() if fpr is not None else None,
                'tpr': tpr.tolist() if tpr is not None else None,
                'roc_auc': roc_auc
            }
            
            print(f"   - F1-Score: {f1:.4f}, Precisión: {precision:.4f}, Recall: {recall:.4f}")
            if roc_auc is not None:
                print(f"   - AUC-ROC: {roc_auc:.4f}")

    def generar_graficos(self):
        """Genera y guarda gráficos de resultados"""
        print("\n🎨 GENERANDO GRÁFICOS DE RESULTADOS...")
        for nombre, res in self.resultados.items():
            # Matriz de Confusión
            plt.figure(figsize=(8, 6))
            sns.heatmap(res['confusion_matrix'], annot=True, fmt='d', cmap='Blues',
                        xticklabels=['Normal', 'Anomalía'], yticklabels=['Normal', 'Anomalía'])
            plt.title(f'Matriz de Confusión - {nombre}')
            plt.ylabel('Etiqueta Real'); plt.xlabel('Etiqueta Predicha')
            plt.savefig(f"results/confusion_matrix_{nombre}.png")
            plt.close()
            
            # Curva ROC (si está disponible)
            if res['roc_auc'] is not None:
                plt.figure(figsize=(8, 6))
                plt.plot(res['fpr'], res['tpr'], color='darkorange', lw=2,
                         label=f"Curva ROC (área = {res['roc_auc']:.2f})")
                plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
                plt.xlim([0.0, 1.0]); plt.ylim([0.0, 1.05])
                plt.xlabel('Tasa de Falsos Positivos'); plt.ylabel('Tasa de Verdaderos Positivos')
                plt.title(f'Curva ROC - {nombre}'); plt.legend(loc="lower right")
                plt.savefig(f"results/roc_curve_{nombre}.png")
                plt.close()
        print("✅ Gráficos guardados en 'results/'.")

    def guardar_resultados(self):
        """Guardar las métricas en archivos de texto y JSON"""
        # (Esta función no necesita cambios, se mantiene igual que antes)
        print("\n💾 GUARDANDO RESULTADOS...")
        # Guardar resumen en .txt
        with open("results/resumen_resultados.txt", 'w') as f:
            for nombre, metrics in self.resultados.items():
                f.write(f"--- MODELO: {nombre} ---\n")
                f.write(f"F1-Score: {metrics['f1_score']:.4f}\n")
                f.write(f"Precision: {metrics['precision']:.4f}\n")
                f.write(f"Recall: {metrics['recall']:.4f}\n")
                if metrics['roc_auc'] is not None:
                    f.write(f"AUC-ROC: {metrics['roc_auc']:.4f}\n")
                f.write(f"Anomalías detectadas: {metrics['anomalias_detectadas']:,}\n\n")
        print("✅ Resultados guardados en 'results/'.")

    def ejecutar_sistema_completo(self):
        """Ejecutar el pipeline completo de Machine Learning"""
        print("\n🚀 INICIANDO PIPELINE COMPLETO DE MACHINE LEARNING")
        print("=" * 60)
        
        inicio = time.time()
        
        # 1. Cargar y Dividir Datos (70/30)
        X_train, X_test, y_train, y_test = self.cargar_y_dividir_datos()
        if X_train is None: return
        
        # 2. Definir y Ajustar Preprocesador (con datos de entrenamiento)
        self.definir_y_ajustar_preprocesador(X_train)
        
        # 3. Aplicar Preprocesamiento
        X_train_proc = self.aplicar_preprocesamiento(X_train)
        X_test_proc = self.aplicar_preprocesamiento(X_test)

        # 4. Optimizar y Entrenar Modelos (con datos de entrenamiento)
        self.optimizar_y_entrenar_modelos(X_train_proc, y_train)
        
        # 5. Evaluar Modelos (con datos de prueba)
        self.evaluar_modelos(X_test_proc, y_test)
        
        # 6. Generar Gráficos
        self.generar_graficos()
        
        # 7. Guardar Resultados
        self.guardar_resultados()
        
        print(f"\n🎉 ¡PIPELINE EJECUTADO CON ÉXITO en {time.time() - inicio:.2f} segundos!")
        print("   Puedes revisar los resultados finales en la carpeta 'results/'.")