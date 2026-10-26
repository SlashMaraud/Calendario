import json
import sys

def main():
    try:
        print("Leyendo el archivo hashes.json...")
        with open('hashes.json', 'r', encoding='utf-8') as f:
            parsed = json.load(f)
        
        # Localizamos dónde están los canales
        target_dict = parsed
        if isinstance(parsed, dict) and "hashes" in parsed:
            target_dict = parsed["hashes"]
        
        modified = False
        if isinstance(target_dict, dict):
            # Buscamos el hash de la NBA/ESPN existente
            source_hash = None
            for key in list(target_dict.keys()):
                key_lower = key.strip().lower()
                if "nba" in key_lower or "espn" in key_lower:
                    source_hash = target_dict[key]
                    break
            
            # Si no se encuentra en el archivo, usamos el hash oficial conocido
            if not source_hash:
                source_hash = "f4991d32784f9c236b087fc864c42bbd18f9720f"
            
            # Lista completa de posibles nombres que la app o la web de eventos puedan buscar
            aliases = [
                "NBA League Pass", 
                "NBA", 
                "League Pass", 
                "NBA ESPN", 
                "NBA TV",
                "NBA ESPN 720p *"
            ]
            
            for alias in aliases:
                if alias not in target_dict:
                    target_dict[alias] = source_hash
                    print(f"¡Alias creado con éxito: '{alias}'!")
                    modified = True
        
        if modified:
            with open('hashes.json', 'w', encoding='utf-8') as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)
            print("¡hashes.json actualizado con todos los alias de la NBA!")
        else:
            print("Todos los alias ya estaban configurados correctamente.")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
