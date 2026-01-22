"""
Script simplificado para entrenar modelos con datos del estudio piloto
Procesa CSV exportado de Google Sheets y entrena modelos ML
"""
import pandas as pd
import sys
import os

# Agregar backend al path
sys.path.append('backend')

from backend.models.tier_mapping import rank_to_tier
from backend.models.train import ModelTrainer

def main():
    print("=" * 70)
    print("🎯 ENTRENAMIENTO DE MODELOS - GAMING PERFORMANCE PREDICTOR")
    print("=" * 70)
    
    # ========== PASO 1: CARGAR DATOS DEL CSV ==========
    print("\n📂 PASO 1: Cargando datos del estudio piloto...")
    
    csv_path = 'data/raw/pilot_data.csv'
    
    if not os.path.exists(csv_path):
        print(f"\n❌ ERROR: No se encuentra el archivo:  {csv_path}")
        print(f"\n📝 Asegúrate de:")
        print(f"   1. Exportar Google Sheets como CSV")
        print(f"   2. Guardar como: data/raw/pilot_data.csv")
        print(f"   3. El CSV debe tener estas columnas:")
        print(f"      participant_id,date,game,rank,reaction_ms_mean,...")
        return False
    
    df = pd.read_csv(csv_path)
    print(f"✅ {len(df)} participantes cargados")
    
    # Mostrar primeras filas
    print(f"\n📋 Primeras 3 filas:")
    print(df.head(3))
    
    # ========== PASO 2: VALIDAR COLUMNAS ==========
    print(f"\n🔍 PASO 2: Validando estructura...")
    
    required_cols = [
        'participant_id', 'date', 'game', 'rank',
        'reaction_ms_mean', 'reaction_ms_std', 'false_starts',
        'aim_accuracy', 'mean_time_to_hit_ms', 'miss_rate',
        'cpm', 'error_rate', 'test_duration_s'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"\n❌ ERROR: Faltan columnas requeridas:")
        for col in missing_cols: 
            print(f"   - {col}")
        print(f"\n📋 Columnas encontradas: {df.columns.tolist()}")
        return False
    
    print(f"✅ Todas las columnas necesarias están presentes")
    
    # ========== PASO 3: VERIFICAR VALORES FALTANTES ==========
    print(f"\n🔍 PASO 3: Verificando valores faltantes...")
    
    missing = df[required_cols].isnull().sum()
    if missing.any():
        print(f"⚠️  Valores faltantes encontrados:")
        print(missing[missing > 0])
        
        response = input(f"\n¿Eliminar filas con valores faltantes? (s/n):  ").lower()
        if response == 's':
            df = df.dropna(subset=required_cols)
            print(f"✅ Filas eliminadas.  Quedan {len(df)} participantes")
    else:
        print(f"✅ No hay valores faltantes")
    
    # ========== PASO 4: CONVERTIR RANGOS A TIERS ==========
    print(f"\n🎮 PASO 4: Convirtiendo rangos a tiers comunes...")
    
    tiers = []
    errors = []
    
    for idx, row in df.iterrows():
        try:
            tier = rank_to_tier(row['game'], row['rank'])
            tiers.append(tier)
            print(f"  ✅ {row['participant_id']}: {row['game']} {row['rank']} → Tier {tier}")
        except ValueError as e:
            errors.append(f"  ❌ Fila {idx} ({row['participant_id']}): {e}")
            tiers.append(None)
    
    if errors:
        print(f"\n⚠️  Errores al convertir rangos:")
        for error in errors:
            print(error)
        
        print(f"\n💡 Rangos válidos por juego:")
        print(f"   Valorant:    Iron 1, Bronze 2, Silver 3, Gold 2, Platinum 1, Diamond 3, etc.")
        print(f"   CS:GO:      Silver I, Gold Nova II, Legendary Eagle, The Global Elite, etc.")
        print(f"   Fortnite:   Bronze I, Gold II, Platinum III, Diamond I, etc.")
        print(f"   Warzone:    Bronze, Silver, Gold, Platinum, Diamond, etc.")
        
        return False
    
    df['tier'] = tiers
    df = df.dropna(subset=['tier'])
    df['tier'] = df['tier']. astype(int)
    
    # ========== PASO 5: MOSTRAR DISTRIBUCIÓN ==========
    print(f"\n📊 PASO 5: Distribución de tiers:")
    
    tier_counts = df['tier'].value_counts().sort_index()
    tier_labels = {0: 'Low', 1: 'Medium', 2: 'High'}
    
    for tier, count in tier_counts. items():
        percentage = (count / len(df)) * 100
        label = tier_labels[tier]
        bar = '█' * int(percentage / 2)
        print(f"  {label:8s} (Tier {tier}): {count:3d} participantes ({percentage:5.1f}%) {bar}")

    
    # Verificar distribución mínima
    if len(tier_counts) < 3:
        print(f"\n⚠️  ADVERTENCIA: Faltan datos de algunos tiers")
        print(f"   Para mejores resultados, necesitas datos de los 3 tiers")
    
    min_samples_per_tier = 3
    if any(tier_counts < min_samples_per_tier):
        print(f"\n⚠️  ADVERTENCIA:  Algunos tiers tienen menos de {min_samples_per_tier} muestras")
        print(f"   Esto puede afectar la precisión del modelo")
    
    # ========== PASO 6: VALIDAR RANGOS DE VALORES ==========
    print(f"\n🔍 PASO 6: Validando rangos de valores...")
    
    validations = {
        'reaction_ms_mean': (100, 500),
        'reaction_ms_std': (5, 100),
        'false_starts':  (0, 10),
        'aim_accuracy':  (0, 1),
        'mean_time_to_hit_ms': (100, 2000),
        'miss_rate':  (0, 1),
        'cpm': (50, 1000),
        'error_rate': (0, 0.5),
        'test_duration_s': (50, 150)
    }
    
    has_issues = False
    for col, (min_val, max_val) in validations.items():
        out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
        if len(out_of_range) > 0:
            has_issues = True
            print(f"  ⚠️  {col}:  {len(out_of_range)} valores fuera de [{min_val}, {max_val}]")
            print(f"      Valores: {out_of_range[col].values}")
    
    if not has_issues:
        print(f"  ✅ Todos los valores están en rangos esperados")
    
    # ========== PASO 7: GUARDAR DATOS PROCESADOS ==========
    print(f"\n💾 PASO 7: Guardando datos procesados...")
    
    feature_columns = [
        'reaction_ms_mean', 'reaction_ms_std', 'false_starts',
        'aim_accuracy', 'mean_time_to_hit_ms', 'miss_rate',
        'cpm', 'error_rate', 'test_duration_s', 'tier'
    ]
    
    df_processed = df[feature_columns]. copy()
    
    output_path = 'data/processed/pilot_study_data.csv'
    os.makedirs(os.path. dirname(output_path), exist_ok=True)
    df_processed.to_csv(output_path, index=False)
    
    print(f"✅ Datos procesados guardados en: {output_path}")
    print(f"📊 {len(df_processed)} participantes válidos")
    
    # ========== PASO 8: ENTRENAR MODELOS ==========
    print(f"\n" + "=" * 70)
    print(f"🤖 PASO 8: ENTRENANDO MODELOS CON LOOCV")
    print(f"=" * 70)
    
    trainer = ModelTrainer()
    
    # Cargar datos
    X, y = trainer.load_data(output_path)
    
    # Entrenar todos los modelos
    results = trainer.train_all_models(X, y, use_loocv=True)
    
    # Guardar modelos
    trainer.save_models('data/models')
    
    # ========== RESUMEN FINAL ==========
    print(f"\n" + "=" * 70)
    print(f"🎉 ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print(f"=" * 70)
    
    print(f"\n📊 Resumen de Resultados:")
    print(f"\n{'Modelo':<25} {'Accuracy':<12} {'Precision':<12} {'F1-Score':<12}")
    print(f"{'-'*60}")
    
    for model_name, res in results.items():
        print(f"{model_name:<25} {res['accuracy']:.4f}      {res['precision']:.4f}      {res['f1_score']:.4f}")
    
    print(f"\n🏆 Mejor Modelo: {trainer.best_model_name. upper()}")
    print(f"🎯 Accuracy (LOOCV): {results[trainer.best_model_name]['accuracy']:.4f}")
    
    print(f"\n📦 Archivos generados:")
    print(f"   data/processed/pilot_study_data.csv")
    print(f"   data/models/best_model.joblib")
    print(f"   data/models/scaler.joblib")
    print(f"   data/models/logistic_regression.joblib")
    print(f"   data/models/random_forest.joblib")
    print(f"   data/models/linear_svm.joblib")
    print(f"   data/models/model_metadata.json")
    
    print(f"\n🚀 Siguiente paso: Iniciar la API")
    print(f"   cd backend")
    print(f"   python app.py")
    
    print(f"\n" + "=" * 70)
    
    return True

if __name__ == '__main__':
    success = main()
    
    if not success:
        print(f"\n❌ El entrenamiento no pudo completarse")
        print(f"💡 Revisa los errores arriba y corrige los datos")
        sys.exit(1)