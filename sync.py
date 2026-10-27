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

        # 1. Buscar exactamente el hash del canal "NBA ESPN 720p *"
        source_hash = None
        for channel in channels:
            title = channel.get("title", "")
            if title == "NBA ESPN 720p *" or title.lower() == "nba espn 720p *":
                source_hash = channel.get("hash")
                print(f"¡Canal fuente exacto localizado: '{title}' (Hash: {source_hash})!")
                break
        
        # Búsqueda flexible de respaldo por si hay variaciones de espacios
        if not source_hash:
            for channel in channels:
                title = channel.get("title", "").lower()
                if "nba espn 720p" in title or ("espn" in title and "720" in title):
                    source_hash = channel.get("hash")
                    print(f"¡Canal fuente flexible localizado: '{channel.get('title')}' (Hash: {source_hash})!")
                    break

        if not source_hash:
            source_hash = "328b312b08023249e858acbd3466dc07b1a21384"
            print("Aviso: No se encontró el canal exacto, usando hash de respaldo.")

        # 2. Asegurar que "NBA League Pass" tenga exactamente ese hash
        target_title = "NBA League Pass"
        found_target = False

        for channel in channels:
            if channel.get("title") == target_title:
                channel["hash"] = source_hash
                channel["group"] = "BALONCESTO"
                found_target = True
                print(f"¡Actualizado '{target_title}' con el hash de NBA ESPN 720p *!")
                break

        if not found_target:
            new_channel = {
                "title": target_title,
                "hash": source_hash,
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }
            channels.append(new_channel)
            print(f"¡Creado '{target_title}' enlazado al hash de NBA ESPN 720p *!")

        if isinstance(parsed, dict) and "hashes" in parsed:
            parsed["hashes"] = channels
        else:
            parsed = channels
            
        with open('hashes.json', 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        print("¡hashes.json actualizado con éxito!")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
