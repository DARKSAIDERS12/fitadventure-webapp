#!/usr/bin/env bash
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
