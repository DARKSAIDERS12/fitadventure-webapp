#!/usr/bin/env bash
# Остановка автомонитора

echo "🛑 Остановка автомонитора FitAdventure..."

pkill -f "simple_auto_monitor.py"

if [ $? -eq 0 ]; then
    echo "✅ Автомонитор остановлен"
else
    echo "⚠️ Автомонитор не был запущен"
fi
