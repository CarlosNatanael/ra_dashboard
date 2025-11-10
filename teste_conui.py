import requests
import os

# Configurar sessão sem proxy
session = requests.Session()
session.trust_env = False

url = "https://retroachievements.org/API/API_GetUserSummary.php"
params = {
    'z': 'SrLeo12',
    'y': 'Oy6GOQ5nOO3l8H3TkvFMw2QABo7Kw1Mn',
    'u': 'SrLeo12',
    'g': '5',
    'a': '5'
}

try:
    response = session.get(url, params=params, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("API funcionando!")
        print(response.text[:500])  # Mostra os primeiros 500 caracteres
    else:
        print(f"Erro HTTP: {response.status_code}")
except Exception as e:
    print(f"Erro completo: {e}")