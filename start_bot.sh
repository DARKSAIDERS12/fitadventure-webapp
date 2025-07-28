#!/bin/bash

echo "🚀 Запуск FitAdventure Bot..."

# Остановка всех процессов
echo "🛑 Остановка предыдущих процессов..."
pkill -f cloudflared
pkill -f "python3.*main.py"
pkill -f "python3.*simple_webapp_server.py"
pkill -f "python3.*public_webapp_server.py"
pkill -f "python3.*https_webapp_server.py"

sleep 2

# Запуск публичного HTTP сервера
echo "🌐 Запуск публичного HTTP сервера..."
python3 public_webapp_server.py &
HTTP_PID=$!
echo "✅ HTTP сервер запущен (PID: $HTTP_PID)"

sleep 3

# Запуск Telegram бота
echo "🤖 Запуск Telegram бота..."
python3 main.py &
BOT_PID=$!
echo "✅ Telegram бот запущен (PID: $BOT_PID)"

sleep 2

echo ""
echo "🎉 Система запущена!"
echo "📱 Telegram Bot: Работает"
echo "🌐 HTTP Server: http://localhost:8080"
echo "📁 Web App: http://localhost:8080/webapp_products.html"
echo ""
echo "⚠️  Для Telegram Web App нужен HTTPS туннель"
echo "🔗 Попробуйте: cloudflared tunnel --url http://localhost:8080"
echo ""
echo "⌨️ Нажмите Ctrl+C для остановки"

# Ожидание сигнала остановки
trap "echo '🛑 Остановка системы...'; pkill -P $$; exit" INT
wait 