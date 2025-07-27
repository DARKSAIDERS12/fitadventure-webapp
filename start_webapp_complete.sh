#!/bin/bash

echo "🚀 Автоматический запуск FitAdventure Web App"
echo "=============================================="

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    exit 1
fi

# Проверяем наличие OpenSSL
if ! command -v openssl &> /dev/null; then
    echo "❌ OpenSSL не найден! Установите: sudo apt install openssl"
    exit 1
fi

# Проверяем наличие curl
if ! command -v curl &> /dev/null; then
    echo "❌ curl не найден! Установите: sudo apt install curl"
    exit 1
fi

echo "✅ Все зависимости найдены"

# Останавливаем предыдущие процессы
echo "🛑 Остановка предыдущих процессов..."
pkill -f "auto_https_server.py" 2>/dev/null
pkill -f "ngrok" 2>/dev/null
sleep 2

# Запускаем HTTPS сервер с ngrok
echo "🌐 Запуск HTTPS Web App сервера..."
python3 auto_https_server.py &

# Ждем запуска
sleep 5

# Проверяем статус
echo "🔍 Проверка статуса..."

# Проверяем HTTPS сервер
if curl -k -s https://localhost:8443/webapp_products.html > /dev/null; then
    echo "✅ HTTPS сервер работает"
else
    echo "❌ HTTPS сервер не отвечает"
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

echo ""
echo "🎉 Настройка завершена!"
echo "📋 Что делать дальше:"
echo "1. Откройте Telegram"
echo "2. Найдите вашего бота"
echo "3. Нажмите '🎮 Мини-приложения'"
echo "4. Выберите '🍎 База продуктов'"
echo "5. Мини-приложение откроется!"
echo ""
echo "⌨️ Для остановки нажмите Ctrl+C"

# Ждем сигнала остановки
trap 'echo ""; echo "🛑 Остановка..."; pkill -f "auto_https_server.py"; pkill -f "ngrok"; echo "✅ Все процессы остановлены"; exit 0' INT

# Держим скрипт активным
while true; do
    sleep 10
    # Показываем статус каждые 10 секунд
    if curl -k -s https://localhost:8443/webapp_products.html > /dev/null; then
        echo "💚 Сервер работает нормально"
    else
        echo "⚠️ Сервер не отвечает"
    fi
done 