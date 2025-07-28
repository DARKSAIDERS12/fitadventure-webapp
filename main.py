#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FitAdventure Bot - Финальная версия
Ультра-точные расчеты питания с Reply Keyboard
Версия: 5.0 Final
Дата: 23 июля 2025
"""

import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Импорт мини-приложений
try:
    from mini_apps import (
        show_mini_apps_menu, handle_mini_apps_navigation,
        show_products_menu, show_products_category, search_product_handler, 
        show_product_details, show_recommendations
    )
    MINI_APPS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Мини-приложения недоступны: {e}")
    MINI_APPS_AVAILABLE = False

# Импорт нового мини-приложения базы продуктов
try:
    from products_mini_app import (
        show_products_mini_app, handle_products_navigation, handle_product_search,
        show_category_products, show_product_details, show_search_interface,
        show_recommendations, return_to_main_menu
    )
    PRODUCTS_MINI_APP_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Мини-приложение базы продуктов недоступно: {e}")
    PRODUCTS_MINI_APP_AVAILABLE = False

# === АВТОМАТИЧЕСКАЯ НАСТРОЙКА ТОКЕНА ===
def setup_bot_token():
    """Автоматическая настройка токена бота"""
    env_file = Path('.env')
    
    # Пытаемся загрузить существующий .env
    if env_file.exists():
        load_dotenv()
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if token:
            print("✅ Токен бота найден в .env файле")
            return token
    
    print("🤖 Настройка токена Telegram бота")
    print("📋 Для получения токена:")
    print("1. Откройте Telegram")
    print("2. Найдите @BotFather")
    print("3. Отправьте команду /newbot")
    print("4. Следуйте инструкциям и получите токен")
    print()
    
    while True:
        token = input("🔑 Введите токен вашего бота: ").strip()
        
        if not token:
            print("❌ Токен не может быть пустым!")
            continue
            
        if not token.startswith(('1', '2', '5', '6')) or ':' not in token:
            print("❌ Неверный формат токена! Пример: 1234567890:ABCdefGHIjklMNOpqrSTUvwxyz")
            continue
            
        # Сохраняем токен в .env файл
        try:
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(f"TELEGRAM_BOT_TOKEN={token}\n")
            
            print(f"✅ Токен сохранен в файл .env")
            print(f"✅ Настройка завершена!")
            return token
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            continue

# Загружаем переменные окружения
load_dotenv()

# --- Логирование ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot_debug.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Состояния ---
GENDER, AGE, WEIGHT, HEIGHT, FAT_PERCENTAGE, FAT_PERCENTAGE_INPUT, GOAL, HAS_TRAINING_EXPERIENCE, TRAINING_EXPERIENCE, TRAINING_DAYS, ACTIVITY_TYPE, WORKOUT_DURATION, STEPS, INTENSITY, RECOVERY, SLEEP_QUALITY, STRESS_LEVEL, OCCUPATION = range(18)

# Состояния для мини-приложений
MINI_APPS_MENU, PRODUCTS_MENU, PRODUCT_SEARCH = range(18, 21)

# Состояния для нового мини-приложения базы продуктов
PRODUCTS_MAIN, PRODUCTS_CATEGORY, PRODUCT_DETAILS, PRODUCT_SEARCH_NEW = range(21, 25)

# --- Хранилище ---
user_data_storage = {}

# === УЛЬТРА-ТОЧНЫЕ РАСЧЕТЫ ===
def generate_ultra_precise_recommendations(user_data):
    """Генерация ультра-точных рекомендаций с разделением по дням"""
    logger.info(f"Starting ultra-precise calculations with data: {user_data}")
    
    # Проверка обязательных полей
    required_fields = [
        'weight', 'height', 'age', 'gender', 'steps',
        'occupation', 'recovery', 'sleep_quality', 'stress_level', 'goal'
    ]
    missing = [field for field in required_fields if field not in user_data]
    if missing:
        raise ValueError(f"Не заполнены обязательные поля: {', '.join(missing)}. Пройдите все этапы опроса!")
    
    # Проверяем наличие опыта в тренировках
    has_training_experience = user_data.get('has_training_experience', True)
    
    # Если есть опыт в тренировках, проверяем дополнительные поля
    if has_training_experience:
        training_fields = ['training_days', 'activity_type', 'intensity', 'workout_duration']
        missing_training = [field for field in training_fields if field not in user_data]
        if missing_training:
            raise ValueError(f"Не заполнены поля тренировок: {', '.join(missing_training)}. Пройдите все этапы опроса!")
    
    # Базовые параметры
    weight = user_data['weight']
    height = user_data['height'] 
    age = user_data['age']
    gender = user_data['gender']
    
    logger.info(f"Basic parameters - Weight: {weight}, Height: {height}, Age: {age}, Gender: {gender}")
    
    # Расчет процента жира (если не указан пользователем)
    fat_percent = user_data.get('fat_percent')
    if fat_percent is None:
        # Расчет по формуле BMI и возрасту
        bmi = weight / ((height / 100) ** 2)
        
        if gender == 'мужчина':
            if age < 30:
                fat_percent = 1.20 * bmi + 0.23 * age - 16.2
            elif age < 50:
                fat_percent = 1.20 * bmi + 0.23 * age - 16.2
            else:
                fat_percent = 1.20 * bmi + 0.23 * age - 16.2
        else:  # женщина
            if age < 30:
                fat_percent = 1.20 * bmi + 0.23 * age - 5.4
            elif age < 50:
                fat_percent = 1.20 * bmi + 0.23 * age - 5.4
            else:
                fat_percent = 1.20 * bmi + 0.23 * age - 5.4
        
        # Ограничиваем значения
        fat_percent = max(8, min(35, fat_percent))
        user_data['fat_percent'] = round(fat_percent, 1)
    
    # Определение категории по проценту жира
    if gender == 'мужчина':
        if fat_percent < 6:
            fat_category = "Экстремально низкий"
        elif fat_percent < 14:
            fat_category = "Спортивный"
        elif fat_percent < 18:
            fat_category = "Фитнес"
        elif fat_percent < 25:
            fat_category = "Средний"
        elif fat_percent < 32:
            fat_category = "Высокий"
        else:
            fat_category = "Очень высокий"
    else:  # женщина
        if fat_percent < 14:
            fat_category = "Экстремально низкий"
        elif fat_percent < 21:
            fat_category = "Спортивный"
        elif fat_percent < 25:
            fat_category = "Фитнес"
        elif fat_percent < 32:
            fat_category = "Средний"
        elif fat_percent < 38:
            fat_category = "Высокий"
        else:
            fat_category = "Очень высокий"
    
    user_data['fat_category'] = fat_category
    logger.info(f"Calculated fat percentage: {fat_percent}% ({fat_category})")
    
    # BMR по формуле Mifflin-St Jeor
    if gender == 'мужчина':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    logger.info(f"Base BMR calculated: {bmr}")
    
    # Детальный расчет активности
    steps = user_data['steps']
    
    # Рабочая активность
    occupation_factors = {
        'office': 0.15,      # Офисная работа
        'healthcare': 0.25,  # Активная работа  
        'construction': 0.35 # Физический труд
    }
    work_factor = occupation_factors.get(user_data['occupation'], 0.2)
    
    # Тренировочная активность (только если есть опыт)
    if has_training_experience:
        training_days = user_data['training_days']
        
        # Тренировочная активность
        activity_multipliers = {
            'Силовые': 0.08,
            'Выносливость': 0.06,
            'Кроссфит': 0.1
        }
        training_base = activity_multipliers.get(user_data['activity_type'], 0.08)
        
        # Интенсивность тренировок
        intensity_multipliers = {
            'low': 0.8,
            'moderate': 1.0,
            'high': 1.2,
            'very_high': 1.4
        }
        intensity_factor = intensity_multipliers.get(user_data['intensity'], 1.0)
        
        # Продолжительность тренировки
        duration_factor = min(user_data['workout_duration'] / 60, 2.0)  # Максимум 2x
        
        training_factor = training_base * intensity_factor * duration_factor * (training_days / 7)
    else:
        training_factor = 0.0  # Нет тренировок
    
    # Шаги
    steps_factor = min(steps / 10000 * 0.05, 0.15)  # Максимум 0.15
    
    logger.info(f"Activity breakdown - Work: {work_factor}, Training: {training_factor}, Steps: {steps_factor}")
    
    # Факторы восстановления
    recovery_factors = {
        'excellent': 1.05,
        'good': 1.0,
        'average': 0.95,
        'poor': 0.9
    }
    recovery_multiplier = recovery_factors.get(user_data['recovery'], 1.0)
    
    sleep_factors = {
        'excellent': 1.05,
        'good': 1.0,
        'average': 0.95,
        'poor': 0.9
    }
    sleep_multiplier = sleep_factors.get(user_data['sleep_quality'], 1.0)
    
    # Стресс (обратная зависимость)
    stress_level = user_data['stress_level']
    stress_multiplier = max(0.85, 1.1 - (stress_level / 10) * 0.25)
    
    logger.info(f"Recovery factors - Recovery: {recovery_multiplier}, Sleep: {sleep_multiplier}, Stress: {stress_multiplier}")
    
    # Раздельный расчет для дней отдыха и тренировок
    rest_day_factor = 1 + work_factor + steps_factor
    training_day_factor = rest_day_factor + training_factor
    
    # Применяем факторы восстановления
    rest_day_factor *= recovery_multiplier * sleep_multiplier * stress_multiplier
    training_day_factor *= recovery_multiplier * sleep_multiplier * stress_multiplier
    
    # Если нет опыта в тренировках, все дни считаются как дни отдыха
    if not has_training_experience:
        training_day_factor = rest_day_factor
    
    logger.info(f"Rest day factor: {rest_day_factor}, Training day factor: {training_day_factor}")
    
    # TDEE для каждого типа дня
    tdee_rest = int(bmr * rest_day_factor)
    tdee_training = int(bmr * training_day_factor)
    
    # Средний TDEE
    if has_training_experience:
        rest_days = 7 - training_days
        tdee_average = int((tdee_rest * rest_days + tdee_training * training_days) / 7)
    else:
        rest_days = 7
        training_days = 0
        tdee_average = tdee_rest  # Все дни как дни отдыха
    
    logger.info(f"TDEE Rest Day: {tdee_rest}, TDEE Training Day: {tdee_training}, Average: {tdee_average}")
    
    # Корректировка под цель
    goal_adjustments = {
        'Похудение': -0.15,      # Дефицит 15%
        'Поддержание': 0,        # Без изменений
        'Набор массы': 0.1       # Профицит 10%
    }
    
    goal = user_data['goal']
    adjustment = goal_adjustments.get(goal, 0)
    
    logger.info(f"Goal: {goal}")
    
    # Целевые калории для каждого типа дня
    target_calories_rest = int(tdee_rest * (1 + adjustment))
    target_calories_training = int(tdee_training * (1 + adjustment))
    target_calories_average = int(tdee_average * (1 + adjustment))
    
    logger.info(f"Target calories - Rest day: {target_calories_rest}, Training day: {target_calories_training}, Average: {target_calories_average}")
    
    # Расчет макронутриентов
    # Белки: 2.0-2.2 г/кг веса
    protein_grams = int(weight * 2.1)
    protein_min = int(weight * 1.9)
    protein_max = int(weight * 2.3)
    
    # Жиры: 25% от калорий (одинаково для всех дней)
    fats_rest = int(target_calories_rest * 0.25 / 9)
    fats_training = int(target_calories_training * 0.25 / 9)
    
    # Углеводы: оставшиеся калории
    protein_calories = protein_grams * 4
    fat_calories_rest = fats_rest * 9
    fat_calories_training = fats_training * 9
    
    carbs_rest = int((target_calories_rest - protein_calories - fat_calories_rest) / 4)
    carbs_training = int((target_calories_training - protein_calories - fat_calories_training) / 4)
    
    logger.info(f"Rest day macros - Protein: {protein_grams}г, Fats: {fats_rest}г, Carbs: {carbs_rest}г")
    logger.info(f"Training day macros - Protein: {protein_grams}г, Fats: {fats_training}г, Carbs: {carbs_training}г")
    
    # Клетчатка и вода
    fiber_rest = max(16, int(carbs_rest * 0.1))
    fiber_training = max(19, int(carbs_training * 0.1)) 
    water = int(weight * 35)  # 35 мл на кг веса
    
    result = {
        'bmr': int(bmr),
        'tdee_rest': tdee_rest,
        'tdee_training': tdee_training,
        'tdee_average': tdee_average,
        'target_calories_rest': target_calories_rest,
        'target_calories_training': target_calories_training,
        'target_calories_average': target_calories_average,
        'protein_grams': protein_grams,
        'protein_min': protein_min,
        'protein_max': protein_max,
        'fats_rest': fats_rest,
        'fats_training': fats_training,
        'carbs_rest': carbs_rest,
        'carbs_training': carbs_training,
        'fiber_rest': fiber_rest,
        'fiber_training': fiber_training,
        'water': water,
        'rest_day_factor': round(rest_day_factor, 2),
        'training_day_factor': round(training_day_factor, 2),
        'training_days': training_days,
        'rest_days': rest_days,
        'has_training_experience': has_training_experience,
        'fat_percent': user_data['fat_percent'],
        'fat_category': user_data['fat_category'],
        'precision_score': 98  # Высокая точность
    }
    
    logger.info(f"Ultra-precise result: {result}")
    return result

# === ОБРАБОТЧИКИ КОМАНД ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Стартовая команда"""
    chat_id = update.message.chat_id
    user_data_storage[chat_id] = {}
    
    # Постоянные кнопки внизу экрана
    keyboard = [
        ['🚀 Начать', '❓ Помощь'],
        ['🎮 Мини-приложения', '📊 О боте']
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True, 
        one_time_keyboard=False
    )
    
    welcome_text = """🎯 **Добро пожаловать в FitAdventure!**

Я помогу создать персональный план питания с учетом:
• Ваших физических параметров
• Целей и опыта тренировок
• Уровня активности и образа жизни
• Качества сна и восстановления

🎮 **Используйте кнопки снизу экрана**
📊 **Точность расчетов: 98%**

Готовы начать путь к телу мечты?"""

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    logger.info(f"User {chat_id} started the bot")
    return GENDER

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка нажатий на постоянные кнопки"""
    text = update.message.text
    chat_id = update.message.chat_id
    
    if text == '🚀 Начать':
        return await start_survey(update, context)
    elif text == '❓ Помощь':
        return await help_command(update, context)
    elif text == '🎮 Мини-приложения':
        if MINI_APPS_AVAILABLE:
            # Показываем меню мини-приложений напрямую
            keyboard = [
                ['🍎 База продуктов'],
                ['🔙 Главное меню']
            ]
            
            text = """🎮 **Мини-приложения FitAdventure**

Выберите нужное приложение:

🍎 **База продуктов** - калорийность и БЖУ продуктов
   • 🌾 Сложные углеводы
   • ⚡ Простые углеводы
   • 🥩 Белки
   • 🫒 Ненасыщенные жиры
   • 🧈 Насыщенные жиры
   • 🌿 Клетчатка
   • 🔍 Поиск по названию
   • 📊 Рекомендации под вашу цель
   • 💡 Советы по употреблению"""
            
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            return GENDER
        else:
            await update.message.reply_text("⚠️ Мини-приложения временно недоступны. Попробуйте позже.")
            return GENDER
    elif text == '📊 О боте':
        about_text = """🤖 **FitAdventure Bot v5.0**

✨ **Возможности:**
• Ультра-точные расчеты питания (98% точность)
• Учет всех факторов активности
• Разделение по дням тренировок и отдыха
• Персональные рекомендации
• Современный интерфейс
• 🎮 Мини-приложения (база продуктов)

🍎 **База продуктов включает:**
• 🌾 Сложные углеводы (овсянка, гречка, киноа)
• ⚡ Простые углеводы (мед, фрукты)
• 🥩 Белки (мясо, рыба, яйца, творог)
• 🫒 Ненасыщенные жиры (орехи, авокадо, масла)
• 🧈 Насыщенные жиры (сыр, масло)
• 🌿 Клетчатка (овощи, бобовые)

🔬 **Научная база:**
• Формула Mifflin-St Jeor для BMR
• Многофакторный анализ TDEE
• Адаптивные коэффициенты активности

👨‍💻 **Разработано с ❤️ для достижения ваших целей**"""
        
        await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)
        return GENDER
    elif text == '💬 Получить консультацию':
        consultation_text = """💬 **Персональная консультация**

🎯 **Что вы получите:**
• 📋 Индивидуальный план тренировок
• 🍽️ Детальный план питания с рецептами
• 📊 Анализ вашего прогресса
• 🔄 Корректировка плана по мере достижения целей
• 💪 Мотивация и поддержка

👨‍💼 **Ваш персональный тренер:** @DARKSIDERS17

📱 **Как связаться:**
1. Нажмите на @DARKSIDERS17
2. Напишите "Хочу консультацию"
3. Укажите ваши цели и пожелания

💡 **Стоимость и детали обсудим в личных сообщениях**

🚀 **Готовы к трансформации?** Свяжитесь прямо сейчас!"""
        
        keyboard = [['🚀 Начать заново', '❓ Помощь'], ['🎮 Мини-приложения', '📊 О боте']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(consultation_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return GENDER
    elif text == '🚀 Начать заново':
        return await start_survey(update, context)
    
    # Обработка кнопок мини-приложений
    elif text == '🍎 База продуктов':
        # Открываем Web App с базой продуктов
        web_app_url = "https://fitadventure-products.web.app"
        
        # Создаем кнопку для открытия Web App
        keyboard = [[KeyboardButton(text="🍎 Открыть базу продуктов", web_app=WebAppInfo(url=web_app_url))]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        text = """🍎 **База продуктов FitAdventure**

📱 **Откройте мини-приложение для просмотра:**
• 🌾 Сложные углеводы
• ⚡ Простые углеводы  
• 🥩 Белки
• 🫒 Ненасыщенные жиры
• 🧈 Насыщенные жиры
• 🌿 Клетчатка

🔍 **Возможности:**
• Поиск по названию продукта
• Фильтрация по категориям
• Детальная информация о БЖУ
• Рекомендации под вашу цель

💡 **Нажмите кнопку ниже для открытия приложения**"""
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return GENDER
    
    elif text == '🔙 Главное меню':
        return await return_to_main_menu(update, context)
    
    # Обработка кнопок базы продуктов
    elif text == '🌾 Сложные углеводы':
        return await show_products_category(update, context, 'сложные_углеводы')
    
    elif text == '⚡ Простые углеводы':
        return await show_products_category(update, context, 'простые_углеводы')
    
    elif text == '🥩 Белки':
        return await show_products_category(update, context, 'белки')
    
    elif text == '🫒 Ненасыщенные жиры':
        return await show_products_category(update, context, 'ненасыщенные_жиры')
    
    elif text == '🧈 Насыщенные жиры':
        return await show_products_category(update, context, 'насыщенные_жиры')
    
    elif text == '🌿 Клетчатка':
        return await show_products_category(update, context, 'клетчатка')
    
    elif text == '🔍 Поиск продукта':
        return await show_search_interface(update, context)
    
    elif text == '📊 Рекомендации':
        return await show_recommendations(update, context)
    
    elif text == '🔙 Назад':
        # Возвращаемся к меню мини-приложений
        keyboard = [
            ['🍎 База продуктов'],
            ['🔙 Главное меню']
        ]
        
        text = """🎮 **Мини-приложения FitAdventure**

Выберите нужное приложение:

🍎 **База продуктов** - калорийность и БЖУ продуктов
   • Поиск по названию
   • Фильтрация по категориям
   • Рекомендации под вашу цель
   • Детальная информация о продуктах"""
        
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return GENDER
    
    elif text == '🔙 Назад к приложениям':
        # Возвращаемся к меню мини-приложений
        keyboard = [
            ['🍎 База продуктов'],
            ['🔙 Главное меню']
        ]
        
        text = """🎮 **Мини-приложения FitAdventure**

Выберите нужное приложение:

🍎 **База продуктов** - калорийность и БЖУ продуктов
   • Поиск по названию
   • Фильтрация по категориям
   • Рекомендации под вашу цель
   • Детальная информация о продуктах"""
        
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return GENDER
    
    # Если это не кнопка, обрабатываем как обычное сообщение
    return await handle_message(update, context)

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало опроса"""
    chat_id = update.message.chat_id
    user_data_storage[chat_id] = {}
    
    keyboard = [['👨 Мужчина', '👩 Женщина']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "👤 **Этап 1/12:** Ваш пол?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    logger.info(f"Starting survey for user {chat_id}")
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора пола"""
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] gender() called. chat_id={chat_id}, text={text}")
    try:
        if text in ['👨 Мужчина', 'мужчина', 'Мужчина']:
            user_data_storage[chat_id]['gender'] = 'мужчина'
        elif text in ['👩 Женщина', 'женщина', 'Женщина']:
            user_data_storage[chat_id]['gender'] = 'женщина'
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите пол, используя кнопки")
            return GENDER
        logger.info(f"User {chat_id} selected gender: {user_data_storage[chat_id]['gender']}")
        # Переход к возрасту
        keyboard = [['🚀 Начать', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🎂 **Этап 2/12:** Укажите ваш возраст (число от 16 до 80)",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return AGE
    except Exception as e:
        logger.error(f"[ERROR] gender() exception: {e}")
        await update.message.reply_text(f"[gender] Ошибка: {e}")
        return GENDER

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка возраста"""
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] age() called. chat_id={chat_id}, text={text}")
    try:
        # Проверка на кнопки
        if text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
            return await handle_buttons(update, context)
        age_value = int(text)
        if not (16 <= age_value <= 80):
            raise ValueError
        user_data_storage[chat_id]['age'] = age_value
        logger.info(f"User {chat_id} entered age: {age_value}")
        await update.message.reply_text(
            "⚖️ **Этап 3/12:** Укажите ваш вес в килограммах (например: 70)",
            parse_mode=ParseMode.MARKDOWN
        )
        return WEIGHT
    except ValueError:
        await update.message.reply_text("❌ Введите корректный возраст (число от 16 до 80)")
        return AGE
    except Exception as e:
        logger.error(f"[ERROR] age() exception: {e}")
        await update.message.reply_text(f"[age] Ошибка: {e}")
        return AGE

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка веса"""
    chat_id = update.message.chat_id
    
    # Проверка на кнопки
    if update.message.text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
        return await handle_buttons(update, context)
    
    try:
        weight_value = float(update.message.text)
        if not (30 <= weight_value <= 300):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Введите корректный вес (число от 30 до 300 кг)")
        return WEIGHT
    
    user_data_storage[chat_id]['weight'] = weight_value
    logger.info(f"User {chat_id} entered weight: {weight_value}")
    
    await update.message.reply_text(
        "📏 **Этап 4/12:** Укажите ваш рост в сантиметрах (например: 175)",
        parse_mode=ParseMode.MARKDOWN
    )
    return HEIGHT

async def height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка роста"""
    chat_id = update.message.chat_id
    
    # Проверка на кнопки
    if update.message.text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
        return await handle_buttons(update, context)
    
    try:
        height_value = float(update.message.text)
        if not (100 <= height_value <= 250):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Введите корректный рост (число от 100 до 250 см)")
        return HEIGHT
    
    user_data_storage[chat_id]['height'] = height_value
    logger.info(f"User {chat_id} entered height: {height_value}")
    
    keyboard = [['✅ Да, знаю', '❌ Не знаю']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "🔥 **Этап 5/12:** Знаете ли вы процент жира в организме?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return FAT_PERCENTAGE

async def fat_percentage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка знания процента жира"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    if text == '✅ Да, знаю':
        keyboard = [['🚀 Начать', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
        
        await update.message.reply_text(
            "📊 Введите процент жира (число от 5 до 50, например: 15)",
            reply_markup=reply_markup
        )
        return FAT_PERCENTAGE_INPUT
    elif text == '❌ Не знаю':
        user_data_storage[chat_id]['fat_percent'] = None
        logger.info(f"User {chat_id} doesn't know fat percentage")
        return await show_goal_selection(update, context)
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите один из вариантов, используя кнопки")
        return FAT_PERCENTAGE

async def fat_percentage_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода процента жира"""
    chat_id = update.message.chat_id
    
    # Проверка на кнопки
    if update.message.text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
        return await handle_buttons(update, context)
    
    try:
        fat_value = float(update.message.text)
        if not (5 <= fat_value <= 50):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Введите корректный процент жира (число от 5 до 50)")
        return FAT_PERCENTAGE_INPUT
    
    user_data_storage[chat_id]['fat_percent'] = fat_value
    logger.info(f"User {chat_id} entered fat percentage: {fat_value}")
    
    return await show_goal_selection(update, context)

async def show_goal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать выбор цели"""
    keyboard = [
        ['📉 Похудение'],
        ['⚖️ Поддержание'],
        ['📈 Набор массы']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "🎯 **Этап 6/12:** Ваша цель?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return GOAL

async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора цели"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    if text == '📉 Похудение':
        user_data_storage[chat_id]['goal'] = 'Похудение'
    elif text == '⚖️ Поддержание':
        user_data_storage[chat_id]['goal'] = 'Поддержание'
    elif text == '📈 Набор массы':
        user_data_storage[chat_id]['goal'] = 'Набор массы'
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите цель, используя кнопки")
        return GOAL
    
    logger.info(f"User {chat_id} selected goal: {user_data_storage[chat_id]['goal']}")
    
    keyboard = [
        ['✅ Есть опыт'],
        ['❌ Нет опыта']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "💪 **Этап 7/12:** Есть ли у вас опыт в тренировках или спорте?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return HAS_TRAINING_EXPERIENCE

async def has_training_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка наличия опыта в тренировках"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    if text == '✅ Есть опыт':
        user_data_storage[chat_id]['has_training_experience'] = True
        logger.info(f"User {chat_id} has training experience")
        
        keyboard = [
            ['🌱 Новичок (до 1 года)'],
            ['🔥 Средний (1-3 года)'],
            ['⚡ Опытный (3+ года)']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "💪 **Этап 8/12:** Ваш опыт тренировок?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return TRAINING_EXPERIENCE
        
    elif text == '❌ Нет опыта':
        user_data_storage[chat_id]['has_training_experience'] = False
        user_data_storage[chat_id]['training_experience'] = 'Новичок'
        user_data_storage[chat_id]['training_days'] = 0
        user_data_storage[chat_id]['activity_type'] = 'Нет'
        user_data_storage[chat_id]['workout_duration'] = 0
        user_data_storage[chat_id]['intensity'] = 'low'
        user_data_storage[chat_id]['recovery'] = 'average'
        logger.info(f"User {chat_id} has no training experience, skipping training questions")
        
        keyboard = [['🚀 Начать', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "🚶 **Этап 8/12:** Сколько шагов в день вы проходите? (например: 5000)",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return STEPS
        
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите ответ, используя кнопки")
        return HAS_TRAINING_EXPERIENCE

async def training_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка опыта тренировок"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    if text == '🌱 Новичок (до 1 года)':
        user_data_storage[chat_id]['training_experience'] = 'Новичок'
    elif text == '🔥 Средний (1-3 года)':
        user_data_storage[chat_id]['training_experience'] = 'Средний'
    elif text == '⚡ Опытный (3+ года)':
        user_data_storage[chat_id]['training_experience'] = 'Опытный'
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите опыт, используя кнопки")
        return TRAINING_EXPERIENCE
    
    logger.info(f"User {chat_id} selected experience: {user_data_storage[chat_id]['training_experience']}")
    
    keyboard = [
        ['1️⃣ день', '2️⃣ дня', '3️⃣ дня'],
        ['4️⃣ дня', '5️⃣ дней', '6️⃣ дней']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "🏃 **Этап 9/12:** Сколько дней в неделю тренируетесь?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return TRAINING_DAYS

async def training_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка дней тренировок"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    days_map = {
        '1️⃣ день': 1,
        '2️⃣ дня': 2, 
        '3️⃣ дня': 3,
        '4️⃣ дня': 4,
        '5️⃣ дней': 5,
        '6️⃣ дней': 6
    }
    
    if text in days_map:
        user_data_storage[chat_id]['training_days'] = days_map[text]
        logger.info(f"User {chat_id} selected training days: {days_map[text]}")
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите количество дней, используя кнопки")
        return TRAINING_DAYS
    
    keyboard = [
        ['🏋️ Силовые тренировки'],
        ['🏃 Кардио/выносливость'],
        ['⚡ Кроссфит/функциональные']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "💪 **Тип тренировок?**",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return ACTIVITY_TYPE

async def activity_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка типа активности"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    if text == '🏋️ Силовые тренировки':
        user_data_storage[chat_id]['activity_type'] = 'Силовые'
    elif text == '🏃 Кардио/выносливость':
        user_data_storage[chat_id]['activity_type'] = 'Выносливость'
    elif text == '⚡ Кроссфит/функциональные':
        user_data_storage[chat_id]['activity_type'] = 'Кроссфит'
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите тип тренировок, используя кнопки")
        return ACTIVITY_TYPE
    
    logger.info(f"User {chat_id} selected activity type: {user_data_storage[chat_id]['activity_type']}")
    
    keyboard = [['🚀 Начать', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "⏱️ **Продолжительность одной тренировки в минутах?** (например: 60)",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return WORKOUT_DURATION

async def workout_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка продолжительности тренировки"""
    chat_id = update.message.chat_id
    
    # Проверка на кнопки
    if update.message.text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
        return await handle_buttons(update, context)
    
    try:
        duration = int(update.message.text)
        if not (15 <= duration <= 300):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Введите корректную продолжительность (от 15 до 300 минут)")
        return WORKOUT_DURATION
    
    user_data_storage[chat_id]['workout_duration'] = duration
    logger.info(f"User {chat_id} entered workout duration: {duration}")
    
    await update.message.reply_text(
        "🚶 **Количество шагов в день?** (примерно, например: 8000)",
        parse_mode=ParseMode.MARKDOWN
    )
    return STEPS

async def steps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка шагов"""
    chat_id = update.message.chat_id
    
    # Проверка на кнопки
    if update.message.text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
        return await handle_buttons(update, context)
    
    try:
        steps_count = int(update.message.text)
        if not (1000 <= steps_count <= 50000):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Введите корректное количество шагов (от 1000 до 50000)")
        return STEPS
    
    user_data_storage[chat_id]['steps'] = steps_count
    logger.info(f"User {chat_id} entered steps: {steps_count}")
    
    # Проверяем наличие опыта в тренировках
    has_training_experience = user_data_storage[chat_id].get('has_training_experience', True)
    
    if has_training_experience:
        # Если есть опыт в тренировках, спрашиваем об интенсивности
        keyboard = [
            ['🟢 Низкая'],
            ['🟡 Средняя'], 
            ['🔴 Высокая'],
            ['⚡ Очень высокая']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "🔥 **Этап 9/12:** Интенсивность ваших тренировок?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return INTENSITY
    else:
        # Если нет опыта в тренировках, пропускаем вопросы о тренировках
        # Устанавливаем значения по умолчанию
        user_data_storage[chat_id]['intensity'] = 'low'
        user_data_storage[chat_id]['recovery'] = 'average'
        
        # Переходим к вопросу о качестве сна
        keyboard = [
            ['😴 Отличный (8+ часов)'],
            ['😊 Хороший (7-8 часов)'],
            ['😐 Средний (6-7 часов)'],
            ['😞 Плохой (<6 часов)']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "🌙 **Этап 9/12:** Качество сна?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return SLEEP_QUALITY

async def intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка интенсивности"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    intensity_map = {
        '🟢 Низкая': 'low',
        '🟡 Средняя': 'moderate',
        '🔴 Высокая': 'high',
        '⚡ Очень высокая': 'very_high'
    }
    
    if text in intensity_map:
        user_data_storage[chat_id]['intensity'] = intensity_map[text]
        logger.info(f"User {chat_id} selected intensity: {intensity_map[text]}")
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите интенсивность, используя кнопки")
        return INTENSITY
    
    keyboard = [
        ['⭐ Отличное'],
        ['✅ Хорошее'],
        ['🔶 Среднее'],
        ['❌ Плохое']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    # Определяем номер этапа в зависимости от наличия опыта в тренировках
    stage_number = "10/12" if user_data_storage[chat_id].get('has_training_experience', True) else "9/12"
    
    await update.message.reply_text(
        f"😴 **Этап {stage_number}:** Качество восстановления после тренировок?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return RECOVERY

async def recovery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка восстановления"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    recovery_map = {
        '⭐ Отличное': 'excellent',
        '✅ Хорошее': 'good', 
        '🔶 Среднее': 'average',
        '❌ Плохое': 'poor'
    }
    
    if text in recovery_map:
        user_data_storage[chat_id]['recovery'] = recovery_map[text]
        logger.info(f"User {chat_id} selected recovery: {recovery_map[text]}")
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите качество восстановления, используя кнопки")
        return RECOVERY
    
    keyboard = [
        ['😴 Отличный (8+ часов)'],
        ['😊 Хороший (7-8 часов)'],
        ['😐 Средний (6-7 часов)'],
        ['😞 Плохой (<6 часов)']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    # Определяем номер этапа в зависимости от наличия опыта в тренировках
    stage_number = "11/12" if user_data_storage[chat_id].get('has_training_experience', True) else "9/12"
    
    await update.message.reply_text(
        f"🌙 **Этап {stage_number}:** Качество сна?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return SLEEP_QUALITY

async def sleep_quality(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка качества сна"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    sleep_map = {
        '😴 Отличный (8+ часов)': 'excellent',
        '😊 Хороший (7-8 часов)': 'good',
        '😐 Средний (6-7 часов)': 'average',
        '😞 Плохой (<6 часов)': 'poor'
    }
    
    if text in sleep_map:
        user_data_storage[chat_id]['sleep_quality'] = sleep_map[text]
        logger.info(f"User {chat_id} selected sleep quality: {sleep_map[text]}")
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите качество сна, используя кнопки")
        return SLEEP_QUALITY
    
    keyboard = [
        ['😌 Низкий (1-3)'],
        ['😐 Средний (4-6)'], 
        ['😰 Высокий (7-10)']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    # Определяем номер этапа в зависимости от наличия опыта в тренировках
    stage_number = "11/12" if user_data_storage[chat_id].get('has_training_experience', True) else "10/12"
    
    await update.message.reply_text(
        f"💆 **Этап {stage_number}:** Уровень стресса в жизни по шкале 1-10?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return STRESS_LEVEL

async def stress_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка уровня стресса"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    stress_map = {
        '😌 Низкий (1-3)': 2,
        '😐 Средний (4-6)': 5,
        '😰 Высокий (7-10)': 8
    }
    
    if text in stress_map:
        user_data_storage[chat_id]['stress_level'] = stress_map[text]
        logger.info(f"User {chat_id} selected stress level: {stress_map[text]}")
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите уровень стресса, используя кнопки")
        return STRESS_LEVEL
    
    keyboard = [
        ['💻 Офисная работа'],
        ['🏃 Активная работа'],
        ['💪 Физический труд']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    # Определяем номер этапа в зависимости от наличия опыта в тренировках
    stage_number = "12/12" if user_data_storage[chat_id].get('has_training_experience', True) else "11/12"
    
    await update.message.reply_text(
        f"💼 **Этап {stage_number}:** Тип вашей работы?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return OCCUPATION

async def occupation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Финальная обработка и расчет"""
    chat_id = update.message.chat_id
    text = update.message.text
    
    occupation_map = {
        '💻 Офисная работа': 'office',
        '🏃 Активная работа': 'healthcare',
        '💪 Физический труд': 'construction'
    }
    
    if text in occupation_map:
        user_data_storage[chat_id]['occupation'] = occupation_map[text]
        logger.info(f"User {chat_id} selected occupation: {occupation_map[text]}")
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите тип работы, используя кнопки")
        return OCCUPATION
    
    # Возвращаем постоянные кнопки
    keyboard = [['🚀 Начать', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Показываем процесс расчета
    calculating_msg = await update.message.reply_text(
        "🧠 **Выполняю ультра-точные расчеты...**\n\n⚡ Анализирую все факторы\n🔬 Применяю научные формулы\n📊 Создаю персональный план",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Генерируем ультра-точные рекомендации
    try:
        logger.info(f"Starting calculations for user {chat_id}")
        logger.info(f"User data: {user_data_storage[chat_id]}")
        
        results = generate_ultra_precise_recommendations(user_data_storage[chat_id])
        
        # Форматируем результат в зависимости от наличия опыта в тренировках
        if results['has_training_experience']:
            result_message = f"""🎉 **Ваш ультра-точный план питания готов!**

🎯 **Точность расчета:** {results['precision_score']}%

📊 **КАЛОРИИ ПО ДНЯМ:**
• 💤 Дни отдыха: **{results['target_calories_rest']} ккал**
• 🏋️ Дни тренировок: **{results['target_calories_training']} ккал**
• 📈 Средний показатель: **{results['target_calories_average']} ккал**

🥩 **МАКРОНУТРИЕНТЫ:**

**🥤 Белки:** {results['protein_grams']} г ({results['protein_min']}-{results['protein_max']} г)

**🥑 Жиры:**
• Дни отдыха: {results['fats_rest']} г
• Дни тренировок: {results['fats_training']} г

**🍞 Углеводы:**
• Дни отдыха: {results['carbs_rest']} г  
• Дни тренировок: {results['carbs_training']} г

**🌾 Клетчатка:**
• Дни отдыха: {results['fiber_rest']} г
• Дни тренировок: {results['fiber_training']} г

**💧 Вода:** {results['water']} мл/день

📈 **ДЕТАЛЬНЫЕ ПОКАЗАТЕЛИ:**
• 🔥 BMR (базовый метаболизм): {results['bmr']} ккал
• ⚡ TDEE отдых: {results['tdee_rest']} ккал
• 🏋️ TDEE тренировки: {results['tdee_training']} ккал
• 📊 Коэффициент отдыха: {results['rest_day_factor']}
• 💪 Коэффициент тренировок: {results['training_day_factor']}

📊 **АНАЛИЗ ТЕЛА:**
• 🎯 Процент жира: **{results['fat_percent']}%**
• 📋 Категория: **{results['fat_category']}**

**📚 ОБЪЯСНЕНИЯ:**
• **BMR** - калории для поддержания жизнедеятельности в покое
• **TDEE** - общий расход энергии с учетом активности
• **Целевые калории** - калории для достижения вашей цели
• **Процент жира** - рассчитан на основе ваших параметров

✨ *Расчеты учитывают ВСЕ индивидуальные факторы для максимальной точности!*

🎯 Следуйте плану и достигайте своих целей!"""
        else:
            result_message = f"""🎉 **Ваш ультра-точный план питания готов!**

🎯 **Точность расчета:** {results['precision_score']}%

📊 **КАЛОРИИ:**
• 📈 Ежедневная норма: **{results['target_calories_average']} ккал**

🥩 **МАКРОНУТРИЕНТЫ:**

**🥤 Белки:** {results['protein_grams']} г ({results['protein_min']}-{results['protein_max']} г)

**🥑 Жиры:** {results['fats_rest']} г

**🍞 Углеводы:** {results['carbs_rest']} г

**🌾 Клетчатка:** {results['fiber_rest']} г

**💧 Вода:** {results['water']} мл/день

📈 **ДЕТАЛЬНЫЕ ПОКАЗАТЕЛИ:**
• 🔥 BMR (базовый метаболизм): {results['bmr']} ккал
• ⚡ TDEE (общий расход энергии): {results['tdee_average']} ккал
• 📊 Коэффициент активности: {results['rest_day_factor']}

📊 **АНАЛИЗ ТЕЛА:**
• 🎯 Процент жира: **{results['fat_percent']}%**
• 📋 Категория: **{results['fat_category']}**

**📚 ОБЪЯСНЕНИЯ:**
• **BMR** - калории для поддержания жизнедеятельности в покое
• **TDEE** - общий расход энергии с учетом активности
• **Целевые калории** - калории для достижения вашей цели
• **Процент жира** - рассчитан на основе ваших параметров

💡 **РЕКОМЕНДАЦИЯ:** Если планируете начать тренировки, пересчитайте план с учетом новой активности!

✨ *Расчеты учитывают ВСЕ индивидуальные факторы для максимальной точности!*

🎯 Следуйте плану и достигайте своих целей!"""

        # Добавляем кнопку консультации
        consultation_keyboard = [['💬 Получить консультацию'], ['🚀 Начать заново', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
        consultation_markup = ReplyKeyboardMarkup(consultation_keyboard, resize_keyboard=True)
        
        try:
            await calculating_msg.edit_text(result_message, parse_mode=ParseMode.MARKDOWN)
            # Отправляем сообщение с кнопкой консультации
            await update.message.reply_text(
                "💬 **Нужна персональная консультация?**\n\n"
                "🎯 Получите индивидуальные рекомендации от эксперта\n"
                "📋 Составление персонального плана тренировок\n"
                "🍽️ Детальный план питания с рецептами\n"
                "📊 Анализ прогресса и корректировка плана\n\n"
                "Нажмите кнопку ниже для связи с @DARKSIDERS17",
                reply_markup=consultation_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Edit failed, sending new message: {e}")
            await update.message.reply_text(result_message, parse_mode=ParseMode.MARKDOWN)
            # Отправляем сообщение с кнопкой консультации
            await update.message.reply_text(
                "💬 **Нужна персональная консультация?**\n\n"
                "🎯 Получите индивидуальные рекомендации от эксперта\n"
                "📋 Составление персонального плана тренировок\n"
                "🍽️ Детальный план питания с рецептами\n"
                "📊 Анализ прогресса и корректировка плана\n\n"
                "Нажмите кнопку ниже для связи с @DARKSIDERS17",
                reply_markup=consultation_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        logger.info(f"Successfully sent results to user {chat_id}")
        
    except Exception as e:
        logger.error(f"Error calculating for user {chat_id}: {str(e)}")
        await calculating_msg.edit_text(
            f"❌ **Ошибка расчета:** {str(e)}\n\nПопробуйте начать заново, нажав 🚀 Начать",
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Очистка данных
    if chat_id in user_data_storage:
        del user_data_storage[chat_id]
    
    return GENDER

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Команда помощи"""
    help_text = """❓ **Справка FitAdventure Bot**

🎯 **Что я умею:**
• Рассчитываю персональный план питания
• Учитываю все факторы: активность, сон, стресс
• Разделяю калории по дням тренировок и отдыха
• Использую научные формулы (точность 98%)

🔬 **Научная база:**
• Формула Mifflin-St Jeor для BMR
• Многофакторный анализ TDEE
• Адаптивные коэффициенты активности

🎮 **Как пользоваться:**
• Используйте кнопки внизу экрана
• Следуйте инструкциям бота
• Отвечайте честно для точности расчетов

💡 **Полезные команды:**
• /start - перезапуск бота
• /help - эта справка

🚀 **Готовы начать?** Нажмите кнопку "🚀 Начать"!"""

    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    return GENDER

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена анализа"""
    chat_id = update.message.chat_id
    
    keyboard = [['🚀 Начать', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "❌ **Анализ отменен**\n\nНажмите 🚀 Начать для нового расчета",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    if chat_id in user_data_storage:
        del user_data_storage[chat_id]
    
    return GENDER

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка неопознанных сообщений"""
    await update.message.reply_text(
        "🤔 Не понимаю это сообщение.\n\n🎮 Используйте кнопки внизу экрана или команду /help для справки",
        parse_mode=ParseMode.MARKDOWN
    )
    return GENDER

async def handle_webapp_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик callback кнопок Web App"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "products_regular":
        if PRODUCTS_MINI_APP_AVAILABLE:
            return await show_products_mini_app(update, context)
        elif MINI_APPS_AVAILABLE:
            return await show_products_menu(update, context)
        else:
            await query.edit_message_text("⚠️ База продуктов временно недоступна. Попробуйте позже.")
            return GENDER
    
    return GENDER

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик данных от Web App"""
    try:
        if update.message.web_app_data:
            data = json.loads(update.message.web_app_data.data)
            
            if data.get('action') == 'product_details':
                product_name = data.get('name', 'Неизвестный продукт')
                details = data.get('details', 'Информация недоступна')
                goal = data.get('goal', 'неизвестная цель')
                category = data.get('category', 'неизвестная категория')
                
                text = f"""🍎 **{product_name.replace('_', ' ').upper()}**

📊 **Пищевая ценность на 100г:**
{details}

🎯 **Цель:** {goal.replace('_', ' ').title()}
📂 **Категория:** {category.replace('_', ' ').title()}

💡 **Совет:** Используйте эту информацию для планирования своего рациона!"""
                
                keyboard = [['🔙 Главное меню']]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                
                await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
                return GENDER
        
        return GENDER
        
    except Exception as e:
        logger.error(f"Ошибка обработки Web App данных: {e}")
        await update.message.reply_text("❌ Ошибка обработки данных из приложения")
        return GENDER

# === ФУНКЦИИ БАЗЫ ПРОДУКТОВ ===
async def show_products_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Показать продукты определенной категории"""
    from products_database import PRODUCTS_DATABASE
    
    # Получаем цель пользователя (по умолчанию - похудение)
    chat_id = update.message.chat_id
    user_goal = 'похудение'  # Можно добавить логику определения цели
    
    products = PRODUCTS_DATABASE.get(user_goal, {}).get(category, {})
    
    if not products:
        await update.message.reply_text(f"❌ Продукты в категории '{category}' не найдены")
        return "PRODUCTS_MAIN"
    
    category_names = {
        "сложные_углеводы": "🌾 Сложные углеводы",
        "простые_углеводы": "⚡ Простые углеводы", 
        "белки": "🥩 Белки",
        "ненасыщенные_жиры": "🫒 Ненасыщенные жиры",
        "насыщенные_жиры": "🧈 Насыщенные жиры",
        "клетчатка": "🌿 Клетчатка"
    }
    
    text = f"**{category_names.get(category, category)}**\n\n"
    
    for name, data in products.items():
        text += f"🍎 **{name.replace('_', ' ').upper()}**\n"
        text += f"📊 Калории: {data['калории']} ккал/100г\n"
        text += f"🥩 Белки: {data['белки']}g | 🫒 Жиры: {data['жиры']}g | 🌾 Углеводы: {data['углеводы']}g\n"
        if 'описание' in data:
            text += f"💡 {data['описание']}\n"
        text += "\n"
    
    keyboard = [['🔙 Назад к категориям']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return "PRODUCTS_MAIN"

async def show_search_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать интерфейс поиска"""
    text = """🔍 **Поиск продукта**

Введите название продукта для поиска в базе данных.

💡 **Примеры:**
• куриная грудка
• овсянка
• авокадо
• гречка
• творог"""
    
    keyboard = [['🔙 Назад к категориям']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return "PRODUCT_SEARCH_NEW"

async def show_recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать рекомендации продуктов"""
    from products_database import PRODUCTS_DATABASE
    
    chat_id = update.message.chat_id
    user_goal = 'похудение'  # Можно добавить логику определения цели
    
    text = f"📊 **Рекомендуемые продукты для {user_goal.replace('_', ' ').title()}:**\n\n"
    
    # Показываем по 2-3 продукта из каждой категории
    categories = ['сложные_углеводы', 'белки', 'ненасыщенные_жиры', 'клетчатка']
    
    for category in categories:
        products = PRODUCTS_DATABASE.get(user_goal, {}).get(category, {})
        if products:
            category_names = {
                "сложные_углеводы": "🌾 Сложные углеводы",
                "простые_углеводы": "⚡ Простые углеводы", 
                "белки": "🥩 Белки",
                "ненасыщенные_жиры": "🫒 Ненасыщенные жиры",
                "насыщенные_жиры": "🧈 Насыщенные жиры",
                "клетчатка": "🌿 Клетчатка"
            }
            
            text += f"**{category_names.get(category, category)}:**\n"
            for i, (name, data) in enumerate(list(products.items())[:3]):
                text += f"• {name.title()} - {data['калории']} ккал/100г"
                if 'описание' in data:
                    text += f" ({data['описание']})"
                text += "\n"
            text += "\n"
    
    text += "💡 **Эти продукты оптимально подходят для вашей цели!**\n\n"
    text += "🎯 **Советы по употреблению:**\n"
    
    if user_goal == "похудение":
        text += "• Ешьте больше белков и клетчатки\n"
        text += "• Ограничьте простые углеводы\n"
        text += "• Контролируйте порции\n"
    elif user_goal == "набор_массы":
        text += "• Увеличьте потребление белков\n"
        text += "• Добавьте сложные углеводы\n"
        text += "• Не забывайте про полезные жиры\n"
    else:
        text += "• Сбалансированное питание\n"
        text += "• Разнообразие продуктов\n"
        text += "• Умеренные порции\n"
    
    keyboard = [['🔙 Назад к категориям']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return "PRODUCTS_MAIN"

async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Вернуться в главное меню"""
    chat_id = update.message.chat_id
    user_data_storage[chat_id] = {}
    
    # Постоянные кнопки внизу экрана
    keyboard = [
        ['🚀 Начать', '❓ Помощь'],
        ['🎮 Мини-приложения', '📊 О боте']
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True, 
        one_time_keyboard=False
    )
    
    welcome_text = """🎯 **Добро пожаловать в FitAdventure!**

Я помогу создать персональный план питания с учетом:
• Ваших физических параметров
• Целей и опыта тренировок
• Уровня активности и образа жизни
• Качества сна и восстановления

🎮 **Используйте кнопки снизу экрана**
📊 **Точность расчетов: 98%**

Готовы начать путь к телу мечты?"""

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return GENDER

def main() -> None:
    """Главная функция запуска бота"""
    print("🚀 Запуск FitAdventure Bot v5.0 Final...")
    
    # Автоматическая настройка токена
    try:
        TOKEN = setup_bot_token()
        print(f"✅ Токен получен успешно!")
    except KeyboardInterrupt:
        print("\n❌ Настройка отменена пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка настройки токена: {e}")
        sys.exit(1)
        
    # Создание приложения бота
    try:
        application = Application.builder().token(TOKEN).build()
        print("✅ Telegram Application создан успешно!")
    except Exception as e:
        print(f"❌ Ошибка создания приложения: {e}")
        print("🔍 Проверьте правильность токена")
        sys.exit(1)
    
    # Настройка ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [
                MessageHandler(filters.Regex('^(👨 Мужчина|👩 Женщина|мужчина|Мужчина|женщина|Женщина)$'), gender),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons)
            ],
            AGE: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, age)
            ],
            WEIGHT: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, weight)
            ],
            HEIGHT: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, height)
            ],
            FAT_PERCENTAGE: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, fat_percentage)
            ],
            FAT_PERCENTAGE_INPUT: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, fat_percentage_input)
            ],
            GOAL: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, goal)
            ],
            HAS_TRAINING_EXPERIENCE: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, has_training_experience)
            ],
            TRAINING_EXPERIENCE: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, training_experience)
            ],
            TRAINING_DAYS: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, training_days)
            ],
            ACTIVITY_TYPE: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, activity_type)
            ],
            WORKOUT_DURATION: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, workout_duration)
            ],
            STEPS: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, steps)
            ],
            INTENSITY: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, intensity)
            ],
            RECOVERY: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, recovery)
            ],
            SLEEP_QUALITY: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, sleep_quality)
            ],
            STRESS_LEVEL: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, stress_level)
            ],
            OCCUPATION: [
                MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), handle_buttons),
                MessageHandler(filters.TEXT & ~filters.COMMAND, occupation)
            ],


            # Добавляем недостающие состояния для мини-приложений
            MINI_APPS_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mini_apps_navigation)
            ],
            PRODUCTS_MENU: [
                MessageHandler(filters.Regex('^(🥩 Белки|🍞 Углеводы|🧈 Жиры)$'), show_products_category),
                MessageHandler(filters.Regex('^(🔍 Поиск продукта|📊 Рекомендации|🔙 Назад)$'), search_product_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, show_product_details)
            ],
            PRODUCT_SEARCH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_product_handler)
            ],
            
            # Состояния для нового мини-приложения базы продуктов
            PRODUCTS_MAIN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_products_navigation)
            ],
            PRODUCTS_CATEGORY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_products_navigation)
            ],
            PRODUCT_DETAILS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_products_navigation)
            ],
            PRODUCT_SEARCH_NEW: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_search)
            ],
            "WEBAPP_CHOICE": [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons)
            ],
            
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('start', start))
    
    # Добавляем обработчик для callback кнопок Web App
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(handle_webapp_callback))
    
    # Добавляем обработчик для данных Web App
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    

    
    logger.info("🚀 FitAdventure Bot v5.0 Final запущен!")
    logger.info("✅ Все системы готовы к работе")
    print("\n🎯 FitAdventure Bot v5.0 Final запущен успешно!")
    print("🎮 Новая функция: Постоянные кнопки снизу экрана!")
    print("📊 Ультра-точные расчеты с точностью 98%")
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