#!/bin/bash

echo "🚀 Запуск FitAdventure Bot с Web App..."

# Остановка всех процессов
echo "🛑 Остановка предыдущих процессов..."
pkill -f cloudflared
pkill -f "python3.*main.py"
pkill -f "python3.*simple_webapp_server.py"

sleep 2

# Запуск веб-сервера
echo "🌐 Запуск веб-сервера..."
python3 simple_webapp_server.py &
WEB_SERVER_PID=$!
echo "✅ Веб-сервер запущен (PID: $WEB_SERVER_PID)"

sleep 3

# Запуск Cloudflare Tunnel
echo "🌍 Запуск Cloudflare Tunnel..."
cloudflared tunnel --url http://localhost:8080 --logfile cloudflared.log &
TUNNEL_PID=$!
echo "✅ Cloudflare Tunnel запущен (PID: $TUNNEL_PID)"

sleep 5

# Получение URL туннеля
echo "🔍 Получение URL туннеля..."
TUNNEL_URL=$(grep "Your quick Tunnel has been created" cloudflared.log | tail -1 | sed 's/.*https:\/\/\([^ ]*\).*/https:\/\/\1/')
echo "🌐 URL туннеля: $TUNNEL_URL"

if [ -n "$TUNNEL_URL" ]; then
    # Обновление URL в коде бота
    echo "📝 Обновление URL в коде бота..."
    sed -i "s|https://[^/]*\.trycloudflare\.com|$TUNNEL_URL|g" main.py
    echo "✅ URL обновлен в main.py"
fi

sleep 2

# Запуск бота
echo "🤖 Запуск Telegram бота..."
python3 main.py &
BOT_PID=$!
echo "✅ Telegram бот запущен (PID: $BOT_PID)"

echo ""
echo "🎉 ВСЕ СИСТЕМЫ ЗАПУЩЕНЫ!"
echo "📱 Откройте Telegram и найдите своего бота"
echo "🍎 Нажмите 'База продуктов' для открытия Web App"
echo ""
echo "📊 Статус процессов:"
echo "   Веб-сервер: $WEB_SERVER_PID"
echo "   Cloudflare Tunnel: $TUNNEL_PID"
echo "   Telegram Bot: $BOT_PID"
echo ""
echo "🛑 Для остановки нажмите Ctrl+C"

# Ожидание сигнала для остановки
trap 'echo ""; echo "🛑 Остановка всех процессов..."; kill $WEB_SERVER_PID $TUNNEL_PID $BOT_PID 2>/dev/null; exit' INT

# Ожидание
wait 