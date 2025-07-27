#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенный скрипт устранения конфликтов сохранения
Без внешних зависимостей, работает везде
"""

import os
import time
import subprocess
from pathlib import Path
from datetime import datetime

def clear_temp_files():
    """Очистка временных файлов"""
    print("🧹 Очистка временных файлов...")
    patterns = ["*.lock", "*.tmp", "*.temp", "*~", "*.swp", "*.swo"]
    cleaned = 0
    
    for pattern in patterns:
        for file in Path.cwd().glob(pattern):
            try:
                file.unlink()
                print(f"   Удален: {file.name}")
                cleaned += 1
            except:
                pass
    
    if cleaned == 0:
        print("   ✅ Временные файлы не найдены")
    else:
        print(f"   ✅ Очищено {cleaned} файлов")

def fix_permissions():
    """Исправление прав доступа"""
    print("🔑 Исправление прав доступа...")
    
    for py_file in Path.cwd().glob("*.py"):
        try:
            os.chmod(py_file, 0o664)
            print(f"   Исправлен: {py_file.name}")
        except Exception as e:
            print(f"   ❌ Ошибка {py_file.name}: {e}")

def sync_filesystem():
    """Синхронизация файловой системы"""
    print("💿 Синхронизация файловой системы...")
    try:
        os.sync()
        print("   ✅ Синхронизация выполнена")
    except Exception as e:
        print(f"   ❌ Ошибка синхронизации: {e}")

def check_cursor_processes():
    """Проверка процессов Cursor"""
    print("🔍 Проверка процессов Cursor...")
    try:
        result = subprocess.run(['pgrep', '-f', 'cursor'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"   📊 Найдено процессов Cursor: {len(pids)}")
            return len(pids)
        else:
            print("   ✅ Процессы Cursor не найдены")
            return 0
    except Exception as e:
        print(f"   ❌ Ошибка проверки процессов: {e}")
        return -1

def create_backup():
    """Создание резервной копии main.py"""
    main_file = Path("main.py")
    if main_file.exists():
        print("📋 Создание резервной копии...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = Path(f"main.py.safe_backup_{timestamp}")
        
        try:
            import shutil
            shutil.copy2(main_file, backup_file)
            print(f"   ✅ Создана копия: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"   ❌ Ошибка создания копии: {e}")
    else:
        print("   ⚠️ Файл main.py не найден")
    
    return None

def kill_cursor_processes():
    """Принудительное закрытие процессов Cursor"""
    print("⏹️ Закрытие процессов Cursor...")
    try:
        result = subprocess.run(['pkill', '-f', 'cursor'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Процессы Cursor закрыты")
            time.sleep(2)  # Даем время процессам закрыться
        else:
            print("   ✅ Процессы Cursor не найдены")
    except Exception as e:
        print(f"   ❌ Ошибка закрытия процессов: {e}")

def emergency_fix():
    """Экстренное исправление всех проблем"""
    print("🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ КОНФЛИКТОВ СОХРАНЕНИЯ")
    print("=" * 60)
    
    # 1. Создание резервной копии
    create_backup()
    
    # 2. Закрытие процессов Cursor
    kill_cursor_processes()
    
    # 3. Очистка временных файлов
    clear_temp_files()
    
    # 4. Исправление прав доступа
    fix_permissions()
    
    # 5. Синхронизация
    sync_filesystem()
    
    print("\n✅ ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print("💡 Теперь можно перезапустить Cursor и сохранить файлы")

def routine_check():
    """Обычная проверка и исправление"""
    print("🔧 Регулярное исправление конфликтов сохранения")
    print("=" * 50)
    
    # Проверки без принудительного закрытия Cursor
    clear_temp_files()
    fix_permissions()
    sync_filesystem()
    check_cursor_processes()
    
    print("\n✅ Проверка завершена!")
    print("💡 Если проблемы остались, запустите:")
    print("   python3 simple_fix.py emergency")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "emergency":
            emergency_fix()
        elif sys.argv[1] == "backup":
            create_backup()
        elif sys.argv[1] == "clean":
            clear_temp_files()
        elif sys.argv[1] == "permissions":
            fix_permissions()
        else:
            print("❌ Неизвестная команда")
            print("Доступные команды:")
            print("  python3 simple_fix.py           - обычная проверка")
            print("  python3 simple_fix.py emergency - экстренное исправление")
            print("  python3 simple_fix.py backup    - создать резервную копию")
            print("  python3 simple_fix.py clean     - очистить временные файлы")
            print("  python3 simple_fix.py permissions - исправить права доступа")
    else:
        routine_check() 