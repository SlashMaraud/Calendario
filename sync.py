import json
import sys
import urllib.request

def main():
    try:
        json_url = "https://ipfs.bytokyo.dpdns.org/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json"
        
        print("Leyendo el JSON desde IPFS...")
        
        # Petición simulando ser un navegador web para evitar el error 403
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

        # Comprobamos si "NBA League Pass" ya existe en la lista de IPFS
        for channel in channels:
            if channel.get("title", "").lower() == target_title.lower():
                found_league_pass = True
                break

        # Si NO existe, lo creamos utilizando NBA ESPN como respaldo para que haga match
        if not found_league_pass:
            print(f"'{target_title}' no está en la lista de IPFS. Buscando 'NBA ESPN' para usarlo como respaldo...")
            
            source_hash = None
            # Buscar el hash del canal fuente "NBA ESPN 720p *"
            for channel in channels:
                title = channel.get("title", "")
                if title == "NBA ESPN 720p *" or title.lower() == "nba espn 720p *":
                    source_hash = channel.get("hash")
                    break
            
            # Búsqueda flexible por si varía el nombre de ESPN
            if not source_hash:
                for channel in channels:
                    title = channel.get("title", "").lower()
                    if "nba espn 720p" in title or ("espn" in title and "720" in title):
                        source_hash = channel.get("hash")
                        break

            # Hash de respaldo final por si tampoco se encuentra ESPN
            if not source_hash:
                source_hash = "328b312b08023249e858acbd3466dc07b1a21384"

            # Creamos el canal faltante para que la app lo reconozca
            new_channel = {
                "title": target_title,
                "hash": source_hash,
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }
            channels.append(new_channel)
            print(f"¡Creado '{target_title}' enlazado al hash de NBA ESPN para garantizar el match!")
        else:
            print(f"'{target_title}' ya existe en la fuente. Se mantienen los hashes independientes.")

        if isinstance(parsed, dict) and "hashes" in parsed:
            parsed["hashes"] = channels
        else:
            parsed = channels
            
        # Guarda el resultado actualizado localmente para GitHub Actions
        with open('hashes.json', 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
            
        print("¡hashes.json procesado y actualizado con éxito!")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
