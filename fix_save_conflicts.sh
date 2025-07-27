#!/bin/bash
# 🔧 FitAdventure - Скрипт для устранения конфликтов сохранения
# Автор: AI Assistant
# Дата: $(date)

echo "🔧 Устранение конфликтов сохранения файлов..."

# Удаление временных файлов редактора
find . -name "*.py~" -delete 2>/dev/null
find . -name ".#*" -delete 2>/dev/null
find . -name "*~" -delete 2>/dev/null
find . -name "*.tmp" -delete 2>/dev/null

# Синхронизация файловой системы
sync

# Установка правильных прав доступа
chmod 664 *.py 2>/dev/null
chmod 775 *.sh 2>/dev/null

# Проверка блокировок файлов
if command -v lsof >/dev/null; then
    echo "📋 Проверка заблокированных файлов:"
    lsof *.py 2>/dev/null || echo "✅ Файлы не заблокированы"
fi

echo "✅ Конфликты устранены! Теперь можно безопасно сохранять файлы."
echo "💡 Запустите этот скрипт, если снова возникнут проблемы с сохранением:"
echo "   bash fix_save_conflicts.sh" 