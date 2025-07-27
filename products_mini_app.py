#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенное мини-приложение "База продуктов" для FitAdventure Bot
Современный дизайн с детальной информацией о продуктах
"""

import json
import datetime
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Импортируем улучшенную базу данных
from products_database import PRODUCTS_DATABASE, get_products_by_goal, get_products_by_category, search_product, format_product_info, get_category_description

# Файл для хранения данных пользователей
USER_DATA_FILE = "user_products_data.json"

def load_user_data():
    """Загрузка данных пользователей"""
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    """Сохранение данных пользователей"""
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_goal(chat_id):
    """Получить цель пользователя"""
    user_data = load_user_data()
    return user_data.get(str(chat_id), {}).get('goal', 'поддержание')

# === ГЛАВНОЕ МЕНЮ МИНИ-ПРИЛОЖЕНИЯ ===
async def show_products_mini_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню мини-приложения базы продуктов"""
    chat_id = update.effective_chat.id
    user_goal = get_user_goal(chat_id)
    
    # Создаем современный интерфейс с обычными кнопками
    text = f"""🍎 **База продуктов FitAdventure**
*мини-приложение*

🎯 **Ваша цель:** {user_goal.replace('_', ' ').title()}

Выберите категорию продуктов для просмотра:"""
    
    # Создаем обычные кнопки для категорий
    keyboard = [
        ['🌾 Сложные углеводы', '⚡ Простые углеводы'],
        ['🥩 Белки', '🫒 Ненасыщенные жиры'],
        ['🧈 Насыщенные жиры', '🌿 Клетчатка'],
        ['🔍 Поиск продукта', '📊 Рекомендации'],
        ['🔙 Главное меню']
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return "PRODUCTS_MAIN"

# === ОБРАБОТЧИКИ КНОПОК ===
async def handle_products_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик навигации в мини-приложении"""
    text = update.message.text
    chat_id = update.effective_chat.id
    user_goal = get_user_goal(chat_id)
    
    # Обработка категорий
    category_map = {
        '🌾 Сложные углеводы': 'сложные_углеводы',
        '⚡ Простые углеводы': 'простые_углеводы',
        '🥩 Белки': 'белки',
        '🫒 Ненасыщенные жиры': 'ненасыщенные_жиры',
        '🧈 Насыщенные жиры': 'насыщенные_жиры',
        '🌿 Клетчатка': 'клетчатка'
    }
    
    if text in category_map:
        category = category_map[text]
        return await show_category_products(update, context, category, user_goal)
    
    elif text == '🔍 Поиск продукта':
        return await show_search_interface(update, context)
    
    elif text == '📊 Рекомендации':
        return await show_recommendations(update, context, user_goal)
    
    elif text == '🔙 Главное меню':
        return await return_to_main_menu(update, context)
    
    elif text == '🔙 Назад к категориям':
        return await show_products_mini_app(update, context)
    
    # Если это не кнопка, возможно это поиск продукта
    else:
        return await handle_product_search(update, context)
    
    return "PRODUCTS_MAIN"

async def show_category_products(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, user_goal: str):
    """Показать продукты по категории"""
    products = PRODUCTS_DATABASE.get(user_goal, {}).get(category, {})
    
    if not products:
        text = f"❌ Продукты для категории '{category.replace('_', ' ').title()}' не найдены"
        keyboard = [['🔙 Назад к категориям']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)
        return "PRODUCTS_MAIN"
    
    # Получаем описание категории
    category_description = get_category_description(category)
    
    # Форматируем название категории
    category_names = {
        "сложные_углеводы": "🌾 Сложные углеводы",
        "простые_углеводы": "⚡ Простые углеводы", 
        "белки": "🥩 Белки",
        "ненасыщенные_жиры": "🫒 Ненасыщенные жиры",
        "насыщенные_жиры": "🧈 Насыщенные жиры",
        "клетчатка": "🌿 Клетчатка"
    }
    
    category_display = category_names.get(category, category.replace('_', ' ').title())
    
    text = f"{category_display}\n"
    text += f"🎯 Для цели: **{user_goal.replace('_', ' ').title()}**\n\n"
    text += f"{category_description}\n\n"
    text += "**Доступные продукты:**\n"
    
    # Показываем все продукты в категории с улучшенным форматированием
    for i, (name, data) in enumerate(products.items(), 1):
        text += f"{i}. **{name.title()}** - {data['калории']} ккал/100г\n"
        text += f"   🥩{data['белки']}г 🧈{data['жиры']}г 🍞{data['углеводы']}г"
        if 'клетчатка' in data:
            text += f" 🌾{data['клетчатка']}г"
        text += "\n"
        if 'описание' in data:
            text += f"   💡 {data['описание']}\n"
        text += "\n"
    
    text += "💡 **Напишите название продукта для подробной информации**"
    
    keyboard = [['🔙 Назад к категориям']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return "PRODUCTS_CATEGORY"

async def show_product_details(update: Update, context: ContextTypes.DEFAULT_TYPE, product_name: str, user_goal: str):
    """Показать подробную информацию о продукте"""
    # Ищем продукт во всех категориях
    product_data = None
    product_category = None
    
    for category, products in PRODUCTS_DATABASE.get(user_goal, {}).items():
        if product_name.lower() in [name.lower() for name in products.keys()]:
            # Находим точное название
            for name, data in products.items():
                if product_name.lower() in name.lower():
                    product_data = data
                    product_category = category
                    product_name = name  # Используем точное название
                    break
            if product_data:
                break
    
    if not product_data:
        text = f"❌ Продукт '{product_name}' не найден в базе данных"
        keyboard = [['🔙 Назад к категориям']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)
        return "PRODUCTS_MAIN"
    
    # Форматируем информацию о продукте
    result = format_product_info(product_name, product_data)
    
    # Добавляем рекомендации
    category_names = {
        "сложные_углеводы": "🌾 Сложные углеводы",
        "простые_углеводы": "⚡ Простые углеводы", 
        "белки": "🥩 Белки",
        "ненасыщенные_жиры": "🫒 Ненасыщенные жиры",
        "насыщенные_жиры": "🧈 Насыщенные жиры",
        "клетчатка": "🌿 Клетчатка"
    }
    
    result += f"\n📂 **Категория:** {category_names.get(product_category, product_category)}\n"
    result += f"🎯 **Рекомендуется для:** {user_goal.replace('_', ' ').title()}\n\n"
    
    # Добавляем советы по употреблению в зависимости от цели
    if user_goal == "похудение":
        if product_category in ["сложные_углеводы", "белки"]:
            result += "💡 **Совет:** Отличный выбор для похудения! Контролируйте порции и ешьте в первой половине дня."
        elif product_category == "клетчатка":
            result += "💡 **Совет:** Отлично для похудения! Клетчатка надолго насыщает и улучшает пищеварение."
        else:
            result += "💡 **Совет:** Употребляйте умеренно для похудения."
    elif user_goal == "набор_массы":
        if product_category in ["сложные_углеводы", "белки"]:
            result += "💡 **Совет:** Отлично для набора массы! Можете увеличить порции, особенно после тренировки."
        elif product_category in ["ненасыщенные_жиры", "насыщенные_жиры"]:
            result += "💡 **Совет:** Полезные жиры для набора массы! Добавляйте в рацион умеренно."
        else:
            result += "💡 **Совет:** Хороший выбор для набора массы!"
    else:  # поддержание
        result += "💡 **Совет:** Сбалансированный продукт для поддержания формы! Подходит для ежедневного употребления."
    
    keyboard = [['🔙 Назад к категориям']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(result, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return "PRODUCT_DETAILS"

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

async def show_recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE, user_goal: str):
    """Показать рекомендации продуктов"""
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

async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вернуться в главное меню"""
    text = "🏠 Возвращаемся в главное меню..."
    keyboard = [['🚀 Начать', '❓ Помощь'], ['🎮 Мини-приложения', '📊 О боте']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(text, reply_markup=reply_markup)
    return "GENDER"  # Возвращаемся к начальному состоянию

# === ОБРАБОТЧИК ПОИСКА ===
async def handle_product_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик поиска продуктов"""
    product_name = update.message.text
    chat_id = update.effective_chat.id
    user_goal = get_user_goal(chat_id)
    
    results = search_product(product_name)
    
    if not results:
        text = f"❌ Продукт '{product_name}' не найден в базе данных\n\n"
        text += "💡 **Попробуйте:**\n"
        text += "• Проверить правильность написания\n"
        text += "• Использовать более общие названия\n"
        text += "• Поискать в категориях продуктов"
        
        keyboard = [['🔙 Назад к категориям']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)
        return "PRODUCTS_MAIN"
    
    # Показываем результаты поиска
    text = f"🔍 **Результаты поиска для '{product_name}':**\n\n"
    
    found_products = []
    
    for goal, categories in results.items():
        if goal == user_goal:  # Показываем только для цели пользователя
            for category, products in categories.items():
                category_names = {
                    "сложные_углеводы": "🌾 Сложные углеводы",
                    "простые_углеводы": "⚡ Простые углеводы", 
                    "белки": "🥩 Белки",
                    "ненасыщенные_жиры": "🫒 Ненасыщенные жиры",
                    "насыщенные_жиры": "🧈 Насыщенные жиры",
                    "клетчатка": "🌿 Клетчатка"
                }
                
                text += f"**{category_names.get(category, category)}:**\n"
                for name, data in products.items():
                    text += f"• {name.title()} - {data['калории']} ккал/100г\n"
                    if 'описание' in data:
                        text += f"  💡 {data['описание']}\n"
                    found_products.append((name, data, category))
                text += "\n"
    
    if not found_products:
        text += f"❌ Для вашей цели '{user_goal}' продукт '{product_name}' не найден"
    else:
        text += "💡 **Напишите точное название продукта для подробной информации**"
    
    keyboard = [['🔙 Назад к категориям']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return "PRODUCTS_MAIN" 