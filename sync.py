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

        # Buscamos una plantilla existente de baloncesto/NBA/ESPN para copiar su hash
        nba_template = None
        for channel in channels:
            title = channel.get("title", "").lower()
            if "nba" in title or "espn" in title or "baloncesto" in title:
                nba_template = channel.copy()
                break
        
        if not nba_template:
            nba_template = {
                "title": "NBA League Pass",
                "hash": "f4991d32784f9c236b087fc864c42bbd18f9720f",
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }

        # Ampliamos masivamente las variantes por si el calendario usa nombres cortos o variados
        target_titles = [
            "NBA League Pass",
            "NBA",
            "League Pass",
            "NBA ESPN",
            "NBA TV",
            "NBA League Pass HD",
            "NBA *",
            "NBA League Pass *"
        ]

        existing_titles = {ch.get("title") for ch in channels}
        modified = False

        for target_title in target_titles:
            if target_title not in existing_titles:
                new_channel = nba_template.copy()
                new_channel["title"] = target_title
                channels.append(new_channel)
                print(f"¡Canal añadido a la lista: '{target_title}'!")
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
            print("Todos los títulos ya estaban presentes.")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
