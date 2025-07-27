#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ FitAdventure Quick Backup
🚀 Быстрое резервное копирование перед изменениями
💾 Автоматический бэкап Ultra Beauty версии
"""

import sys
import datetime
from backup_system import FitAdventureBackup

# Красивые символы
QUICK = "⚡"
SAFE = "🔒"
SUCCESS = "✅"
ERROR = "❌"
INFO = "💡"

def quick_backup(description=None):
    """Быстрое создание резервной копии"""
    print(f"{QUICK} FitAdventure Quick Backup")
    print("=" * 40)
    
    if description is None:
        description = f"Автоматический бэкап перед изменениями - {datetime.datetime.now().strftime('%H:%M:%S')}"
    
    backup_system = FitAdventureBackup()
    
    print(f"{INFO} {description}")
    success = backup_system.create_backup(description)
    
    if success:
        print(f"{SUCCESS} Резервная копия создана успешно!")
        print(f"{SAFE} Теперь можно безопасно вносить изменения")
        return True
    else:
        print(f"{ERROR} Ошибка создания резервной копии!")
        return False

if __name__ == "__main__":
    # Получаем описание из аргументов командной строки
    if len(sys.argv) > 1:
        description = " ".join(sys.argv[1:])
        quick_backup(description)
    else:
        quick_backup() 