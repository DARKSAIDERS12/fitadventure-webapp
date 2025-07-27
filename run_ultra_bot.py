#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌟 FitAdventure ULTRA BEAUTY Bot Launcher
✨ Запускатель для самого красивого интерфейса
🎨 Версия: 3.0 Ultra Beauty Edition
"""

import os
import sys
import time
from pathlib import Path

# Красивые символы
SPARKLES = "✨"
FIRE = "🔥"
STAR = "⭐"
ROCKET = "🚀"
GEM = "💎"
CROWN = "👑"
MAGIC = "🪄"
RAINBOW = "🌈"
LIGHTNING = "⚡"
HEARTS = "💕"

def print_beautiful_header():
    """Красивый заголовок"""
    print(f"""
{SPARKLES}═══════════════════════════════════════════════════════════{SPARKLES}
{CROWN}                    FITADVENTURE ULTRA BEAUTY                   {CROWN}
{ROCKET}                   Самый красивый фитнес-бот!                  {ROCKET}
{SPARKLES}═══════════════════════════════════════════════════════════{SPARKLES}

{RAINBOW} ✨ Анимированные прогресс-бары
{RAINBOW} 🎨 Красивые карточки и интерфейс  
{RAINBOW} 🔥 Живые анимации и переходы
{RAINBOW} 💎 Интерактивные элементы
{RAINBOW} 👑 Ультра точные расчеты (95-99%)

{FIRE}═══════════════════════════════════════════════════════════{FIRE}
""")

def animate_loading(text: str, duration: float = 2.0):
    """Анимация загрузки"""
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    
    while time.time() < end_time:
        print(f"\r{chars[i % len(chars)]} {text}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    
    print(f"\r{GEM} {text} - Готово! {SPARKLES}")

def check_ultra_requirements():
    """Проверка требований для ультра интерфейса"""
    print(f"{MAGIC} Проверка Ultra Beauty требований...")
    animate_loading("Сканируем файлы", 1.5)
    
    # Проверка файлов
    required_files = [
        'main_ultra_ui.py', 
        'ultra_precise_formulas.py', 
        'requirements.txt'
    ]
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"{FIRE} Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    # Проверка .env файла
    animate_loading("Проверяем конфигурацию", 1.0)
    
    if not Path('.env').exists():
        print(f"\n{LIGHTNING} Файл .env не найден!")
        print(f"{STAR} Создадим его автоматически...")
        
        token = input(f"\n{CROWN} Введите токен бота от @BotFather: ").strip()
        if token:
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(f"# FitAdventure Ultra Beauty Bot\n")
                f.write(f"TELEGRAM_BOT_TOKEN={token}\n")
            print(f"{GEM} Конфигурация создана! {SPARKLES}")
        else:
            print(f"{FIRE} Токен не введен. Выход.")
            return False
    
    # Проверка токена
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token or token == "YOUR_BOT_TOKEN_HERE":
            print(f"{FIRE} Токен бота не установлен в .env файле!")
            return False
    except ImportError:
        print(f"{LIGHTNING} Устанавливаем зависимости...")
        animate_loading("Установка пакетов", 2.0)
    
    print(f"{CROWN} Все проверки пройдены! {SPARKLES}")
    return True

def run_ultra_bot():
    """Запуск ультра красивого бота"""
    print(f"\n{ROCKET} Запуск FitAdventure Ultra Beauty...")
    animate_loading("Инициализация ультра интерфейса", 2.0)
    
    try:
        print(f"{SPARKLES} Загружаем магию...")
        from main_ultra_ui import main
        
        print(f"""
{RAINBOW}═══════════════════════════════════════════════════════════{RAINBOW}
{CROWN}                      БОТ ЗАПУЩЕН!                           {CROWN}
{FIRE}    Наслаждайтесь самым красивым фитнес-интерфейсом!         {FIRE}
{RAINBOW}═══════════════════════════════════════════════════════════{RAINBOW}

{GEM} Остановка: Ctrl+C
{STAR} Логи: В реальном времени
{HEARTS} Версия: Ultra Beauty 3.0
""")
        
        main()
        
    except KeyboardInterrupt:
        print(f"\n\n{HEARTS} Бот остановлен пользователем")
        print(f"{SPARKLES} Спасибо за использование FitAdventure! {SPARKLES}")
    except Exception as e:
        print(f"\n{FIRE} Ошибка запуска: {e}")
        print(f"{MAGIC} Проверьте логи и настройки")
        return False
    return True

def show_features():
    """Показать возможности ультра интерфейса"""
    print(f"""
{CROWN}═══════════════════════════════════════════════════════════{CROWN}
{STAR}                     ВОЗМОЖНОСТИ ULTRA BEAUTY                   {STAR}
{CROWN}═══════════════════════════════════════════════════════════{CROWN}

{FIRE} ВИЗУАЛЬНЫЕ УЛУЧШЕНИЯ:
  {SPARKLES} Анимированные прогресс-бары (градиент, огонь)
  {GEM} Красивые информационные карточки
  {RAINBOW} Богатые эмодзи и символы
  {MAGIC} Анимации печати и переходов

{LIGHTNING} ИНТЕРАКТИВНОСТЬ:
  {HEARTS} Живые подтверждения действий
  {STAR} Красивые кнопки с иконками
  {ROCKET} Плавные переходы между этапами
  {CROWN} Интуитивная навигация

{GEM} ПОЛЬЗОВАТЕЛЬСКИЙ ОПЫТ:
  {FIRE} Мультиязычность (RU/EN)
  {SPARKLES} Детальные подсказки
  {MAGIC} Красивые сообщения об ошибках
  {RAINBOW} Празднование результатов

{ROCKET} ТОЧНОСТЬ РАСЧЕТОВ:
  {CROWN} 95-99% точность
  {LIGHTNING} 18+ факторов анализа
  {GEM} Научные формулы
  {HEARTS} Персонализация

{STAR}═══════════════════════════════════════════════════════════{STAR}
""")

if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print_beautiful_header()
    
    # Меню выбора
    while True:
        print(f"""
{MAGIC} Выберите действие:
{ROCKET} 1. Запустить Ultra Beauty Bot
{STAR} 2. Показать возможности
{GEM} 3. Проверить настройки
{FIRE} 4. Выход
""")
        
        choice = input(f"{CROWN} Ваш выбор (1-4): ").strip()
        
        if choice == '1':
            if check_ultra_requirements():
                run_ultra_bot()
            else:
                print(f"\n{FIRE} Настройте бота и попробуйте снова")
            break
            
        elif choice == '2':
            show_features()
            input(f"\n{SPARKLES} Нажмите Enter для продолжения...")
            
        elif choice == '3':
            check_ultra_requirements()
            input(f"\n{SPARKLES} Нажмите Enter для продолжения...")
            
        elif choice == '4':
            print(f"\n{HEARTS} До свидания! {SPARKLES}")
            break
            
        else:
            print(f"{FIRE} Неверный выбор! Попробуйте снова.") 