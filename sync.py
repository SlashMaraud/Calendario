import json
import sys
import urllib.request

def main():
    try:
        json_url = "https://ipfs.bytokyo.dpdns.org/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json"
        
        print("Leyendo el JSON desde IPFS...")
        
        req = urllib.request.Request(
            json_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            parsed = json.loads(response.read().decode('utf-8'))
        
        if isinstance(parsed, dict) and "hashes" in parsed and isinstance(parsed["hashes"], list):
            channels = parsed["hashes"]
        elif isinstance(parsed, list):
            channels = parsed
        else:
            channels = []

        target_keyword = "nba league pass"
        found_league_pass = False

        # Comprobamos de forma flexible si ya existe algún canal que contenga "nba league pass"
        for channel in channels:
            title = channel.get("title", "").lower()
            if target_keyword in title:
                found_league_pass = True
                print(f"¡Canal encontrado: '{channel.get('title')}'! Ya existe en tus canales, se respeta intacto.")
                break

        # Si de verdad no existe ninguno en absoluto, buscamos el de la ESPN y lo creamos
        if not found_league_pass:
            print("No se encontró ningún canal de League Pass en la fuente. Buscando NBA ESPN para crearlo...")
            
            source_hash = None
            for channel in channels:
                title = channel.get("title", "").lower()
                if "nba espn" in title:
                    source_hash = channel.get("hash")
                    break
            
            if not source_hash:
                source_hash = "328b312b08023249e858acbd3466dc07b1a21384"

            new_channel = {
                "title": "NBA League Pass",
                "hash": source_hash,
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }
            channels.append(new_channel)
            print("¡Creado 'NBA League Pass' usando el ID de NBA ESPN como comodín!")
        else:
            print("Los canales de League Pass ya están presentes en la fuente. No se modifica nada.")

        if isinstance(parsed, dict) and "hashes" in parsed:
            parsed["hashes"] = channels
        else:
            parsed = channels
            
        with open('hashes.json', 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
            
        print("¡hashes.json procesado con éxito!")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
