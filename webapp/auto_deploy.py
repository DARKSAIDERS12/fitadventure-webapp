#!/usr/bin/env python3
"""
Автоматическое развертывание Web App на GitHub Pages
"""

import subprocess
import time
import os

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - успешно!")
            return True
        else:
            print(f"❌ {description} - ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False

def main():
    print("🚀 Автоматическое развертывание FitAdventure Products Web App")
    print("=" * 60)
    
    # Проверяем, что мы в правильной директории
    if not os.path.exists("index.html"):
        print("❌ Файл index.html не найден!")
        return False
    
    # Инициализируем git (если еще не инициализирован)
    if not os.path.exists(".git"):
        run_command("git init", "Инициализация git репозитория")
        run_command("git branch -m main", "Переименование ветки в main")
    
    # Настраиваем git
    run_command('git config user.email "darksaiders@example.com"', "Настройка email")
    run_command('git config user.name "darksaiders"', "Настройка имени пользователя")
    
    # Добавляем файлы
    run_command("git add .", "Добавление файлов в git")
    
    # Коммитим изменения
    run_command('git commit -m "Update Web App"', "Создание коммита")
    
    # Удаляем старый remote (если есть)
    run_command("git remote remove origin", "Удаление старого remote")
    
    # Добавляем новый remote
    remote_url = "https://github.com/darksaiders/fitadventure-products.git"
    run_command(f"git remote add origin {remote_url}", "Добавление remote")
    
    # Отправляем код
    success = run_command("git push -u origin main --force", "Отправка кода в репозиторий")
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Web App успешно развернут!")
        print("🌐 URL: https://darksaiders.github.io/fitadventure-products/")
        print("\n📋 Следующие шаги:")
        print("1. Откройте https://github.com/darksaiders/fitadventure-products")
        print("2. Перейдите в Settings → Pages")
        print("3. Source: Deploy from a branch")
        print("4. Branch: main, Folder: / (root)")
        print("5. Нажмите Save")
        print("\n📱 После настройки Pages обновите URL в боте:")
        print("   https://darksaiders.github.io/fitadventure-products/")
        
        return True
    else:
        print("\n❌ Развертывание не удалось!")
        print("📋 Попробуйте создать репозиторий вручную:")
        print("1. Откройте https://github.com/new")
        print("2. Название: fitadventure-products")
        print("3. Public репозиторий")
        print("4. Создайте репозиторий")
        print("5. Запустите скрипт снова")
        
        return False

if __name__ == "__main__":
    main() 