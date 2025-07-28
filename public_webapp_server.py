#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Публичный HTTP Web App Server для FitAdventure Bot
"""

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class WebAppHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки для Telegram Web App
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Перенаправляем корневой путь на Web App
        if self.path == '/':
            self.path = '/webapp_products.html'
        return super().do_GET()

def main():
    # Настройки сервера
    PORT = 8080
    HOST = '0.0.0.0'  # Слушаем на всех интерфейсах
    
    # Проверяем наличие Web App файла
    webapp_file = Path('webapp_products.html')
    if not webapp_file.exists():
        print(f"❌ Web App файл не найден: {webapp_file}")
        return
    
    # Создаем HTTP сервер
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, WebAppHandler)
    
    print(f"🚀 Публичный HTTP Web App Server запущен")
    print(f"🌐 Хост: {HOST}")
    print(f"📡 Порт: {PORT}")
    print(f"📁 Web App: {webapp_file.absolute()}")
    print(f"🌐 HTTP URL: http://localhost:{PORT}")
    print(f"📱 Web App URL: http://localhost:{PORT}/webapp_products.html")
    print("⚠️  Внимание: Для Telegram Web App нужен HTTPS")
    print("⌨️ Нажмите Ctrl+C для остановки")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
        httpd.server_close()

if __name__ == '__main__':
    main() 