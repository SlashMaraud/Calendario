import json
import sys

def main():
    try:
        print("Leyendo el archivo hashes.json...")
        with open('hashes.json', 'r', encoding='utf-8') as f:
            parsed = json.load(f)
        
        if isinstance(parsed, dict) and "hashes" in parsed and isinstance(parsed["hashes"], list):
            channels = parsed["hashes"]
        elif isinstance(parsed, list):
            channels = parsed
        else:
            channels = []

        # 1. Buscamos el hash exacto del canal "NBA ESPN 720*" o cualquier variante de NBA ESPN
        source_hash = None
        for channel in channels:
            title = channel.get("title", "")
            # Buscamos coincidencias que incluyan "nba espn"
            if "nba espn" in title.lower():
                source_hash = channel.get("hash")
                print(f"¡Encontrado canal fuente: '{title}' con hash: {source_hash}!")
                break
        
        # Si por lo que sea no lo encuentra exacto, buscamos cualquier variante de ESPN o baloncesto
        if not source_hash:
            for channel in channels:
                title = channel.get("title", "").lower()
                if "espn" in title or "baloncesto" in title:
                    source_hash = channel.get("hash")
                    break

        if not source_hash:
            print("Aviso: No se encontró el canal de NBA ESPN, usando hash de respaldo.")
            source_hash = "328b312b08023249e858acbd3466dc07b1a21384"

        # 2. Aseguramos que "NBA League Pass" (el de la web) exista y tenga el hash de NBA ESPN
        target_title = "NBA League Pass"
        found_target = False

        for channel in channels:
            if channel.get("title") == target_title:
                channel["hash"] = source_hash
                channel["group"] = "BALONCESTO"
                found_target = True
                print(f"¡Actualizado '{target_title}' para que use el hash de NBA ESPN!")
                break

        # Si no existía en el JSON, lo creamos directamente con ese hash
        if not found_target:
            new_channel = {
                "title": target_title,
                "hash": source_hash,
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }
            channels.append(new_channel)
            print(f"¡Creado nuevo canal '{target_title}' enlazado al hash de NBA ESPN!")

        if isinstance(parsed, dict) and "hashes" in parsed:
            parsed["hashes"] = channels
        else:
            parsed = channels
            
        with open('hashes.json', 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        print("¡hashes.json sincronizado correctamente!")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
