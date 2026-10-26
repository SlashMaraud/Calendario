import json
import sys

def main():
    try:
        # Leemos el archivo hashes.json que ya está en tu repositorio
        print("Leyendo el archivo hashes.json local...")
        with open('hashes.json', 'r', encoding='utf-8') as f:
            parsed = json.load(f)
        
        modified = False
        if isinstance(parsed, dict):
            # Buscamos cualquier variante de "nba espn" (720p, 1080p, etc.)
            for key in list(parsed.keys()):
                if "nba espn" in key.strip().lower():
                    # Si "NBA League Pass" no está creado o es diferente, lo mapeamos
                    if "NBA League Pass" not in parsed:
                        parsed["NBA League Pass"] = parsed[key]
                        print(f"¡Canal duplicado con éxito! 'NBA League Pass' mapeado desde '{key}'")
                        modified = True
                    else:
                        print("El alias 'NBA League Pass' ya existe en el JSON.")

        if modified:
            # Guardamos el archivo actualizado con el nuevo alias
            new_content = json.dumps(parsed, ensure_ascii=False, indent=2)
            with open('hashes.json', 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("hashes.json guardado correctamente con el alias de la NBA.")
        else:
            print("No se realizaron cambios (el alias ya estaba presente o no se encontró la clave).")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
