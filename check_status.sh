#!/bin/bash

echo "🔍 Проверка статуса FitAdventure Bot..."
echo ""

# Проверка Telegram Bot
echo "🤖 Telegram Bot:"
if pgrep -f "python3.*main.py" > /dev/null; then
    BOT_PID=$(pgrep -f "python3.*main.py")
    echo "   ✅ Работает (PID: $BOT_PID)"
else
    echo "   ❌ Не запущен"
fi

echo ""

# Проверка HTTP сервера
echo "🌐 HTTP Web App Server:"
if pgrep -f "python3.*simple_webapp_server.py" > /dev/null; then
    HTTP_PID=$(pgrep -f "python3.*simple_webapp_server.py")
    echo "   ✅ Работает (PID: $HTTP_PID)"
    echo "   🌐 URL: http://localhost:8080/webapp_products.html"
else
    echo "   ❌ Не запущен"
fi

echo ""

# Проверка HTTPS сервера
echo "🔒 HTTPS Web App Server:"
if pgrep -f "python3.*https_webapp_server.py" > /dev/null; then
    HTTPS_PID=$(pgrep -f "python3.*https_webapp_server.py")
    echo "   ✅ Работает (PID: $HTTPS_PID)"
    echo "   🌐 URL: https://localhost:8443/webapp_products.html"
else
    echo "   ❌ Не запущен"
fi

echo ""

# Проверка Cloudflare Tunnel
echo "🌍 Cloudflare Tunnel:"
if pgrep cloudflared > /dev/null; then
    TUNNEL_PID=$(pgrep cloudflared)
    echo "   ✅ Работает (PID: $TUNNEL_PID)"
    if [ -f "cloudflared_final.log" ]; then
        TUNNEL_URL=$(grep "https://" cloudflared_final.log | tail -1 | grep -o 'https://[^ ]*' | head -1)
        if [ -n "$TUNNEL_URL" ]; then
            echo "   🌐 URL: $TUNNEL_URL/webapp_products.html"
        fi
    fi
else
    echo "   ❌ Не запущен"
fi

echo ""

# Тест HTTP сервера
echo "🔍 Тест HTTP сервера:"
if curl -s "http://localhost:8080/webapp_products.html" > /dev/null; then
    echo "   ✅ HTTP сервер отвечает"
else
    echo "   ❌ HTTP сервер не отвечает"
fi

echo ""

# Тест HTTPS сервера
echo "🔍 Тест HTTPS сервера:"
if curl -k -s "https://localhost:8443/webapp_products.html" > /dev/null; then
    echo "   ✅ HTTPS сервер отвечает"
else
    echo "   ❌ HTTPS сервер не отвечает"
fi

echo ""

echo "📱 Для использования:"
echo "1. Откройте Telegram"
echo "2. Найдите своего бота"
echo "3. Нажмите '🍎 База продуктов'"
echo "4. Web App должен открыться" 