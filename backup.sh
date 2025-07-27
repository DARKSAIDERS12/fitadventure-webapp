#!/bin/bash
# 💾 FitAdventure Backup Script
# Удобный интерфейс для резервного копирования

echo "💾 FitAdventure Backup System"
echo "================================"

# Функция быстрого резервного копирования
quick_backup() {
    echo "⚡ Быстрое резервное копирование..."
    python3 quick_backup.py "$@"
}

# Функция полного управления резервными копиями
full_backup() {
    echo "🔧 Полная система резервного копирования..."
    python3 backup_system.py
}

# Функция запуска бота с автобэкапом
safe_start_bot() {
    echo "🔒 Безопасный запуск бота с резервным копированием..."
    echo "📝 Создание резервной копии перед запуском..."
    python3 quick_backup.py "Бэкап перед запуском бота"
    
    if [ $? -eq 0 ]; then
        echo "✅ Резервная копия создана. Запуск бота..."
        source venv/bin/activate
        python3 main_ultra_ui.py
    else
        echo "❌ Ошибка создания резервной копии. Запуск отменен."
    fi
}

# Показать меню
if [ $# -eq 0 ]; then
    echo ""
    echo "💡 Выберите действие:"
    echo "1. ⚡ Быстрое резервное копирование"
    echo "2. 🔧 Полное управление резервными копиями"
    echo "3. 🔒 Безопасный запуск бота"
    echo "4. 📋 Показать последние копии"
    echo ""
    read -p "👑 Ваш выбор (1-4): " choice
    
    case $choice in
        1) quick_backup ;;
        2) full_backup ;;
        3) safe_start_bot ;;
        4) ls -la backups/*.zip 2>/dev/null || echo "❌ Резервные копии не найдены" ;;
        *) echo "❌ Неверный выбор" ;;
    esac
else
    # Если переданы аргументы, выполняем быстрое резервное копирование
    case $1 in
        quick|q) quick_backup "${@:2}" ;;
        full|f) full_backup ;;
        safe|s) safe_start_bot ;;
        list|l) ls -la backups/ 2>/dev/null || echo "❌ Папка backups не найдена" ;;
        *) quick_backup "$@" ;;
    esac
fi 