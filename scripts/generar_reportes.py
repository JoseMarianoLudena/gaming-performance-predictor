"""
Generador de reportes profesionales para la tesis
Ejecutar desde scripts/:   python generar_reportes.py
O desde raíz:   python scripts/generar_reportes.py
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.metrics import confusion_matrix, classification_report
import joblib
import os
import sys

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class ReportGenerator:
    def __init__(self):
        self.output_dir = 'reportes_tesis'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # ✅ DETECTAR SI ESTAMOS EN scripts/ O EN RAÍZ
        if os. path.exists('data/processed/pilot_study_data.csv'):
            # Estamos en la raíz
            data_path = 'data/processed/pilot_study_data.csv'
            metadata_path = 'data/models/model_metadata.json'
            model_path = 'data/models/best_model.joblib'
        elif os.path.exists('../data/processed/pilot_study_data. csv'):
            # Estamos en scripts/
            data_path = '../data/processed/pilot_study_data.csv'
            metadata_path = '../data/models/model_metadata.json'
            model_path = '../data/models/best_model.joblib'
        else:
            raise FileNotFoundError("❌ No se encuentran los archivos.  Ejecuta desde la raíz o desde scripts/")
        
        # Cargar datos
        self.df = pd. read_csv(data_path)
        
        # Cargar metadatos
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        # Cargar mejor modelo
        self.best_model = joblib.load(model_path)
        
        print(f"✅ Datos cargados:  {len(self.df)} participantes")
    
    def generar_reporte_completo(self):
        """Genera todos los reportes y gráficos"""
        print("\n" + "="*70)
        print("📊 GENERATING PROFESSIONAL REPORTS FOR THESIS")
        print("="*70)
        
        # 1. Distribución de datos
        self.plot_distribucion_tiers()
        
        # 2. Comparativa de modelos
        self.plot_comparativa_modelos()
        
        # 3. Matriz de confusión
        self. plot_confusion_matrix()
        
        # 4. Feature Importance
        self.plot_feature_importance()
        
        # 5. Análisis de métricas por feature
        self.plot_features_por_tier()
        
        # 6. Curvas de aprendizaje
        self. plot_performance_metrics()
        
        # 7. Reporte escrito
        self.generar_reporte_texto()
        
        print(f"\n✅ All reports saved in: {self.output_dir}/")
        print("="*70)
    
    def plot_distribucion_tiers(self):
        """Gráfico de distribución de participantes por tier"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Gráfico 1: Conteo
        tier_counts = self.df['tier'].value_counts().sort_index()
        tier_labels = {0: 'Low\n(Bronze-Silver)', 1: 'Medium\n(Gold-Platinum)', 2: 'High\n(Diamond+)'}
        
        colors = ['#e74c3c', '#f39c12', '#2ecc71']
        axes[0].bar([tier_labels[i] for i in tier_counts. index], 
                   tier_counts.values, color=colors, alpha=0.7, edgecolor='black')
        axes[0].set_ylabel('Number of Participants', fontsize=12)
        axes[0].set_title('Participant Distribution by Tier', fontsize=14, fontweight='bold')
        axes[0].grid(axis='y', alpha=0.3)
        
        for i, (tier, count) in enumerate(tier_counts.items()):
            axes[0].text(i, count + 5, str(count), ha='center', fontweight='bold', fontsize=11)
        
        # Gráfico 2: Porcentaje
        axes[1].pie(tier_counts.values, labels=[tier_labels[i] for i in tier_counts.index],
                   autopct='%1.1f%%', colors=colors, startangle=90, 
                   textprops={'fontsize': 11, 'fontweight': 'bold'})
        axes[1].set_title('Participant Proportion', fontsize=14, fontweight='bold')
        
        plt. tight_layout()
        plt.savefig(f'{self. output_dir}/1_distribucion_tiers.png', dpi=300, bbox_inches='tight')
        print("  ✅ Graph 1: Tier distribution")
        plt.close()
    
    def plot_comparativa_modelos(self):
        """Comparativa de rendimiento de los 3 modelos"""
        results = self.metadata['results']
        
        models = list(results.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        metric_labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(models))
        width = 0.2
        
        colors = ['#3498db', '#9b59b6', '#e74c3c', '#2ecc71']
        
        for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
            values = [results[model][metric] * 100 for model in models]
            ax.bar(x + i * width, values, width, label=label, color=colors[i], alpha=0.8)
        
        ax. set_xlabel('Model', fontsize=12, fontweight='bold')
        ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Supervised Learning Model Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels(['Logistic\nRegression', 'Random\nForest', 'Linear\nSVM'])
        ax.legend(loc='lower right', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([75, 95])
        
        # Añadir línea del mejor modelo
        best_acc = max([results[m]['accuracy'] for m in models]) * 100
        ax.axhline(y=best_acc, color='red', linestyle='--', linewidth=2, alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/2_comparativa_modelos.png', dpi=300, bbox_inches='tight')
        print("  ✅ Graph 2: Model comparison")
        plt.close()
    
    def plot_confusion_matrix(self):
        """Matriz de confusión del mejor modelo"""
        # Obtener matriz de confusión del metadata
        best_model_name = self.metadata['best_model']
        cm = np.array(self.metadata['results'][best_model_name]['confusion_matrix'])
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Count'},
                   xticklabels=['Low', 'Medium', 'High'],
                   yticklabels=['Low', 'Medium', 'High'],
                   ax=ax, annot_kws={'fontsize': 14, 'fontweight': 'bold'})
        
        ax.set_xlabel('Prediction', fontsize=13, fontweight='bold')
        ax.set_ylabel('Actual Value', fontsize=13, fontweight='bold')
        ax.set_title(f'Confusion Matrix - {best_model_name.replace("_", " ").title()}\n' + 
                    f'Accuracy: {self.metadata["results"][best_model_name]["accuracy"]*100:.2f}%',
                    fontsize=14, fontweight='bold')
        
        # Calcular accuracy por tier
        accuracies = cm.diagonal() / cm.sum(axis=1)
        for i, acc in enumerate(accuracies):
            ax.text(3.5, i + 0.5, f'{acc*100:.1f}%', 
                   fontsize=11, fontweight='bold', va='center')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/3_matriz_confusion.png', dpi=300, bbox_inches='tight')
        print("  ✅ Graph 3: Confusion matrix")
        plt.close()
    
    def plot_feature_importance(self):
        """Feature Importance del Random Forest"""
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model. feature_importances_
            
            features = [
                'Reaction Time\n(Mean)',
                'Reaction Time\n(Std Dev)',
                'False Starts',
                'Aim\nAccuracy',
                'Time to\nTarget',
                'Miss Rate',
                'Clicks/Minute',
                'Error Rate',
                'Total Test\nDuration'
            ]
            
            # Ordenar por importancia
            indices = np.argsort(importances)[::-1]
            
            fig, ax = plt.subplots(figsize=(12, 7))
            
            colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(features)))
            bars = ax.barh([features[i] for i in indices], 
                          importances[indices] * 100, 
                          color=colors, edgecolor='black', alpha=0.8)
            
            ax.set_xlabel('Importance (%)', fontsize=12, fontweight='bold')
            ax.set_title('Feature Importance\n' +
                        'Most Influential Motor and Cognitive Abilities',
                        fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Añadir valores
            for i, (bar, imp) in enumerate(zip(bars, importances[indices])):
                ax.text(imp * 100 + 0.5, bar.get_y() + bar.get_height()/2, 
                       f'{imp*100:.1f}%', va='center', fontsize=10, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(f'{self.output_dir}/4_feature_importance.png', dpi=300, bbox_inches='tight')
            print("  ✅ Graph 4: Feature importance")
            plt.close()
    
    def plot_features_por_tier(self):
        """Distribución de features por tier"""
        features_to_plot = [
            ('reaction_ms_mean', 'Reaction Time (ms)'),
            ('aim_accuracy', 'Aim Accuracy'),
            ('cpm', 'Clicks per Minute'),
            ('mean_time_to_hit_ms', 'Time to Target (ms)')
        ]
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        tier_labels = {0: 'Low', 1: 'Medium', 2: 'High'}
        colors = ['#e74c3c', '#f39c12', '#2ecc71']
        
        for idx, (feature, title) in enumerate(features_to_plot):
            ax = axes[idx]
            
            for tier in [0, 1, 2]:  
                data = self.df[self.df['tier'] == tier][feature]
                ax.hist(data, bins=30, alpha=0.6, label=tier_labels[tier], 
                       color=colors[tier], edgecolor='black')
            
            ax.set_xlabel(title, fontsize=11, fontweight='bold')
            ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
            ax.set_title(f'Distribution: {title}', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
        
        plt.suptitle('Feature Analysis by Tier', fontsize=15, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/5_features_por_tier.png', dpi=300, bbox_inches='tight')
        print("  ✅ Graph 5: Features by tier")
        plt.close()
    
    def plot_performance_metrics(self):
        """Métricas de performance detalladas"""
        best_model_name = self.metadata['best_model']
        report = self.metadata['results'][best_model_name]['classification_report']
        
        tiers = ['Low', 'Medium', 'High']
        metrics = ['precision', 'recall', 'f1-score']
        metric_labels = ['Precision', 'Recall', 'F1-Score']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(tiers))
        width = 0.25
        
        colors = ['#3498db', '#9b59b6', '#2ecc71']
        
        for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
            values = [report[tier][metric] * 100 for tier in tiers]
            bars = ax.bar(x + i * width, values, width, label=label, color=colors[i], alpha=0.8)
            
            # Añadir valores
            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{val:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_xlabel('Tier', fontsize=12, fontweight='bold')
        ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'Performance Metrics by Tier - {best_model_name. replace("_", " ").title()}',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x + width)
        ax.set_xticklabels(tiers)
        ax.legend(loc='lower right', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([0, 105])
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/6_metricas_por_tier.png', dpi=300, bbox_inches='tight')
        print("  ✅ Graph 6: Metrics by tier")
        plt.close()
    
    def generar_reporte_texto(self):
        """Genera reporte en texto para la tesis"""
        best_model_name = self.metadata['best_model']
        results = self.metadata['results'][best_model_name]
        
        reporte = f"""
{'='*80}
REPORTE DE RESULTADOS - SISTEMA DE PREDICCIÓN DE SKILL TIER
{'='*80}

1. INFORMACIÓN DEL DATASET
{'─'*80}
   Total de Participantes: {len(self. df)}
   
   Distribución por Tier:
   {self.df['tier'].value_counts().sort_index().to_string()}
   
   Porcentaje por Tier:
   {(self.df['tier']. value_counts(normalize=True).sort_index() * 100).round(2).to_string()}%

2. MODELO SELECCIONADO
{'─'*80}
   Algoritmo: {best_model_name. replace('_', ' ').title()}
   Método de Validación: {self.metadata['validation_method']}
   Fecha de Entrenamiento: {self.metadata['training_date']}

3. MÉTRICAS GLOBALES
{'─'*80}
   Accuracy:    {results['accuracy']*100:.2f}% ± {results['accuracy_std']*100:.2f}%
   Precision (macro): {results['precision']*100:.2f}%
   Recall (macro): {results['recall']*100:.2f}%
   F1-Score (macro): {results['f1_score']*100:.2f}%

4. MÉTRICAS POR TIER
{'─'*80}
"""
        
        for tier in ['Low', 'Medium', 'High']:
            tier_metrics = results['classification_report'][tier]
            reporte += f"""
   {tier. upper()}:
     Precision: {tier_metrics['precision']*100:.2f}%
     Recall:     {tier_metrics['recall']*100:.2f}%
     F1-Score:  {tier_metrics['f1-score']*100:.2f}%
    Support:   {int(tier_metrics['support'])} participants

"""
        
        reporte += f"""
5. CONFUSION MATRIX
{'─'*80}
{np.array(results['confusion_matrix'])}

6. MODEL COMPARISON
{'─'*80}
"""
        
        for model_name, model_results in self.metadata['results'].items():
            reporte += f"""
   {model_name.replace('_', ' ').title()}:
     Accuracy:  {model_results['accuracy']*100:.2f}%
     F1-Score:  {model_results['f1_score']*100:.2f}%
"""
        
        reporte += f"""
{'='*80}
END OF REPORT
{'='*80}
"""
        
        # Guardar reporte
        with open(f'{self. output_dir}/REPORTE_COMPLETO.txt', 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        print("  ✅ Text report generated")

        
        # También imprimir en consola
        print(reporte)

# Ejecutar
if __name__ == '__main__':
    generator = ReportGenerator()
    generator.generar_reporte_completo()