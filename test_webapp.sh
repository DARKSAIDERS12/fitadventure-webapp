#!/bin/bash

echo "🚀 Запуск тестирования Web App..."

# Запускаем Flask приложение в фоне
echo "📡 Запуск Flask сервера..."
python3 webapp_products.py &
FLASK_PID=$!

# Ждем немного для запуска
sleep 3

# Запускаем ngrok
echo "🌐 Запуск ngrok туннеля..."
./ngrok http 5000 > ngrok.log 2>&1 &
NGROK_PID=$!

# Ждем запуска ngrok
sleep 5

# Получаем HTTPS URL
HTTPS_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | cut -d'"' -f4 | head -1)

if [ -n "$HTTPS_URL" ]; then
    echo "✅ HTTPS URL получен: $HTTPS_URL"
    echo ""
    echo "🔧 Обновите URL в main.py:"
    echo "web_app_url = \"$HTTPS_URL\""
    echo ""
    echo "📱 Теперь можете протестировать Web App в боте!"
    echo "🌐 Для просмотра логов ngrok: tail -f ngrok.log"
    echo "📊 Для просмотра интерфейса ngrok: http://localhost:4040"
    echo ""
    echo "⌨️ Нажмите Ctrl+C для остановки"
    
    # Сохраняем URL в файл
    echo "$HTTPS_URL" > webapp_url.txt
else
    echo "❌ Ошибка получения HTTPS URL"
fi

# Ждем Ctrl+C
trap "echo '🛑 Остановка...'; kill $FLASK_PID $NGROK_PID; exit" INT
wait 