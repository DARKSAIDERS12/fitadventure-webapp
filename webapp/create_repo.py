#!/usr/bin/env python3
"""
Скрипт для создания GitHub репозитория через API
"""

import requests
import json
import os
import subprocess

def create_github_repo():
    """Создает репозиторий на GitHub"""
    
    # Настройки репозитория
    repo_name = "fitadventure-products"
    description = "Telegram Web App для базы продуктов FitAdventure Bot"
    
    # GitHub API URL
    api_url = f"https://api.github.com/user/repos"
    
    # Данные для создания репозитория
    repo_data = {
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": True,
        "gitignore_template": None,
        "license_template": "mit"
    }
    
    print("🔧 Создание GitHub репозитория...")
    print(f"📝 Название: {repo_name}")
    print(f"📄 Описание: {description}")
    
    # Запрос токена от пользователя
    print("\n🔑 Для создания репозитория нужен GitHub Personal Access Token")
    print("📋 Создайте токен на https://github.com/settings/tokens")
    print("   - Выберите 'repo' права")
    print("   - Скопируйте токен")
    
    token = input("\n🔑 Введите ваш GitHub токен: ").strip()
    
    if not token:
        print("❌ Токен не введен. Создание репозитория отменено.")
        return False
    
    # Заголовки для API
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Создаем репозиторий
        response = requests.post(api_url, headers=headers, json=repo_data)
        
        if response.status_code == 201:
            repo_info = response.json()
            repo_url = repo_info["html_url"]
            clone_url = repo_info["clone_url"]
            
            print(f"\n✅ Репозиторий создан успешно!")
            print(f"🌐 URL: {repo_url}")
            print(f"📁 Clone URL: {clone_url}")
            
            # Добавляем remote и отправляем код
            print("\n📤 Отправка кода в репозиторий...")
            
            # Добавляем remote
            subprocess.run(["git", "remote", "add", "origin", clone_url], check=True)
            
            # Отправляем код
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            
            print("✅ Код отправлен в репозиторий!")
            print(f"\n🌐 Web App будет доступен по адресу:")
            print(f"   https://darksaiders.github.io/{repo_name}/")
            
            return True
            
        else:
            print(f"❌ Ошибка создания репозитория: {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка git: {e}")
        return False

if __name__ == "__main__":
    create_github_repo() 