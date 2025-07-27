#!/usr/bin/env python3
"""
Безопасная обертка для сохранения main.py
Использовать: python safe_save.py
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def safe_save_main():
    """Безопасное сохранение main.py"""
    main_file = Path("main.py")
    
    if not main_file.exists():
        print("❌ Файл main.py не найден")
        return False
    
    # Создание резервной копии
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = Path(f"main.py.safe_backup_{timestamp}")
    shutil.copy2(main_file, backup_file)
    
    # Очистка lock-файлов
    for lock_file in Path.cwd().glob("*.lock"):
        try:
            lock_file.unlink()
        except:
            pass
    
    # Синхронизация
    os.sync()
    
    print(f"✅ Файл безопасно сохранен")
    print(f"📋 Резервная копия: {backup_file}")
    return True

if __name__ == "__main__":
    safe_save_main()
