import json
import sys

def main():
    try:
        print("Leyendo el archivo hashes.json del repositorio...")
        with open('hashes.json', 'r', encoding='utf-8') as f:
            parsed = json.load(f)
        
        # Localizamos dónde están los canales
        target_dict = parsed
        if isinstance(parsed, dict) and "hashes" in parsed:
            target_dict = parsed["hashes"]
        
        modified = False
        if isinstance(target_dict, dict):
            # 1. Intentamos buscar si ya existe alguna clave de la NBA/ESPN en el repo
            found = False
            for key in list(target_dict.keys()):
                if "nba" in key.strip().lower() or "espn" in key.strip().lower():
                    found = True
                    if "NBA League Pass" not in target_dict:
                        target_dict["NBA League Pass"] = target_dict[key]
                        print(f"¡Canal duplicado desde '{key}' como 'NBA League Pass'!")
                        modified = True
            
            # 2. RED DE SEGURIDAD: Si GitHub no tenía el canal, lo inyectamos directamente con tu hash exacto
            if not found and "NBA League Pass" not in target_dict:
                target_dict["NBA League Pass"] = "f4991d32784f9c236b087fc864c42bbd18f9720f"
                print("¡Canal 'NBA League Pass' inyectado directamente con el hash oficial!")
                modified = True
        
        if modified:
            with open('hashes.json', 'w', encoding='utf-8') as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)
            print("¡hashes.json actualizado y guardado correctamente en GitHub!")
        else:
            print("El alias 'NBA League Pass' ya estaba presente en el archivo.")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
