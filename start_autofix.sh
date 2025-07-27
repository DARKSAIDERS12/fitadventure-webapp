#!/usr/bin/env bash
# Запуск автомонитора конфликтов сохранения

echo "🚀 Запуск автомонитора FitAdventure..."

# Проверяем, не запущен ли уже
if pgrep -f "simple_auto_monitor.py" > /dev/null; then
    echo "⚠️ Автомонитор уже запущен!"
    exit 1
fi

# Запускаем в фоновом режиме
cd "/home/darksaiders/Загрузки/мой бот2"
nohup python3 simple_auto_monitor.py > autofix.log 2>&1 &

echo "✅ Автомонитор запущен в фоновом режиме"
echo "📄 Логи: /home/darksaiders/Загрузки/мой бот2/autofix.log"
echo "🛑 Остановить: ./stop_autofix.sh"
