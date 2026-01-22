"""
Pipeline completo de procesamiento de datos
Desde raw data hasta modelo entrenado
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

def visualizar_pipeline():
    """Genera diagrama visual del pipeline"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Colores
    color_input = '#3498db'
    color_process = '#f39c12'
    color_output = '#2ecc71'
    
    # PASO 1: Input
    paso1 = FancyBboxPatch((0.5, 10), 3, 1.2, boxstyle="round,pad=0.1", 
                          edgecolor=color_input, facecolor=color_input, alpha=0.3, linewidth=2)
    ax.add_patch(paso1)
    ax.text(2, 10.6, 'PASO 1: Recopilación', ha='center', fontsize=11, fontweight='bold')
    ax.text(2, 10.2, 'Mini-Test → Google Forms', ha='center', fontsize=9)
    
    # Flecha
    ax.arrow(2, 9.9, 0, -0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # PASO 2: CSV Raw
    paso2 = FancyBboxPatch((0.5, 8), 3, 1.2, boxstyle="round,pad=0.1",
                          edgecolor=color_input, facecolor=color_input, alpha=0.3, linewidth=2)
    ax.add_patch(paso2)
    ax.text(2, 8.6, 'PASO 2: Exportación', ha='center', fontsize=11, fontweight='bold')
    ax.text(2, 8.2, 'data/raw/pilot_data.csv', ha='center', fontsize=9, family='monospace')
    
    # Flecha
    ax. arrow(2, 7.9, 0, -0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # PASO 3: Procesamiento
    paso3 = FancyBboxPatch((0.5, 5.5), 3, 1.7, boxstyle="round,pad=0.1",
                          edgecolor=color_process, facecolor=color_process, alpha=0.3, linewidth=2)
    ax.add_patch(paso3)
    ax.text(2, 6.9, 'PASO 3: Procesamiento', ha='center', fontsize=11, fontweight='bold')
    ax.text(2, 6.5, '• Validación de columnas', ha='center', fontsize=8)
    ax.text(2, 6.2, '• Conversión rangos → tiers', ha='center', fontsize=8)
    ax.text(2, 5.9, '• Limpieza de outliers', ha='center', fontsize=8)
    
    # Flecha
    ax.arrow(3.6, 6.3, 1.3, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # PASO 4: Feature Engineering
    paso4 = FancyBboxPatch((5, 5.5), 3.5, 1.7, boxstyle="round,pad=0.1",
                          edgecolor=color_process, facecolor=color_process, alpha=0.3, linewidth=2)
    ax.add_patch(paso4)
    ax.text(6.75, 6.9, 'PASO 4: Feature Engineering', ha='center', fontsize=11, fontweight='bold')
    ax.text(6.75, 6.4, '9 Features Extraídas:', ha='center', fontsize=9, fontweight='bold')
    ax.text(6.75, 6.0, 'reaction_ms_mean, reaction_ms_std,', ha='center', fontsize=7, family='monospace')
    ax.text(6.75, 5.7, 'aim_accuracy, cpm, etc.', ha='center', fontsize=7, family='monospace')
    
    # Flecha hacia abajo
    ax.arrow(6.75, 5.4, 0, -0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # PASO 5: Normalización
    paso5 = FancyBboxPatch((5, 3.5), 3.5, 1.2, boxstyle="round,pad=0.1",
                          edgecolor=color_process, facecolor=color_process, alpha=0.3, linewidth=2)
    ax.add_patch(paso5)
    ax.text(6.75, 4.3, 'PASO 5: Normalización', ha='center', fontsize=11, fontweight='bold')
    ax.text(6.75, 3.8, 'StandardScaler (μ=0, σ=1)', ha='center', fontsize=9, family='monospace')
    
    # Flecha
    ax.arrow(6.75, 3.4, 0, -0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # PASO 6: Entrenamiento
    paso6 = FancyBboxPatch((5, 1.3), 3.5, 1.5, boxstyle="round,pad=0.1",
                          edgecolor=color_output, facecolor=color_output, alpha=0.3, linewidth=2)
    ax.add_patch(paso6)
    ax.text(6.75, 2.5, 'PASO 6: Entrenamiento', ha='center', fontsize=11, fontweight='bold')
    ax.text(6.75, 2.1, '3 Modelos + LOOCV', ha='center', fontsize=9)
    ax.text(6.75, 1.7, 'Random Forest (MEJOR)', ha='center', fontsize=9, fontweight='bold')
    
    # Flecha hacia salida
    ax.arrow(5, 2.1, -1.3, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # PASO 7: Output
    paso7 = FancyBboxPatch((0.5, 1.3), 3, 1.5, boxstyle="round,pad=0.1",
                          edgecolor=color_output, facecolor=color_output, alpha=0.3, linewidth=2)
    ax.add_patch(paso7)
    ax.text(2, 2.5, 'PASO 7: Modelos', ha='center', fontsize=11, fontweight='bold')
    ax.text(2, 2.1, 'best_model. joblib', ha='center', fontsize=8, family='monospace')
    ax.text(2, 1.8, 'scaler.joblib', ha='center', fontsize=8, family='monospace')
    ax.text(2, 1.5, 'metadata. json', ha='center', fontsize=8, family='monospace')
    
    # Título
    ax.text(5, 11.5, 'PIPELINE DE PROCESAMIENTO DE DATOS', ha='center', 
           fontsize=15, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('reportes_tesis/PIPELINE_PROCESAMIENTO.png', dpi=300, bbox_inches='tight')
    print("✅ Diagrama del pipeline generado")
    plt.close()

if __name__ == '__main__': 
    visualizar_pipeline()