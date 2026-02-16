import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent 
sys.path.insert(0, str(root))

from config import config 

def analizar_corpus(archivo):
    """
    Analiza problemas de capitalización en el corpus.
    """
    print(f"\n{'='*60}")
    print(f"Analizando: {archivo}")
    print(f"{'='*60}\n")
    
    palabras_variantes = {}
    total_lineas = 0
    palabras_unicas = set()
    
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            total_lineas += 1
            palabras = linea.strip().split()            

            for palabra in palabras:
                # Guardar palabra original
                palabras_unicas.add(palabra)
                
                # Agrupar por versión en minúsculas
                palabra_lower = palabra.lower()
                if palabra_lower not in palabras_variantes:
                    palabras_variantes[palabra_lower] = []
                palabras_variantes[palabra_lower].append(palabra)
    
    # Encontrar palabras con múltiples variantes
    problemas = {}
    for palabra_base, variantes in palabras_variantes.items():
        variantes_unicas = set(variantes)
        if len(variantes_unicas) > 1:
            problemas[palabra_base] = {
                'variantes': list(variantes_unicas),
                'frecuencia': len(variantes)
            }
    
    # Reportar estadísticas
    print(f"📊 Estadísticas:")
    print(f"  - Total de líneas: {total_lineas:,}")
    print(f"  - Palabras únicas (con mayúsculas): {len(palabras_unicas):,}")
    print(f"  - Palabras únicas (sin mayúsculas): {len(palabras_variantes):,}")
    print(f"  - Palabras con variantes de capitalización: {len(problemas):,}")
    
    # Calcular ahorro potencial
    ahorro = len(palabras_unicas) - len(palabras_variantes)
    porcentaje_ahorro = (ahorro / len(palabras_unicas) * 100) if palabras_unicas else 0
    print(f"\n💡 Ahorro potencial en vocabulario: {ahorro:,} palabras ({porcentaje_ahorro:.1f}%)")
    
    # Mostrar ejemplos de problemas
    if problemas:
        print(f"\n⚠️  Ejemplos de palabras con variantes:")
        for i, (palabra_base, info) in enumerate(list(problemas.items())[:10]):
            print(f"  {i+1}. '{palabra_base}' tiene {len(info['variantes'])} variantes:")
            print(f"     {', '.join(info['variantes'])}")
    
    return {
        'total_lineas': total_lineas,
        'vocabulario_original': len(palabras_unicas),
        'vocabulario_normalizado': len(palabras_variantes),
        'problemas': len(problemas),
        'ahorro': ahorro
    }

# Uso
if __name__ == "__main__":
    stats_origen = analizar_corpus(config.corpus_esp_path())
    stats_destino = analizar_corpus(config.corpus_yor_path())
    
    print(f"\n{'='*60}")
    print("RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"\nAhorro total en vocabulario:")
    print(f"  - Origen: {stats_origen['ahorro']:,} palabras")
    print(f"  - Destino: {stats_destino['ahorro']:,} palabras")
    print(f"  - Total: {stats_origen['ahorro'] + stats_destino['ahorro']:,} palabras")