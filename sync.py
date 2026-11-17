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

        target_title = "NBA League Pass"
        found_league_pass = False

        # 1. Comprobar si "NBA League Pass" ya existe en tus canales
        for channel in channels:
            if channel.get("title", "").lower() == target_title.lower():
                found_league_pass = True
                break

        # 2. Si YA existe: No lo tocamos, se queda con su propio archivo/hash original.
        if found_league_pass:
            print(f"'{target_title}' existe en tus canales. Se mantiene intacto con su propio hash.")
        
        # 3. Si NO existe en absoluto: Buscamos el ID de NBA ESPN y lo creamos con ese ID.
        else:
            print(f"'{target_title}' no aparece en tus canales. Buscando 'NBA ESPN' para asignarle su ID...")
            
            source_hash = None
            for channel in channels:
                title = channel.get("title", "").lower()
                if "nba espn" in title:
                    source_hash = channel.get("hash")
                    break
            
            if not source_hash:
                source_hash = "328b312b08023249e858acbd3466dc07b1a21384" # ID de respaldo por defecto

            new_channel = {
                "title": target_title,
                "hash": source_hash,
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }
            channels.append(new_channel)
            print(f"¡Creado '{target_title}' asignándole el ID de NBA ESPN!")

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
