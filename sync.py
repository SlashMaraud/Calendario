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

        # Buscamos un canal de baloncesto para copiar su hash como plantilla válida
        basket_template = None
        for channel in channels:
            title = channel.get("title", "").lower()
            if "baloncesto" in title or "dazn" in title:
                basket_template = channel.copy()
                break
        
        if not basket_template:
            basket_template = {
                "title": "DAZN Baloncesto 720p *",
                "hash": "328b312b08023249e858acbd3466dc07b1a21384",
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }

        # Títulos exactos que extrae la web y que debemos contemplar
        target_titles = [
            "NBA League Pass",
            "NBA",
            "League Pass"
        ]

        existing_titles = {ch.get("title") for ch in channels}
        modified = False

        for target_title in target_titles:
            if target_title not in existing_titles:
                new_channel = basket_template.copy()
                new_channel["title"] = target_title
                new_channel["group"] = "BALONCESTO"
                channels.append(new_channel)
                print(f"¡Canal añadido: '{target_title}'!")
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
            print("Los títulos ya estaban presentes.")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
