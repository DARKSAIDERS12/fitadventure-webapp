#!/usr/bin/env python3
"""
🔧 Cursor Cache Reset - Скрипт для устранения проблем с сохранением файлов
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

def reset_cursor_cache():
    """Принудительный сброс кеша Cursor"""
    print("🔧 Сброс кеша Cursor...")
    
    # 1. Создаем резервную копию файла
    main_file = Path("main.py")
    if main_file.exists():
        backup_name = f"main_cache_backup_{int(time.time())}.py"
        shutil.copy2(main_file, backup_name)
        print(f"✅ Создана резервная копия: {backup_name}")
    
    # 2. Временно переименовываем файл
    if main_file.exists():
        temp_name = f"main_temp_{int(time.time())}.py"
        main_file.rename(temp_name)
        print(f"📋 Файл временно переименован в {temp_name}")
        
        # Ждем 2 секунды чтобы Cursor заметил изменения
        time.sleep(2)
        
        # Возвращаем оригинальное имя
        Path(temp_name).rename(main_file)
        print("✅ Файл восстановлен")
    
    # 3. Обновляем временные метки
    if main_file.exists():
        current_time = time.time()
        os.utime(main_file, (current_time, current_time))
        print("🕒 Временные метки обновлены")
    
    # 4. Устанавливаем права доступа
    if main_file.exists():
        os.chmod(main_file, 0o664)
        print("🔐 Права доступа обновлены")
    
    # 5. Синхронизируем файловую систему
    try:
        subprocess.run(["sync"], check=True, capture_output=True)
        print("💾 Файловая система синхронизирована")
    except:
        pass
    
    print("\n✅ Сброс кеша завершен!")
    print("💡 Теперь попробуйте сохранить файл в Cursor")

if __name__ == "__main__":
    try:
        reset_cursor_cache()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1) 