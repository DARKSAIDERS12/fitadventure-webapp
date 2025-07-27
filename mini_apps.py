#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мини-приложения для FitAdventure Bot
"""

import json
import datetime
from pathlib import Path
from products_database import (
    PRODUCTS_DATABASE, 
    get_products_by_goal, 
    get_products_by_category,
    search_product,
    format_product_info,
    get_recommended_products
)

# Файл для хранения данных пользователей
USER_DATA_FILE = "user_mini_apps_data.json"

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

# === МИНИ-ПРИЛОЖЕНИЕ: БАЗА ПРОДУКТОВ ===
async def show_products_menu(update, context):
    """Показать меню базы продуктов"""
    keyboard = [
        ['🥩 Белки', '🍞 Углеводы'],
        ['🧈 Жиры', '🔍 Поиск продукта'],
        ['📊 Рекомендации', '🔙 Назад']
    ]
    
    text = """🍎 **База продуктов FitAdventure**

Выберите категорию продуктов или найдите конкретный продукт:

🥩 **Белки** - мясо, рыба, яйца, молочные продукты
🍞 **Углеводы** - крупы, овощи, фрукты, хлеб
🧈 **Жиры** - орехи, масла, семена
🔍 **Поиск** - найти продукт по названию
📊 **Рекомендации** - продукты под вашу цель"""
    
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return 19  # PRODUCTS_MENU state

async def show_products_category(update, context):
    """Показать продукты по категории"""
    text = update.message.text
    chat_id = str(update.message.chat_id)
    
    # Получаем цель пользователя
    user_data = load_user_data()
    user_goal = user_data.get(chat_id, {}).get('goal', 'поддержание')
    
    category_map = {
        '🥩 Белки': 'белки',
        '🍞 Углеводы': 'углеводы', 
        '🧈 Жиры': 'жиры'
    }
    
    if text in category_map:
        category = category_map[text]
        products = get_products_by_category(user_goal, category)
        
        if not products:
            await update.message.reply_text(f"❌ Продукты для категории '{category}' не найдены")
            return 19  # PRODUCTS_MENU state
        
        # Показываем первые 10 продуктов
        result = f"🍎 **{category.title()}** для цели: **{user_goal.replace('_', ' ').title()}**\n\n"
        
        for i, (name, data) in enumerate(list(products.items())[:10], 1):
            result += f"{i}. **{name}** - {data['калории']} ккал/100г\n"
            result += f"   🥩{data['белки']}г 🧈{data['жиры']}г 🍞{data['углеводы']}г\n\n"
        
        if len(products) > 10:
            result += f"... и еще {len(products) - 10} продуктов\n"
        
        result += "\n💡 Напишите название продукта для подробной информации"
        
        await update.message.reply_text(result, parse_mode='Markdown')
        return 19  # PRODUCTS_MENU state
    
    return 19  # PRODUCTS_MENU state

async def search_product_handler(update, context):
    """Обработчик поиска продукта"""
    text = update.message.text
    
    if text == '🔍 Поиск продукта':
        await update.message.reply_text("🔍 Введите название продукта для поиска:")
        return 20  # PRODUCT_SEARCH state
    
    # Поиск продукта
    results = search_product(text)
    
    if not results:
        await update.message.reply_text(f"❌ Продукт '{text}' не найден в базе")
        return 19  # PRODUCTS_MENU state
    
    # Показываем результаты
    result = f"🔍 **Результаты поиска для '{text}':**\n\n"
    
    for goal, categories in results.items():
        result += f"🎯 **{goal.replace('_', ' ').title()}:**\n"
        for category, products in categories.items():
            result += f"  📂 {category.title()}:\n"
            for name, data in products.items():
                result += f"    • {name} - {data['калории']} ккал/100г\n"
        result += "\n"
    
    result += "💡 Напишите точное название продукта для подробной информации"
    
    await update.message.reply_text(result, parse_mode='Markdown')
    return 19  # PRODUCTS_MENU state

async def show_product_details(update, context):
    """Показать подробную информацию о продукте"""
    product_name = update.message.text
    results = search_product(product_name)
    
    if not results:
        await update.message.reply_text(f"❌ Продукт '{product_name}' не найден")
        return 19  # PRODUCTS_MENU state
    
    # Ищем точное совпадение
    exact_match = None
    for goal, categories in results.items():
        for category, products in categories.items():
            for name, data in products.items():
                if name.lower() == product_name.lower():
                    exact_match = (name, data, goal, category)
                    break
    
    if exact_match:
        name, data, goal, category = exact_match
        result = format_product_info(name, data)
        result += f"\n\n🎯 **Рекомендуется для:** {goal.replace('_', ' ').title()}"
        result += f"\n📂 **Категория:** {category.title()}"
        
        # Добавляем рекомендации по употреблению
        if goal == "похудение":
            result += "\n\n💡 **Рекомендации:** Отличный выбор для похудения!"
        elif goal == "набор_массы":
            result += "\n\n💡 **Рекомендации:** Отлично подходит для набора массы!"
        else:
            result += "\n\n💡 **Рекомендации:** Сбалансированный продукт для поддержания формы!"
        
        await update.message.reply_text(result, parse_mode='Markdown')
    else:
        # Показываем все найденные варианты
        result = f"🔍 **Найдено несколько вариантов для '{product_name}':**\n\n"
        for goal, categories in results.items():
            for category, products in categories.items():
                for name, data in products.items():
                    result += f"• **{name}** ({goal.replace('_', ' ').title()})\n"
                    result += f"  {data['калории']} ккал/100г\n\n"
        
        result += "💡 Напишите точное название для подробной информации"
        await update.message.reply_text(result, parse_mode='Markdown')
    
    return 19  # PRODUCTS_MENU state

async def show_recommendations(update, context):
    """Показать рекомендации продуктов"""
    text = update.message.text
    
    if text != '📊 Рекомендации':
        return 19  # PRODUCTS_MENU state
    
    chat_id = str(update.message.chat_id)
    user_data = load_user_data()
    user_goal = user_data.get(chat_id, {}).get('goal', 'поддержание')
    
    result = f"📊 **Рекомендуемые продукты для {user_goal.replace('_', ' ').title()}:**\n\n"
    
    categories = ['белки', 'углеводы', 'жиры']
    for category in categories:
        recommended = get_recommended_products(user_goal, category, 3)
        if recommended:
            result += f"**{category.title()}:**\n"
            for name, data in recommended:
                result += f"• {name} - {data['калории']} ккал/100г\n"
            result += "\n"
    
    result += "💡 Эти продукты оптимально подходят для вашей цели!"
    
    await update.message.reply_text(result, parse_mode='Markdown')
    return 19  # PRODUCTS_MENU state

# === МИНИ-ПРИЛОЖЕНИЕ: ТРЕКЕР ВОДЫ ===
async def show_water_tracker(update, context):
    """Показать трекер воды"""
    chat_id = str(update.message.chat_id)
    user_data = load_user_data()
    
    today = datetime.date.today().isoformat()
    water_data = user_data.get(chat_id, {}).get('water', {})
    today_water = water_data.get(today, 0)
    
    # Рекомендуемая норма воды (в мл)
    recommended_water = 2500  # 2.5 литра в день
    
    progress = min(today_water / recommended_water * 100, 100)
    progress_bar = "💧" * int(progress / 10) + "⬜" * (10 - int(progress / 10))
    
    keyboard = [
        ['💧 +250мл', '💧 +500мл'],
        ['💧 +1000мл', '🔄 Сбросить'],
        ['📊 Статистика', '🔙 Назад']
    ]
    
    text = f"""💧 **Трекер воды**

Сегодня выпито: **{today_water}мл** из **{recommended_water}мл**
Прогресс: {progress_bar} **{progress:.1f}%**

{get_water_motivation(progress)}

Выберите количество воды для добавления:"""
    
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return "WATER_TRACKER"

def get_water_motivation(progress):
    """Получить мотивационное сообщение"""
    if progress >= 100:
        return "🎉 Отлично! Вы достигли дневной нормы воды!"
    elif progress >= 80:
        return "👍 Почти достигли цели! Осталось совсем немного!"
    elif progress >= 60:
        return "💪 Хорошо идете! Продолжайте в том же духе!"
    elif progress >= 40:
        return "🚰 Не забывайте пить воду регулярно!"
    elif progress >= 20:
        return "💧 Начните день с воды! Вашему организму это нужно!"
    else:
        return "🌊 Время пить воду! Начните прямо сейчас!"

async def add_water(update, context):
    """Добавить воду в трекер"""
    text = update.message.text
    chat_id = str(update.message.chat_id)
    
    water_amounts = {
        '💧 +250мл': 250,
        '💧 +500мл': 500,
        '💧 +1000мл': 1000
    }
    
    if text in water_amounts:
        amount = water_amounts[text]
        
        user_data = load_user_data()
        if chat_id not in user_data:
            user_data[chat_id] = {}
        if 'water' not in user_data[chat_id]:
            user_data[chat_id]['water'] = {}
        
        today = datetime.date.today().isoformat()
        if today not in user_data[chat_id]['water']:
            user_data[chat_id]['water'][today] = 0
        
        user_data[chat_id]['water'][today] += amount
        save_user_data(user_data)
        
        new_total = user_data[chat_id]['water'][today]
        recommended_water = 2500
        progress = min(new_total / recommended_water * 100, 100)
        
        progress_bar = "💧" * int(progress / 10) + "⬜" * (10 - int(progress / 10))
        
        result = f"✅ Добавлено **{amount}мл** воды!\n\n"
        result += f"Всего сегодня: **{new_total}мл** из **{recommended_water}мл**\n"
        result += f"Прогресс: {progress_bar} **{progress:.1f}%**\n\n"
        result += get_water_motivation(progress)
        
        await update.message.reply_text(result, parse_mode='Markdown')
        return "WATER_TRACKER"
    
    elif text == '🔄 Сбросить':
        user_data = load_user_data()
        if chat_id in user_data and 'water' in user_data[chat_id]:
            today = datetime.date.today().isoformat()
            user_data[chat_id]['water'][today] = 0
            save_user_data(user_data)
        
        await update.message.reply_text("🔄 Счетчик воды сброшен!")
        return "WATER_TRACKER"
    
    elif text == '📊 Статистика':
        await show_water_statistics(update, context)
        return "WATER_TRACKER"
    
    return "WATER_TRACKER"

async def show_water_statistics(update, context):
    """Показать статистику воды"""
    chat_id = str(update.message.chat_id)
    user_data = load_user_data()
    water_data = user_data.get(chat_id, {}).get('water', {})
    
    if not water_data:
        await update.message.reply_text("📊 Статистика воды пуста. Начните отслеживать потребление воды!")
        return "WATER_TRACKER"
    
    # Последние 7 дней
    today = datetime.date.today()
    stats = []
    
    for i in range(7):
        date = today - datetime.timedelta(days=i)
        date_str = date.isoformat()
        amount = water_data.get(date_str, 0)
        stats.append((date, amount))
    
    result = "📊 **Статистика воды за последние 7 дней:**\n\n"
    
    for date, amount in reversed(stats):
        day_name = date.strftime("%A")  # День недели
        date_str = date.strftime("%d.%m")
        progress = min(amount / 2500 * 100, 100)
        progress_bar = "💧" * int(progress / 20) + "⬜" * (5 - int(progress / 20))
        
        result += f"**{day_name}** ({date_str}): {amount}мл {progress_bar} {progress:.1f}%\n"
    
    result += "\n💡 Рекомендуемая норма: 2500мл в день"
    
    await update.message.reply_text(result, parse_mode='Markdown')
    return "WATER_TRACKER"

# === МИНИ-ПРИЛОЖЕНИЕ: ТРЕКЕР ЦЕЛЕЙ ===
async def show_goals_tracker(update, context):
    """Показать трекер целей"""
    chat_id = str(update.message.chat_id)
    user_data = load_user_data()
    
    goals = user_data.get(chat_id, {}).get('goals', {})
    
    keyboard = [
        ['📝 Добавить цель', '✅ Отметить прогресс'],
        ['📊 Мои цели', '🗑️ Удалить цель'],
        ['🔙 Назад']
    ]
    
    text = "🎯 **Трекер целей**\n\n"
    
    if goals:
        text += "Ваши текущие цели:\n"
        for i, (goal_id, goal_data) in enumerate(goals.items(), 1):
            progress = goal_data.get('progress', 0)
            target = goal_data.get('target', 0)
            if target > 0:
                progress_percent = min(progress / target * 100, 100)
            else:
                progress_percent = 0
            
            text += f"{i}. **{goal_data['name']}**\n"
            text += f"   Прогресс: {progress}/{target} ({progress_percent:.1f}%)\n\n"
    else:
        text += "У вас пока нет целей. Добавьте первую цель!"
    
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return "GOALS_TRACKER"

async def add_goal(update, context):
    """Добавить новую цель"""
    text = update.message.text
    
    if text == '📝 Добавить цель':
        await update.message.reply_text(
            "📝 Введите название цели (например: 'Сбросить 5 кг'):"
        )
        return "ADD_GOAL_NAME"
    
    return "GOALS_TRACKER"

async def handle_goal_name(update, context):
    """Обработать название цели"""
    goal_name = update.message.text
    chat_id = str(update.message.chat_id)
    
    # Сохраняем название цели во временные данные
    user_data = load_user_data()
    if chat_id not in user_data:
        user_data[chat_id] = {}
    if 'temp_goal' not in user_data[chat_id]:
        user_data[chat_id]['temp_goal'] = {}
    
    user_data[chat_id]['temp_goal']['name'] = goal_name
    save_user_data(user_data)
    
    await update.message.reply_text(
        f"📊 Введите целевое значение для '{goal_name}' (например: 5 для 5 кг):"
    )
    return "ADD_GOAL_TARGET"

async def handle_goal_target(update, context):
    """Обработать целевое значение"""
    try:
        target = float(update.message.text)
        chat_id = str(update.message.chat_id)
        
        user_data = load_user_data()
        temp_goal = user_data.get(chat_id, {}).get('temp_goal', {})
        goal_name = temp_goal.get('name', 'Новая цель')
        
        # Создаем новую цель
        if 'goals' not in user_data[chat_id]:
            user_data[chat_id]['goals'] = {}
        
        goal_id = str(len(user_data[chat_id]['goals']) + 1)
        user_data[chat_id]['goals'][goal_id] = {
            'name': goal_name,
            'target': target,
            'progress': 0,
            'created': datetime.date.today().isoformat()
        }
        
        # Удаляем временные данные
        if 'temp_goal' in user_data[chat_id]:
            del user_data[chat_id]['temp_goal']
        
        save_user_data(user_data)
        
        await update.message.reply_text(
            f"✅ Цель '{goal_name}' с целевым значением {target} добавлена!"
        )
        
        return await show_goals_tracker(update, context)
        
    except ValueError:
        await update.message.reply_text("❌ Пожалуйста, введите число!")
        return "ADD_GOAL_TARGET"

# === ГЛАВНОЕ МЕНЮ МИНИ-ПРИЛОЖЕНИЙ ===
async def show_mini_apps_menu(update, context):
    """Показать главное меню мини-приложений"""
    keyboard = [
        ['🍎 База продуктов', '💧 Трекер воды'],
        ['🎯 Трекер целей', '📊 Статистика'],
        ['🔙 Главное меню']
    ]
    
    text = """🎮 **Мини-приложения FitAdventure**

Выберите нужное приложение:

🍎 **База продуктов** - калорийность и БЖУ продуктов
💧 **Трекер воды** - отслеживание потребления воды
🎯 **Трекер целей** - отслеживание прогресса к целям
📊 **Статистика** - ваша статистика и прогресс"""
    
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return 18  # MINI_APPS_MENU state

async def handle_mini_apps_navigation(update, context):
    """Обработка навигации в мини-приложениях"""
    text = update.message.text
    
    if text == '🍎 База продуктов':
        return await show_products_menu(update, context)
    elif text == '💧 Трекер воды':
        return await show_water_tracker(update, context)
    elif text == '🎯 Трекер целей':
        return await show_goals_tracker(update, context)
    elif text == '📊 Статистика':
        return await show_general_statistics(update, context)
    elif text == '🔙 Главное меню':
        return await return_to_main_menu(update, context)
    
    return 18  # MINI_APPS_MENU state

async def show_general_statistics(update, context):
    """Показать общую статистику"""
    chat_id = str(update.message.chat_id)
    user_data = load_user_data()
    
    text = "📊 **Ваша статистика**\n\n"
    
    # Статистика воды
    water_data = user_data.get(chat_id, {}).get('water', {})
    if water_data:
        total_water_days = len(water_data)
        total_water = sum(water_data.values())
        avg_water = total_water / total_water_days if total_water_days > 0 else 0
        
        text += f"💧 **Вода:**\n"
        text += f"   Дней отслеживания: {total_water_days}\n"
        text += f"   Всего выпито: {total_water}мл\n"
        text += f"   Среднее в день: {avg_water:.0f}мл\n\n"
    
    # Статистика целей
    goals = user_data.get(chat_id, {}).get('goals', {})
    if goals:
        active_goals = len(goals)
        completed_goals = sum(1 for goal in goals.values() 
                            if goal.get('progress', 0) >= goal.get('target', 0))
        
        text += f"🎯 **Цели:**\n"
        text += f"   Активных целей: {active_goals}\n"
        text += f"   Достигнутых: {completed_goals}\n\n"
    
    if not water_data and not goals:
        text += "У вас пока нет данных для статистики.\n"
        text += "Начните использовать мини-приложения!"
    
    keyboard = [['🔙 Назад к приложениям']]
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return "STATISTICS"

async def return_to_main_menu(update, context):
    """Вернуться в главное меню"""
    # Импортируем функцию из основного файла
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from main import return_to_main_menu as main_return_to_main_menu
        return await main_return_to_main_menu(update, context)
    except ImportError:
        # Если не удалось импортировать, возвращаемся к начальному состоянию
        return "GENDER" 