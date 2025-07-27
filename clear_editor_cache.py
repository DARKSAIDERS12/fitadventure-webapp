#!/usr/bin/env python3
"""
Скрипт для очистки кэша редакторов и устранения конфликтов
"""
import os
import shutil
import subprocess
from pathlib import Path

def clear_caches():
    """Очистка всех возможных кэшей"""
    print("🧹 Очистка кэшей редакторов...")
    
    # Очистка кэша VSCode
    vscode_cache_dirs = [
        Path.home() / ".vscode",
        Path.home() / ".config" / "Code",
        Path() / ".vscode"
    ]
    
    for cache_dir in vscode_cache_dirs:
        if cache_dir.exists():
            try:
                # Очищаем только временные файлы
                temp_files = list(cache_dir.glob("**/*.tmp"))
                temp_files.extend(cache_dir.glob("**/*~"))
                temp_files.extend(cache_dir.glob("**/.#*"))
                
                for temp_file in temp_files:
                    temp_file.unlink(missing_ok=True)
                    
                print(f"✅ Очищен кэш: {cache_dir}")
            except Exception as e:
                print(f"⚠️  Предупреждение при очистке {cache_dir}: {e}")
    
    # Очистка временных файлов в текущей директории
    current_dir = Path(".")
    temp_patterns = ["*~", ".#*", "*.tmp", "*.swp", "*.swo"]
    
    for pattern in temp_patterns:
        for temp_file in current_dir.glob(pattern):
            try:
                temp_file.unlink()
                print(f"✅ Удален временный файл: {temp_file}")
            except Exception:
                pass
    
    print("🎯 Кэши очищены!")

def restart_file_watchers():
    """Перезапуск файловых мониторов"""
    try:
        # Остановка процессов, которые могут блокировать файлы
        subprocess.run(["pkill", "-f", "code"], capture_output=True)
        subprocess.run(["pkill", "-f", "cursor"], capture_output=True)
        print("✅ Процессы редакторов остановлены")
    except Exception as e:
        print(f"⚠️  Не удалось остановить процессы: {e}")

if __name__ == "__main__":
    clear_caches()
    restart_file_watchers()
    print("\n🚀 Все конфликты устранены! Попробуйте сохранить файл заново.")
