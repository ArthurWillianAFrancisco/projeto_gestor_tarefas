# 🛡️ Sentinel Manager - Sistema de Gestão de Incidentes IoT

Este projeto é um sistema de gerenciamento de tarefas (Kanban) focado em segurança cibernética, onde incidentes são gerados automaticamente por um robô simulador de sensores IoT.
pagina do projeto: https://projeto-gestor-tarefas.onrender.com/login-page

## 🚀 Funcionalidades principais
- **CRUD Completo**: Criação, listagem, edição e exclusão de cards.
- **Dashboard Colaborativo**: Visualização global de incidentes para toda a equipe.
- **Autenticação JWT**: Segurança de ponta com níveis de acesso (Admin/User).
- **Integração IoT**: Simulador Python que detecta ataques (MQTT) e abre cards via API.
- **Deploy Cloud**: Hospedado no Render com banco de dados PostgreSQL.

## 🛠️ Tecnologias Utilizadas
- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended.
- **Frontend**: HTML5, CSS3 (Tailwind), JavaScript.
- **IoT/Protocolo**: MQTT (Paho-MQTT), HiveMQ Broker.
- **Database**: PostgreSQL (Produção) / SQLite (Desenvolvimento).

## 🤖 Como rodar o Simulador de Ataques (IoT)
O grande diferencial deste projeto é o robô de segurança. Para testar:
1. Garanta que você tem o Python instalado.
2. No terminal, instale as dependências: `pip install paho-mqtt requests python-dotenv`.
3. Configure o arquivo `.env` com suas credenciais.
4. Execute: `python iot_simulator.py`.
5. No site [HiveMQ Web Client](http://www.hivemq.com/demos/websocket-client/), envie uma mensagem `ATAQUE_IP` para o tópico `lockdown/seguranca/alertas`.

## 👨‍💻 Desenvolvedor
- **Arthur Willian** - IFRO