#!/usr/bin/env bash
# Экстренное исправление конфликтов сохранения

echo "🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ КОНФЛИКТОВ СОХРАНЕНИЯ"
echo "================================================"

# Остановка всех процессов Cursor
echo "⏹️ Остановка процессов Cursor..."
pkill -f cursor 2>/dev/null || true
sleep 2

# Создание резервной копии main.py
if [ -f "main.py" ]; then
    echo "📋 Создание резервной копии..."
    cp main.py "main.py.emergency_backup_$(date +%Y%m%d_%H%M%S)"
fi

# Очистка временных файлов
echo "🧹 Очистка временных файлов..."
find . -name "*.lock" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true  
find . -name "*.temp" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true
find . -name "*.swp" -delete 2>/dev/null || true
find . -name "*.swo" -delete 2>/dev/null || true

# Синхронизация файловой системы
echo "💿 Синхронизация..."
sync

# Исправление прав доступа
echo "🔑 Исправление прав доступа..."
chmod 664 *.py 2>/dev/null || true

# Очистка кеша Cursor
echo "💾 Очистка кеша..."
rm -rf ~/.cursor/logs/* 2>/dev/null || true
rm -rf ~/.cache/cursor/* 2>/dev/null || true

echo ""
echo "✅ ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!"
echo "💡 Теперь можно перезапустить Cursor и попробовать сохранить файл"
echo "🔄 Если проблемы остались, запустите: python3 simple_fix.py emergency" 