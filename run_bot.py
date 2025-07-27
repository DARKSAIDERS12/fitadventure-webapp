#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 FitAdventure Bot Launcher
Проверяет настройки и запускает бота
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Проверка необходимых файлов и настроек"""
    print("🔍 Проверка настроек FitAdventure Bot...")
    
    # Проверка файлов
    required_files = ['main.py', 'ultra_precise_formulas.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    # Проверка .env файла
    if not Path('.env').exists():
        print("⚠️  Файл .env не найден!")
        print("📋 Создайте файл .env и добавьте токен бота:")
        print("   TELEGRAM_BOT_TOKEN=ваш_токен_бота")
        print("\n💡 Получить токен: https://t.me/BotFather")
        
        # Предложить создать .env
        create_env = input("\n❓ Создать файл .env сейчас? (y/n): ").lower()
        if create_env == 'y':
            token = input("🔑 Введите токен бота: ").strip()
            if token:
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(f"# FitAdventure Bot Configuration\n")
                    f.write(f"TELEGRAM_BOT_TOKEN={token}\n")
                print("✅ Файл .env создан!")
            else:
                print("❌ Токен не введен. Выход.")
                return False
        else:
            return False
    
    # Проверка токена
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Токен бота не установлен в .env файле!")
        print("📝 Отредактируйте файл .env и добавьте реальный токен")
        return False
    
    print("✅ Все настройки корректны!")
    return True

def run_bot():
    """Запуск основного бота"""
    print("🚀 Запуск FitAdventure Bot...")
    try:
        from main import main
        main()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        return False
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("🎯 FitAdventure Bot - Ультра-точные расчеты")
    print("=" * 50)
    
    if check_requirements():
        run_bot()
    else:
        print("\n📚 Смотрите SETUP_INSTRUCTIONS.md для подробной настройки")
        sys.exit(1) 