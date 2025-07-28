#!/bin/bash

echo "🚀 Запуск FitAdventure Bot с публичным Web App..."

# Остановка всех процессов
echo "🛑 Остановка предыдущих процессов..."
pkill -f cloudflared
pkill -f "python3.*main.py"
pkill -f "python3.*simple_webapp_server.py"
pkill -f "python3.*https_webapp_server.py"

sleep 2

# Запуск HTTP сервера
echo "🌐 Запуск HTTP сервера..."
python3 simple_webapp_server.py &
HTTP_PID=$!
echo "✅ HTTP сервер запущен (PID: $HTTP_PID)"

sleep 3

# Запуск Cloudflare Tunnel
echo "🌍 Запуск Cloudflare Tunnel..."
cloudflared tunnel --url http://localhost:8080 --logfile cloudflared_final.log &
TUNNEL_PID=$!
echo "✅ Cloudflare Tunnel запущен (PID: $TUNNEL_PID)"

sleep 10

# Получение URL туннеля
echo "🔍 Получение URL туннеля..."
TUNNEL_URL=$(grep "Your quick Tunnel has been created" cloudflared_final.log | tail -1 | sed 's/.*https/https/' | sed 's/ .*//')

if [ -n "$TUNNEL_URL" ]; then
    echo "✅ Туннель создан: $TUNNEL_URL"
    
    # Обновление URL в коде бота
    echo "📝 Обновление URL в коде бота..."
    sed -i "s|web_app_url = \".*\"|web_app_url = \"$TUNNEL_URL/webapp_products.html\"|" main.py
    
    # Запуск бота
    echo "🤖 Запуск Telegram бота..."
    python3 main.py &
    BOT_PID=$!
    echo "✅ Telegram бот запущен (PID: $BOT_PID)"
    
    sleep 3
    
    echo ""
    echo "🎉 Система запущена!"
    echo "📱 Telegram Bot: Работает"
    echo "🌐 HTTP Server: http://localhost:8080"
    echo "🌍 Cloudflare Tunnel: $TUNNEL_URL"
    echo "📱 Web App: $TUNNEL_URL/webapp_products.html"
    echo ""
    echo "📋 Для использования:"
    echo "1. Откройте Telegram"
    echo "2. Найдите своего бота"
    echo "3. Нажмите '🍎 База продуктов'"
    echo "4. Web App должен открыться без проблем"
    
else
    echo "❌ Не удалось получить URL туннеля"
    echo "🔍 Проверьте логи: tail -f cloudflared_final.log"
fi 