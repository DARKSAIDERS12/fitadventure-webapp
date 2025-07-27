#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTPS веб-сервер для размещения Web App базы продуктов
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def run_https_server(port=8443):
    """Запуск HTTPS веб-сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    
    # Создаем самоподписанный сертификат
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    # Создаем временный сертификат
    import tempfile
    import subprocess
    
    # Создаем временные файлы для сертификата
    with tempfile.NamedTemporaryFile(delete=False, suffix='.key') as key_file:
        key_path = key_file.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.crt') as cert_file:
        cert_path = cert_file.name
    
    try:
        # Генерируем самоподписанный сертификат
        subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048', 
            '-keyout', key_path, '-out', cert_path, '-days', '365', '-nodes',
            '-subj', '/C=RU/ST=State/L=City/O=Organization/CN=localhost'
        ], check=True, capture_output=True)
        
        context.load_cert_chain(cert_path, key_path)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        
        print(f"🔒 HTTPS веб-сервер запущен на порту {port}")
        print(f"📱 Web App доступен по адресу: https://localhost:{port}/products_webapp.html")
        print("⚠️  Используйте самоподписанный сертификат (может потребоваться подтверждение в браузере)")
        print("🔄 Нажмите Ctrl+C для остановки")
        
        httpd.serve_forever()
        
    except subprocess.CalledProcessError:
        print("❌ Ошибка создания SSL сертификата")
        print("💡 Попробуем альтернативный способ...")
        
        # Альтернативный способ без OpenSSL
        try:
            context.load_default_certs()
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print(f"🔒 HTTPS веб-сервер запущен на порту {port}")
            print(f"📱 Web App доступен по адресу: https://localhost:{port}/products_webapp.html")
            print("🔄 Нажмите Ctrl+C для остановки")
            
            httpd.serve_forever()
            
        except Exception as e:
            print(f"❌ Ошибка запуска HTTPS сервера: {e}")
            print("💡 Запускаем HTTP сервер вместо HTTPS...")
            run_http_server(port)
    
    finally:
        # Удаляем временные файлы
        try:
            os.unlink(key_path)
            os.unlink(cert_path)
        except:
            pass

def run_http_server(port=8000):
    """Запуск HTTP веб-сервера как fallback"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    print(f"🌐 HTTP веб-сервер запущен на порту {port}")
    print(f"📱 Web App доступен по адресу: http://localhost:{port}/products_webapp.html")
    print("🔄 Нажмите Ctrl+C для остановки")
    httpd.serve_forever()

if __name__ == '__main__':
    run_https_server() 