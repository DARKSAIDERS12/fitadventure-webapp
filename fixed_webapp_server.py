#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправленный веб-сервер для Web App базы продуктов
"""

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
        print(f"📥 Получен запрос: {self.path}")
        
        # Перенаправляем корневой путь на наш HTML файл
        if self.path == '/':
            self.path = '/webapp_products.html'
            print(f"🔄 Перенаправление на: {self.path}")
        
        # Проверяем, существует ли файл
        file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))
        if not os.path.exists(file_path):
            print(f"❌ Файл не найден: {file_path}")
            self.send_error(404, "File not found")
            return
        
        print(f"✅ Файл найден: {file_path}")
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Улучшенное логирование
        print(f"📝 {format % args}")

def main():
    port = 8080
    print(f"🚀 Запуск исправленного веб-сервера на порту {port}")
    
    # Меняем директорию на текущую
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    print(f"📁 Рабочая директория: {current_dir}")
    
    # Проверяем наличие HTML файла
    html_file = os.path.join(current_dir, 'webapp_products.html')
    if os.path.exists(html_file):
        print(f"✅ HTML файл найден: {html_file}")
    else:
        print(f"❌ HTML файл не найден: {html_file}")
        return
    
    try:
        # Создаем HTTP сервер
        server = HTTPServer(('localhost', port), CustomHandler)
        
        print(f"🌐 HTTP URL: http://localhost:{port}")
        print(f"📱 Web App URL: http://localhost:{port}/webapp_products.html")
        print("⚠️  Внимание: Для Telegram Web App нужен HTTPS")
        print("⌨️ Нажмите Ctrl+C для остановки")
        print("🔍 Тестирование: curl http://localhost:8080/webapp_products.html")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n✅ Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 