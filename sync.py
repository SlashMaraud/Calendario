import json
import urllib.request
import sys

SOURCE_URLS = [
    "https://tokyo.elcano-ipfs.workers.dev/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json",
    "https://ipfs.io/ipfs/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json",
    "https://dweb.link/ipfs/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json"
]

def fetch_json():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    for url in SOURCE_URLS:
        try:
            print(f"Intentando descargar desde: {url}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    data_str = response.read().decode('utf-8')
                    parsed = json.loads(data_str)
                    
                    # Detecta cualquier variante (720p, 1080p, etc.) que contenga "nba espn"
                    if isinstance(parsed, dict):
                        for key in list(parsed.keys()):
                            key_lower = key.strip().lower()
                            if "nba espn" in key_lower:
                                parsed["NBA League Pass"] = parsed[key]
                                print(f"Canal duplicado con éxito: 'NBA League Pass' mapeado desde '{key}'")
                    
                    data = json.dumps(parsed, ensure_ascii=False, indent=2)
                    print(f"Éxito descargando desde {url}. Elementos: {len(parsed) if isinstance(parsed, (list, dict)) else 'Objeto'}")
                    return data
        except Exception as e:
            print(f"Error descargando desde {url}: {e}")
    return None

def main():
    new_content = fetch_json()
    if not new_content:
        print("No se pudo descargar de ninguna fuente. Se mantendrá la versión existente.")
        sys.exit(0)

    try:
        with open('hashes.json', 'r', encoding='utf-8') as f:
            old_content = f.read()
    except FileNotFoundError:
        old_content = ""

    if new_content.strip() != old_content.strip():
        print("¡Se han detectado cambios! Actualizando hashes.json...")
        with open('hashes.json', 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        print("No hay cambios en la fuente. Todo actualizado.")

if __name__ == '__main__':
    main()
