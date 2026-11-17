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
        
        # Guardamos el archivo exactamente tal y como viene de la fuente original,
        # sin modificar, relacionar ni crear ningún canal artificial.
        with open('hashes.json', 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
            
        print("¡hashes.json actualizado con éxito manteniendo los canales totalmente independientes!")

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
