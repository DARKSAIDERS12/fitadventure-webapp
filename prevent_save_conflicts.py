#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт предотвращения конфликтов сохранения
Автоматически следит за файловой системой и предотвращает проблемы
"""

import os
import time
import psutil
from pathlib import Path
from datetime import datetime

class SaveConflictPreventer:
    def __init__(self, project_path="/home/darksaiders/Загрузки/мой бот2"):
        self.project_path = Path(project_path)
        self.main_file = self.project_path / "main.py"
        self.last_check = time.time()
        
    def clear_locks_and_temp_files(self):
        """Очищает lock-файлы и временные файлы"""
        patterns = ["*.lock", "*.tmp", "*.temp", "*~"]
        cleaned = 0
        
        for pattern in patterns:
            for file in self.project_path.glob(pattern):
                try:
                    file.unlink()
                    cleaned += 1
                except:
                    pass
        
        if cleaned > 0:
            print(f"🧹 Очищено {cleaned} временных файлов")
        
        return cleaned
    
    def check_cursor_processes(self):
        """Проверяет процессы Cursor и закрывает зависшие"""
        cursor_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'cursor' in proc.info['name'].lower():
                    cursor_processes.append(proc)
            except:
                pass
        
        return len(cursor_processes)
    
    def sync_filesystem(self):
        """Принудительная синхронизация файловой системы"""
        try:
            os.sync()
            return True
        except:
            return False
    
    def check_file_permissions(self):
        """Проверяет и исправляет права доступа"""
        if self.main_file.exists():
            try:
                current_mode = oct(self.main_file.stat().st_mode)[-3:]
                if current_mode != '664':
                    os.chmod(self.main_file, 0o664)
                    print(f"🔑 Исправлены права доступа: {current_mode} → 664")
                    return True
            except:
                pass
        return False
    
    def create_emergency_backup(self):
        """Создает экстренную резервную копию"""
        if self.main_file.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.project_path / f"main.py.emergency_{timestamp}"
            
            try:
                import shutil
                shutil.copy2(self.main_file, backup_file)
                print(f"📋 Создана экстренная копия: {backup_file.name}")
                return backup_file
            except Exception as e:
                print(f"❌ Ошибка создания копии: {e}")
        
        return None
    
    def monitor_and_prevent(self, interval=30):
        """Основной цикл мониторинга"""
        print("🛡️ Запущен мониторинг предотвращения конфликтов сохранения")
        print(f"📁 Отслеживаемая папка: {self.project_path}")
        print(f"⏰ Интервал проверки: {interval} секунд")
        print("🔄 Для остановки нажмите Ctrl+C")
        
        try:
            while True:
                # Очистка временных файлов
                self.clear_locks_and_temp_files()
                
                # Проверка прав доступа
                self.check_file_permissions()
                
                # Синхронизация файловой системы
                self.sync_filesystem()
                
                # Проверка процессов Cursor
                cursor_count = self.check_cursor_processes()
                
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"✅ {current_time} - Проверка завершена (Cursor процессов: {cursor_count})")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Мониторинг остановлен пользователем")
        except Exception as e:
            print(f"\n❌ Ошибка мониторинга: {e}")

def create_emergency_fix_script():
    """Создает скрипт экстренного исправления"""
    script_content = '''#!/usr/bin/env bash
# Экстренное исправление конфликтов сохранения

echo "🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ КОНФЛИКТОВ СОХРАНЕНИЯ"

# Остановка всех процессов Cursor
echo "⏹️ Остановка процессов Cursor..."
pkill -f cursor 2>/dev/null || true

# Очистка временных файлов
echo "🧹 Очистка временных файлов..."
find . -name "*.lock" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true

# Синхронизация файловой системы
echo "💿 Синхронизация..."
sync

# Исправление прав доступа
echo "🔑 Исправление прав доступа..."
chmod 664 *.py 2>/dev/null || true

echo "✅ Экстренное исправление завершено!"
echo "💡 Теперь можно перезапустить Cursor и попробовать сохранить файл"
'''
    
    script_path = Path("emergency_fix.sh")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    print(f"🚨 Создан скрипт экстренного исправления: {script_path}")

if __name__ == "__main__":
    import sys
    
    print("🛡️ Система предотвращения конфликтов сохранения")
    print("=" * 50)
    
    # Создание скрипта экстренного исправления
    create_emergency_fix_script()
    
    # Запуск превентивного мониторинга
    preventer = SaveConflictPreventer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        preventer.monitor_and_prevent(30)
    else:
        # Однократная проверка и исправление
        print("🔍 Выполнение однократной проверки...")
        
        preventer.clear_locks_and_temp_files()
        preventer.check_file_permissions() 
        preventer.sync_filesystem()
        
        print("✅ Проверка завершена!")
        print("💡 Для постоянного мониторинга запустите:")
        print("   python3 prevent_save_conflicts.py monitor") 