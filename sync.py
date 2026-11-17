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

        # 1. Buscar cualquier hash disponible de League Pass (ignorando si pone 1080p, 720p, etc.)
        league_pass_hash = None
        for channel in channels:
            title = channel.get("title", "").lower().strip()
            if "nba league pass" in title:
                league_pass_hash = channel.get("hash")
                break

        # 2. Buscar el hash de NBA ESPN como respaldo por si la fuente no trae nada de League Pass
        espn_hash = None
        for channel in channels:
            title = channel.get("title", "").lower().strip()
            if "nba espn" in title:
                espn_hash = channel.get("hash")
                break
        
        if not espn_hash:
            espn_hash = "328b312b08023249e858acbd3466dc07b1a21384"

        # Definir qué hash usar (prioridad al League Pass de la fuente, si no, ESPN)
        chosen_hash = league_pass_hash if league_pass_hash else espn_hash

        # 3. Asegurar que exista exactamente el título limpio "NBA League Pass" para el match
        target_title = "NBA League Pass"
        found_exact = False

        for channel in channels:
            if channel.get("title", "").strip().lower() == target_title.lower():
                found_exact = True
                channel["hash"] = chosen_hash  # Actualizamos por si el enlace cambió
                break

        # Si no existe exactamente con ese nombre limpio, lo creamos
        if not found_exact:
            new_channel = {
                "title": target_title,
                "hash": chosen_hash,
                "group": "BALONCESTO",
                "logo": "",
                "tvg_id": ""
            }
            channels.append(new_channel)
            print(f"Creado '{target_title}' limpio para forzar el match.")
        else:
            print(f"El canal '{target_title}' ya existe y está sincronizado.")

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
