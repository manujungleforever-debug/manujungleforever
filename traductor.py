import sys
import argparse
import time

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Error: Librería no encontrada.")
    print("Por favor, instala la librería ejecutando el siguiente comando en la terminal:")
    print("pip install deep-translator")
    sys.exit(1)

def traducir_archivo(ruta_entrada, ruta_salida, idioma_origen='es', idioma_destino='en'):
    print(f"Iniciando traducción: {ruta_entrada} -> {ruta_salida}")
    print(f"De: {idioma_origen} a {idioma_destino}")
    
    try:
        with open(ruta_entrada, 'r', encoding='utf-8') as f:
            texto_original = f.read()
            
        # Dividir el texto en fragmentos (chunks) si es muy grande (límite de Google 5000 chars)
        max_chunk = 4500
        fragmentos = [texto_original[i:i+max_chunk] for i in range(0, len(texto_original), max_chunk)]
        
        traductor = GoogleTranslator(source=idioma_origen, target=idioma_destino)
        texto_traducido = ""
        
        for i, frag in enumerate(fragmentos):
            print(f"Tradiciendo fragmento {i+1}/{len(fragmentos)}...")
            texto_traducido += traductor.translate(frag)
            time.sleep(1) # Pausa pequeña para no saturar la API
            
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(texto_traducido)
            
        print("✅ Traducción completada con éxito. CERO tokens de IA consumidos.")
        
    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Traductor Local Gratuito (Sin Tokens)')
    parser.add_argument('entrada', help='Ruta del archivo a traducir (ej: post_es.md)')
    parser.add_argument('salida', help='Ruta donde guardar el archivo traducido (ej: post_en.md)')
    parser.add_argument('--origen', default='es', help='Idioma de origen (por defecto: es)')
    parser.add_argument('--destino', default='en', help='Idioma de destino (por defecto: en)')
    
    args = parser.parse_args()
    
    traducir_archivo(args.entrada, args.salida, args.origen, args.destino)
