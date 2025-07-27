#!/usr/bin/env python3
"""
Простой скрипт для развертывания Web App
"""

import subprocess
import os

def main():
    print("🚀 Простое развертывание Web App")
    print("=" * 50)
    
    # Проверяем файлы
    if not os.path.exists("index.html"):
        print("❌ Файл index.html не найден!")
        return
    
    print("✅ Файлы готовы к развертыванию")
    
    # Показываем инструкции
    print("\n📋 Инструкции для развертывания:")
    print("1. Откройте https://github.com/new")
    print("2. Название репозитория: fitadventure-products")
    print("3. Описание: Telegram Web App для базы продуктов FitAdventure Bot")
    print("4. Выберите Public")
    print("5. НЕ ставьте галочки на README, .gitignore, license")
    print("6. Нажмите 'Create repository'")
    
    print("\n🔗 После создания репозитория выполните команды:")
    print("git remote add origin https://github.com/darksaiders/fitadventure-products.git")
    print("git push -u origin main")
    
    print("\n⚙️ Настройка GitHub Pages:")
    print("1. Перейдите в Settings репозитория")
    print("2. Найдите раздел 'Pages'")
    print("3. Source: Deploy from a branch")
    print("4. Branch: main, Folder: / (root)")
    print("5. Нажмите 'Save'")
    
    print("\n🌐 Web App будет доступен по адресу:")
    print("https://darksaiders.github.io/fitadventure-products/")
    
    print("\n📱 Обновите URL в боте на этот адрес")
    
    # Пытаемся отправить код
    print("\n🔄 Попытка автоматической отправки кода...")
    
    try:
        # Добавляем remote
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/darksaiders/fitadventure-products.git"], 
                      capture_output=True, text=True)
        
        # Отправляем код
        result = subprocess.run(["git", "push", "-u", "origin", "main"], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Код успешно отправлен!")
            print("🌐 Web App: https://darksaiders.github.io/fitadventure-products/")
        else:
            print("❌ Ошибка отправки кода:")
            print(result.stderr)
            print("\n📋 Выполните команды вручную:")
            print("git remote add origin https://github.com/darksaiders/fitadventure-products.git")
            print("git push -u origin main")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\n📋 Выполните команды вручную:")
        print("git remote add origin https://github.com/darksaiders/fitadventure-products.git")
        print("git push -u origin main")

if __name__ == "__main__":
    main() 