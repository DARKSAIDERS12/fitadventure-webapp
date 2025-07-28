#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обработчики команд FitAdventure Bot
Оптимизированные обработчики с улучшенной структурой
"""

import logging
from typing import Dict, Any
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import States, Keyboards, Messages, CalculationConstants
from calculations import generate_ultra_precise_recommendations

logger = logging.getLogger(__name__)

# Глобальное хранилище данных пользователей
user_data_storage: Dict[int, Dict[str, Any]] = {}

class InputValidator:
    """Класс для валидации пользовательского ввода"""
    
    @staticmethod
    def validate_age(text: str) -> int:
        """Валидация возраста"""
        try:
            age = int(text)
            if not (CalculationConstants.MIN_AGE <= age <= CalculationConstants.MAX_AGE):
                raise ValueError
            return age
        except ValueError:
            raise ValueError(f"Введите корректный возраст (число от {CalculationConstants.MIN_AGE} до {CalculationConstants.MAX_AGE})")
    
    @staticmethod
    def validate_weight(text: str) -> float:
        """Валидация веса"""
        try:
            weight = float(text)
            if not (CalculationConstants.MIN_WEIGHT <= weight <= CalculationConstants.MAX_WEIGHT):
                raise ValueError
            return weight
        except ValueError:
            raise ValueError(f"Введите корректный вес (число от {CalculationConstants.MIN_WEIGHT} до {CalculationConstants.MAX_WEIGHT} кг)")
    
    @staticmethod
    def validate_height(text: str) -> float:
        """Валидация роста"""
        try:
            height = float(text)
            if not (CalculationConstants.MIN_HEIGHT <= height <= CalculationConstants.MAX_HEIGHT):
                raise ValueError
            return height
        except ValueError:
            raise ValueError(f"Введите корректный рост (число от {CalculationConstants.MIN_HEIGHT} до {CalculationConstants.MAX_HEIGHT} см)")
    
    @staticmethod
    def validate_fat_percentage(text: str) -> float:
        """Валидация процента жира"""
        try:
            fat_percent = float(text)
            if not (CalculationConstants.MIN_FAT_PERCENT <= fat_percent <= CalculationConstants.MAX_FAT_PERCENT):
                raise ValueError
            return fat_percent
        except ValueError:
            raise ValueError(f"Введите корректный процент жира (число от {CalculationConstants.MIN_FAT_PERCENT} до {CalculationConstants.MAX_FAT_PERCENT})")
    
    @staticmethod
    def validate_steps(text: str) -> int:
        """Валидация количества шагов"""
        try:
            steps = int(text)
            if not (CalculationConstants.MIN_STEPS <= steps <= CalculationConstants.MAX_STEPS):
                raise ValueError
            return steps
        except ValueError:
            raise ValueError(f"Введите корректное количество шагов (от {CalculationConstants.MIN_STEPS} до {CalculationConstants.MAX_STEPS})")
    
    @staticmethod
    def validate_workout_duration(text: str) -> int:
        """Валидация продолжительности тренировки"""
        try:
            duration = int(text)
            if not (CalculationConstants.MIN_WORKOUT_DURATION <= duration <= CalculationConstants.MAX_WORKOUT_DURATION):
                raise ValueError
            return duration
        except ValueError:
            raise ValueError(f"Введите корректную продолжительность (от {CalculationConstants.MIN_WORKOUT_DURATION} до {CalculationConstants.MAX_WORKOUT_DURATION} минут)")

class MessageFormatter:
    """Класс для форматирования сообщений"""
    
    @staticmethod
    def format_results_message(results: Dict[str, Any]) -> str:
        """Форматирование результатов расчета"""
        if results['has_training_experience']:
            return f"""🎉 **Ваш ультра-точный план питания готов!**

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
            return f"""🎉 **Ваш ультра-точный план питания готов!**

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

class CommandHandlers:
    """Класс для обработчиков команд"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Стартовая команда"""
        chat_id = update.message.chat_id
        user_data_storage[chat_id] = {}
        
        reply_markup = ReplyKeyboardMarkup(
            Keyboards.MAIN_MENU, 
            resize_keyboard=True, 
            one_time_keyboard=False
        )
        
        await update.message.reply_text(
            Messages.WELCOME,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"User {chat_id} started the bot")
        return States.GENDER
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Команда помощи"""
        await update.message.reply_text(Messages.HELP, parse_mode=ParseMode.MARKDOWN)
        return States.GENDER
    
    @staticmethod
    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Отмена анализа"""
        chat_id = update.message.chat_id
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.MAIN_MENU, resize_keyboard=True)
        
        await update.message.reply_text(
            "❌ **Анализ отменен**\n\nНажмите 🚀 Начать для нового расчета",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        if chat_id in user_data_storage:
            del user_data_storage[chat_id]
        
        return States.GENDER

class SurveyHandlers:
    """Класс для обработчиков опроса"""
    
    @staticmethod
    async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Начало опроса"""
        chat_id = update.message.chat_id
        user_data_storage[chat_id] = {}
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.GENDER_CHOICE, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "👤 **Этап 1/12:** Ваш пол?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"Starting survey for user {chat_id}")
        return States.GENDER
    
    @staticmethod
    async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка выбора пола"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        try:
            if text in ['👨 Мужчина', 'мужчина', 'Мужчина']:
                user_data_storage[chat_id]['gender'] = 'мужчина'
            elif text in ['👩 Женщина', 'женщина', 'Женщина']:
                user_data_storage[chat_id]['gender'] = 'женщина'
            else:
                await update.message.reply_text("❌ Пожалуйста, выберите пол, используя кнопки")
                return States.GENDER
            
            logger.info(f"User {chat_id} selected gender: {user_data_storage[chat_id]['gender']}")
            
            reply_markup = ReplyKeyboardMarkup(Keyboards.MAIN_MENU, resize_keyboard=True)
            await update.message.reply_text(
                "🎂 **Этап 2/12:** Укажите ваш возраст (число от 16 до 80)",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            return States.AGE
            
        except Exception as e:
            logger.error(f"[ERROR] gender() exception: {e}")
            await update.message.reply_text(f"[gender] Ошибка: {e}")
            return States.GENDER
    
    @staticmethod
    async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка возраста"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        try:
            # Проверка на кнопки
            if text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
                return await ButtonHandlers.handle_buttons(update, context)
            
            age_value = InputValidator.validate_age(text)
            user_data_storage[chat_id]['age'] = age_value
            
            logger.info(f"User {chat_id} entered age: {age_value}")
            await update.message.reply_text(
                "⚖️ **Этап 3/12:** Укажите ваш вес в килограммах (например: 70)",
                parse_mode=ParseMode.MARKDOWN
            )
            return States.WEIGHT
            
        except ValueError as e:
            await update.message.reply_text(f"❌ {str(e)}")
            return States.AGE
        except Exception as e:
            logger.error(f"[ERROR] age() exception: {e}")
            await update.message.reply_text(f"[age] Ошибка: {e}")
            return States.AGE
    
    @staticmethod
    async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка веса"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        try:
            # Проверка на кнопки
            if text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
                return await ButtonHandlers.handle_buttons(update, context)
            
            weight_value = InputValidator.validate_weight(text)
            user_data_storage[chat_id]['weight'] = weight_value
            
            logger.info(f"User {chat_id} entered weight: {weight_value}")
            await update.message.reply_text(
                "📏 **Этап 4/12:** Укажите ваш рост в сантиметрах (например: 175)",
                parse_mode=ParseMode.MARKDOWN
            )
            return States.HEIGHT
            
        except ValueError as e:
            await update.message.reply_text(f"❌ {str(e)}")
            return States.WEIGHT
    
    @staticmethod
    async def height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка роста"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        try:
            # Проверка на кнопки
            if text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
                return await ButtonHandlers.handle_buttons(update, context)
            
            height_value = InputValidator.validate_height(text)
            user_data_storage[chat_id]['height'] = height_value
            
            logger.info(f"User {chat_id} entered height: {height_value}")
            
            reply_markup = ReplyKeyboardMarkup(Keyboards.FAT_PERCENTAGE_CHOICE, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(
                "🔥 **Этап 5/12:** Знаете ли вы процент жира в организме?",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            return States.FAT_PERCENTAGE
            
        except ValueError as e:
            await update.message.reply_text(f"❌ {str(e)}")
            return States.HEIGHT
    
    @staticmethod
    async def fat_percentage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка знания процента жира"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        if text == '✅ Да, знаю':
            reply_markup = ReplyKeyboardMarkup(Keyboards.MAIN_MENU, resize_keyboard=True, persistent=True)
            await update.message.reply_text(
                "📊 Введите процент жира (число от 5 до 50, например: 15)",
                reply_markup=reply_markup
            )
            return States.FAT_PERCENTAGE_INPUT
        elif text == '❌ Не знаю':
            user_data_storage[chat_id]['fat_percent'] = None
            logger.info(f"User {chat_id} doesn't know fat percentage")
            return await SurveyHandlers.show_goal_selection(update, context)
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите один из вариантов, используя кнопки")
            return States.FAT_PERCENTAGE
    
    @staticmethod
    async def fat_percentage_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка ввода процента жира"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        try:
            # Проверка на кнопки
            if text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
                return await ButtonHandlers.handle_buttons(update, context)
            
            fat_value = InputValidator.validate_fat_percentage(text)
            user_data_storage[chat_id]['fat_percent'] = fat_value
            
            logger.info(f"User {chat_id} entered fat percentage: {fat_value}")
            return await SurveyHandlers.show_goal_selection(update, context)
            
        except ValueError as e:
            await update.message.reply_text(f"❌ {str(e)}")
            return States.FAT_PERCENTAGE_INPUT
    
    @staticmethod
    async def show_goal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Показать выбор цели"""
        reply_markup = ReplyKeyboardMarkup(Keyboards.GOAL_CHOICE, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "🎯 **Этап 6/12:** Ваша цель?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.GOAL
    
    @staticmethod
    async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка выбора цели"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        goal_map = {
            '📉 Похудение': 'Похудение',
            '⚖️ Поддержание': 'Поддержание',
            '📈 Набор массы': 'Набор массы'
        }
        
        if text in goal_map:
            user_data_storage[chat_id]['goal'] = goal_map[text]
            logger.info(f"User {chat_id} selected goal: {goal_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите цель, используя кнопки")
            return States.GOAL
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.TRAINING_EXPERIENCE, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "💪 **Этап 7/12:** Есть ли у вас опыт в тренировках или спорте?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.HAS_TRAINING_EXPERIENCE

class ButtonHandlers:
    """Класс для обработки кнопок"""
    
    @staticmethod
    async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка нажатий на постоянные кнопки"""
        text = update.message.text
        chat_id = update.message.chat_id
        
        button_handlers = {
            '🚀 Начать': SurveyHandlers.start_survey,
            '❓ Помощь': CommandHandlers.help_command,
            '📊 О боте': ButtonHandlers.show_about,
            '💬 Получить консультацию': ButtonHandlers.show_consultation,
            '🚀 Начать заново': SurveyHandlers.start_survey
        }
        
        if text in button_handlers:
            return await button_handlers[text](update, context)
        
        # Обработка кнопок мини-приложений
        if text == '🎮 Мини-приложения':
            return await ButtonHandlers.show_mini_apps_menu(update, context)
        elif text == '🔙 Главное меню':
            return await ButtonHandlers.return_to_main_menu(update, context)
        
        # Если это не кнопка, обрабатываем как обычное сообщение
        return await ButtonHandlers.handle_message(update, context)
    
    @staticmethod
    async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Показать информацию о боте"""
        await update.message.reply_text(Messages.ABOUT, parse_mode=ParseMode.MARKDOWN)
        return States.GENDER
    
    @staticmethod
    async def show_consultation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Показать информацию о консультации"""
        consultation_keyboard = [['💬 Получить консультацию'], ['🚀 Начать заново', '❓ Помощь'], ['🌍 Язык', '📊 О боте']]
        reply_markup = ReplyKeyboardMarkup(consultation_keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            Messages.CONSULTATION,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.GENDER
    
    @staticmethod
    async def show_mini_apps_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Показать меню мини-приложений"""
        reply_markup = ReplyKeyboardMarkup(Keyboards.MINI_APPS_MENU, resize_keyboard=True)
        
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
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return States.GENDER
    
    @staticmethod
    async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Вернуться в главное меню"""
        chat_id = update.message.chat_id
        user_data_storage[chat_id] = {}
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.MAIN_MENU, resize_keyboard=True, one_time_keyboard=False)
        
        await update.message.reply_text(
            Messages.WELCOME,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return States.GENDER
    
    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка неопознанных сообщений"""
        await update.message.reply_text(
            "🤔 Не понимаю это сообщение.\n\n🎮 Используйте кнопки внизу экрана или команду /help для справки",
            parse_mode=ParseMode.MARKDOWN
        )
        return States.GENDER 