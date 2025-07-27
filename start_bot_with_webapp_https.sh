#!/bin/bash

echo "🚀 Запуск FitAdventure Bot с HTTPS Web App..."

# Проверяем, что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: main.py не найден. Запустите скрипт из директории бота."
    exit 1
fi

# Останавливаем существующие процессы
echo "🛑 Остановка существующих процессов..."
pkill -f "python3 main.py" 2>/dev/null
pkill -f "https_webapp_server.py" 2>/dev/null
sleep 2

# Запускаем HTTPS Web App сервер
echo "🌐 Запуск HTTPS Web App сервера..."
python3 https_webapp_server.py > webapp_https.log 2>&1 &
WEBAPP_PID=$!
echo "✅ HTTPS Web App сервер запущен (PID: $WEBAPP_PID)"

# Ждем немного, чтобы сервер запустился
sleep 5

# Проверяем, что HTTPS Web App работает
if curl -k -s https://localhost:8443 > /dev/null 2>&1; then
    echo "✅ HTTPS Web App сервер работает на https://localhost:8443"
else
    echo "❌ Ошибка: HTTPS Web App сервер не запустился"
    exit 1
fi

# Запускаем бота
echo "🤖 Запуск Telegram бота..."
python3 main.py &
BOT_PID=$!
echo "✅ Бот запущен (PID: $BOT_PID)"

echo ""
echo "🎯 FitAdventure Bot v5.0 Final запущен!"
echo "📱 Web App URL: https://localhost:8443/webapp_products.html"
echo "🤖 Бот готов к работе в Telegram"
echo ""
echo "📊 Статус процессов:"
echo "   HTTPS Web App сервер: PID $WEBAPP_PID"
echo "   Telegram бот: PID $BOT_PID"
echo ""
echo "🎮 Теперь при нажатии '🍎 База продуктов' откроется полноценное Web App!"
echo ""
echo "⌨️ Нажмите Ctrl+C для остановки всех процессов"
echo "📋 Логи Web App: tail -f webapp_https.log"
echo "📋 Логи бота: tail -f bot_debug.log"

# Функция для остановки процессов при выходе
cleanup() {
    echo ""
    echo "🛑 Остановка процессов..."
    kill $WEBAPP_PID 2>/dev/null
    kill $BOT_PID 2>/dev/null
    echo "✅ Все процессы остановлены"
    exit 0
}

# Перехватываем сигнал завершения
trap cleanup SIGINT SIGTERM

# Ждем завершения
wait 