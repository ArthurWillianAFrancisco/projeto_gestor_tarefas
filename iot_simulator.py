import os
import json
import time
import requests
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

API_URL = os.getenv("API_URL")
BOT_USER = os.getenv("BOT_USER")
BOT_PASS = os.getenv("BOT_PASS")
TOPICO_ALERTA = "lockdown/seguranca/alertas"

def obter_token_automatico():
    """Faz login na API e retorna o access_token"""
    print("🔑 Tentando autenticar robô na API...")
    url_login = f"{API_URL}/auth/login"
    payload = {
        "username": BOT_USER,
        "password": BOT_PASS
    }
    
    try:
        response = requests.post(url_login, json=payload)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("✅ Autenticação realizada com sucesso!")
            return token
        else:
            print(f"❌ Erro no login: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"⚠️ Falha de conexão ao tentar logar: {e}")
        return None

# Inicializa o Token (O robô já nasce autenticado)
TOKEN_ADMIN = obter_token_automatico()

def criar_card_via_bot(titulo, descricao, checklist):
    """Envia o POST para criar o card no Kanban"""
    if not TOKEN_ADMIN:
        print("🚫 Robô sem token. Não é possível criar o card.")
        return

    headers = {
        "Authorization": f"Bearer {TOKEN_ADMIN}",
        "Content-Type": "application/json"
    }
    
    # Formato especial que o nosso Front-end entende para o Checklist
    full_desc = f"{descricao}---CHECK---{json.dumps(checklist)}"
    
    payload = {
        "title": f"[BOT] {titulo}",
        "description": full_desc,
        "status": "pendente"
    }
    
    try:
        response = requests.post(f"{API_URL}/tasks", json=payload, headers=headers)
        if response.status_code == 201:
            print(f"🚀 Card criado no Dashboard: {titulo}")
        elif response.status_code == 401:
            print("❌ Token expirado! Reinicie o robô para renovar o acesso.")
        else:
            print(f"❌ Erro da API: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Erro ao enviar para o servidor: {e}")

def on_message(client, userdata, msg):
    comando = msg.payload.decode()
    print(f"📩 Sinal MQTT recebido: {comando}")
    
    if comando == "ATAQUE_IP":
        criar_card_via_bot(
            "Invasão Detectada: Brute Force",
            "O sensor identificou múltiplas tentativas de acesso falhas originadas do IP 192.168.1.105.",
            [
                {"text": "Bloquear IP no Gateway", "done": False},
                {"text": "Isolar máquina afetada", "done": False},
                {"text": "Resetar chaves de acesso", "done": False}
            ]
        )

# Configuração do Cliente MQTT
client = mqtt.Client()
client.on_message = on_message

try:
    print("🌐 Conectando ao Broker MQTT...")
    client.connect("broker.hivemq.com", 1883, 60)
    client.subscribe(TOPICO_ALERTA)
    print(f"🤖 Monitorando tópico: {TOPICO_ALERTA}")
    print("📡 Aguardando alertas do sensor...")
    client.loop_forever()
except Exception as e:
    print(f"💥 Erro fatal no robô: {e}")