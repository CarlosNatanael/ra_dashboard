import requests
import os

# Limpar variáveis de proxy
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

# Testar conexão básica
try:
    response = requests.get("https://retroachievements.org", timeout=10)
    print(f"Status Code: {response.status_code}")
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro: {e}")