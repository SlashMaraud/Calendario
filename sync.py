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

        # 1. Encontrar un hash de referencia válido (baloncesto o ESPN)
        target_hash = None
        for channel in channels:
            title = channel.get("title", "").lower()
            if "espn" in title or "dazn" in title or "baloncesto" in title:
                if channel.get("hash"):
                    target_hash = channel.get("hash")
                    break
        
        if not target_hash:
            target_hash = "328b312b08023249e858acbd3466dc07b1a21384"

        # 2. Depurar la lista eliminando variantes confusas y asegurando la correcta
        cleaned_channels = []
        found_exact = False

        for channel in channels:
            title = channel.get("title", "")
            # Omitimos variantes sucias o con asteriscos para unificarlas
            if title.lower() in ["nba league pass *", "nba league pass hd", "nba *"]:
                continue
            if title == "NBA League Pass":
                found_exact = True
                if not channel.get("hash"):
                    channel["hash"] = target_hash
            cleaned_channels.append(channel)

        # Si no existía la entrada exacta limpia, la añadimos
        if not found_exact:
            new_channel = {
                "title": "NBA League Pass",
                "hash": target_hash,
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }
            cleaned_channels.append(new_channel)
            print("¡Entrada 'NBA League Pass' creada con éxito!")
        else:
            print("Entrada 'NBA League Pass' verificada y depurada.")

        if isinstance(parsed, dict) and "hashes" in parsed:
            parsed["hashes"] = cleaned_channels
        else:
            parsed = cleaned_channels
            
        with open('hashes.json', 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        print("¡hashes.json actualizado y guardado correctamente!")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
