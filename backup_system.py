#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ FitAdventure Backup System
💾 Система резервного копирования проекта
🔒 Версия: 1.0 - Safe Archive
"""

import os
import shutil
import datetime
import json
from pathlib import Path
import subprocess

# Красивые символы для вывода
BACKUP = "💾"
SAFE = "🔒"
ARCHIVE = "📦"
SUCCESS = "✅"
WARNING = "⚠️"
ERROR = "❌"
INFO = "💡"
TIME = "⏰"

class FitAdventureBackup:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.backup_dir = self.project_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Важные файлы для резервного копирования
        self.important_files = [
            "main.py",
            "main_ultra_ui.py", 
            "ultra_precise_formulas.py",
            "run_bot.py",
            "run_ultra_bot.py",
            "requirements.txt",
            ".env",
            "*.md",  # Все markdown файлы
            "start_*.sh"
        ]
        
        # Папки для копирования
        self.important_dirs = [
            "__pycache__",  # На случай если нужны скомпилированные файлы
        ]
        
        # Исключить из копирования
        self.exclude_patterns = [
            "*.log",
            "venv/",
            "backups/",
            ".git/",
            "*.pyc",
            "__pycache__/*",
            "*.tmp",
            ".DS_Store"
        ]

    def create_backup_info(self, backup_name: str) -> dict:
        """Создание информации о резервной копии"""
        return {
            "backup_name": backup_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "Ultra Beauty v3.0",
            "files_count": 0,
            "description": "FitAdventure Ultra Beauty полная резервная копия",
            "components": [
                "Ultra Beautiful UI (main_ultra_ui.py)",
                "Smart Launcher (run_ultra_bot.py)",
                "Precise Formulas (ultra_precise_formulas.py)",
                "Complete Documentation",
                "Configuration Files"
            ],
            "features": [
                "Анимированные прогресс-бары",
                "Красивые карточки интерфейса", 
                "Мультиязычность (RU/EN)",
                "Интерактивные элементы",
                "95-99% точность расчетов",
                "Система диагностики"
            ]
        }

    def get_backup_name(self, custom_name: str = None) -> str:
        """Генерация имени резервной копии"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if custom_name:
            return f"FitAdventure_{custom_name}_{timestamp}"
        return f"FitAdventure_UltraBeauty_{timestamp}"

    def create_backup(self, description: str = "Автоматическая резервная копия") -> bool:
        """Создание полной резервной копии"""
        backup_name = self.get_backup_name()
        backup_path = self.backup_dir / backup_name
        
        print(f"{BACKUP} Создание резервной копии: {backup_name}")
        print(f"{TIME} Время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Создаем папку для резервной копии
            backup_path.mkdir(exist_ok=True)
            files_copied = 0
            
            # Копируем важные файлы
            print(f"{INFO} Копирование файлов...")
            for pattern in self.important_files:
                if "*" in pattern:
                    # Обработка масок файлов
                    for file_path in self.project_dir.glob(pattern):
                        if file_path.is_file() and self._should_include(file_path):
                            shutil.copy2(file_path, backup_path)
                            files_copied += 1
                            print(f"  {SUCCESS} {file_path.name}")
                else:
                    file_path = self.project_dir / pattern
                    if file_path.exists() and self._should_include(file_path):
                        if file_path.is_file():
                            shutil.copy2(file_path, backup_path)
                        else:
                            shutil.copytree(file_path, backup_path / pattern, dirs_exist_ok=True)
                        files_copied += 1
                        print(f"  {SUCCESS} {pattern}")
            
            # Создаем информацию о резервной копии
            backup_info = self.create_backup_info(backup_name)
            backup_info["files_count"] = files_copied
            backup_info["description"] = description
            
            # Сохраняем информацию
            with open(backup_path / "backup_info.json", 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)
            
            # Создаем README для резервной копии
            self._create_backup_readme(backup_path, backup_info)
            
            # Создаем архив
            archive_path = self.backup_dir / f"{backup_name}.zip"
            shutil.make_archive(str(backup_path), 'zip', str(backup_path))
            
            # Удаляем временную папку
            shutil.rmtree(backup_path)
            
            print(f"{SUCCESS} Резервная копия создана: {archive_path.name}")
            print(f"{ARCHIVE} Файлов скопировано: {files_copied}")
            print(f"{SAFE} Размер архива: {self._get_file_size(archive_path)}")
            
            return True
            
        except Exception as e:
            print(f"{ERROR} Ошибка создания резервной копии: {e}")
            return False

    def _should_include(self, file_path: Path) -> bool:
        """Проверка, нужно ли включать файл в резервную копию"""
        file_str = str(file_path.relative_to(self.project_dir))
        for pattern in self.exclude_patterns:
            if pattern.replace("*", "") in file_str or file_str.endswith(pattern.replace("*", "")):
                return False
        return True

    def _create_backup_readme(self, backup_path: Path, backup_info: dict):
        """Создание README для резервной копии"""
        readme_content = f"""# {BACKUP} Резервная копия FitAdventure Ultra Beauty

## {INFO} Информация о резервной копии

- **Название:** {backup_info['backup_name']}
- **Дата создания:** {backup_info['timestamp'][:19].replace('T', ' ')}
- **Версия:** {backup_info['version']}
- **Количество файлов:** {backup_info['files_count']}
- **Описание:** {backup_info['description']}

## {ARCHIVE} Компоненты проекта

"""
        for component in backup_info['components']:
            readme_content += f"- {SUCCESS} {component}\n"

        readme_content += f"""
## {SAFE} Функции Ultra Beauty

"""
        for feature in backup_info['features']:
            readme_content += f"- ✨ {feature}\n"

        readme_content += f"""
## {INFO} Восстановление из резервной копии

### 1. Распаковка архива
```bash
unzip {backup_info['backup_name']}.zip
cd {backup_info['backup_name']}
```

### 2. Копирование файлов
```bash
# Скопируйте файлы в рабочую папку проекта
cp * /path/to/your/project/
```

### 3. Настройка окружения
```bash
# Установите зависимости
pip install -r requirements.txt

# Настройте токен в .env файле
# TELEGRAM_BOT_TOKEN=ваш_токен
```

### 4. Запуск бота
```bash
# Ультра красивая версия
python3 run_ultra_bot.py

# Или прямой запуск
python3 main_ultra_ui.py
```

## {WARNING} Важные замечания

- Не забудьте настроить токен бота в .env файле
- Убедитесь что установлены все зависимости
- Проверьте права доступа к файлам после восстановления

---
*Резервная копия создана автоматически системой FitAdventure Backup*
"""
        
        with open(backup_path / "RESTORE_README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)

    def _get_file_size(self, file_path: Path) -> str:
        """Получение размера файла в читаемом формате"""
        size = file_path.stat().st_size
        for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} ТБ"

    def list_backups(self):
        """Список всех резервных копий"""
        print(f"{BACKUP} Список резервных копий:")
        print("=" * 60)
        
        backups = list(self.backup_dir.glob("*.zip"))
        if not backups:
            print(f"{WARNING} Резервные копии не найдены")
            return
        
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        for i, backup_file in enumerate(backups, 1):
            size = self._get_file_size(backup_file)
            mtime = datetime.datetime.fromtimestamp(backup_file.stat().st_mtime)
            print(f"{i}. {backup_file.name}")
            print(f"   {TIME} {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   {ARCHIVE} {size}")
            print()

    def restore_backup(self, backup_name: str, target_dir: str = None):
        """Восстановление из резервной копии"""
        if target_dir is None:
            target_dir = str(self.project_dir)
        
        backup_path = self.backup_dir / f"{backup_name}.zip"
        if not backup_path.exists():
            print(f"{ERROR} Резервная копия не найдена: {backup_name}")
            return False
        
        print(f"{INFO} Восстановление из: {backup_name}")
        print(f"{WARNING} ВНИМАНИЕ: Текущие файлы могут быть перезаписаны!")
        
        confirm = input(f"Продолжить восстановление? (y/N): ").lower()
        if confirm != 'y':
            print(f"{INFO} Восстановление отменено")
            return False
        
        try:
            # Распаковываем архив
            shutil.unpack_archive(str(backup_path), str(target_dir))
            print(f"{SUCCESS} Резервная копия восстановлена в: {target_dir}")
            return True
        except Exception as e:
            print(f"{ERROR} Ошибка восстановления: {e}")
            return False

    def cleanup_old_backups(self, keep_count: int = 10):
        """Очистка старых резервных копий"""
        backups = list(self.backup_dir.glob("*.zip"))
        if len(backups) <= keep_count:
            print(f"{INFO} Очистка не требуется ({len(backups)} резервных копий)")
            return
        
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        to_delete = backups[keep_count:]
        
        print(f"{WARNING} Будет удалено {len(to_delete)} старых резервных копий")
        for backup in to_delete:
            print(f"  - {backup.name}")
        
        confirm = input(f"Удалить старые копии? (y/N): ").lower()
        if confirm == 'y':
            for backup in to_delete:
                backup.unlink()
                print(f"{SUCCESS} Удалено: {backup.name}")

def main():
    """Главная функция для интерактивной работы"""
    backup_system = FitAdventureBackup()
    
    print(f"""
{BACKUP}═══════════════════════════════════════════════════════════{BACKUP}
{SAFE}                FITADVENTURE BACKUP SYSTEM                   {SAFE}
{ARCHIVE}              Система резервного копирования               {ARCHIVE}
{BACKUP}═══════════════════════════════════════════════════════════{BACKUP}

{INFO} Выберите действие:
1. {BACKUP} Создать резервную копию
2. {ARCHIVE} Список резервных копий
3. {SAFE} Восстановить из резервной копии
4. {WARNING} Очистить старые копии
5. {ERROR} Выход
""")
    
    while True:
        choice = input(f"\n{INFO} Ваш выбор (1-5): ").strip()
        
        if choice == '1':
            description = input(f"{INFO} Описание резервной копии (Enter для автоматического): ").strip()
            if not description:
                description = "Ручная резервная копия Ultra Beauty"
            backup_system.create_backup(description)
            
        elif choice == '2':
            backup_system.list_backups()
            
        elif choice == '3':
            backup_system.list_backups()
            backup_name = input(f"{INFO} Введите имя резервной копии (без .zip): ").strip()
            if backup_name:
                backup_system.restore_backup(backup_name)
            
        elif choice == '4':
            try:
                keep = int(input(f"{INFO} Сколько последних копий оставить? (по умолчанию 10): ") or "10")
                backup_system.cleanup_old_backups(keep)
            except ValueError:
                print(f"{ERROR} Некорректное число")
            
        elif choice == '5':
            print(f"{SAFE} До свидания!")
            break
            
        else:
            print(f"{ERROR} Неверный выбор")

if __name__ == "__main__":
    main() 