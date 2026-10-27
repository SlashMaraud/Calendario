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

        # 1. Buscamos el hash exacto del canal "NBA ESPN" o un equivalente de baloncesto
        target_hash = None
        for channel in channels:
            title = channel.get("title", "").lower()
            if "nba espn" in title or "espn" in title:
                target_hash = channel.get("hash")
                break
        
        # Si no encuentra ESPN específico, busca cualquier NBA o baloncesto
        if not target_hash:
            for channel in channels:
                title = channel.get("title", "").lower()
                if "nba" in title or "baloncesto" in title:
                    target_hash = channel.get("hash")
                    break

        if not target_hash:
            target_hash = "328b312b08023249e858acbd3466dc07b1a21384" # Fallback por seguridad

        # 2. El título exacto que la web emite y que la app busca
        web_title = "NBA League Pass"

        existing_titles = {ch.get("title") for ch in channels}
        modified = False

        if web_title not in existing_titles:
            new_channel = {
                "title": web_title,
                "hash": target_hash,
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }
            channels.append(new_channel)
            print(f"¡Canal puente añadido: '{web_title}' enlazado al hash de NBA ESPN!")
            modified = True

        if modified:
            if isinstance(parsed, dict) and "hashes" in parsed:
                parsed["hashes"] = channels
            else:
                parsed = channels
                
            with open('hashes.json', 'w', encoding='utf-8') as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)
            print("¡hashes.json actualizado con éxito!")
        else:
            print("El título ya estaba presente en el JSON.")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
