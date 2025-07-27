#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой веб-сервер для размещения Web App базы продуктов
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import ssl

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def run_server(port=8000):
    """Запуск веб-сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    print(f"🌐 Веб-сервер запущен на порту {port}")
    print(f"📱 Web App доступен по адресу: http://localhost:{port}/products_webapp.html")
    print("🔄 Нажмите Ctrl+C для остановки")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 