#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматический HTTPS сервер для Telegram Web App
"""

import ssl
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
import subprocess
import json
import time
from pathlib import Path

class WebAppHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки для Telegram Web App
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Security-Policy', "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://telegram.org")
        super().end_headers()
    
    def do_GET(self):
        print(f"📥 Запрос: {self.path}")
        
        # Перенаправляем корневой путь на Web App
        if self.path == '/':
            self.path = '/webapp_products.html'
            print(f"🔄 Перенаправление на Web App")
        
        # Проверяем существование файла
        file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))
        if not os.path.exists(file_path):
            print(f"❌ Файл не найден: {file_path}")
            self.send_error(404, "File not found")
            return
        
        print(f"✅ Файл найден: {file_path}")
        return super().do_GET()
    
    def log_message(self, format, *args):
        print(f"📝 {format % args}")

def create_ssl_cert():
    """Создаем SSL сертификат"""
    cert_file = 'webapp_cert.pem'
    key_file = 'webapp_key.pem'
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("🔐 Создание SSL сертификата...")
        try:
            # Создаем самоподписанный сертификат
            cmd = f'openssl req -x509 -newkey rsa:4096 -keyout {key_file} -out {cert_file} -days 365 -nodes -subj "/C=RU/ST=Moscow/L=Moscow/O=FitAdventure/CN=localhost"'
            subprocess.run(cmd, shell=True, check=True)
            print("✅ SSL сертификат создан")
        except subprocess.CalledProcessError:
            print("❌ Ошибка создания сертификата")
            return None, None
    
    return cert_file, key_file

def setup_ngrok():
    """Настраиваем ngrok для публичного доступа"""
    ngrok_file = 'ngrok'
    
    # Проверяем наличие ngrok
    if not os.path.exists(ngrok_file):
        print("📥 Загрузка ngrok...")
        try:
            # Скачиваем ngrok
            subprocess.run('wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz', shell=True, check=True)
            subprocess.run('tar -xzf ngrok-v3-stable-linux-amd64.tgz', shell=True, check=True)
            print("✅ ngrok установлен")
        except subprocess.CalledProcessError:
            print("❌ Ошибка установки ngrok")
            return None
    
    return ngrok_file

def start_ngrok_tunnel(port):
    """Запускаем ngrok туннель"""
    ngrok_file = setup_ngrok()
    if not ngrok_file:
        return None
    
    print("🌐 Запуск ngrok туннеля...")
    try:
        # Запускаем ngrok в фоне
        ngrok_process = subprocess.Popen(
            [f'./{ngrok_file}', 'http', str(port), '--log=stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем запуска туннеля
        time.sleep(3)
        
        # Получаем URL туннеля
        try:
            response = subprocess.run(['curl', '-s', 'http://localhost:4040/api/tunnels'], 
                                   capture_output=True, text=True, timeout=5)
            tunnels = json.loads(response.stdout)
            if tunnels and 'tunnels' in tunnels:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"✅ Публичный URL: {public_url}")
                return public_url, ngrok_process
        except:
            pass
        
        print("⚠️ Не удалось получить публичный URL, но туннель запущен")
        return None, ngrok_process
        
    except Exception as e:
        print(f"❌ Ошибка запуска ngrok: {e}")
        return None, None

def main():
    port = 8443
    print("🚀 Автоматическая настройка HTTPS Web App сервера")
    
    # Меняем директорию
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"📁 Рабочая директория: {os.getcwd()}")
    
    # Проверяем HTML файл
    if not os.path.exists('webapp_products.html'):
        print("❌ webapp_products.html не найден!")
        return
    
    # Создаем SSL сертификат
    cert_file, key_file = create_ssl_cert()
    if not cert_file or not key_file:
        print("❌ Не удалось создать SSL сертификат")
        return
    
    # Запускаем ngrok туннель
    public_url, ngrok_process = start_ngrok_tunnel(port)
    
    try:
        # Создаем HTTPS сервер
        server = HTTPServer(('0.0.0.0', port), WebAppHandler)
        
        # Настраиваем SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        server.socket = context.wrap_socket(server.socket, server_side=True)
        
        print(f"\n🎉 HTTPS Web App сервер запущен!")
        print(f"🌐 Локальный HTTPS: https://localhost:{port}")
        print(f"📱 Web App URL: https://localhost:{port}/webapp_products.html")
        
        if public_url:
            print(f"🌍 Публичный URL: {public_url}")
            print(f"📱 Публичный Web App: {public_url}/webapp_products.html")
            
            # Сохраняем URL для бота
            with open('webapp_url.txt', 'w') as f:
                f.write(public_url)
            print("💾 URL сохранен в webapp_url.txt")
        
        print("\n📋 Инструкции:")
        print("1. Откройте Telegram бота")
        print("2. Нажмите '🎮 Мини-приложения'")
        print("3. Выберите '🍎 База продуктов'")
        print("4. Мини-приложение откроется в Telegram")
        
        print("\n⌨️ Нажмите Ctrl+C для остановки")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n✅ Остановка сервера...")
        if ngrok_process:
            ngrok_process.terminate()
        print("✅ Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        if ngrok_process:
            ngrok_process.terminate()

if __name__ == "__main__":
    main() 