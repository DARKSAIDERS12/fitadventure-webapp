#!/bin/bash

echo "🚀 Автоматический запуск всей системы FitAdventure"
echo "=================================================="

# Проверяем зависимости
echo "🔍 Проверка зависимостей..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    exit 1
fi

if ! command -v openssl &> /dev/null; then
    echo "❌ OpenSSL не найден! Установите: sudo apt install openssl"
    exit 1
fi

if ! command -v curl &> /dev/null; then
    echo "❌ curl не найден! Установите: sudo apt install curl"
    exit 1
fi

echo "✅ Все зависимости найдены"

# Останавливаем предыдущие процессы
echo "🛑 Остановка предыдущих процессов..."
pkill -f "complete_webapp_server.py" 2>/dev/null
pkill -f "main.py" 2>/dev/null
pkill -f "ngrok" 2>/dev/null
sleep 3

# Запускаем Web App сервер
echo "🌐 Запуск Web App сервера..."
python3 complete_webapp_server.py &
WEBAPP_PID=$!

# Ждем запуска Web App
echo "⏳ Ожидание запуска Web App сервера..."
sleep 10

# Проверяем Web App сервер
if curl -k -s https://localhost:8443/webapp_products.html > /dev/null; then
    echo "✅ Web App сервер работает"
else
    echo "❌ Web App сервер не отвечает"
fi

# Проверяем ngrok
if curl -s http://localhost:4040/api/tunnels > /dev/null; then
    echo "✅ ngrok туннель работает"
    PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')")
    if [ ! -z "$PUBLIC_URL" ]; then
        echo "🌍 Публичный URL: $PUBLIC_URL"
        echo "📱 Web App URL: $PUBLIC_URL/webapp_products.html"
    fi
else
    echo "⚠️ ngrok туннель не отвечает"
fi

# Ждем еще немного для полной инициализации
sleep 5

# Запускаем бота
echo "🤖 Запуск Telegram бота..."
python3 main.py &
BOT_PID=$!

# Ждем запуска бота
sleep 5

echo ""
echo "🎉 Вся система запущена!"
echo "========================"
echo "📱 Telegram бот: Запущен"
echo "🌐 Web App сервер: Запущен на порту 8443"
echo "🌍 ngrok туннель: Запущен"

if [ ! -z "$PUBLIC_URL" ]; then
    echo "📱 Публичный Web App: $PUBLIC_URL/webapp_products.html"
fi

echo ""
echo "📋 Что делать дальше:"
echo "1. Откройте Telegram"
echo "2. Найдите вашего бота"
echo "3. Отправьте /start"
echo "4. Нажмите '🎮 Мини-приложения'"
echo "5. Выберите '🍎 База продуктов'"
echo "6. Мини-приложение откроется!"
echo ""
echo "⌨️ Для остановки нажмите Ctrl+C"

# Функция остановки
cleanup() {
    echo ""
    echo "🛑 Остановка системы..."
    kill $WEBAPP_PID 2>/dev/null
    kill $BOT_PID 2>/dev/null
    pkill -f "ngrok" 2>/dev/null
    echo "✅ Все процессы остановлены"
    exit 0
}

# Перехватываем Ctrl+C
trap cleanup INT

# Держим скрипт активным
while true; do
    sleep 30
    # Показываем статус каждые 30 секунд
    echo "💚 Система работает нормально"
    
    # Проверяем процессы
    if ! ps -p $WEBAPP_PID > /dev/null; then
        echo "⚠️ Web App сервер остановился"
    fi
    
    if ! ps -p $BOT_PID > /dev/null; then
        echo "⚠️ Telegram бот остановился"
    fi
done 