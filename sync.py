import json
import sys

def main():
    try:
        print("Leyendo el archivo hashes.json local...")
        with open('hashes.json', 'r', encoding='utf-8') as f:
            parsed = json.load(f)
        
        # Localizamos dónde están los canales (si están dentro de "hashes" o en la raíz)
        target_dict = parsed
        if isinstance(parsed, dict) and "hashes" in parsed:
            print("Estructura contenedora detectada. Buscando dentro de 'hashes'...")
            target_dict = parsed["hashes"]
        
        modified = False
        if isinstance(target_dict, dict):
            print(f"Explorando {len(target_dict)} elementos...")
            for key in list(target_dict.keys()):
                key_lower = key.strip().lower()
                if "nba espn" in key_lower:
                    print(f"-> ¡Canal encontrado: '{key}'!")
                    if "NBA League Pass" not in target_dict:
                        target_dict["NBA League Pass"] = target_dict[key]
                        print(f"   --> ¡Duplicado con éxito como 'NBA League Pass'!")
                        modified = True
                    else:
                        print(f"   --> El alias 'NBA League Pass' ya existía.")
        
        if modified:
            with open('hashes.json', 'w', encoding='utf-8') as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)
            print("¡hashes.json actualizado y guardado con éxito!")
        else:
            print("No se realizaron cambios (es posible que el canal de la NBA no esté todavía en este archivo).")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
