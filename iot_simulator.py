import paho.mqtt.client as mqtt
import requests
import json
import time

# --- CONFIGURAÇÕES ---
# Coloque aqui o link do seu Render (sem a barra no final)
API_URL = "https://projeto-gestor-tarefas.onrender.com"
# Coloque um Token de Admin válido (pegue fazendo login no seu site e olhando o console ou Network)
TOKEN_ADMIN = "COLE_SEU_TOKEN_AQUI" 

TOPICO_ALERTA = "lockdown/seguranca/alertas"

def criar_card_via_bot(titulo, descricao, checklist):
    headers = {
        "Authorization": f"Bearer {TOKEN_ADMIN}",
        "Content-Type": "application/json"
    }
    
    # Formatando a descrição com o padrão de checklist que criamos no Front
    full_desc = f"{descricao}---CHECK---{json.dumps(checklist)}"
    
    payload = {
        "title": f"[AUTO-BOT] {titulo}",
        "description": full_desc,
        "status": "pendente"
    }
    
    try:
        response = requests.post(f"{API_URL}/tasks", json=payload, headers=headers)
        if response.status_code == 201:
            print(f"✅ Card criado com sucesso: {titulo}")
        else:
            print(f"❌ Erro na API: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ Falha de conexão: {e}")

def on_message(client, userdata, msg):
    print(f"📩 Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    
    # Simulação: Se a mensagem for "ATAQUE_IP", criamos o card
    if msg.payload.decode() == "ATAQUE_IP":
        criar_card_via_bot(
            "ALERTA: Força Bruta Detectada",
            "O sensor de rede detectou 50+ tentativas de login falhas do IP 187.55.12.3.",
            [
                {"text": "Bloquear IP no Firewall", "done": False},
                {"text": "Verificar logs do servidor", "done": False},
                {"text": "Notificar equipe de infra", "done": False}
            ]
        )

# Configurando o Cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe(TOPICO_ALERTA)

print("🤖 Robô de Segurança Online e aguardando sinais MQTT...")
client.loop_forever()