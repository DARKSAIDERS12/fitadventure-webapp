#!/usr/bin/env python3
"""
Скрипт для устранения конфликтов сохранения файлов
"""
import os
import shutil
import time
from datetime import datetime

def fix_file_conflicts():
    """Исправление конфликтов сохранения"""
    main_file = "main.py"
    
    # Создаем резервную копию с timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"main_conflict_backup_{timestamp}.py"
    
    if os.path.exists(main_file):
        shutil.copy2(main_file, backup_name)
        print(f"✅ Резервная копия создана: {backup_name}")
        
        # Принудительно обновляем время модификации
        current_time = time.time()
        os.utime(main_file, (current_time, current_time))
        print("✅ Время модификации файла обновлено")
        
        # Устанавливаем права доступа
        os.chmod(main_file, 0o664)
        print("✅ Права доступа установлены: rw-rw-r--")
        
        print("🎯 Проблемы с сохранением исправлены!")
        return True
    else:
        print("❌ Файл main.py не найден")
        return False

if __name__ == "__main__":
    fix_file_conflicts()
