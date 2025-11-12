# main.py - SCRIPT PRINCIPAL (ACTUALIZADO)
import os
import sys

# Agregar la carpeta src al path para poder importar módulos
sys.path.append('src')

from src.sistema import SistemaDeteccionAnomalias

def verificar_estructura():
    """Verificar que toda la estructura del proyecto esté creada"""
    print("🔍 VERIFICANDO ESTRUCTURA DEL PROYECTO...")
    carpetas_requeridas = ['data', 'results']
    for carpeta in carpetas_requeridas:
        if not os.path.exists(carpeta):
            print(f"📁 Creando carpeta: {carpeta}")
            os.makedirs(carpeta, exist_ok=True)
    if not os.path.exists('data/dataset_ciberseguridad.csv'):
        print("❌ ERROR: Dataset no encontrado en data/dataset_ciberseguridad.csv")
        return False
    else:
        print("✅ Dataset encontrado")
        return True

def limpiar_resultados_anteriores():
    """Vacía la carpeta de resultados antes de una nueva ejecución."""
    print("\n🧹 LIMPIANDO RESULTADOS ANTERIORES...")
    results_dir = 'results'
    # Verificar si la carpeta existe y tiene archivos
    if os.path.exists(results_dir) and os.listdir(results_dir):
        for archivo in os.listdir(results_dir):
            os.remove(os.path.join(results_dir, archivo))
        print("✅ Carpeta 'results' limpiada.")
    else:
        print("✅ La carpeta 'results' ya está vacía.")

def main():
    """Función principal del proyecto"""
    print("🎯 PROYECTO COMPLETO - DETECCIÓN DE ANOMALÍAS EN CIBERSEGURIDAD")
    print("=" * 60)
    
    # 1. Verificar estructura
    if not verificar_estructura():
        return
    
    # 2. Limpiar resultados de ejecuciones pasadas
    limpiar_resultados_anteriores()
    
    # 3. Crear y ejecutar el sistema
    sistema = SistemaDeteccionAnomalias()
    sistema.ejecutar_sistema_completo()

if __name__ == "__main__":
    main()