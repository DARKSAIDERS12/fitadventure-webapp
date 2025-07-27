#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для отправки уведомления об исправлении функции консультации
"""

import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

# Загружаем токен
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def test_fixed_consultation():
    """Тестирование исправленной функции консультации"""
    bot = Bot(token=TOKEN)
    
    # Тестовое сообщение об исправлении
    fixed_message = """🔧 **ИСПРАВЛЕНИЕ: Функция консультации обновлена!** ✅

🎯 **Что исправлено:**
• Кнопка консультации теперь появляется ПОСЛЕ расчетов
• При нажатии на консультацию больше не запрашивается пол
• Функция работает корректно и показывает информацию о консультации

📱 **Как теперь работает:**
1. Пройдите полный опрос бота
2. Получите ваши персональные рекомендации
3. После результатов появится кнопка "💬 Получить консультацию эксперта"
4. Нажмите на неё для получения информации о консультации
5. Свяжитесь с экспертом @DARKSIDERS17

💡 **Логика работы:**
• Кнопка консультации появляется только после завершения расчетов
• Это более логично - сначала получите рекомендации, потом консультацию
• Никаких лишних запросов о поле или других данных

🚀 **Готово к использованию!**

С уважением,
Команда FitAdventure Bot 🎯"""
    
    # ID подписчиков (замените на реальные ID)
    test_subscribers = [901387781]  # Замените на реальные ID подписчиков
    
    success_count = 0
    error_count = 0
    
    for subscriber_id in test_subscribers:
        try:
            await bot.send_message(
                chat_id=subscriber_id,
                text=fixed_message,
                parse_mode='Markdown'
            )
            print(f"✅ Сообщение об исправлении отправлено пользователю {subscriber_id}")
            success_count += 1
        except Exception as e:
            print(f"❌ Ошибка отправки пользователю {subscriber_id}: {e}")
            error_count += 1
    
    print(f"\n📊 Результат отправки:")
    print(f"✅ Успешно: {success_count}")
    print(f"❌ Ошибок: {error_count}")
    print(f"📊 Всего: {len(test_subscribers)}")

if __name__ == "__main__":
    print("🔧 Отправка уведомления об исправлении функции консультации...")
    asyncio.run(test_fixed_consultation())
    print("✅ Тест завершен!") 