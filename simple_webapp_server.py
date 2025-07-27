#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой веб-сервер для Web App базы продуктов
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

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

def main():
    port = 8080
    print(f"🚀 Запуск веб-сервера на порту {port}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"📱 Web App URL: http://localhost:{port}/webapp_products.html")
    print("⌨️ Нажмите Ctrl+C для остановки")
    
    # Меняем директорию на текущую
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        server = HTTPServer(('0.0.0.0', port), CustomHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 