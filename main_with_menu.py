#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FitAdventure Bot v4.0 - Clean Version with Menu System
Чистая версия без декоративных символов + Система меню
"""

import os
import asyncio
import logging
import json
import random
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, BotCommand
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# Импортируем формулы
try:
    from ultra_precise_formulas_FIXED import generate_maximum_precision_recommendations
except ImportError:
    from ultra_precise_formulas import generate_maximum_precision_recommendations

# === АВТОМАТИЧЕСКАЯ НАСТРОЙКА ТОКЕНА ===
def setup_bot_token():
    """Автоматическая настройка токена бота"""
    env_file = Path('.env')
    
    if env_file.exists():
        load_dotenv()
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if token:
            print("✅ Токен бота найден в .env файле")
            return token
    
    print("🤖 Настройка токена Telegram бота")
    print("1. Откройте Telegram")
    print("2. Найдите @BotFather")
    print("3. Отправьте команду /newbot")
    print("4. Следуйте инструкциям и получите токен")
    
    while True:
        token = input("🔑 Введите токен вашего бота: ").strip()
        
        if not token:
            print("❌ Токен не может быть пустым!")
            continue
            
        if not token.startswith(('1', '2', '5', '6')) or ':' not in token:
            print("❌ Неверный формат токена!")
            continue
            
        try:
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(f"TELEGRAM_BOT_TOKEN={token}\n")
            
            print(f"✅ Токен сохранен в файл .env")
            return token
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            continue

load_dotenv()

# --- Логирование ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Состояния ---
LANGUAGE_CHOICE, GENDER, AGE, WEIGHT, HEIGHT, FAT_PERCENTAGE, FAT_PERCENTAGE_INPUT, GOAL, TRAINING_EXPERIENCE, TRAINING_DAYS, ACTIVITY_TYPE, WORKOUT_DURATION, STEPS, INTENSITY, RECOVERY, SLEEP_QUALITY, STRESS_LEVEL, OCCUPATION, USER_SETTINGS, MENU_STATE = range(20)

# --- Хранилище ---
user_data_storage = {}
user_settings = {}
achievements_data = {}

# === ПРОСТЫЕ ПРОГРЕСС-БАРЫ БЕЗ ДЕКОРА ===
def create_clean_progress(current: int, total: int = 12) -> str:
    """Создание простого прогресс-бара без декоративных элементов"""
    progress_percent = min(current / total, 1.0) * 100
    filled = int(current * 10 / total)
    
    # Простой прогресс-бар из обычных символов
    progress_bar = "█" * filled + "░" * (10 - filled)
    
    return f"📊 Прогресс: {current}/{total} ({progress_percent:.0f}%)\n{progress_bar}"

# === СИСТЕМА ДОСТИЖЕНИЙ ===
def check_achievements(user_id: int, action: str, value=None) -> list:
    """Проверка достижений пользователя"""
    if user_id not in achievements_data:
        achievements_data[user_id] = {
            'started_survey': False,
            'completed_survey': False,
            'perfectionist': False,
            'fitness_expert': False,
            'health_enthusiast': False
        }
    
    new_achievements = []
    
    if action == "start_survey" and not achievements_data[user_id]['started_survey']:
        achievements_data[user_id]['started_survey'] = True
        new_achievements.append({
            'name': 'Первые шаги',
            'description': 'Начали анализ здоровья',
            'icon': '🌟'
        })
    
    elif action == "complete_survey" and not achievements_data[user_id]['completed_survey']:
        achievements_data[user_id]['completed_survey'] = True
        new_achievements.append({
            'name': 'Исследователь',
            'description': 'Завершили полный опрос',
            'icon': '🚀'
        })
    
    elif action == "high_precision" and value and value >= 98 and not achievements_data[user_id]['perfectionist']:
        achievements_data[user_id]['perfectionist'] = True
        new_achievements.append({
            'name': 'Перфекционист',
            'description': 'Получили точность 98%+',
            'icon': '👑'
        })
    
    return new_achievements

def format_achievement_notification(achievements: list) -> str:
    """Форматирование уведомлений о достижениях"""
    if not achievements:
        return ""
    
    notification = f"\n👑 НОВЫЕ ДОСТИЖЕНИЯ 👑\n"
    for achievement in achievements:
        notification += f"{achievement['icon']} **{achievement['name']}**\n"
        notification += f"   _{achievement['description']}_\n"
    notification += f"👑 Поздравляем! 👑\n"
    
    return notification

# === НАСТРОЙКИ ПОЛЬЗОВАТЕЛЯ ===
def get_user_theme(user_id: int) -> str:
    """Получить тему пользователя"""
    return user_settings.get(user_id, {}).get('theme', 'default')

def set_user_theme(user_id: int, theme: str):
    """Установить тему пользователя"""
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]['theme'] = theme

def save_user_progress(user_id: int, step: int):
    """Сохранить прогресс пользователя"""
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]['last_step'] = step
    user_settings[user_id]['last_session'] = datetime.now().isoformat()

# === УМНЫЕ РЕКОМЕНДАЦИИ ===
def generate_smart_tips(user_data: dict) -> list:
    """Генерация умных рекомендаций на основе данных пользователя"""
    tips = []
    
    # Рекомендации по возрасту
    age = user_data.get('age', 0)
    if age < 25:
        tips.append({
            'title': 'Совет для молодых',
            'text': 'Сосредоточьтесь на формировании здоровых привычек питания',
            'icon': '🌱'
        })
    elif age > 40:
        tips.append({
            'title': 'Совет для опытных',
            'text': 'Обратите внимание на качество белков и омега-3',
            'icon': '👑'
        })
    
    # Рекомендации по цели
    goal = user_data.get('goal', '')
    if 'Похудение' in goal:
        tips.append({
            'title': 'Для похудения',
            'text': 'Создайте умеренный дефицит калорий 10-20%',
            'icon': '🔥'
        })
    
    return tips

def format_smart_tips(tips: list) -> str:
    """Форматирование умных рекомендаций"""
    if not tips:
        return ""
    
    formatted = f"\n🪄 ПЕРСОНАЛЬНЫЕ СОВЕТЫ 🪄\n"
    for tip in tips:
        formatted += f"{tip['icon']} **{tip['title']}**\n"
        formatted += f"   _{tip['text']}_\n\n"
    
    return formatted

# === ПЕРСОНАЛИЗИРОВАННЫЕ ПОЗДРАВЛЕНИЯ ===
def generate_personalized_celebration(user_data: dict) -> str:
    """Генерация персонализированного поздравления"""
    age = user_data.get('age', 25)
    goal = user_data.get('goal', '')
    
    styles = ['energetic', 'motivational', 'wise']
    style = random.choice(styles)
    
    if style == 'energetic' and age < 30:
        return f"""
🎉 ПОЗДРАВЛЯЕМ! 🎉
Ваш персональный план готов!
Время изменить свою жизнь!
"""
    elif style == 'motivational':
        return f"""
💪 ОТЛИЧНО! 💪
Вы сделали важный шаг к здоровью
Ваши цели достижимы!
"""
    else:
        return f"""
✨ ПРЕВОСХОДНО! ✨
Ваш индивидуальный план питания создан
Путь к успеху начинается сегодня
"""

# === ЭКСПОРТ РЕЗУЛЬТАТОВ ===
def create_result_summary(user_data: dict, results: dict) -> str:
    """Создание резюме результатов для экспорта"""
    summary = f"""
🔮 FITADVENTURE ULTRA v4.0 🔮
Дата анализа: {datetime.now().strftime('%d.%m.%Y %H:%M')}

👤 Пользователь: {user_data.get('user_id', 'Unknown')}
🎯 Цель: {user_data.get('goal', 'Не указана')}
💪 Опыт: {user_data.get('training_experience', 'Не указан')}

📊 РЕЗУЛЬТАТЫ:
Целевые калории: {results.get('target_calories', 0)} ккал
Белки: {results.get('protein_min', 0)}-{results.get('protein_max', 0)} г
Жиры: {results.get('fats', 0)} г
Углеводы: {results.get('carbs', 0)} г

🎯 Точность: {results.get('precision_score', 0)}%
"""
    return summary

# === СИСТЕМА МЕНЮ ===
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать главное меню бота"""
    chat_id = update.effective_chat.id
    user_lang = user_data_storage.get(chat_id, {}).get('language', 'ru')
    
    if user_lang == 'ru':
        menu_text = """
🤖 **FITADVENTURE BOT v4.0 - ГЛАВНОЕ МЕНЮ**

Добро пожаловать в самый точный фитнес-бот!

📋 **Доступные функции:**
🎯 Создание персонального плана питания
⚙️ Настройки и персонализация
🏆 Система достижений
📊 Экспорт результатов
💡 Умные рекомендации

Выберите действие:
"""
        keyboard = [
            [InlineKeyboardButton("🎯 Начать анализ", callback_data='start_analysis')],
            [InlineKeyboardButton("⚙️ Настройки", callback_data='show_settings'),
             InlineKeyboardButton("📊 О боте", callback_data='about_bot')],
            [InlineKeyboardButton("🏆 Достижения", callback_data='show_achievements'),
             InlineKeyboardButton("💡 Советы", callback_data='show_tips')],
            [InlineKeyboardButton("🌍 Язык", callback_data='change_language'),
             InlineKeyboardButton("❓ Помощь", callback_data='help_info')]
        ]
    else:
        menu_text = """
🤖 **FITADVENTURE BOT v4.0 - MAIN MENU**

Welcome to the most accurate fitness bot!

📋 **Available features:**
🎯 Personal nutrition plan creation
⚙️ Settings and personalization
🏆 Achievement system
📊 Results export
💡 Smart recommendations

Choose an action:
"""
        keyboard = [
            [InlineKeyboardButton("🎯 Start Analysis", callback_data='start_analysis')],
            [InlineKeyboardButton("⚙️ Settings", callback_data='show_settings'),
             InlineKeyboardButton("📊 About Bot", callback_data='about_bot')],
            [InlineKeyboardButton("🏆 Achievements", callback_data='show_achievements'),
             InlineKeyboardButton("💡 Tips", callback_data='show_tips')],
            [InlineKeyboardButton("🌍 Language", callback_data='change_language'),
             InlineKeyboardButton("❓ Help", callback_data='help_info')]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            menu_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            menu_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    return MENU_STATE

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Команда /menu для показа главного меню"""
    return await show_main_menu(update, context)

async def about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Информация о боте"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_lang = user_data_storage.get(chat_id, {}).get('language', 'ru')
    
    if user_lang == 'ru':
        about_text = """
🔮 **FITADVENTURE BOT v4.0 CLEAN**

🎯 **О проекте:**
Самый точный бот для расчета персонального питания с точностью 95-99%

🚀 **Возможности:**
• 12-этапный детальный анализ
• Учет всех индивидуальных факторов
• Система достижений и мотивации
• Умные персональные рекомендации
• Экспорт результатов
• Поддержка двух языков

⚡ **Технологии:**
• Ультра-точные формулы расчета
• Адаптивное TDEE
• Мультиязычный интерфейс
• Система прогресса пользователя

📅 **Версия:** 4.0 Clean Edition
📊 **Точность:** 95-99%
🌟 **Создано:** С любовью к здоровому образу жизни
"""
    else:
        about_text = """
🔮 **FITADVENTURE BOT v4.0 CLEAN**

🎯 **About the project:**
The most accurate bot for personal nutrition calculation with 95-99% accuracy

🚀 **Features:**
• 12-step detailed analysis
• Consideration of all individual factors
• Achievement and motivation system
• Smart personal recommendations
• Results export
• Support for two languages

⚡ **Technologies:**
• Ultra-precise calculation formulas
• Adaptive TDEE
• Multilingual interface
• User progress system

📅 **Version:** 4.0 Clean Edition
📊 **Accuracy:** 95-99%
🌟 **Created:** With love for healthy lifestyle
"""
    
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню" if user_lang == 'ru' else "🏠 Main Menu", callback_data='main_menu')]
    ]
    
    await query.edit_message_text(
        about_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return MENU_STATE

async def show_user_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать достижения пользователя"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_lang = user_data_storage.get(chat_id, {}).get('language', 'ru')
    
    user_achievements = achievements_data.get(chat_id, {})
    
    if user_lang == 'ru':
        achievements_text = "🏆 **ВАШИ ДОСТИЖЕНИЯ**\n\n"
        
        if not any(user_achievements.values()):
            achievements_text += "😔 У вас пока нет достижений\n\nНачните анализ, чтобы получить первое достижение!"
        else:
            if user_achievements.get('started_survey'):
                achievements_text += "🌟 **Первые шаги** - Начали анализ здоровья\n"
            if user_achievements.get('completed_survey'):
                achievements_text += "🚀 **Исследователь** - Завершили полный опрос\n"
            if user_achievements.get('perfectionist'):
                achievements_text += "👑 **Перфекционист** - Получили точность 98%+\n"
            if user_achievements.get('fitness_expert'):
                achievements_text += "💪 **Фитнес-эксперт** - Продвинутые параметры\n"
            if user_achievements.get('health_enthusiast'):
                achievements_text += "❤️ **Энтузиаст здоровья** - Правильные привычки\n"
    else:
        achievements_text = "🏆 **YOUR ACHIEVEMENTS**\n\n"
        
        if not any(user_achievements.values()):
            achievements_text += "😔 You don't have any achievements yet\n\nStart the analysis to get your first achievement!"
        else:
            if user_achievements.get('started_survey'):
                achievements_text += "🌟 **First Steps** - Started health analysis\n"
            if user_achievements.get('completed_survey'):
                achievements_text += "🚀 **Explorer** - Completed full survey\n"
            if user_achievements.get('perfectionist'):
                achievements_text += "👑 **Perfectionist** - Achieved 98%+ accuracy\n"
            if user_achievements.get('fitness_expert'):
                achievements_text += "💪 **Fitness Expert** - Advanced parameters\n"
            if user_achievements.get('health_enthusiast'):
                achievements_text += "❤️ **Health Enthusiast** - Healthy habits\n"
    
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню" if user_lang == 'ru' else "🏠 Main Menu", callback_data='main_menu')]
    ]
    
    await query.edit_message_text(
        achievements_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return MENU_STATE

async def show_quick_tips(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать быстрые советы"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_lang = user_data_storage.get(chat_id, {}).get('language', 'ru')
    
    if user_lang == 'ru':
        tips_text = """
💡 **БЫСТРЫЕ СОВЕТЫ ПО ПИТАНИЮ**

🥗 **Основы здорового питания:**
• Пейте 2-3 литра воды в день
• Ешьте 4-5 раз в день небольшими порциями
• Включайте белки в каждый прием пищи
• Не пропускайте завтрак

🔥 **Для похудения:**
• Создайте дефицит калорий 10-20%
• Увеличьте потребление белка
• Ограничьте простые углеводы
• Добавьте кардио нагрузки

💪 **Для набора массы:**
• Увеличьте калорийность на 10-15%
• Ешьте каждые 3 часа
• Фокус на сложных углеводах
• Силовые тренировки 3-4 раза в неделю

⚡ **Общие советы:**
• Планируйте питание заранее
• Читайте состав продуктов
• Готовьте дома чаще
• Высыпайтесь 7-8 часов
"""
    else:
        tips_text = """
💡 **QUICK NUTRITION TIPS**

🥗 **Healthy eating basics:**
• Drink 2-3 liters of water daily
• Eat 4-5 times a day in small portions
• Include proteins in every meal
• Don't skip breakfast

🔥 **For weight loss:**
• Create 10-20% calorie deficit
• Increase protein intake
• Limit simple carbohydrates
• Add cardio workouts

💪 **For muscle gain:**
• Increase calories by 10-15%
• Eat every 3 hours
• Focus on complex carbohydrates
• Strength training 3-4 times a week

⚡ **General tips:**
• Plan your meals in advance
• Read product ingredients
• Cook at home more often
• Get 7-8 hours of sleep
"""
    
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню" if user_lang == 'ru' else "🏠 Main Menu", callback_data='main_menu')]
    ]
    
    await query.edit_message_text(
        tips_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return MENU_STATE

async def change_language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Меню смены языка"""
    query = update.callback_query
    await query.answer()
    
    language_text = """
🌍 **ВЫБОР ЯЗЫКА / LANGUAGE SELECTION**

Выберите предпочитаемый язык интерфейса
Choose your preferred interface language
"""
    
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='set_lang_ru')],
        [InlineKeyboardButton("🇺🇸 English", callback_data='set_lang_en')],
        [InlineKeyboardButton("🏠 Главное меню / Main Menu", callback_data='main_menu')]
    ]
    
    await query.edit_message_text(
        language_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return MENU_STATE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Установка языка"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    
    if query.data == 'set_lang_ru':
        if chat_id not in user_data_storage:
            user_data_storage[chat_id] = {}
        user_data_storage[chat_id]['language'] = 'ru'
        success_text = "✅ Язык изменен на русский"
    else:
        if chat_id not in user_data_storage:
            user_data_storage[chat_id] = {}
        user_data_storage[chat_id]['language'] = 'en'
        success_text = "✅ Language changed to English"
    
    await query.answer(success_text)
    return await show_main_menu(update, context)

# === МУЛЬТИЯЗЫЧНАЯ СТРУКТУРА ===
TEXTS = {
    'ru': {
        'welcome': "🎯 **Добро пожаловать в FitAdventure v4.0!**\n\nЯ помогу создать персональный план питания для достижения ваших целей.\n\n🚀 Готовы начать путь к телу мечты?",
        'choose_language': "🌍 **Выберите язык / Choose language:**",
        'language_set': "✅ Язык установлен: Русский",
        'start_journey': "🎯 **Начать путешествие**",
        'help_info': "ℹ️ **Подробнее**",
        'help_button': "❓ **Помощь**",
        'settings': "⚙️ **Настройки**",
        'stage_titles': {
            'gender': "👤 **Этап 1/12:** Ваш пол?",
            'age': "🎂 **Этап 2/12:** Ваш возраст?",
            'weight': "⚖️ **Этап 3/12:** Ваш вес (кг)?",
            'height': "📏 **Этап 4/12:** Ваш рост (см)?",
            'fat': "🔥 **Этап 5/12:** Знаете ли вы процент жира?",
            'goal': "🎯 **Этап 6/12:** Ваша цель?",
            'experience': "💪 **Этап 7/12:** Опыт тренировок?",
            'activity': "🏃 **Этап 8/12:** Детали активности",
            'intensity': "🔥 **Этап 9/12:** Интенсивность тренировок?",
            'recovery': "😴 **Этап 10/12:** Качество восстановления?",
            'sleep': "🌙 **Этап 11/12:** Качество сна?",
            'lifestyle': "💼 **Этап 12/12:** Образ жизни"
        },
        'buttons': {
            'male': "👨 Мужчина",
            'female': "👩 Женщина",
            'know_fat': "✅ Да, знаю",
            'dont_know_fat': "❌ Не знаю",
            'goal_loss': "📉 Похудение",
            'goal_maintain': "⚖️ Поддержание",
            'goal_gain': "📈 Набор массы",
            'exp_beginner': "🌱 Новичок",
            'exp_intermediate': "🔥 Средний",
            'exp_advanced': "⚡ Опытный",
            'activity_strength': "🏋️ Силовые",
            'activity_cardio': "🏃 Выносливость",
            'activity_crossfit': "⚡ Кроссфит",
            'intensity_low': "🟢 Низкая",
            'intensity_moderate': "🟡 Средняя",
            'intensity_high': "🔴 Высокая",
            'intensity_very_high': "⚡ Очень высокая",
            'recovery_excellent': "⭐ Отлично",
            'recovery_good': "✅ Хорошо",
            'recovery_average': "🔶 Средне",
            'recovery_poor': "❌ Плохо",
            'sleep_excellent': "😴 Отлично (8+ ч)",
            'sleep_good': "😊 Хорошо (7-8 ч)",
            'sleep_average': "😐 Средне (6-7 ч)",
            'sleep_poor': "😞 Плохо (<6 ч)",
            'stress_low': "😌 Низкий",
            'stress_medium': "😐 Средний",
            'stress_high': "😰 Высокий",
            'occupation_office': "💻 Офисная работа",
            'occupation_active': "🏃 Активная работа",
            'occupation_physical': "💪 Физический труд"
        },
        'result_title': "🎉 **Ваш ультра-точный план питания готов!**",
        'calculating': "🧠 Выполняю ультра-точные расчеты с учетом всех факторов...",
        'precision_info': "🎯 **Точность расчета:** {precision}%",
        'error_invalid': "❌ Пожалуйста, введите корректное значение",
        'canceled': "❌ Анализ отменен",
        'help_text': "📚 **Справка FitAdventure v4.0**\n\n🎯 Этот бот поможет рассчитать персональный план питания\n\n📊 Мы учитываем:\n• Ваши физические параметры\n• Цели и опыт тренировок\n• Уровень активности\n• Процент жира в организме\n• Качество сна и восстановления\n• Уровень стресса\n• Тип профессиональной деятельности\n\n✨ Получите точные рекомендации с точностью 95-99%!"
    },
    'en': {
        'welcome': "🎯 **Welcome to FitAdventure v4.0!**\n\nI'll help create a personalized nutrition plan to achieve your goals.\n\n🚀 Ready to start your journey to your dream body?",
        'choose_language': "🌍 **Choose language / Выберите язык:**",
        'language_set': "✅ Language set: English",
        'start_journey': "🎯 **Start Journey**",
        'help_info': "ℹ️ **More Info**",
        'help_button': "❓ **Help**",
        'settings': "⚙️ **Settings**",
        'stage_titles': {
            'gender': "👤 **Step 1/12:** Your gender?",
            'age': "🎂 **Step 2/12:** Your age?",
            'weight': "⚖️ **Step 3/12:** Your weight (kg)?",
            'height': "📏 **Step 4/12:** Your height (cm)?",
            'fat': "🔥 **Step 5/12:** Do you know your body fat %?",
            'goal': "🎯 **Step 6/12:** Your goal?",
            'experience': "💪 **Step 7/12:** Training experience?",
            'activity': "🏃 **Step 8/12:** Activity details",
            'intensity': "🔥 **Step 9/12:** Training intensity?",
            'recovery': "😴 **Step 10/12:** Recovery quality?",
            'sleep': "🌙 **Step 11/12:** Sleep quality?",
            'lifestyle': "💼 **Step 12/12:** Lifestyle"
        },
        'buttons': {
            'male': "👨 Male",
            'female': "👩 Female",
            'know_fat': "✅ Yes, I know",
            'dont_know_fat': "❌ Don't know",
            'goal_loss': "📉 Weight Loss",
            'goal_maintain': "⚖️ Maintenance",
            'goal_gain': "📈 Muscle Gain",
            'exp_beginner': "🌱 Beginner",
            'exp_intermediate': "🔥 Intermediate",
            'exp_advanced': "⚡ Advanced",
            'activity_strength': "🏋️ Strength",
            'activity_cardio': "🏃 Cardio",
            'activity_crossfit': "⚡ CrossFit",
            'intensity_low': "🟢 Low",
            'intensity_moderate': "🟡 Moderate",
            'intensity_high': "🔴 High",
            'intensity_very_high': "⚡ Very High",
            'recovery_excellent': "⭐ Excellent",
            'recovery_good': "✅ Good",
            'recovery_average': "🔶 Average",
            'recovery_poor': "❌ Poor",
            'sleep_excellent': "😴 Excellent (8+ h)",
            'sleep_good': "😊 Good (7-8 h)",
            'sleep_average': "😐 Average (6-7 h)",
            'sleep_poor': "😞 Poor (<6 h)",
            'stress_low': "😌 Low",
            'stress_medium': "😐 Medium",
            'stress_high': "😰 High",
            'occupation_office': "💻 Office work",
            'occupation_active': "🏃 Active work",
            'occupation_physical': "💪 Physical work"
        },
        'result_title': "🎉 **Your ultra-precise nutrition plan is ready!**",
        'calculating': "🧠 Performing ultra-precise calculations with all factors...",
        'precision_info': "🎯 **Calculation Accuracy:** {precision}%",
        'error_invalid': "❌ Please enter a valid value",
        'canceled': "❌ Analysis canceled",
        'help_text': "📚 **FitAdventure v4.0 Help**\n\n🎯 This bot helps calculate personalized nutrition plans\n\n📊 We consider:\n• Your physical parameters\n• Goals and training experience\n• Activity level\n• Body fat percentage\n• Sleep and recovery quality\n• Stress levels\n• Professional activity type\n\n✨ Get precise recommendations with 95-99% accuracy!"
    }
}

def get_text(user_id: int, key: str) -> str:
    """Получить текст на языке пользователя"""
    user_lang = user_data_storage.get(user_id, {}).get('language', 'ru')
    return TEXTS[user_lang].get(key, TEXTS['ru'].get(key, ""))

# === ОБРАБОТЧИКИ КОМАНД ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Стартовая команда с выбором языка"""
    chat_id = update.message.chat_id
    user_data_storage[chat_id] = {}
    
    # Проверка достижений
    new_achievements = check_achievements(chat_id, "start_survey")
    achievement_text = format_achievement_notification(new_achievements)
    
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("🇺🇸 English", callback_data='lang_en')]
    ]
    
    await update.message.reply_text(
        "🌍 **Выберите язык / Choose language:**" + achievement_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return LANGUAGE_CHOICE

async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора языка"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    if query.data == 'lang_ru':
        user_data_storage[chat_id]['language'] = 'ru'
        lang_text = "✅ Язык установлен: Русский"
    else:
        user_data_storage[chat_id]['language'] = 'en'
        lang_text = "✅ Language set: English"
    
    await query.answer(lang_text)
    return await show_main_menu(update, context)

async def start_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало анализа"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    save_user_progress(chat_id, 1)
    progress = create_clean_progress(1, 12)
    stage_text = get_text(chat_id, 'stage_titles')['gender']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['male'], callback_data='мужчина')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['female'], callback_data='женщина')]
    ]
    
    await query.edit_message_text(
        f"{progress}\n\n{stage_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора пола"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['gender'] = query.data
    save_user_progress(chat_id, 2)
    
    progress = create_clean_progress(2, 12)
    stage_text = get_text(chat_id, 'stage_titles')['age']
    
    await query.edit_message_text(
        f"{progress}\n\n{stage_text}",
        parse_mode=ParseMode.MARKDOWN
    )
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка возраста"""
    try:
        age_value = int(update.message.text)
        if not (10 <= age_value <= 100):
            raise ValueError
    except ValueError:
        await update.message.reply_text(get_text(update.message.chat_id, 'error_invalid'))
        return AGE
    
    chat_id = update.message.chat_id
    user_data_storage[chat_id]['age'] = age_value
    save_user_progress(chat_id, 3)
    
    # Возрастная реакция
    if age_value < 20:
        reaction = "🌱 Молодость - время формировать правильные привычки!"
    elif age_value > 50:
        reaction = "👑 Опыт - ваше преимущество в достижении целей!"
    else:
        reaction = "💪 Отличный возраст для активных изменений!"
    
    progress = create_clean_progress(3, 12)
    stage_text = get_text(chat_id, 'stage_titles')['weight']
    
    await update.message.reply_text(
        f"{reaction}\n\n{progress}\n\n{stage_text}",
        parse_mode=ParseMode.MARKDOWN
    )
    return WEIGHT

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка веса"""
    try:
        weight_value = float(update.message.text)
        if not (30 <= weight_value <= 300):
            raise ValueError
    except ValueError:
        await update.message.reply_text(get_text(update.message.chat_id, 'error_invalid'))
        return WEIGHT
    
    chat_id = update.message.chat_id
    user_data_storage[chat_id]['weight'] = weight_value
    save_user_progress(chat_id, 4)
    
    progress = create_clean_progress(4, 12)
    stage_text = get_text(chat_id, 'stage_titles')['height']
    
    await update.message.reply_text(
        f"{progress}\n\n{stage_text}",
        parse_mode=ParseMode.MARKDOWN
    )
    return HEIGHT

async def height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка роста"""
    try:
        height_value = float(update.message.text)
        if not (100 <= height_value <= 250):
            raise ValueError
    except ValueError:
        await update.message.reply_text(get_text(update.message.chat_id, 'error_invalid'))
        return HEIGHT
    
    chat_id = update.message.chat_id
    user_data_storage[chat_id]['height'] = height_value
    save_user_progress(chat_id, 5)
    
    progress = create_clean_progress(5, 12)
    stage_text = get_text(chat_id, 'stage_titles')['fat']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['know_fat'], callback_data='know_fat')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['dont_know_fat'], callback_data='dont_know_fat')]
    ]
    
    await update.message.reply_text(
        f"{progress}\n\n{stage_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return FAT_PERCENTAGE

async def fat_percentage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка знания процента жира"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    
    if query.data == 'know_fat':
        await query.edit_message_text("🔥 Введите процент жира (5-50%):")
        return FAT_PERCENTAGE_INPUT
    else:
        user_data_storage[chat_id]['fat_percent'] = None
        return await show_goal_selection(query, chat_id)

async def fat_percentage_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода процента жира"""
    try:
        fat_value = float(update.message.text)
        if not (5 <= fat_value <= 50):
            raise ValueError
    except ValueError:
        await update.message.reply_text(get_text(update.message.chat_id, 'error_invalid'))
        return FAT_PERCENTAGE_INPUT
    
    chat_id = update.message.chat_id
    user_data_storage[chat_id]['fat_percent'] = fat_value
    
    return await show_goal_selection_text(update, chat_id)

async def show_goal_selection(query, chat_id) -> int:
    """Показать выбор цели (callback)"""
    save_user_progress(chat_id, 6)
    progress = create_clean_progress(6, 12)
    stage_text = get_text(chat_id, 'stage_titles')['goal']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['goal_loss'], callback_data='Похудение')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['goal_maintain'], callback_data='Поддержание')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['goal_gain'], callback_data='Набор массы')]
    ]
    
    await query.edit_message_text(
        f"{progress}\n\n{stage_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return GOAL

async def show_goal_selection_text(update, chat_id) -> int:
    """Показать выбор цели (text)"""
    save_user_progress(chat_id, 6)
    progress = create_clean_progress(6, 12)
    stage_text = get_text(chat_id, 'stage_titles')['goal']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['goal_loss'], callback_data='Похудение')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['goal_maintain'], callback_data='Поддержание')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['goal_gain'], callback_data='Набор массы')]
    ]
    
    await update.message.reply_text(
        f"{progress}\n\n{stage_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return GOAL

async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора цели"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['goal'] = query.data
    save_user_progress(chat_id, 7)
    
    progress = create_clean_progress(7, 12)
    stage_text = get_text(chat_id, 'stage_titles')['experience']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['exp_beginner'], callback_data='Новичок')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['exp_intermediate'], callback_data='Средний')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['exp_advanced'], callback_data='Опытный')]
    ]
    
    await query.edit_message_text(
        f"{progress}\n\n{stage_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return TRAINING_EXPERIENCE

async def training_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка опыта тренировок"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['training_experience'] = query.data
    save_user_progress(chat_id, 8)
    
    progress = create_clean_progress(8, 12)
    
    keyboard = [
        [InlineKeyboardButton("1 день", callback_data='1'),
         InlineKeyboardButton("2 дня", callback_data='2'),
         InlineKeyboardButton("3 дня", callback_data='3')],
        [InlineKeyboardButton("4 дня", callback_data='4'),
         InlineKeyboardButton("5 дней", callback_data='5'),
         InlineKeyboardButton("6 дней", callback_data='6')]
    ]
    
    await query.edit_message_text(
        f"{progress}\n\n🏃 **Сколько дней в неделю тренируетесь?**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return TRAINING_DAYS

async def training_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка дней тренировок"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['training_days'] = int(query.data)
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['activity_strength'], callback_data='Силовые')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['activity_cardio'], callback_data='Выносливость')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['activity_crossfit'], callback_data='Кроссфит')]
    ]
    
    await query.edit_message_text(
        "💪 **Тип тренировок?**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return ACTIVITY_TYPE

async def activity_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка типа активности"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['activity_type'] = query.data
    
    await query.edit_message_text(
        "⏱️ **Продолжительность одной тренировки (минуты)?**",
        parse_mode=ParseMode.MARKDOWN
    )
    return WORKOUT_DURATION

async def workout_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка продолжительности тренировки"""
    try:
        duration = int(update.message.text)
        if not (15 <= duration <= 300):
            raise ValueError
    except ValueError:
        await update.message.reply_text(get_text(update.message.chat_id, 'error_invalid'))
        return WORKOUT_DURATION
    
    chat_id = update.message.chat_id
    user_data_storage[chat_id]['workout_duration'] = duration
    
    await update.message.reply_text(
        "🚶 **Количество шагов в день (примерно)?**",
        parse_mode=ParseMode.MARKDOWN
    )
    return STEPS

async def steps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка шагов"""
    try:
        steps_count = int(update.message.text)
        if not (1000 <= steps_count <= 50000):
            raise ValueError
    except ValueError:
        await update.message.reply_text(get_text(update.message.chat_id, 'error_invalid'))
        return STEPS
    
    chat_id = update.message.chat_id
    user_data_storage[chat_id]['steps'] = steps_count
    save_user_progress(chat_id, 9)
    
    progress = create_clean_progress(9, 12)
    stage_text = get_text(chat_id, 'stage_titles')['intensity']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['intensity_low'], callback_data='low')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['intensity_moderate'], callback_data='moderate')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['intensity_high'], callback_data='high')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['intensity_very_high'], callback_data='very_high')]
    ]
    
    await update.message.reply_text(
        f"{progress}\n\n{stage_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return INTENSITY

async def intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка интенсивности"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['intensity'] = query.data
    save_user_progress(chat_id, 10)
    
    progress = create_clean_progress(10, 12)
    stage_text = get_text(chat_id, 'stage_titles')['recovery']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['recovery_excellent'], callback_data='excellent')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['recovery_good'], callback_data='good')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['recovery_average'], callback_data='average')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['recovery_poor'], callback_data='poor')]
    ]
    
    await query.edit_message_text(
        f"{progress}\n\n{stage_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return RECOVERY

async def recovery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка восстановления"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['recovery'] = query.data
    save_user_progress(chat_id, 11)
    
    progress = create_clean_progress(11, 12)
    stage_text = get_text(chat_id, 'stage_titles')['sleep']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['sleep_excellent'], callback_data='excellent')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['sleep_good'], callback_data='good')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['sleep_average'], callback_data='average')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['sleep_poor'], callback_data='poor')]
    ]
    
    await query.edit_message_text(
        f"{progress}\n\n{stage_text}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return SLEEP_QUALITY

async def sleep_quality(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка сна"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['sleep_quality'] = query.data
    save_user_progress(chat_id, 12)
    
    progress = create_clean_progress(12, 12)
    stage_text = get_text(chat_id, 'stage_titles')['lifestyle']
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['stress_low'], callback_data='2')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['stress_medium'], callback_data='5')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['stress_high'], callback_data='8')]
    ]
    
    await query.edit_message_text(
        f"{progress}\n\n💆 **Уровень стресса в жизни?**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return STRESS_LEVEL

async def stress_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка стресса"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['stress_level'] = int(query.data)
    
    keyboard = [
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['occupation_office'], callback_data='office')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['occupation_active'], callback_data='healthcare')],
        [InlineKeyboardButton(get_text(chat_id, 'buttons')['occupation_physical'], callback_data='construction')]
    ]
    
    await query.edit_message_text(
        "💼 **Тип работы?**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return OCCUPATION

async def occupation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Финальная обработка и расчет"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data_storage[chat_id]['occupation'] = query.data
    user_data_storage[chat_id]['user_id'] = str(chat_id)
    
    # Проверяем достижения
    new_achievements = check_achievements(chat_id, "complete_survey")
    
    # Показываем процесс расчета
    calculating_msg = await query.edit_message_text(
        get_text(chat_id, 'calculating'),
        parse_mode=ParseMode.MARKDOWN
    )
    
    try:
        # Генерируем результаты
        results = generate_maximum_precision_recommendations(user_data_storage[chat_id])
        
        # Проверяем достижение высокой точности
        precision_achievements = check_achievements(chat_id, "high_precision", results['precision_score'])
        all_achievements = new_achievements + precision_achievements
        
        # Генерируем персонализированное поздравление
        celebration = generate_personalized_celebration(user_data_storage[chat_id])
        
        # Генерируем умные рекомендации
        smart_tips = generate_smart_tips(user_data_storage[chat_id])
        tips_text = format_smart_tips(smart_tips)
        
        # Форматируем достижения
        achievement_text = format_achievement_notification(all_achievements)
        
        # Создаем резюме для экспорта
        summary = create_result_summary(user_data_storage[chat_id], results)
        
        # Финальное сообщение с результатами
        result_title = get_text(chat_id, 'result_title')
        precision_info = get_text(chat_id, 'precision_info').format(precision=results['precision_score'])
        
        final_message = f"""{result_title}

{celebration}

{precision_info}

🔥 **Целевые калории:** {results['target_calories']} ккал
🥩 **Белки:** {results['protein_min']}-{results['protein_max']} г
🥑 **Жиры:** {results['fats']} г  
🍞 **Углеводы:** {results['carbs']} г
🌾 **Клетчатка:** {results['fiber']} г

📊 **Детальная разбивка:**
• TDEE: {results['tdee']} ккал
• BMR: {results['bmr']} ккал  
• NEAT: {results['neat']} ккал
• EAT: {results['eat']} ккал
• TEF: {results['tef']} ккал
• LBM: {results['lbm']} кг

{tips_text}{achievement_text}

✨ Расчеты учитывают ВСЕ индивидуальные факторы для максимальной точности!"""
        
        # Добавляем кнопку возврата в меню
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')],
            [InlineKeyboardButton("📊 Экспорт результатов", callback_data='export_results')]
        ]
        
        await calculating_msg.edit_text(
            final_message, 
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Отправляем резюме как отдельное сообщение при запросе экспорта
        if chat_id not in user_data_storage:
            user_data_storage[chat_id] = {}
        user_data_storage[chat_id]['last_results'] = summary
        
    except Exception as e:
        await calculating_msg.edit_text(f"❌ Ошибка расчета: {str(e)}")
        logger.error(f"Calculation error: {e}")
    
    return MENU_STATE

async def export_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Экспорт результатов"""
    query = update.callback_query
    await query.answer("📋 Подготавливаю экспорт результатов...")
    
    chat_id = query.message.chat_id
    summary = user_data_storage.get(chat_id, {}).get('last_results', "Результаты не найдены")
    
    await query.message.reply_text(
        f"📋 **ЭКСПОРТ РЕЗУЛЬТАТОВ:**\n```\n{summary}\n```",
        parse_mode=ParseMode.MARKDOWN
    )
    
    return MENU_STATE

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать меню настроек"""
    query = update.callback_query
    await query.answer("🔮 Открываем настройки!")
    
    chat_id = query.message.chat_id
    current_theme = get_user_theme(chat_id)
    user_lang = user_data_storage.get(chat_id, {}).get('language', 'ru')
    
    if user_lang == 'ru':
        settings_text = f"""
⚙️ **НАСТРОЙКИ FITADVENTURE v4.0**

🎨 **Текущая тема:** {current_theme}
📊 **Стиль прогресс-баров**
🎯 **Персонализация интерфейса**

Выберите новую тему оформления:
"""
        keyboard = [
            [InlineKeyboardButton("🎨 Классический", callback_data='theme_default')],
            [InlineKeyboardButton("🌟 Градиентный", callback_data='theme_gradient')],
            [InlineKeyboardButton("🔥 Огненный", callback_data='theme_fire')],
            [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
        ]
    else:
        settings_text = f"""
⚙️ **FITADVENTURE v4.0 SETTINGS**

🎨 **Current theme:** {current_theme}
📊 **Progress bar style**
🎯 **Interface personalization**

Choose a new design theme:
"""
        keyboard = [
            [InlineKeyboardButton("🎨 Classic", callback_data='theme_default')],
            [InlineKeyboardButton("🌟 Gradient", callback_data='theme_gradient')],
            [InlineKeyboardButton("🔥 Fire", callback_data='theme_fire')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
    
    await query.edit_message_text(
        settings_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return USER_SETTINGS

async def change_theme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Смена темы"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    theme = query.data.replace('theme_', '')
    set_user_theme(chat_id, theme)
    
    # Демонстрация новой темы
    demo_progress = create_clean_progress(8, 12)
    
    keyboard = [
        [InlineKeyboardButton("✅ Применить", callback_data='main_menu')],
        [InlineKeyboardButton("🎨 Другая тема", callback_data='show_settings')]
    ]
    
    theme_names = {
        'default': 'Классический',
        'gradient': 'Градиентный', 
        'fire': 'Огненный'
    }
    
    await query.edit_message_text(
        f"🎨 **Тема изменена на:** {theme_names.get(theme, theme)}\n\n**Демонстрация:**\n{demo_progress}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return USER_SETTINGS

async def help_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Подробная информация"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    help_text = get_text(chat_id, 'help_text')
    
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
    ]
    
    await query.edit_message_text(
        help_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    return MENU_STATE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена анализа"""
    chat_id = update.message.chat_id
    await update.message.reply_text(
        get_text(chat_id, 'canceled'),
        reply_markup=ReplyKeyboardRemove()
    )
    if chat_id in user_data_storage:
        del user_data_storage[chat_id]
    return ConversationHandler.END

# === НОВЫЕ КОМАНДЫ ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await show_main_menu(update, context)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /info - краткая информация о боте"""
    info_text = """
🤖 **FitAdventure Bot v4.0 Clean**

🎯 **Быстрые команды:**
/start - Начать работу с ботом
/menu - Показать главное меню
/help - Помощь и навигация
/info - Информация о боте
/cancel - Отменить текущее действие

💡 **Возможности:**
• Персональные планы питания
• Точность расчетов 95-99%
• Система достижений
• Умные рекомендации
• Поддержка русского и английского языков

📱 Используйте /menu для доступа ко всем функциям!
"""
    
    await update.message.reply_text(info_text, parse_mode=ParseMode.MARKDOWN)

def main() -> None:
    """Главная функция запуска бота"""
    print("🚀 Запуск FitAdventure Bot v4.0 Clean with Menu...")
    
    # Автоматическая настройка токена
    try:
        TOKEN = setup_bot_token()
        print(f"✅ Токен получен успешно!")
    except KeyboardInterrupt:
        print("\n❌ Настройка отменена пользователем")
        return
    except Exception as e:
        print(f"❌ Ошибка настройки токена: {e}")
        return
        
    # Создание приложения бота
    try:
        application = Application.builder().token(TOKEN).build()
        print("✅ Telegram Application создан успешно!")
    except Exception as e:
        print(f"❌ Ошибка создания приложения: {e}")
        return
    
    # Настройка команд бота
    async def set_bot_commands():
        commands = [
            BotCommand("start", "🚀 Начать работу с ботом"),
            BotCommand("menu", "📋 Главное меню"),
            BotCommand("help", "❓ Помощь и навигация"),
            BotCommand("info", "ℹ️ Информация о боте"),
            BotCommand("cancel", "❌ Отменить действие")
        ]
        await application.bot.set_my_commands(commands)
    
    # Настройка ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE_CHOICE: [
                CallbackQueryHandler(language_choice, pattern='^lang_'),
                CallbackQueryHandler(show_main_menu, pattern='^main_menu$'),
            ],
            MENU_STATE: [
                CallbackQueryHandler(start_analysis, pattern='^start_analysis$'),
                CallbackQueryHandler(show_settings, pattern='^show_settings$'),
                CallbackQueryHandler(about_bot, pattern='^about_bot$'),
                CallbackQueryHandler(show_user_achievements, pattern='^show_achievements$'),
                CallbackQueryHandler(show_quick_tips, pattern='^show_tips$'),
                CallbackQueryHandler(change_language_menu, pattern='^change_language$'),
                CallbackQueryHandler(help_info, pattern='^help_info$'),
                CallbackQueryHandler(show_main_menu, pattern='^main_menu$'),
                CallbackQueryHandler(set_language, pattern='^set_lang_'),
                CallbackQueryHandler(export_results, pattern='^export_results$'),
            ],
            GENDER: [CallbackQueryHandler(gender)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weight)],
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, height)],
            FAT_PERCENTAGE: [CallbackQueryHandler(fat_percentage)],
            FAT_PERCENTAGE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, fat_percentage_input)],
            GOAL: [CallbackQueryHandler(goal)],
            TRAINING_EXPERIENCE: [CallbackQueryHandler(training_experience)],
            TRAINING_DAYS: [CallbackQueryHandler(training_days)],
            ACTIVITY_TYPE: [CallbackQueryHandler(activity_type)],
            WORKOUT_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, workout_duration)],
            STEPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, steps)],
            INTENSITY: [CallbackQueryHandler(intensity)],
            RECOVERY: [CallbackQueryHandler(recovery)],
            SLEEP_QUALITY: [CallbackQueryHandler(sleep_quality)],
            STRESS_LEVEL: [CallbackQueryHandler(stress_level)],
            OCCUPATION: [CallbackQueryHandler(occupation)],
            USER_SETTINGS: [
                CallbackQueryHandler(change_theme, pattern='^theme_'),
                CallbackQueryHandler(show_settings, pattern='^show_settings$'),
                CallbackQueryHandler(show_main_menu, pattern='^main_menu$')
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
    )

    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('menu', menu_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('info', info_command))
    
    # Устанавливаем команды бота
    application.job_queue.run_once(lambda context: set_bot_commands(), 0)
    
    logger.info("🎯 FitAdventure Bot v4.0 Clean with Menu запущен!")
    logger.info("📋 Система меню активирована")
    logger.info("✅ Все системы готовы к работе")
    print("\n🎯 FitAdventure Bot v4.0 Clean with Menu запущен успешно!")
    print("📋 Доступные команды: /start, /menu, /help, /info, /cancel")
    print("📱 Откройте Telegram и найдите своего бота")
    print("⌨️ Нажмите Ctrl+C для остановки")
    
    try:
        application.run_polling()
    except KeyboardInterrupt:
        print("\n✅ Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка работы бота: {e}")

if __name__ == '__main__':
    main() 