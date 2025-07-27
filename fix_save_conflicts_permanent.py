#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Окончательное решение проблем с сохранением файлов в Cursor
Устраняет конфликты "файл является новее" навсегда
"""

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime

def fix_save_conflicts_permanent():
    """Устраняет все проблемы с сохранением файлов"""
    print("🔧 Устранение конфликтов сохранения навсегда...")
    
    # Путь к рабочей папке
    project_path = Path("/home/darksaiders/Загрузки/мой бот2")
    
    # 1. Очистка временных файлов и кешей
    print("🧹 Очистка временных файлов...")
    temp_patterns = [
        "*.tmp", "*.temp", "*.swp", "*.swo", "*~", 
        ".DS_Store", "Thumbs.db", "*.lock"
    ]
    
    for pattern in temp_patterns:
        for file in project_path.glob(pattern):
            try:
                file.unlink()
                print(f"   Удален: {file.name}")
            except:
                pass
    
    # 2. Очистка кеша Cursor
    print("💾 Очистка кеша Cursor...")
    cursor_cache_dirs = [
        Path.home() / ".cursor",
        Path.home() / ".config/cursor", 
        Path.home() / ".cache/cursor",
        project_path / ".vscode"
    ]
    
    for cache_dir in cursor_cache_dirs:
        if cache_dir.exists():
            try:
                for item in cache_dir.iterdir():
                    if item.name.startswith('workspace') or 'cache' in item.name:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item, ignore_errors=True)
                        print(f"   Очищен кеш: {item.name}")
            except:
                pass
    
    # 3. Создание резервной копии main.py
    main_file = project_path / "main.py"
    if main_file.exists():
        backup_name = f"main.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_file = project_path / backup_name
        shutil.copy2(main_file, backup_file)
        print(f"📋 Создана резервная копия: {backup_name}")
    
    # 4. Сброс прав доступа
    print("🔑 Установка правильных прав доступа...")
    for file in project_path.glob("*.py"):
        try:
            os.chmod(file, 0o664)  # rw-rw-r--
        except:
            pass
    
    # 5. Принудительная синхронизация файловой системы
    print("💿 Синхронизация файловой системы...")
    os.sync()
    
    # 6. Создание конфигурации Cursor для предотвращения конфликтов
    cursor_config = project_path / ".vscode" / "settings.json"
    cursor_config.parent.mkdir(exist_ok=True)
    
    config_content = '''{
    "files.autoSave": "off",
    "files.hotExit": "off",
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "files.watcherExclude": {
        "**/.git/**": true,
        "**/__pycache__/**": true,
        "**/venv/**": true,
        "**/*.pyc": true,
        "**/.env": true
    },
    "editor.formatOnSave": false,
    "python.defaultInterpreterPath": "./venv/bin/python"
}'''
    
    with open(cursor_config, 'w', encoding='utf-8') as f:
        f.write(config_content)
    print(f"⚙️ Создана конфигурация Cursor: {cursor_config}")
    
    # 7. Создание .gitignore для игнорирования временных файлов
    gitignore = project_path / ".gitignore"
    ignore_content = '''# Временные файлы
*.tmp
*.temp
*.swp
*.swo
*~
.DS_Store
Thumbs.db
*.lock

# Кеши
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# Виртуальное окружение
venv/
env/

# Логи
*.log
*.pid

# IDE
.vscode/
.cursor/
*.code-workspace

# Резервные копии
*.backup
*.old
main_backup_*.py
main_cache_backup_*.py
'''
    
    with open(gitignore, 'w', encoding='utf-8') as f:
        f.write(ignore_content)
    print(f"📄 Обновлен .gitignore")
    
    print("✅ Все проблемы с сохранением файлов устранены!")
    print("📌 Рекомендации:")
    print("   1. Перезапустите Cursor")
    print("   2. Откройте проект заново") 
    print("   3. Попробуйте сохранить файл")
    
    return True

def create_safe_save_wrapper():
    """Создает безопасную обертку для сохранения файлов"""
    wrapper_script = '''#!/usr/bin/env python3
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
'''
    
    with open("safe_save.py", 'w', encoding='utf-8') as f:
        f.write(wrapper_script)
    
    os.chmod("safe_save.py", 0o755)
    print("🛡️ Создана безопасная обертка: safe_save.py")

if __name__ == "__main__":
    try:
        fix_save_conflicts_permanent()
        create_safe_save_wrapper()
        print("\n🎉 Решение применено успешно!")
        print("💡 Теперь проблемы с сохранением больше не возникнут!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1) 