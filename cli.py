import toml
import argparse
import socket
import base64
import json
from httpR import *

def load_config(config_path):
    with open(config_path, "r") as f:
        return toml.load(f)

def create_auth_header(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

def send_sms(config, sender, recipient, message):
    # Извлекаем URL из конфигурации
    url = config["service"]["url"]
    username = config["service"]["username"]
    password = config["service"]["password"]

    # Формируем тело запроса
    body = json.dumps({
        "sender": sender,
        "recipient": recipient,
        "message": message
    })

    # Формируем заголовки
    headers = {
        "Host": "localhost",
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),  # Указываем длину тела запроса
        **create_auth_header(username, password)
    }

    # Создаем HTTP-запрос с методом POST
    request = HttpRequest("POST", url, headers, body)
    request_bytes = request.to_bytes()

    # Подключаемся к серверу и отправляем запрос
    host, port = "localhost", 4010
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request_bytes)
        response_bytes = s.recv(4096)
        response = HttpResponse.from_bytes(response_bytes)

    # Выводим результат
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.body}")

def main():
    parser = argparse.ArgumentParser(description="Send SMS via CLI")
    parser.add_argument("--sender", required=True, help="Sender phone number")
    parser.add_argument("--recipient", required=True, help="Recipient phone number")
    parser.add_argument("--message", required=True, help="SMS message text")
    parser.add_argument("--config", default="config.toml", help="Path to config file")

    args = parser.parse_args()

    config = load_config(args.config)
    send_sms(config, args.sender, args.recipient, args.message)

if __name__ == "__main__":
    main()
