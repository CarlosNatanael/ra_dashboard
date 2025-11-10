# teste_http.py
import requests

def testar_api_http():
    print("=== Testando API via HTTP ===")
    
    # Tente forçar HTTP (pode não funcionar, mas vale tentar)
    url = "http://retroachievements.org/API/API_GetUserSummary.php"
    params = {
        'z': 'SrLeo12',
        'y': 'Oy6GOQ5nOO3l8H3TkvFMw2QABo7Kw1Mn',
        'u': 'SrLeo12',
        'g': '5',
        'a': '5'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Sucesso via HTTP!")
            return response.text
        else:
            print(f"Resposta: {response.text[:200]}")
    except Exception as e:
        print(f"✗ HTTP também falhou: {e}")
        return None

testar_api_http()