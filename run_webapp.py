#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для запуска веб-приложения базы продуктов
"""

import subprocess
import sys
import os

def main():
    print("🚀 Запуск веб-приложения базы продуктов...")
    
    # Проверяем, что Flask установлен
    try:
        import flask
        print("✅ Flask установлен")
    except ImportError:
        print("❌ Flask не установлен. Устанавливаем...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "--break-system-packages"])
    
    # Запускаем веб-приложение
    print("🌐 Запуск веб-сервера на http://localhost:5000")
    print("📱 Для использования в Telegram Web App:")
    print("   1. Разместите приложение на хостинге")
    print("   2. Обновите URL в main.py")
    print("   3. Настройте SSL сертификат")
    print("\n🔗 Локальный URL: http://localhost:5000")
    print("⌨️ Нажмите Ctrl+C для остановки")
    
    # Запускаем Flask приложение
    os.environ['FLASK_APP'] = 'webapp_products.py'
    os.environ['FLASK_ENV'] = 'development'
    
    subprocess.run([sys.executable, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"])

if __name__ == "__main__":
    main() 