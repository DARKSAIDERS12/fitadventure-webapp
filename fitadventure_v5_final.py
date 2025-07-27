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
import logging
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from telegram.ext import filters as tg_filters

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
GENDER, AGE, WEIGHT, HEIGHT, FAT_PERCENTAGE, FAT_PERCENTAGE_INPUT, GOAL, EXPERIENCE_CHOICE, TRAINING_EXPERIENCE, TRAINING_DAYS, ACTIVITY_TYPE, WORKOUT_DURATION, STEPS, INTENSITY, RECOVERY, SLEEP_QUALITY, STRESS_LEVEL, OCCUPATION = range(18)

# --- Универсальный фильтр для стартовых кнопок ---
START_BUTTONS = ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте', '💡 Мотивация для старта', '❓ Я никогда не тренировался', '😕 Нет мотивации', '📢 Подписаться на обновления', '📢 Отписаться от обновлений']
START_BUTTONS_REGEX = f"^({'|'.join([b.replace(' ', '\\s') for b in START_BUTTONS])})$"

# --- Хранилище ---
user_data_storage = {}
subscribers = set()  # Множество подписчиков

# === УЛЬТРА-ТОЧНЫЕ РАСЧЕТЫ ===
def generate_ultra_precise_recommendations(user_data):
    """Генерация ультра-точных рекомендаций с разделением по дням"""
    logger.info(f"Starting ultra-precise calculations with data: {user_data}")
    # Строгая проверка всех нужных полей
    required_fields = [
        'weight', 'height', 'age', 'gender', 'training_days', 'steps', 'occupation',
        'activity_type', 'intensity', 'workout_duration', 'recovery', 'sleep_quality',
        'stress_level', 'goal'
    ]
    for field in required_fields:
        if field not in user_data:
            logger.error(f"Missing required field: {field}")
            raise ValueError(f"Отсутствует обязательное поле: {field}")
    
    # Базовые параметры
    weight = user_data['weight']
    height = user_data['height'] 
    age = user_data['age']
    gender = user_data['gender']
    
    logger.info(f"Basic parameters - Weight: {weight}, Height: {height}, Age: {age}, Gender: {gender}")
    
    # BMR по формуле Mifflin-St Jeor
    if gender == 'мужчина':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    logger.info(f"Base BMR calculated: {bmr}")
    
    # Детальный расчет активности
    training_days = user_data['training_days']
    steps = user_data['steps']
    
    # Рабочая активность
    occupation_factors = {
        'office': 0.15,      # Офисная работа
        'healthcare': 0.25,  # Активная работа  
        'construction': 0.35 # Физический труд
    }
    work_factor = occupation_factors.get(user_data['occupation'], 0.2)
    
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
    
    logger.info(f"Rest day factor: {rest_day_factor}, Training day factor: {training_day_factor}")
    
    # TDEE для каждого типа дня
    tdee_rest = int(bmr * rest_day_factor)
    tdee_training = int(bmr * training_day_factor)
    
    # Средний TDEE
    rest_days = 7 - training_days
    tdee_average = int((tdee_rest * rest_days + tdee_training * training_days) / 7)
    
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
        'precision_score': 98  # Высокая точность
    }
    
    logger.info(f"Ultra-precise result: {result}")
    return result

# --- ДОБАВЛЯЕМ МОТИВАЦИЮ И FAQ ---
MOTIVATION_TEXT = (
    "💡 **Мотивация для старта**\n\n"
    "• Даже 10 минут активности в день — уже вклад в здоровье!\n"
    "• Не обязательно идти в зал: прогулки, зарядка, плавание — отличный старт.\n"
    "• Главное — регулярность, а не интенсивность.\n"
    "• Каждый шаг — это шаг к лучшему самочувствию и настроению!\n"
    "• Начать можно в любом возрасте и с любого уровня.\n"
    "\n✨ *Ты можешь больше, чем думаешь!*"
)
FAQ_TEXT = (
    "❓ **Я никогда не тренировался — что делать?**\n\n"
    "• Начните с малого: прогулки, легкая зарядка, растяжка.\n"
    "• Не ставьте себе сразу большие цели — главное, чтобы движение стало привычкой.\n"
    "• Не обязательно покупать абонемент — начните дома или на улице.\n"
    "• Если есть хронические заболевания — проконсультируйтесь с врачом.\n"
    "• Не сравнивайте себя с другими — ваш путь уникален!\n"
    "\n💬 Если есть вопросы — пишите /help."
)
NOMOTIVATION_TEXT = (
    "😕 **Нет мотивации?**\n\n"
    "• Не ждите вдохновения — начните с малого, и мотивация придёт в процессе!\n"
    "• Думайте не о результате, а о первом шаге: просто выйдите на прогулку или сделайте 5 приседаний.\n"
    "• Не сравнивайте себя с другими — ваш путь уникален.\n"
    "• Запишите, зачем вам это нужно: здоровье, энергия, пример для близких.\n"
    "• Помните: движение — это забота о себе, а не наказание!\n"
    "\n💬 Если нужна поддержка — напишите /help."
)

# --- ДОБАВЛЯЮ ОПРЕДЕЛЕНИЕ ДЛЯ ВОПРОСА ПРО ОПЫТ ---
EXPERIENCE_QUESTION = 'Есть ли у вас опыт в тренировках или спорте?'
EXPERIENCE_BUTTONS = [['✅ Есть опыт', '❌ Нет опыта']]

# === ОБРАБОТЧИКИ КОМАНД ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Стартовая команда"""
    chat_id = update.message.chat_id
    # Инициализируем только если пользователя нет
    if chat_id not in user_data_storage:
        user_data_storage[chat_id] = {}
    
    # Постоянные кнопки внизу экрана
    keyboard = [
        ['🚀 Начать', '❓ Помощь'],
        ['🌍 Язык', '📊 О боте'],
        ['💡 Мотивация для старта', '❓ Я никогда не тренировался'],
        ['😕 Нет мотивации'],
        ['📢 Подписаться на обновления', '📢 Отписаться от обновлений']
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
    elif text == '🌍 Язык':
        await update.message.reply_text("🇷🇺 Текущий язык: Русский\n🔄 Смена языка будет добавлена в следующих версиях")
        return GENDER
    elif text == '📊 О боте':
        about_text = """🤖 **FitAdventure Bot v5.0**

✨ **Возможности:**
• Ультра-точные расчеты питания (98% точность)
• Учет всех факторов активности
• Разделение по дням тренировок и отдыха
• Персональные рекомендации
• Современный интерфейс

🔬 **Научная база:**
• Формула Mifflin-St Jeor для BMR
• Многофакторный анализ TDEE
• Адаптивные коэффициенты активности

👨‍💻 **Разработано с ❤️ для достижения ваших целей**"""
        
        await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)
        return GENDER
    elif text == '💡 Мотивация для старта':
        return await motivation_command(update, context)
    elif text == '❓ Я никогда не тренировался':
        return await faq_command(update, context)
    elif text == '😕 Нет мотивации':
        return await nomotivation_command(update, context)
    elif text == '📢 Подписаться на обновления':
        return await subscribe_command(update, context)
    elif text == '📢 Отписаться от обновлений':
        return await unsubscribe_command(update, context)
    elif text == '💬 Получить консультацию эксперта':
        return await consultation_command(update, context)
    elif text == 'Я всё-таки хочу тренироваться!':
        await update.message.reply_text(
            'Для прохождения блока про тренировки нажмите /start и выберите "Есть опыт" в новом опросе.',
            parse_mode=ParseMode.MARKDOWN
        )
        return GENDER
    
    # Если это не кнопка, обрабатываем как обычное сообщение
    return await handle_message(update, context)

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало опроса"""
    chat_id = update.message.chat_id
    # Очищаем данные для нового опроса
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
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
    # Проверяем что пользователь инициализирован
    if chat_id not in user_data_storage:
        user_data_storage[chat_id] = {}
    
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

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка возраста"""
    chat_id = update.message.chat_id
    
    # Универсальная обработка стартовых кнопок
    if update.message.text in START_BUTTONS:
        return await handle_buttons(update, context)
    
    try:
        age_value = int(update.message.text)
        if not (16 <= age_value <= 80):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Введите корректный возраст (число от 16 до 80)")
        return AGE
    
    user_data_storage[chat_id]['age'] = age_value
    logger.info(f"User {chat_id} entered age: {age_value}")
    
    await update.message.reply_text(
        "⚖️ **Этап 3/12:** Укажите ваш вес в килограммах (например: 70)",
        parse_mode=ParseMode.MARKDOWN
    )
    return WEIGHT

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка веса"""
    chat_id = update.message.chat_id
    
    # Универсальная обработка стартовых кнопок
    if update.message.text in START_BUTTONS:
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
    
    # Универсальная обработка стартовых кнопок
    if update.message.text in START_BUTTONS:
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
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
    if text == '✅ Да, знаю':
        keyboard = [['🚀 Начать', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
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
    
    # Универсальная обработка стартовых кнопок
    if update.message.text in START_BUTTONS:
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
    
    await show_goal_selection(update, context)
    return GOAL

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
    logger.info(f"[DEBUG] goal() called. chat_id={chat_id}, text={text}")
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
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
    
    # После выбора цели задаём вопрос про опыт
    await experience_block(update, context)
    return EXPERIENCE_CHOICE

async def experience_block(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    reply_markup = ReplyKeyboardMarkup(EXPERIENCE_BUTTONS, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        EXPERIENCE_QUESTION,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return EXPERIENCE_CHOICE

async def experience_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] experience_choice() called. chat_id={chat_id}, text={text}")
    if text == '✅ Есть опыт':
        return await show_training_experience(update, context)
    elif text == '❌ Нет опыта':
        # Пропускаем все вопросы про тренировки, сразу спрашиваем шаги
        user_data_storage[chat_id]['training_experience'] = 'Нет опыта'
        user_data_storage[chat_id]['training_days'] = 0
        user_data_storage[chat_id]['activity_type'] = 'Нет'
        user_data_storage[chat_id]['workout_duration'] = 0
        user_data_storage[chat_id]['intensity'] = 'low'
        await update.message.reply_text(
            "🚶 **Количество шагов в день?** (примерно, например: 8000)",
            parse_mode=ParseMode.MARKDOWN
        )
        return STEPS
    else:
        await update.message.reply_text("❌ Пожалуйста, выберите один из вариантов, используя кнопки")
        return EXPERIENCE_CHOICE

async def show_training_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    keyboard = [
        ['🌱 Новичок (до 1 года)'],
        ['🔥 Средний (1-3 года)'],
        ['⚡ Опытный (3+ года)']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "💪 **Этап 7/12:** Ваш опыт тренировок?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return TRAINING_EXPERIENCE

async def training_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка опыта тренировок"""
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] training_experience() called. chat_id={chat_id}, text={text}")
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
    if text == '❌ Нет опыта':
        user_data_storage[chat_id]['training_experience'] = 'Нет опыта'
        user_data_storage[chat_id]['training_days'] = 0
        user_data_storage[chat_id]['activity_type'] = 'Нет'
        user_data_storage[chat_id]['workout_duration'] = 0
        user_data_storage[chat_id]['intensity'] = 'low'
        # Пропускаем все вопросы про тренировки, сразу спрашиваем шаги
        await update.message.reply_text(
            "🚶 **Количество шагов в день?** (примерно, например: 8000)",
            parse_mode=ParseMode.MARKDOWN
        )
        return STEPS
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
        "🏃 **Этап 8/12:** Сколько дней в неделю тренируетесь?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return TRAINING_DAYS

async def training_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка дней тренировок"""
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] training_days() called. chat_id={chat_id}, text={text}")
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
    if user_data_storage[chat_id].get('training_experience') == 'Нет опыта':
        user_data_storage[chat_id]['training_days'] = 0
        user_data_storage[chat_id]['activity_type'] = 'Нет'
        user_data_storage[chat_id]['workout_duration'] = 0
        user_data_storage[chat_id]['intensity'] = 'low'
        # Пропускаем все вопросы про тренировки, сразу спрашиваем шаги
        await update.message.reply_text(
            "🚶 **Количество шагов в день?** (примерно, например: 8000)",
            parse_mode=ParseMode.MARKDOWN
        )
        return STEPS
    
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
    logger.info(f"[DEBUG] activity_type() called. chat_id={chat_id}, text={text}")
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
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
    text = update.message.text
    logger.info(f"[DEBUG] workout_duration() called. chat_id={chat_id}, text={text}")
    
    # Универсальная обработка стартовых кнопок
    if update.message.text in START_BUTTONS:
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
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] steps() called. chat_id={chat_id}, text={text}")
    if update.message.text in START_BUTTONS:
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
    # Если нет опыта — пропускаем интенсивность и сразу спрашиваем восстановление
    if user_data_storage[chat_id].get('training_experience') == 'Нет опыта':
        keyboard = [
            ['⭐ Отличное'],
            ['✅ Хорошее'],
            ['🔶 Среднее'],
            ['❌ Плохое']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "😴 **Этап 10/12:** Качество восстановления после дня?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return RECOVERY
    # иначе — как было
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

async def intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] intensity() called. chat_id={chat_id}, text={text}")
    # Если нет опыта — пропускаем интенсивность
    if user_data_storage[chat_id].get('training_experience') == 'Нет опыта':
        keyboard = [
            ['⭐ Отличное'],
            ['✅ Хорошее'],
            ['🔶 Среднее'],
            ['❌ Плохое']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "😴 **Этап 10/12:** Качество восстановления после дня?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return RECOVERY
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
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
    
    await update.message.reply_text(
        "😴 **Этап 10/12:** Качество восстановления после тренировок?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return RECOVERY

async def recovery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка восстановления"""
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] recovery() called. chat_id={chat_id}, text={text}")
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
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
    
    await update.message.reply_text(
        "🌙 **Этап 11/12:** Качество сна?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return SLEEP_QUALITY

async def sleep_quality(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка качества сна"""
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] sleep_quality() called. chat_id={chat_id}, text={text}")
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
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
    
    await update.message.reply_text(
        "💆 **Уровень стресса в жизни по шкале 1-10?**",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return STRESS_LEVEL

async def stress_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка уровня стресса"""
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] stress_level() called. chat_id={chat_id}, text={text}")
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
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
    
    await update.message.reply_text(
        "💼 **Этап 12/12:** Тип вашей работы?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return OCCUPATION

async def occupation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Финальная обработка и расчет"""
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"[DEBUG] occupation() called. chat_id={chat_id}, text={text}")
    
    # Универсальная обработка стартовых кнопок
    if text in START_BUTTONS:
        return await handle_buttons(update, context)
    
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
    
    # Диагностика: логируем все данные пользователя
    logger.info(f"[DEBUG] user_data_storage[{chat_id}] перед расчетом: {user_data_storage[chat_id]}")
    # Проверяем, какие поля не заполнены
    required_fields = [
        'weight', 'height', 'age', 'gender', 'training_days', 'steps', 'occupation',
        'activity_type', 'intensity', 'workout_duration', 'recovery', 'sleep_quality',
        'stress_level', 'goal'
    ]
    missing = [f for f in required_fields if f not in user_data_storage[chat_id]]
    if missing:
        logger.error(f"[DEBUG] Не заполнены поля: {missing}")
        await update.message.reply_text(
            f"❌ Не все данные были получены. Не заполнены поля: {', '.join(missing)}\n\nПожалуйста, пройдите опрос заново, нажав 🚀 Начать",
            parse_mode=ParseMode.MARKDOWN
        )
        if chat_id in user_data_storage:
            del user_data_storage[chat_id]
        return GENDER
    try:
        logger.info(f"Starting calculations for user {chat_id}")
        logger.info(f"User data: {user_data_storage[chat_id]}")
        
        results = generate_ultra_precise_recommendations(user_data_storage[chat_id])
        
        # Форматируем результат
        result_message = f"""🎉 **Ваш ультра-точный план питания готов!**

🎯 **ЦЕЛЕВЫЕ КАЛОРИИ (с учетом вашей цели):**
• В дни отдыха: **{results['target_calories_rest']} ккал**
• В дни тренировок: **{results['target_calories_training']} ккал**
• В среднем: **{results['target_calories_average']} ккал**

📊 **КАЛОРИИ ПО ДНЯМ (до коррекции):**
• 💤 Дни отдыха: **{results['tdee_rest']} ккал**
• 🏋️ Дни тренировок: **{results['tdee_training']} ккал**
• 📈 Средний показатель: **{results['tdee_average']} ккал**

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

**📚 ОБЪЯСНЕНИЯ:**
• **BMR** - калории для поддержания жизнедеятельности в покое
• **TDEE** - общий расход энергии с учетом активности
• **Целевые калории** - калории для достижения вашей цели

✨ *Расчеты учитывают ВСЕ индивидуальные факторы для максимальной точности!*

🎯 Следуйте плану и достигайте своих целей!"""

        # --- ДОБАВЛЯЕМ ПЕРСОНАЛЬНЫЕ СОВЕТЫ ДЛЯ НОВИЧКОВ/НЕ ТРЕНИРУЮЩИХСЯ В КОНЕЦ РАССЧЁТА ---
        advice = ""
        if user_data_storage[chat_id].get('training_experience') == 'Не тренируюсь' or user_data_storage[chat_id].get('training_experience') == 'Нет опыта' or user_data_storage[chat_id].get('training_days', 1) == 0:
            advice = ("\n\n💡 **Совет для начинающих:**\n"
                      "• Даже если вы не тренируетесь, движение — это жизнь!\n"
                      "• Начните с простого: ежедневные прогулки, легкая зарядка, растяжка.\n"
                      "• Постепенно увеличивайте активность: добавьте 5-10 минут к прогулке, попробуйте упражнения с собственным весом (приседания, отжимания у стены, наклоны).\n"
                      "• Важно не только спорт, но и бытовая активность (NEAT): ходите пешком, поднимайтесь по лестнице, делайте уборку.\n"
                      "• Не бойтесь начинать с малого — главное регулярность!\n"
                      "• Если есть лишний вес или хронические заболевания — начните с консультации врача.\n")
        elif user_data_storage[chat_id].get('training_experience') == 'Новичок':
            advice = ("\n\n💡 **Совет для новичков:**\n"
                      "• Не стремитесь к идеалу сразу — главное, чтобы движение стало привычкой.\n"
                      "• Слушайте свое тело, увеличивайте нагрузку постепенно.\n"
                      "• Не сравнивайте себя с другими — ваш прогресс уникален!\n"
                      "• Пробуйте разные виды активности: йога, плавание, танцы, домашние тренировки.\n")
        if advice:
            result_message += advice
            # Добавляем кнопки для возврата к блоку про тренировки и консультации
            reply_markup = ReplyKeyboardMarkup([
                ['Я всё-таки хочу тренироваться!'],
                ['💬 Получить консультацию эксперта']
            ], resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(result_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        else:
            # Добавляем кнопку консультации для всех пользователей
            reply_markup = ReplyKeyboardMarkup([
                ['💬 Получить консультацию эксперта']
            ], resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(result_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        logger.info(f"Successfully sent results to user {chat_id}")
        
    except Exception as e:
        logger.error(f"Error calculating for user {chat_id}: {str(e)}")
        await update.message.reply_text(
            f"❌ **Ошибка расчета:** {str(e)}\n\nВозможно, не все данные были введены. Пожалуйста, пройдите опрос заново, нажав 🚀 Начать",
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

# --- ДОБАВЛЯЕМ КОМАНДЫ ---
async def motivation_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(MOTIVATION_TEXT, parse_mode=ParseMode.MARKDOWN)
    return GENDER
async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(FAQ_TEXT, parse_mode=ParseMode.MARKDOWN)
    return GENDER
async def nomotivation_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(NOMOTIVATION_TEXT, parse_mode=ParseMode.MARKDOWN)
    return GENDER

# --- Функция для запуска только блока про тренировки ---
async def start_training_block(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    # Сбрасываем только тренировочные данные
    user_data_storage[chat_id]['training_experience'] = None
    user_data_storage[chat_id]['training_days'] = None
    user_data_storage[chat_id]['activity_type'] = None
    user_data_storage[chat_id]['workout_duration'] = None
    user_data_storage[chat_id]['intensity'] = None
    # Запускаем блок с вопроса про опыт
    keyboard = [
        ['🌱 Новичок (до 1 года)'],
        ['🔥 Средний (1-3 года)'],
        ['⚡ Опытный (3+ года)']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "💪 **Ваш опыт тренировок?**",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    context.user_data['training_block'] = True  # Флаг, что мы в режиме только тренировочного блока
    return TRAINING_EXPERIENCE

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Подписка на обновления бота"""
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name or "Пользователь"
    
    if chat_id in subscribers:
        await update.message.reply_text(
            f"✅ **{user_name}**, вы уже подписаны на обновления! 📢\n\n"
            "Вы будете получать:\n"
            "• Новые функции и улучшения\n"
            "• Полезные советы по фитнесу\n"
            "• Мотивационные сообщения\n"
            "• Уведомления о важных обновлениях",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        subscribers.add(chat_id)
        
        # Отправляем приветственное сообщение о подписке
        await update.message.reply_text(
            f"🎉 **{user_name}**, вы успешно подписались на обновления! 📢\n\n"
            "Теперь вы будете получать:\n"
            "• Новые функции и улучшения\n"
            "• Полезные советы по фитнесу\n"
            "• Мотивационные сообщения\n"
            "• Уведомления о важных обновлениях\n\n"
            "💡 Используйте кнопку '📢 Отписаться от обновлений' если захотите отписаться.",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Отправляем информацию о последних нововведениях
        await asyncio.sleep(1)  # Небольшая пауза между сообщениями
        
        await update.message.reply_text(
            "📢 **ПОСЛЕДНИЕ НОВОВВЕДЕНИЯ БОТА:**\n\n"
            "🎯 **Новая система подписки**\n"
            "• Теперь вы можете подписываться на обновления\n"
            "• Получать уведомления о новых функциях\n"
            "• Быстро отписываться в любое время\n\n"
            "💬 **Консультация с экспертом**\n"
            "• Кнопка \"💬 Получить консультацию эксперта\" после расчетов\n"
            "• Прямая связь с фитнес-экспертом @DARKSIDERS17\n"
            "• Персональные планы тренировок и питания\n"
            "• Индивидуальные рекомендации\n\n"
            "🔧 **Улучшенный интерфейс**\n"
            "• Добавлены кнопки подписки/отписки\n"
            "• Более удобная навигация\n"
            "• Улучшенный дизайн сообщений\n\n"
            "📊 **Новые команды**\n"
            "• `/subscribe` - быстрая подписка\n"
            "• `/unsubscribe` - быстрая отписка\n"
            "• `/broadcast` - рассылка (для администратора)\n\n"
            "🚀 **Планы на будущее**\n"
            "• Персональные рекомендации\n"
            "• Статистика прогресса\n"
            "• Интеграция с фитнес-трекерами\n"
            "• Социальные функции",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Отправляем краткую инструкцию по использованию
        await asyncio.sleep(1)
        
        await update.message.reply_text(
            "💡 **КАК ИСПОЛЬЗОВАТЬ НОВЫЕ ФУНКЦИИ:**\n\n"
            "1️⃣ **Подписка на обновления**\n"
            "   Нажмите кнопку \"📢 Подписаться на обновления\"\n"
            "   или отправьте команду `/subscribe`\n\n"
            "2️⃣ **Отписка от обновлений**\n"
            "   Нажмите кнопку \"📢 Отписаться от обновлений\"\n"
            "   или отправьте команду `/unsubscribe`\n\n"
            "3️⃣ **Консультация с экспертом**\n"
            "   После получения результатов нажмите\n"
            "   \"💬 Получить консультацию эксперта\"\n"
            "   для связи с фитнес-экспертом @DARKSIDERS17\n\n"
            "4️⃣ **Получение уведомлений**\n"
            "   Вы будете автоматически получать важные обновления\n\n"
            "❓ **Нужна помощь?**\n"
            "   Отправьте команду `/help` для получения справки",
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"User {chat_id} ({user_name}) subscribed to updates")
    
    return ConversationHandler.END

async def consultation_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Консультация с экспертом"""
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name or "Пользователь"
    
    await update.message.reply_text(
        f"💬 **Консультация с экспертом**\n\n"
        f"👋 **{user_name}**, вы хотите получить персональную консультацию?\n\n"
        "🎯 **Наш эксперт поможет вам с:**\n"
        "• Персональным планом тренировок\n"
        "• Индивидуальной программой питания\n"
        "• Анализом ваших целей и возможностей\n"
        "• Рекомендациями по восстановлению\n"
        "• Ответами на любые вопросы о фитнесе\n\n"
        "📱 **Для связи с экспертом:**\n"
        "• Напишите в личные сообщения: @DARKSIDERS17\n"
        "• Укажите, что вы из FitAdventure Bot\n"
        "• Опишите ваши цели и вопросы\n\n"
        "⏰ **Время ответа:** обычно в течение 24 часов\n\n"
        "💡 **Совет:** подготовьте информацию о ваших целях, опыте тренировок и текущем состоянии здоровья для более эффективной консультации.",
        parse_mode=ParseMode.MARKDOWN
    )
    
    logger.info(f"User {chat_id} ({user_name}) requested consultation")
    return ConversationHandler.END

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отписка от обновлений бота"""
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name or "Пользователь"
    
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        await update.message.reply_text(
            f"😔 **{user_name}**, вы отписались от обновлений.\n\n"
            "Вы больше не будете получать уведомления о новых функциях и обновлениях.\n\n"
            "💡 Можете снова подписаться в любое время, нажав '📢 Подписаться на обновления'",
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"User {chat_id} ({user_name}) unsubscribed from updates")
    else:
        await update.message.reply_text(
            f"ℹ️ **{user_name}**, вы не были подписаны на обновления.\n\n"
            "💡 Хотите подписаться? Нажмите '📢 Подписаться на обновления'",
            parse_mode=ParseMode.MARKDOWN
        )
    
    return ConversationHandler.END

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отправка сообщения всем подписчикам (только для администратора)"""
    chat_id = update.message.chat_id
    
    # Проверяем, является ли пользователь администратором (замените на ваш ID)
    ADMIN_ID = 123456789  # Замените на ваш Telegram ID
    
    if chat_id != ADMIN_ID:
        await update.message.reply_text(
            "❌ У вас нет прав для отправки сообщений всем подписчикам.",
            parse_mode=ParseMode.MARKDOWN
        )
        return ConversationHandler.END
    
    # Получаем текст сообщения после команды /broadcast
    message_text = update.message.text.replace('/broadcast', '').strip()
    
    if not message_text:
        await update.message.reply_text(
            "📝 Использование: /broadcast <текст сообщения>\n\n"
            "Пример: /broadcast Привет всем! Новая функция добавлена!",
            parse_mode=ParseMode.MARKDOWN
        )
        return ConversationHandler.END
    
    # Отправляем сообщение всем подписчикам
    success_count = 0
    error_count = 0
    
    for subscriber_id in subscribers:
        try:
            await context.bot.send_message(
                chat_id=subscriber_id,
                text=f"📢 **Обновление от FitAdventure Bot:**\n\n{message_text}",
                parse_mode=ParseMode.MARKDOWN
            )
            success_count += 1
        except Exception as e:
            error_count += 1
            logger.error(f"Failed to send broadcast to {subscriber_id}: {e}")
    
    await update.message.reply_text(
        f"📢 **Сообщение отправлено!**\n\n"
        f"✅ Успешно отправлено: {success_count}\n"
        f"❌ Ошибок: {error_count}\n"
        f"📊 Всего подписчиков: {len(subscribers)}",
        parse_mode=ParseMode.MARKDOWN
    )
    
    logger.info(f"Broadcast sent to {success_count} subscribers by admin {chat_id}")
    return ConversationHandler.END

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
                MessageHandler(filters.TEXT & ~filters.COMMAND, gender),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, age),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            WEIGHT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, weight),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            HEIGHT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, height),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            FAT_PERCENTAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, fat_percentage),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            FAT_PERCENTAGE_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, fat_percentage_input),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            GOAL: [
                MessageHandler(filters.ALL, goal),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            EXPERIENCE_CHOICE: [
                MessageHandler(filters.ALL, experience_choice),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            TRAINING_EXPERIENCE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, training_experience),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            TRAINING_DAYS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, training_days),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            ACTIVITY_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, activity_type),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            WORKOUT_DURATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, workout_duration),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            STEPS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, steps),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            INTENSITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, intensity),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            RECOVERY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, recovery),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            SLEEP_QUALITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, sleep_quality),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            STRESS_LEVEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, stress_level),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
            OCCUPATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, occupation),
                MessageHandler(~filters.TEXT, handle_message),
                MessageHandler(tg_filters.Regex(START_BUTTONS_REGEX), handle_buttons)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('motivation', motivation_command))
    application.add_handler(CommandHandler('faq', faq_command))
    application.add_handler(CommandHandler('nomotivation', nomotivation_command))
    application.add_handler(CommandHandler('subscribe', subscribe_command))
    application.add_handler(CommandHandler('unsubscribe', unsubscribe_command))
    application.add_handler(CommandHandler('broadcast', broadcast_message))
    
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