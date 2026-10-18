import json
import urllib.request
import sys

# URL de origen (puedes añadir o cambiar URLs si cambian)
SOURCE_URLS = [
    "https://tokyo.elcano-ipfs.workers.dev/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json",
    "https://ipfs.io/ipns/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json",
    "https://dweb.link/ipns/k51qzi5uqu5dh5qej4b9wlcr5i6vhc7rcfkekhrxqek5c9lk6gdaiik820fecs/hashes.json"
]

def fetch_json():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for url in SOURCE_URLS:
        try:
            print(f"Intentando descargar desde: {url}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    # Validar que es JSON válido
                    parsed = json.loads(data)
                    print(f"Éxito descargando desde {url}. Elementos: {len(parsed) if isinstance(parsed, list) else 'Objeto'}")
                    return data
        except Exception as e:
            print(f"Error descargando {url}: {e}")
    return None

def main():
    new_content = fetch_json()
    if not new_content:
        print("No se pudo descargar de ninguna fuente. Se mantendrá la versión existente.")
        sys.exit(0)

    # Cargar contenido existente para comparar
    try:
        with open("hashes.json", "r", encoding="utf-8") as f:
            old_content = f.read()
    except FileNotFoundError:
        old_content = ""

    if new_content.strip() != old_content.strip():
        print("¡Se han detectado cambios! Actualizando hashes.json...")
        with open("hashes.json", "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        print("No hay cambios en la fuente. Todo actualizado.")

if __name__ == "__main__":
    main()
