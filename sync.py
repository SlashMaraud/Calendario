import json
import sys

def main():
    try:
        print("Leyendo el archivo hashes.json local...")
        with open('hashes.json', 'r', encoding='utf-8') as f:
            parsed = json.load(f)
        
        print(f"Tipo de estructura detectada: {type(parsed)}")
        
        if isinstance(parsed, dict):
            print(f"Total de canales en el diccionario: {len(parsed)}")
            print(f"Ejemplos de claves (primeros 10): {list(parsed.keys())[:10]}")
            
            modified = False
            for key in list(parsed.keys()):
                # Buscamos cualquier pista de nba o espn de forma muy amplia
                key_lower = key.strip().lower()
                if "nba" in key_lower or "espn" in key_lower:
                    print(f"-> ¡Canal encontrado con coincidencia parcial!: '{key}'")
                    if "NBA League Pass" not in parsed:
                        parsed["NBA League Pass"] = parsed[key]
                        print(f"   --> ¡Duplicado con éxito como 'NBA League Pass'!")
                        modified = True
                    else:
                        print(f"   --> El alias 'NBA League Pass' ya existía.")
            
            if modified:
                with open('hashes.json', 'w', encoding='utf-8') as f:
                    json.dump(parsed, f, ensure_ascii=False, indent=2)
                print("¡hashes.json actualizado y guardado con éxito!")
            else:
                print("No se pudo duplicar porque ninguna clave cumplió la condición.")
                
        elif isinstance(parsed, list):
            print(f"El archivo es una lista con {len(parsed)} elementos.")
            print(f"Primer elemento de muestra: {parsed[0] if parsed else 'Vacío'}")
        else:
            print("Estructura de JSON no reconocida.")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
