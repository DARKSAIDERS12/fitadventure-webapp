#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTPS веб-сервер для Web App базы продуктов
"""

import ssl
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
from pathlib import Path

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки для Web App
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Перенаправляем корневой путь на наш HTML файл
        if self.path == '/':
            self.path = '/webapp_products.html'
        return super().do_GET()

def create_self_signed_cert():
    """Создаем самоподписанный сертификат"""
    cert_file = 'webapp_cert.pem'
    key_file = 'webapp_key.pem'
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("🔐 Создание самоподписанного сертификата...")
        
        # Создаем сертификат с помощью OpenSSL
        os.system(f'openssl req -x509 -newkey rsa:4096 -keyout {key_file} -out {cert_file} -days 365 -nodes -subj "/C=RU/ST=Moscow/L=Moscow/O=FitAdventure/CN=localhost"')
        
        if os.path.exists(cert_file) and os.path.exists(key_file):
            print("✅ Сертификат создан успешно")
        else:
            print("❌ Ошибка создания сертификата")
            return None, None
    
    return cert_file, key_file

def main():
    port = 8443
    print(f"🚀 Запуск HTTPS веб-сервера на порту {port}")
    
    # Меняем директорию на текущую
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Создаем сертификат
    cert_file, key_file = create_self_signed_cert()
    
    if not cert_file or not key_file:
        print("❌ Не удалось создать сертификат")
        return
    
    try:
        # Создаем HTTPS сервер
        server = HTTPServer(('0.0.0.0', port), CustomHandler)
        
        # Настраиваем SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        server.socket = context.wrap_socket(server.socket, server_side=True)
        
        print(f"🌐 HTTPS URL: https://localhost:{port}")
        print(f"📱 Web App URL: https://localhost:{port}/webapp_products.html")
        print("⚠️  Внимание: Используйте самоподписанный сертификат для локальной разработки")
        print("⌨️ Нажмите Ctrl+C для остановки")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n✅ Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 