import json
import sys

def main():
    try:
        print("Leyendo el archivo hashes.json...")
        with open('hashes.json', 'r', encoding='utf-8') as f:
            parsed = json.load(f)
        
        # 'hashes' es una lista de canales, no un diccionario
        if isinstance(parsed, dict) and "hashes" in parsed and isinstance(parsed["hashes"], list):
            channels = parsed["hashes"]
        elif isinstance(parsed, list):
            channels = parsed
        else:
            channels = []

        # Buscamos una plantilla existente de la NBA/ESPN en la lista para copiar su hash y propiedades
        nba_template = None
        for channel in channels:
            title = channel.get("title", "").lower()
            if "nba" in title or "espn" in title:
                nba_template = channel.copy()
                break
        
        # Si por algún motivo no estuviera, usamos el hash oficial que nos pasaste
        if not nba_template:
            nba_template = {
                "title": "NBA ESPN 720p *",
                "hash": "f4991d32784f9c236b087fc864c42bbd18f9720f",
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }

        # Lista de títulos/alias que la app o la web de eventos podrían buscar
        target_titles = [
            "NBA League Pass",
            "NBA",
            "League Pass",
            "NBA ESPN",
            "NBA ESPN 720p *"
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
            print("Todos los títulos de la NBA ya estaban presentes en la lista.")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
