# Exemplo para Vercel/Netlify function
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/retroachievements/<username>')
def get_achievements(username):
    try:
        api_key = "sua_chave_aqui"
        url = f"https://retroachievements.org/API/API_GetUserSummary.php"
        params = {
            'z': username,
            'y': api_key,
            'u': username
        }
        
        response = requests.get(url, params=params, timeout=30)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500