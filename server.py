import http.server
import socketserver
import smtplib
from email.mime.text import MIMEText
from json import dumps
from urllib.parse import parse_qs
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

PORT = 8000

# Чтение данных из переменных окружения
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Извлекаем длину содержимого (данные из формы)
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        form_data = parse_qs(body.decode('utf-8'))
        
        name = form_data.get('name', [''])[0]
        phone = form_data.get('phone', [''])[0]
        project = form_data.get('project', [''])[0]

        self.send_email(name, phone, project)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"status": "success", "message": "Message sent successfully!"}
        self.wfile.write(dumps(response).encode('utf-8'))

    def send_email(self, name, phone, project):
        # Формируем текст сообщения
        subject = "Новое сообщение с формы сайта"
        body = f"Имя: {name}\nТелефон: {phone}\nПроект: {project}"

        # Создаем объект MIMEText
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        # Отправляем письмо
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  # Шифруем соединение
                server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Авторизуемся
                server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
                print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")

# Запускаем сервер
with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Сервер запущен на http://localhost:{PORT}")
    httpd.serve_forever()
