# teste_conexao.py
import requests
import socket

def testar_conexao():
    print("=== Testes de Conexão ===")
    
    # Teste 1: DNS resolution
    try:
        ip = socket.gethostbyname('retroachievements.org')
        print(f"✓ DNS resolve: {ip}")
    except Exception as e:
        print(f"✗ DNS falhou: {e}")
        return False
    
    # Teste 2: Conexão básica HTTP
    try:
        response = requests.get("http://retroachievements.org", timeout=10)
        print(f"✓ HTTP funciona - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ HTTP falhou: {e}")
    
    # Teste 3: Conexão HTTPS
    try:
        response = requests.get("https://retroachievements.org", timeout=10)
        print(f"✓ HTTPS funciona - Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ HTTPS falhou: {e}")
        return False

if __name__ == "__main__":
    testar_conexao()