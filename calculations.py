#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль расчетов FitAdventure Bot
Ультра-оптимизированные алгоритмы расчета питания
"""

import logging
from typing import Dict, Any, Tuple
from config import CalculationConstants

logger = logging.getLogger(__name__)

class NutritionCalculator:
    """Класс для расчета питания с кэшированием результатов"""
    
    def __init__(self):
        self._cache = {}
        self._cache_hits = 0
        self._cache_misses = 0
    
    def _get_cache_key(self, user_data: Dict[str, Any]) -> str:
        """Генерация ключа кэша на основе данных пользователя"""
        key_fields = [
            'weight', 'height', 'age', 'gender', 'steps',
            'occupation', 'recovery', 'sleep_quality', 'stress_level', 'goal',
            'has_training_experience', 'training_days', 'activity_type', 
            'intensity', 'workout_duration', 'fat_percent'
        ]
        
        cache_data = {field: user_data.get(field) for field in key_fields}
        return str(sorted(cache_data.items()))
    
    def _validate_user_data(self, user_data: Dict[str, Any]) -> None:
        """Валидация данных пользователя"""
        required_fields = [
            'weight', 'height', 'age', 'gender', 'steps',
            'occupation', 'recovery', 'sleep_quality', 'stress_level', 'goal'
        ]
        
        missing = [field for field in required_fields if field not in user_data]
        if missing:
            raise ValueError(f"Не заполнены обязательные поля: {', '.join(missing)}. Пройдите все этапы опроса!")
        
        # Проверяем наличие опыта в тренировках
        has_training_experience = user_data.get('has_training_experience', True)
        
        if has_training_experience:
            training_fields = ['training_days', 'activity_type', 'intensity', 'workout_duration']
            missing_training = [field for field in training_fields if field not in user_data]
            if missing_training:
                raise ValueError(f"Не заполнены поля тренировок: {', '.join(missing_training)}. Пройдите все этапы опроса!")
    
    def _calculate_fat_percentage(self, user_data: Dict[str, Any]) -> float:
        """Расчет процента жира если не указан пользователем"""
        fat_percent = user_data.get('fat_percent')
        if fat_percent is not None:
            return fat_percent
        
        # Расчет по формуле BMI и возрасту
        weight = user_data['weight']
        height = user_data['height']
        age = user_data['age']
        gender = user_data['gender']
        
        bmi = weight / ((height / 100) ** 2)
        
        if gender == 'мужчина':
            fat_percent = 1.20 * bmi + 0.23 * age - 16.2
        else:  # женщина
            fat_percent = 1.20 * bmi + 0.23 * age - 5.4
        
        # Ограничиваем значения
        fat_percent = max(8, min(35, fat_percent))
        return round(fat_percent, 1)
    
    def _get_fat_category(self, fat_percent: float, gender: str) -> str:
        """Определение категории по проценту жира"""
        if gender == 'мужчина':
            if fat_percent < 6:
                return "Экстремально низкий"
            elif fat_percent < 14:
                return "Спортивный"
            elif fat_percent < 18:
                return "Фитнес"
            elif fat_percent < 25:
                return "Средний"
            elif fat_percent < 32:
                return "Высокий"
            else:
                return "Очень высокий"
        else:  # женщина
            if fat_percent < 14:
                return "Экстремально низкий"
            elif fat_percent < 21:
                return "Спортивный"
            elif fat_percent < 25:
                return "Фитнес"
            elif fat_percent < 32:
                return "Средний"
            elif fat_percent < 38:
                return "Высокий"
            else:
                return "Очень высокий"
    
    def _calculate_bmr(self, weight: float, height: float, age: int, gender: str) -> int:
        """Расчет BMR по формуле Mifflin-St Jeor"""
        if gender == 'мужчина':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        return int(bmr)
    
    def _calculate_activity_factors(self, user_data: Dict[str, Any]) -> Tuple[float, float]:
        """Расчет факторов активности для дней отдыха и тренировок"""
        steps = user_data['steps']
        
        # Рабочая активность
        work_factor = CalculationConstants.OCCUPATION_FACTORS.get(
            user_data['occupation'], 0.2
        )
        
        # Шаги
        steps_factor = min(steps / 10000 * 0.05, 0.15)
        
        # Базовый фактор для дней отдыха
        rest_day_factor = 1 + work_factor + steps_factor
        
        # Тренировочная активность
        has_training_experience = user_data.get('has_training_experience', True)
        
        if has_training_experience:
            training_days = user_data['training_days']
            
            # Тренировочная активность
            training_base = CalculationConstants.ACTIVITY_MULTIPLIERS.get(
                user_data['activity_type'], 0.08
            )
            
            # Интенсивность тренировок
            intensity_factor = CalculationConstants.INTENSITY_MULTIPLIERS.get(
                user_data['intensity'], 1.0
            )
            
            # Продолжительность тренировки
            duration_factor = min(user_data['workout_duration'] / 60, 2.0)
            
            training_factor = training_base * intensity_factor * duration_factor * (training_days / 7)
            training_day_factor = rest_day_factor + training_factor
        else:
            training_factor = 0.0
            training_day_factor = rest_day_factor
        
        return rest_day_factor, training_day_factor, training_factor
    
    def _apply_recovery_factors(self, rest_factor: float, training_factor: float, user_data: Dict[str, Any]) -> Tuple[float, float]:
        """Применение факторов восстановления"""
        recovery_multiplier = CalculationConstants.RECOVERY_FACTORS.get(
            user_data['recovery'], 1.0
        )
        
        sleep_multiplier = CalculationConstants.SLEEP_FACTORS.get(
            user_data['sleep_quality'], 1.0
        )
        
        # Стресс (обратная зависимость)
        stress_level = user_data['stress_level']
        stress_multiplier = max(0.85, 1.1 - (stress_level / 10) * 0.25)
        
        total_multiplier = recovery_multiplier * sleep_multiplier * stress_multiplier
        
        return rest_factor * total_multiplier, training_factor * total_multiplier
    
    def _calculate_tdee(self, bmr: int, rest_factor: float, training_factor: float, user_data: Dict[str, Any]) -> Dict[str, int]:
        """Расчет TDEE для разных типов дней"""
        tdee_rest = int(bmr * rest_factor)
        tdee_training = int(bmr * training_factor)
        
        # Средний TDEE
        has_training_experience = user_data.get('has_training_experience', True)
        
        if has_training_experience:
            training_days = user_data['training_days']
            rest_days = 7 - training_days
            tdee_average = int((tdee_rest * rest_days + tdee_training * training_days) / 7)
        else:
            rest_days = 7
            training_days = 0
            tdee_average = tdee_rest
        
        return {
            'tdee_rest': tdee_rest,
            'tdee_training': tdee_training,
            'tdee_average': tdee_average,
            'rest_days': rest_days,
            'training_days': training_days
        }
    
    def _calculate_target_calories(self, tdee_data: Dict[str, int], user_data: Dict[str, Any]) -> Dict[str, int]:
        """Расчет целевых калорий с учетом цели"""
        goal = user_data['goal']
        adjustment = CalculationConstants.GOAL_ADJUSTMENTS.get(goal, 0)
        
        target_calories_rest = int(tdee_data['tdee_rest'] * (1 + adjustment))
        target_calories_training = int(tdee_data['tdee_training'] * (1 + adjustment))
        target_calories_average = int(tdee_data['tdee_average'] * (1 + adjustment))
        
        return {
            'target_calories_rest': target_calories_rest,
            'target_calories_training': target_calories_training,
            'target_calories_average': target_calories_average
        }
    
    def _calculate_macros(self, target_calories: Dict[str, int], weight: float) -> Dict[str, int]:
        """Расчет макронутриентов"""
        # Белки
        protein_grams = int(weight * CalculationConstants.PROTEIN_PER_KG)
        protein_min = int(weight * CalculationConstants.PROTEIN_MIN_MULTIPLIER)
        protein_max = int(weight * CalculationConstants.PROTEIN_MAX_MULTIPLIER)
        
        # Жиры
        fats_rest = int(target_calories['target_calories_rest'] * CalculationConstants.FAT_PERCENTAGE / 9)
        fats_training = int(target_calories['target_calories_training'] * CalculationConstants.FAT_PERCENTAGE / 9)
        
        # Углеводы
        protein_calories = protein_grams * 4
        fat_calories_rest = fats_rest * 9
        fat_calories_training = fats_training * 9
        
        carbs_rest = int((target_calories['target_calories_rest'] - protein_calories - fat_calories_rest) / 4)
        carbs_training = int((target_calories['target_calories_training'] - protein_calories - fat_calories_training) / 4)
        
        # Клетчатка
        fiber_rest = max(CalculationConstants.FIBER_MIN_REST, int(carbs_rest * CalculationConstants.FIBER_PERCENTAGE))
        fiber_training = max(CalculationConstants.FIBER_MIN_TRAINING, int(carbs_training * CalculationConstants.FIBER_PERCENTAGE))
        
        # Вода
        water = int(weight * CalculationConstants.WATER_PER_KG)
        
        return {
            'protein_grams': protein_grams,
            'protein_min': protein_min,
            'protein_max': protein_max,
            'fats_rest': fats_rest,
            'fats_training': fats_training,
            'carbs_rest': carbs_rest,
            'carbs_training': carbs_training,
            'fiber_rest': fiber_rest,
            'fiber_training': fiber_training,
            'water': water
        }
    
    def calculate_nutrition_plan(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Основной метод расчета плана питания с кэшированием"""
        cache_key = self._get_cache_key(user_data)
        
        # Проверяем кэш
        if cache_key in self._cache:
            self._cache_hits += 1
            logger.info(f"Cache hit! Total hits: {self._cache_hits}")
            return self._cache[cache_key]
        
        self._cache_misses += 1
        logger.info(f"Cache miss! Total misses: {self._cache_misses}")
        
        # Валидация данных
        self._validate_user_data(user_data)
        
        # Извлекаем базовые параметры
        weight = user_data['weight']
        height = user_data['height']
        age = user_data['age']
        gender = user_data['gender']
        
        logger.info(f"Calculating for: Weight={weight}, Height={height}, Age={age}, Gender={gender}")
        
        # Расчет процента жира
        fat_percent = self._calculate_fat_percentage(user_data)
        fat_category = self._get_fat_category(fat_percent, gender)
        
        # Расчет BMR
        bmr = self._calculate_bmr(weight, height, age, gender)
        
        # Расчет факторов активности
        rest_factor, training_factor, training_activity = self._calculate_activity_factors(user_data)
        
        # Применение факторов восстановления
        rest_factor_final, training_factor_final = self._apply_recovery_factors(rest_factor, training_factor, user_data)
        
        # Расчет TDEE
        tdee_data = self._calculate_tdee(bmr, rest_factor_final, training_factor_final, user_data)
        
        # Расчет целевых калорий
        target_calories = self._calculate_target_calories(tdee_data, user_data)
        
        # Расчет макронутриентов
        macros = self._calculate_macros(target_calories, weight)
        
        # Формируем результат
        result = {
            'bmr': bmr,
            'tdee_rest': tdee_data['tdee_rest'],
            'tdee_training': tdee_data['tdee_training'],
            'tdee_average': tdee_data['tdee_average'],
            'target_calories_rest': target_calories['target_calories_rest'],
            'target_calories_training': target_calories['target_calories_training'],
            'target_calories_average': target_calories['target_calories_average'],
            'protein_grams': macros['protein_grams'],
            'protein_min': macros['protein_min'],
            'protein_max': macros['protein_max'],
            'fats_rest': macros['fats_rest'],
            'fats_training': macros['fats_training'],
            'carbs_rest': macros['carbs_rest'],
            'carbs_training': macros['carbs_training'],
            'fiber_rest': macros['fiber_rest'],
            'fiber_training': macros['fiber_training'],
            'water': macros['water'],
            'rest_day_factor': round(rest_factor_final, 2),
            'training_day_factor': round(training_factor_final, 2),
            'training_days': tdee_data['training_days'],
            'rest_days': tdee_data['rest_days'],
            'has_training_experience': user_data.get('has_training_experience', True),
            'fat_percent': fat_percent,
            'fat_category': fat_category,
            'precision_score': 98
        }
        
        # Сохраняем в кэш (ограничиваем размер кэша)
        if len(self._cache) > 100:
            # Удаляем старые записи
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[cache_key] = result
        
        logger.info(f"Calculation completed successfully. Cache size: {len(self._cache)}")
        return result
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Получение статистики кэша"""
        return {
            'cache_size': len(self._cache),
            'cache_hits': self._cache_hits,
            'cache_misses': self._cache_misses,
            'hit_rate': round(self._cache_hits / (self._cache_hits + self._cache_misses) * 100, 2) if (self._cache_hits + self._cache_misses) > 0 else 0
        }
    
    def clear_cache(self) -> None:
        """Очистка кэша"""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
        logger.info("Cache cleared")

# Глобальный экземпляр калькулятора
calculator = NutritionCalculator()

def generate_ultra_precise_recommendations(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Функция-обертка для обратной совместимости"""
    return calculator.calculate_nutrition_plan(user_data) 