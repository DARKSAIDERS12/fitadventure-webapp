#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание systemd сервиса для автозапуска автомонитора конфликтов сохранения
"""

import os
import sys
import subprocess
from pathlib import Path

def create_systemd_service():
    """Создание systemd сервиса"""
    project_path = Path("/home/darksaiders/Загрузки/мой бот2")
    user = os.getenv("USER", "darksaiders")
    python_path = sys.executable
    
    service_content = f"""[Unit]
Description=FitAdventure Auto-Fix Monitor - Автоматическое исправление конфликтов сохранения
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
User={user}
Group={user}
WorkingDirectory={project_path}
ExecStart={python_path} {project_path}/simple_auto_monitor.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/1000

[Install]
WantedBy=graphical-session.target
"""
    
    # Путь к сервисному файлу
    service_file = Path.home() / ".config" / "systemd" / "user" / "fitadventure-autofix.service"
    
    # Создание директории если не существует
    service_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Запись сервисного файла
    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(service_content)
    
    print(f"✅ Создан systemd сервис: {service_file}")
    return service_file

def create_desktop_autostart():
    """Создание autostart файла для рабочего стола"""
    project_path = Path("/home/darksaiders/Загрузки/мой бот2")
    python_path = sys.executable
    
    desktop_content = f"""[Desktop Entry]
Type=Application
Name=FitAdventure Auto-Fix Monitor
Comment=Автоматическое исправление конфликтов сохранения файлов
Exec={python_path} {project_path}/simple_auto_monitor.py
Icon=applications-system
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
StartupNotify=false
Terminal=false
"""
    
    # Путь к autostart файлу
    autostart_dir = Path.home() / ".config" / "autostart"
    autostart_dir.mkdir(parents=True, exist_ok=True)
    
    autostart_file = autostart_dir / "fitadventure-autofix.desktop"
    
    with open(autostart_file, 'w', encoding='utf-8') as f:
        f.write(desktop_content)
    
    # Делаем файл исполняемым
    os.chmod(autostart_file, 0o755)
    
    print(f"✅ Создан autostart файл: {autostart_file}")
    return autostart_file

def create_management_scripts():
    """Создание скриптов управления автозапуском"""
    project_path = Path("/home/darksaiders/Загрузки/мой бот2")
    
    # Скрипт запуска
    start_script = f"""#!/usr/bin/env bash
# Запуск автомонитора конфликтов сохранения

echo "🚀 Запуск автомонитора FitAdventure..."

# Проверяем, не запущен ли уже
if pgrep -f "simple_auto_monitor.py" > /dev/null; then
    echo "⚠️ Автомонитор уже запущен!"
    exit 1
fi

# Запускаем в фоновом режиме
cd "{project_path}"
nohup python3 simple_auto_monitor.py > autofix.log 2>&1 &

echo "✅ Автомонитор запущен в фоновом режиме"
echo "📄 Логи: {project_path}/autofix.log"
echo "🛑 Остановить: ./stop_autofix.sh"
"""

    # Скрипт остановки
    stop_script = """#!/usr/bin/env bash
# Остановка автомонитора

echo "🛑 Остановка автомонитора FitAdventure..."

pkill -f "simple_auto_monitor.py"

if [ $? -eq 0 ]; then
    echo "✅ Автомонитор остановлен"
else
    echo "⚠️ Автомонитор не был запущен"
fi
"""

    # Скрипт проверки статуса
    status_script = """#!/usr/bin/env bash
# Проверка статуса автомонитора

echo "📊 Статус автомонитора FitAdventure"
echo "=================================="

if pgrep -f "simple_auto_monitor.py" > /dev/null; then
    PID=$(pgrep -f "simple_auto_monitor.py")
    echo "✅ Автомонитор работает (PID: $PID)"
    
    # Показываем последние строки лога
    if [ -f "autofix.log" ]; then
        echo ""
        echo "📄 Последние записи лога:"
        tail -5 autofix.log
    fi
else
    echo "❌ Автомонитор не запущен"
    echo "🚀 Запустить: ./start_autofix.sh"
fi
"""

    # Создание файлов скриптов
    scripts = {
        "start_autofix.sh": start_script,
        "stop_autofix.sh": stop_script,  
        "status_autofix.sh": status_script
    }
    
    created_scripts = []
    for script_name, script_content in scripts.items():
        script_path = project_path / script_name
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Делаем скрипт исполняемым
        os.chmod(script_path, 0o755)
        created_scripts.append(script_path)
        print(f"✅ Создан скрипт: {script_name}")
    
    return created_scripts

def setup_systemd_service():
    """Настройка и активация systemd сервиса"""
    try:
        # Перезагрузка конфигурации systemd
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
        
        # Включение автозапуска
        result = subprocess.run(
            ["systemctl", "--user", "enable", "fitadventure-autofix.service"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("✅ Автозапуск через systemd активирован")
        else:
            print(f"⚠️ Проблема с активацией systemd: {result.stderr}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Ошибка настройки systemd: {e}")
        return False

def main():
    """Главная функция настройки автозапуска"""
    print("🔧 Настройка автозапуска автомонитора конфликтов сохранения")
    print("=" * 60)
    
    try:
        # 1. Создание systemd сервиса
        service_file = create_systemd_service()
        
        # 2. Создание desktop autostart
        autostart_file = create_desktop_autostart()
        
        # 3. Создание скриптов управления
        scripts = create_management_scripts()
        
        # 4. Настройка systemd сервиса
        systemd_success = setup_systemd_service()
        
        print("\n🎉 АВТОЗАПУСК НАСТРОЕН УСПЕШНО!")
        print("=" * 40)
        print("📋 Созданные компоненты:")
        print(f"   • systemd сервис: {service_file}")
        print(f"   • Desktop autostart: {autostart_file}")
        print("   • Скрипты управления:")
        for script in scripts:
            print(f"     - {script.name}")
        
        print("\n🚀 Способы управления:")
        print("   • Ручной запуск: ./start_autofix.sh")
        print("   • Остановка: ./stop_autofix.sh")
        print("   • Статус: ./status_autofix.sh")
        print("   • systemd: systemctl --user start fitadventure-autofix")
        
        print("\n✨ Автомонитор будет автоматически:")
        print("   • Запускаться при входе в систему")
        print("   • Обнаруживать конфликты сохранения")
        print("   • Автоматически их исправлять")
        print("   • Отправлять уведомления")
        
        if systemd_success:
            print("\n💡 Автозапуск активен! Перезайдите в систему для активации")
        else:
            print("\n💡 Используйте ./start_autofix.sh для ручного запуска")
            
    except Exception as e:
        print(f"❌ Ошибка настройки: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 