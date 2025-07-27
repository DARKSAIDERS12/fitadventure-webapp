#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для отправки уведомления о новой функции консультации
"""

import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

# Загружаем токен
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def test_consultation_notification():
    """Тестирование уведомления о новой функции консультации"""
    bot = Bot(token=TOKEN)
    
    # Тестовое сообщение о новой функции
    consultation_message = """🎉 **НОВАЯ ФУНКЦИЯ: Консультация с экспертом!** 💬

🚀 **Что нового:**
• Добавлена кнопка "💬 Консультация с экспертом"
• Прямая связь с фитнес-экспертом @DARKSIDERS17
• Персональные планы тренировок и питания
• Индивидуальные рекомендации

📱 **Как использовать:**
1. Нажмите кнопку "💬 Консультация с экспертом"
2. Получите подробную информацию о консультации
3. Напишите эксперту @DARKSIDERS17
4. Укажите, что вы из FitAdventure Bot

⏰ **Время ответа:** обычно в течение 24 часов

💡 **Совет:** подготовьте информацию о ваших целях и опыте для более эффективной консультации.

С уважением,
Команда FitAdventure Bot 🚀"""
    
    # ID подписчиков (замените на реальные ID)
    # В реальном боте это будет из множества subscribers
    test_subscribers = [901387781]  # Замените на реальные ID подписчиков
    
    success_count = 0
    error_count = 0
    
    for subscriber_id in test_subscribers:
        try:
            await bot.send_message(
                chat_id=subscriber_id,
                text=consultation_message,
                parse_mode='Markdown'
            )
            print(f"✅ Сообщение отправлено пользователю {subscriber_id}")
            success_count += 1
        except Exception as e:
            print(f"❌ Ошибка отправки пользователю {subscriber_id}: {e}")
            error_count += 1
    
    print(f"\n📊 Результат отправки:")
    print(f"✅ Успешно: {success_count}")
    print(f"❌ Ошибок: {error_count}")
    print(f"📊 Всего: {len(test_subscribers)}")

if __name__ == "__main__":
    print("🚀 Отправка уведомления о новой функции консультации...")
    asyncio.run(test_consultation_notification())
    print("✅ Тест завершен!") 