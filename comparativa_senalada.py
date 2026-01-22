"""
Comparativa detallada de modelos con tabla profesional
"""
import pandas as pd
import matplotlib.pyplot as plt
import json

def generar_tabla_comparativa():
    """Tabla comparativa profesional de los 3 modelos"""
    
    # Cargar metadatos
    with open('data/models/model_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    results = metadata['results']
    
    # Crear DataFrame
    data = []
    for model_name, metrics in results.items():
        data.append({
            'Modelo': model_name. replace('_', ' ').title(),
            'Accuracy (%)': f"{metrics['accuracy']*100:. 2f}",
            'Precision (%)': f"{metrics['precision']*100:.2f}",
            'Recall (%)': f"{metrics['recall']*100:.2f}",
            'F1-Score (%)': f"{metrics['f1_score']*100:. 2f}",
            'CV Method': metrics['cv_method']
        })
    
    df = pd.DataFrame(data)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    
    # Crear tabla
    table = ax.table(cellText=df.values, colLabels=df.columns,
                    cellLoc='center', loc='center',
                    colWidths=[0.25, 0.15, 0.15, 0.15, 0.15, 0.3])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    # Estilizar header
    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Estilizar filas
    colors = ['#ecf0f1', 'white']
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            table[(i, j)].set_facecolor(colors[i % 2])
            
            # Destacar mejor modelo
            if i == 2:  # Random Forest
                table[(i, j)].set_edgecolor('#2ecc71')
                table[(i, j)].set_linewidth(2)
    
    plt.title('Comparativa de Modelos de Aprendizaje Supervisado', 
             fontsize=14, fontweight='bold', pad=20)
    
    plt.savefig('reportes_tesis/TABLA_COMPARATIVA_MODELOS.png', dpi=300, bbox_inches='tight')
    print("✅ Tabla comparativa generada")
    plt.close()

if __name__ == '__main__':
    generar_tabla_comparativa()