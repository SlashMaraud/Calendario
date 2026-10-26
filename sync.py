import json
import urllib.request
import sys

# URL que funciona (responde con HTTP 200)
SOURCE_URLS = [
    "https://tokyo.elcano-ipfs.workers.dev/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json"
]

def fetch_json():
    # Cabeceras avanzadas para evitar que Cloudflare bloquee o devuelva datos parciales al robot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://tokyo.elcano-ipfs.workers.dev/"
    }
    
    for url in SOURCE_URLS:
        try:
            print(f"Intentando descargar desde: {url}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    data_str = response.read().decode('utf-8')
                    parsed = json.loads(data_str)
                    
                    if isinstance(parsed, dict):
                        # Mapeo flexible para cualquier variante de "nba espn" (720p, 1080p, etc.)
                        for key in list(parsed.keys()):
                            if "nba espn" in key.strip().lower():
                                parsed["NBA League Pass"] = parsed[key]
                                print(f"Canal duplicado con éxito: 'NBA League Pass' mapeado desde '{key}'")
                        
                        data = json.dumps(parsed, ensure_ascii=False, indent=2)
                        print(f"Éxito descargando el archivo. Total elementos: {len(parsed)}")
                        return data
        except Exception as e:
            print(f"Error descargando desde {url}: {e}")
    return None

def main():
    new_content = fetch_json()
    if not new_content:
        print("No se pudo descargar de ninguna fuente válida. Se mantendrá la versión existente.")
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
