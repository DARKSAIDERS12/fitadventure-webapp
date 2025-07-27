#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для развертывания Web App на Railway
"""

import os
import subprocess
import json

def create_railway_config():
    """Создает конфигурацию для Railway"""
    
    # Создаем railway.json
    railway_config = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python webapp_products.py",
            "healthcheckPath": "/",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open('railway.json', 'w') as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ railway.json создан")

def create_vercel_config():
    """Создает конфигурацию для Vercel"""
    
    # Создаем vercel.json
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "webapp_products.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "webapp_products.py"
            }
        ]
    }
    
    with open('vercel.json', 'w') as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ vercel.json создан")

def create_heroku_config():
    """Создает конфигурацию для Heroku"""
    
    # Создаем Procfile (если не существует)
    if not os.path.exists('Procfile'):
        with open('Procfile', 'w') as f:
            f.write('web: python webapp_products.py\n')
        print("✅ Procfile создан")
    
    # Создаем runtime.txt (если не существует)
    if not os.path.exists('runtime.txt'):
        with open('runtime.txt', 'w') as f:
            f.write('python-3.12.0\n')
        print("✅ runtime.txt создан")

def main():
    """Основная функция"""
    
    print("🚀 Подготовка к развертыванию Web App...")
    
    # Создаем конфигурации для разных хостингов
    create_railway_config()
    create_vercel_config()
    create_heroku_config()
    
    print("\n📋 Инструкции по развертыванию:")
    print("\n🌐 Railway (рекомендуется):")
    print("1. Зарегистрируйтесь на railway.app")
    print("2. Подключите GitHub репозиторий")
    print("3. Railway автоматически развернет приложение")
    print("4. Получите HTTPS URL и обновите в main.py")
    
    print("\n⚡ Vercel:")
    print("1. Установите Vercel CLI: npm i -g vercel")
    print("2. Запустите: vercel")
    print("3. Следуйте инструкциям")
    
    print("\n🦊 Heroku:")
    print("1. Установите Heroku CLI")
    print("2. Создайте приложение: heroku create your-app-name")
    print("3. Разверните: git push heroku main")
    
    print("\n✅ Все файлы конфигурации созданы!")
    print("🎯 Выберите хостинг и следуйте инструкциям выше")

if __name__ == "__main__":
    main() 