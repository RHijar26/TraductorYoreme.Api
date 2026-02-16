import re
import unicodedata

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent 
sys.path.insert(0, str(root))

from config import config 

def normalize(texto):
    """
    Normalización más completa para corpus de entrenamiento.
    """
    # 1. Convertir a minúsculas
    texto = texto.lower()
    
    # 2. Normalizar caracteres Unicode (é → e, ñ se mantiene)
    # Usar NFD para descomponer, luego eliminar acentos    
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(char for char in texto if unicodedata.category(char) != 'Mn')
    
    # 3. Normalizar comillas y apóstrofes
    texto = texto.replace('"', '"').replace('"', '"')
    texto = texto.replace(''', "'").replace(''', "'")
    
    # 4. Normalizar guiones
    texto = texto.replace('—', '-').replace('–', '-')
    
    # 5. Normalizar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    
    # 6. Eliminar espacios antes de puntuación
    texto = re.sub(r'\s+([.,;:!?])', r'\1', texto)
    
    # 7. Trim
    texto = texto.strip()
    
    return texto

def processCorpus(archivo_entrada, archivo_salida):
    """
    Procesa corpus con normalización avanzada.
    """
    print(f"Procesando (avanzado): {archivo_entrada}")
    
    lineas_procesadas = 0
    lineas_vacias = 0
    
    with open(archivo_entrada, 'r', encoding='utf-8') as f_in:
        with open(archivo_salida, 'w', encoding='utf-8') as f_out:
            for i, linea in enumerate(f_in, 1):
                # Normalizar
                linea_normalizada = normalize(linea)
                
                # Escribir solo si no está vacía
                if linea_normalizada:
                    if lineas_procesadas > 0:
                        f_out.write('\n' + linea_normalizada)
                    else:
                        f_out.write(linea_normalizada)
                    lineas_procesadas += 1
                else:
                    lineas_vacias += 1
                    print(f"  - Línea {i} eliminada (vacía tras normalización)")
                                              
    
    print(f"✓ Líneas procesadas: {lineas_procesadas:,}")
    print(f"✓ Líneas vacías eliminadas: {lineas_vacias:,}")
    print(f"✓ Guardado en: {archivo_salida}")

# Uso
if __name__ == "__main__":

    #Origen
    processCorpus(
        config.corpus_esp_clean_path(),
        config.corpus_esp_path()
    )
    #destino
    processCorpus(
        config.corpus_yor_clean_path(),
        config.corpus_yor_path()
    )