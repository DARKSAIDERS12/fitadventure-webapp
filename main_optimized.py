#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FitAdventure Bot - Ультра-оптимизированная версия
Модульная архитектура с кэшированием и улучшенной производительностью
Версия: 6.0 Ultra
Дата: 23 июля 2025
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any

# Импорт конфигурации
from config import (
    get_bot_token, States, Keyboards, Messages, 
    LoggingConfig, BOT_VERSION, BOT_NAME
)

# Импорт обработчиков
from handlers import (
    CommandHandlers, SurveyHandlers, ButtonHandlers,
    user_data_storage
)

# Импорт расчетов
from calculations import generate_ultra_precise_recommendations

# Импорт Telegram библиотек
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, WebAppInfo
from telegram.ext import (
    Application, CommandHandler, ConversationHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)
from telegram.constants import ParseMode

# Импорт мини-приложений (с обработкой ошибок)
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

# Заглушки для отсутствующих функций
if not MINI_APPS_AVAILABLE:
    async def show_mini_apps_menu(update, context): return States.GENDER
    async def handle_mini_apps_navigation(update, context): return States.GENDER
    async def show_products_menu(update, context): return States.GENDER
    async def search_product_handler(update, context): return States.GENDER
    async def show_product_details(update, context): return States.GENDER

if not PRODUCTS_MINI_APP_AVAILABLE:
    async def show_products_mini_app(update, context): return States.GENDER
    async def handle_products_navigation(update, context): return States.GENDER
    async def handle_product_search(update, context): return States.GENDER
    async def show_category_products(update, context): return States.GENDER
    async def show_search_interface(update, context): return States.GENDER

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
def setup_logging():
    """Настройка системы логирования"""
    logging.basicConfig(
        format=LoggingConfig.FORMAT,
        level=getattr(logging, LoggingConfig.LEVEL),
        handlers=[
            logging.FileHandler(LoggingConfig.FILE, encoding=LoggingConfig.ENCODING),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# === КЛАСС УПРАВЛЕНИЯ БОТОМ ===
class FitAdventureBot:
    """Основной класс бота с оптимизированной архитектурой"""
    
    def __init__(self):
        self.logger = setup_logging()
        self.application = None
        self.token = None
        self.stats = {
            'start_time': None,
            'total_requests': 0,
            'successful_calculations': 0,
            'errors': 0
        }
    
    async def setup_bot(self) -> bool:
        """Инициализация бота"""
        try:
            # Получение токена
            self.token = get_bot_token()
            self.logger.info("✅ Токен получен успешно!")
            
            # Создание приложения
            self.application = Application.builder().token(self.token).build()
            self.logger.info("✅ Telegram Application создан успешно!")
            
            # Настройка обработчиков
            self._setup_handlers()
            self.logger.info("✅ Обработчики настроены успешно!")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка инициализации бота: {e}")
            return False
    
    def _setup_handlers(self):
        """Настройка всех обработчиков"""
        # Основной ConversationHandler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', CommandHandlers.start)],
            states={
                States.GENDER: [
                    MessageHandler(filters.Regex('^(👨 Мужчина|👩 Женщина|мужчина|Мужчина|женщина|Женщина)$'), SurveyHandlers.gender),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, ButtonHandlers.handle_buttons)
                ],
                States.AGE: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, SurveyHandlers.age)
                ],
                States.WEIGHT: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, SurveyHandlers.weight)
                ],
                States.HEIGHT: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, SurveyHandlers.height)
                ],
                States.FAT_PERCENTAGE: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, SurveyHandlers.fat_percentage)
                ],
                States.FAT_PERCENTAGE_INPUT: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, SurveyHandlers.fat_percentage_input)
                ],
                States.GOAL: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, SurveyHandlers.goal)
                ],
                States.HAS_TRAINING_EXPERIENCE: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_training_experience)
                ],
                States.TRAINING_EXPERIENCE: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_training_experience_level)
                ],
                States.TRAINING_DAYS: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_training_days)
                ],
                States.ACTIVITY_TYPE: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_activity_type)
                ],
                States.WORKOUT_DURATION: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_workout_duration)
                ],
                States.STEPS: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_steps)
                ],
                States.INTENSITY: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_intensity)
                ],
                States.RECOVERY: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_recovery)
                ],
                States.SLEEP_QUALITY: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_sleep_quality)
                ],
                States.STRESS_LEVEL: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_stress_level)
                ],
                States.OCCUPATION: [
                    MessageHandler(filters.Regex('^(🚀 Начать|❓ Помощь|🎮 Мини-приложения|📊 О боте)$'), ButtonHandlers.handle_buttons),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_occupation)
                ],
                
                # Состояния для мини-приложений
                States.MINI_APPS_MENU: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mini_apps_navigation)
                ],
                States.PRODUCTS_MENU: [
                    MessageHandler(filters.Regex('^(🥩 Белки|🍞 Углеводы|🧈 Жиры)$'), show_products_category),
                    MessageHandler(filters.Regex('^(🔍 Поиск продукта|📊 Рекомендации|🔙 Назад)$'), search_product_handler),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, show_product_details)
                ],
                States.PRODUCT_SEARCH: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, search_product_handler)
                ],
                
                # Состояния для базы продуктов
                States.PRODUCTS_MAIN: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_products_navigation)
                ],
                States.PRODUCTS_CATEGORY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_products_navigation)
                ],
                States.PRODUCT_DETAILS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_products_navigation)
                ],
                States.PRODUCT_SEARCH_NEW: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_search)
                ],
            },
            fallbacks=[CommandHandler('cancel', CommandHandlers.cancel)],
        )

        self.application.add_handler(conv_handler)
        self.application.add_handler(CommandHandler('help', CommandHandlers.help_command))
        
        # Обработчики Web App
        self.application.add_handler(CallbackQueryHandler(self._handle_webapp_callback))
        self.application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, self._handle_webapp_data))
    
    # === ОБРАБОТЧИКИ ОПРОСА ===
    async def _handle_training_experience(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка наличия опыта в тренировках"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        if text == '✅ Есть опыт':
            user_data_storage[chat_id]['has_training_experience'] = True
            self.logger.info(f"User {chat_id} has training experience")
            
            reply_markup = ReplyKeyboardMarkup(Keyboards.EXPERIENCE_LEVEL, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(
                "💪 **Этап 8/12:** Ваш опыт тренировок?",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            return States.TRAINING_EXPERIENCE
            
        elif text == '❌ Нет опыта':
            user_data_storage[chat_id]['has_training_experience'] = False
            user_data_storage[chat_id]['training_experience'] = 'Новичок'
            user_data_storage[chat_id]['training_days'] = 0
            user_data_storage[chat_id]['activity_type'] = 'Нет'
            user_data_storage[chat_id]['workout_duration'] = 0
            user_data_storage[chat_id]['intensity'] = 'low'
            user_data_storage[chat_id]['recovery'] = 'average'
            self.logger.info(f"User {chat_id} has no training experience, skipping training questions")
            
            reply_markup = ReplyKeyboardMarkup(Keyboards.MAIN_MENU, resize_keyboard=True)
            await update.message.reply_text(
                "🚶 **Этап 8/12:** Сколько шагов в день вы проходите? (например: 5000)",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            return States.STEPS
            
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите ответ, используя кнопки")
            return States.HAS_TRAINING_EXPERIENCE
    
    async def _handle_training_experience_level(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка уровня опыта тренировок"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        experience_map = {
            '🌱 Новичок (до 1 года)': 'Новичок',
            '🔥 Средний (1-3 года)': 'Средний',
            '⚡ Опытный (3+ года)': 'Опытный'
        }
        
        if text in experience_map:
            user_data_storage[chat_id]['training_experience'] = experience_map[text]
            self.logger.info(f"User {chat_id} selected experience: {experience_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите опыт, используя кнопки")
            return States.TRAINING_EXPERIENCE
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.TRAINING_DAYS, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "🏃 **Этап 9/12:** Сколько дней в неделю тренируетесь?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.TRAINING_DAYS
    
    async def _handle_training_days(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка дней тренировок"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        days_map = {
            '1️⃣ день': 1, '2️⃣ дня': 2, '3️⃣ дня': 3,
            '4️⃣ дня': 4, '5️⃣ дней': 5, '6️⃣ дней': 6
        }
        
        if text in days_map:
            user_data_storage[chat_id]['training_days'] = days_map[text]
            self.logger.info(f"User {chat_id} selected training days: {days_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите количество дней, используя кнопки")
            return States.TRAINING_DAYS
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.ACTIVITY_TYPES, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "💪 **Тип тренировок?**",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.ACTIVITY_TYPE
    
    async def _handle_activity_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка типа активности"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        activity_map = {
            '🏋️ Силовые тренировки': 'Силовые',
            '🏃 Кардио/выносливость': 'Выносливость',
            '⚡ Кроссфит/функциональные': 'Кроссфит'
        }
        
        if text in activity_map:
            user_data_storage[chat_id]['activity_type'] = activity_map[text]
            self.logger.info(f"User {chat_id} selected activity type: {activity_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите тип тренировок, используя кнопки")
            return States.ACTIVITY_TYPE
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(
            "⏱️ **Продолжительность одной тренировки в минутах?** (например: 60)",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.WORKOUT_DURATION
    
    async def _handle_workout_duration(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка продолжительности тренировки"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        try:
            if text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
                return await ButtonHandlers.handle_buttons(update, context)
            
            duration = int(text)
            if not (15 <= duration <= 300):
                raise ValueError
            
            user_data_storage[chat_id]['workout_duration'] = duration
            self.logger.info(f"User {chat_id} entered workout duration: {duration}")
            
            await update.message.reply_text(
                "🚶 **Количество шагов в день?** (примерно, например: 8000)",
                parse_mode=ParseMode.MARKDOWN
            )
            return States.STEPS
            
        except ValueError:
            await update.message.reply_text("❌ Введите корректную продолжительность (от 15 до 300 минут)")
            return States.WORKOUT_DURATION
    
    async def _handle_steps(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработка шагов"""
        chat_id = update.message.chat_id
        text = update.message.text
        
        try:
            if text in ['🚀 Начать', '❓ Помощь', '🌍 Язык', '📊 О боте']:
                return await ButtonHandlers.handle_buttons(update, context)
            
            steps_count = int(text)
            if not (1000 <= steps_count <= 50000):
                raise ValueError
            
            user_data_storage[chat_id]['steps'] = steps_count
            self.logger.info(f"User {chat_id} entered steps: {steps_count}")
            
            # Проверяем наличие опыта в тренировках
            has_training_experience = user_data_storage[chat_id].get('has_training_experience', True)
            
            if has_training_experience:
                reply_markup = ReplyKeyboardMarkup(Keyboards.INTENSITY_LEVELS, resize_keyboard=True, one_time_keyboard=True)
                await update.message.reply_text(
                    "🔥 **Этап 9/12:** Интенсивность ваших тренировок?",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
                return States.INTENSITY
            else:
                # Устанавливаем значения по умолчанию
                user_data_storage[chat_id]['intensity'] = 'low'
                user_data_storage[chat_id]['recovery'] = 'average'
                
                reply_markup = ReplyKeyboardMarkup(Keyboards.SLEEP_QUALITY, resize_keyboard=True, one_time_keyboard=True)
                await update.message.reply_text(
                    "🌙 **Этап 9/12:** Качество сна?",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
                return States.SLEEP_QUALITY
                
        except ValueError:
            await update.message.reply_text("❌ Введите корректное количество шагов (от 1000 до 50000)")
            return States.STEPS
    
    async def _handle_intensity(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
            self.logger.info(f"User {chat_id} selected intensity: {intensity_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите интенсивность, используя кнопки")
            return States.INTENSITY
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.RECOVERY_QUALITY, resize_keyboard=True, one_time_keyboard=True)
        stage_number = "10/12" if user_data_storage[chat_id].get('has_training_experience', True) else "9/12"
        
        await update.message.reply_text(
            f"😴 **Этап {stage_number}:** Качество восстановления после тренировок?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.RECOVERY
    
    async def _handle_recovery(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
            self.logger.info(f"User {chat_id} selected recovery: {recovery_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите качество восстановления, используя кнопки")
            return States.RECOVERY
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.SLEEP_QUALITY, resize_keyboard=True, one_time_keyboard=True)
        stage_number = "11/12" if user_data_storage[chat_id].get('has_training_experience', True) else "9/12"
        
        await update.message.reply_text(
            f"🌙 **Этап {stage_number}:** Качество сна?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.SLEEP_QUALITY
    
    async def _handle_sleep_quality(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
            self.logger.info(f"User {chat_id} selected sleep quality: {sleep_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите качество сна, используя кнопки")
            return States.SLEEP_QUALITY
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.STRESS_LEVELS, resize_keyboard=True, one_time_keyboard=True)
        stage_number = "11/12" if user_data_storage[chat_id].get('has_training_experience', True) else "10/12"
        
        await update.message.reply_text(
            f"💆 **Этап {stage_number}:** Уровень стресса в жизни по шкале 1-10?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.STRESS_LEVEL
    
    async def _handle_stress_level(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
            self.logger.info(f"User {chat_id} selected stress level: {stress_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите уровень стресса, используя кнопки")
            return States.STRESS_LEVEL
        
        reply_markup = ReplyKeyboardMarkup(Keyboards.OCCUPATION_TYPES, resize_keyboard=True, one_time_keyboard=True)
        stage_number = "12/12" if user_data_storage[chat_id].get('has_training_experience', True) else "11/12"
        
        await update.message.reply_text(
            f"💼 **Этап {stage_number}:** Тип вашей работы?",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return States.OCCUPATION
    
    async def _handle_occupation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
            self.logger.info(f"User {chat_id} selected occupation: {occupation_map[text]}")
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите тип работы, используя кнопки")
            return States.OCCUPATION
        
        # Возвращаем постоянные кнопки
        reply_markup = ReplyKeyboardMarkup(Keyboards.MAIN_MENU, resize_keyboard=True)
        
        # Показываем процесс расчета
        calculating_msg = await update.message.reply_text(
            "🧠 **Выполняю ультра-точные расчеты...**\n\n⚡ Анализирую все факторы\n🔬 Применяю научные формулы\n📊 Создаю персональный план",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Генерируем ультра-точные рекомендации
        try:
            self.logger.info(f"Starting calculations for user {chat_id}")
            self.logger.info(f"User data: {user_data_storage[chat_id]}")
            
            results = generate_ultra_precise_recommendations(user_data_storage[chat_id])
            self.stats['successful_calculations'] += 1
            
            # Форматируем результат
            from handlers import MessageFormatter
            result_message = MessageFormatter.format_results_message(results)
            
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
                self.logger.error(f"Edit failed, sending new message: {e}")
                await update.message.reply_text(result_message, parse_mode=ParseMode.MARKDOWN)
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
            
            self.logger.info(f"Successfully sent results to user {chat_id}")
            
        except Exception as e:
            self.logger.error(f"Error calculating for user {chat_id}: {str(e)}")
            self.stats['errors'] += 1
            await calculating_msg.edit_text(
                f"❌ **Ошибка расчета:** {str(e)}\n\nПопробуйте начать заново, нажав 🚀 Начать",
                parse_mode=ParseMode.MARKDOWN
            )
        
        # Очистка данных
        if chat_id in user_data_storage:
            del user_data_storage[chat_id]
        
        return States.GENDER
    
    # === ОБРАБОТЧИКИ WEB APP ===
    async def _handle_webapp_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
                return States.GENDER
        
        return States.GENDER
    
    async def _handle_webapp_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
                    return States.GENDER
            
            return States.GENDER
            
        except Exception as e:
            self.logger.error(f"Ошибка обработки Web App данных: {e}")
            await update.message.reply_text("❌ Ошибка обработки данных из приложения")
            return States.GENDER
    
    async def run(self):
        """Запуск бота"""
        try:
            self.stats['start_time'] = asyncio.get_event_loop().time()
            self.logger.info(f"🚀 {BOT_NAME} {BOT_VERSION} запущен!")
            self.logger.info("✅ Все системы готовы к работе")
            
            print(f"\n🎯 {BOT_NAME} {BOT_VERSION} запущен успешно!")
            print("🎮 Новая функция: Постоянные кнопки снизу экрана!")
            print("📊 Ультра-точные расчеты с точностью 98%")
            print("📱 Откройте Telegram и найдите своего бота")
            print("⌨️ Нажмите Ctrl+C для остановки")
            
            await self.application.run_polling()
            
        except KeyboardInterrupt:
            print("\n✅ Бот остановлен пользователем")
        except Exception as e:
            print(f"\n❌ Ошибка работы бота: {e}")
            self.logger.error(f"Critical error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики бота"""
        return {
            **self.stats,
            'cache_stats': generate_ultra_precise_recommendations.__self__.get_cache_stats() if hasattr(generate_ultra_precise_recommendations, '__self__') else {}
        }

# === ГЛАВНАЯ ФУНКЦИЯ ===
async def main():
    """Главная функция запуска бота"""
    print(f"🚀 Запуск {BOT_NAME} {BOT_VERSION}...")
    
    bot = FitAdventureBot()
    
    if await bot.setup_bot():
        await bot.run()
    else:
        print("❌ Не удалось инициализировать бота")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main()) 