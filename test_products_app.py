#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый файл для проверки мини-приложения базы продуктов
"""

from products_database import PRODUCTS_DATABASE, search_product, format_product_info, get_category_description

def test_products_database():
    """Тестирование базы продуктов"""
    print("🧪 Тестирование базы продуктов...")
    
    # Проверяем структуру базы данных
    goals = list(PRODUCTS_DATABASE.keys())
    print(f"✅ Найдены цели: {goals}")
    
    for goal in goals:
        categories = list(PRODUCTS_DATABASE[goal].keys())
        print(f"📂 Цель '{goal}': категории {categories}")
        
        for category in categories:
            products = list(PRODUCTS_DATABASE[goal][category].keys())
            print(f"   🍎 Категория '{category}': {len(products)} продуктов")
            for product in products[:3]:  # Показываем первые 3
                data = PRODUCTS_DATABASE[goal][category][product]
                print(f"      • {product}: {data['калории']} ккал")
    
    print("\n🔍 Тестирование поиска...")
    
    # Тестируем поиск
    test_products = ["куриная грудка", "овсянка", "авокадо", "гречка"]
    for product in test_products:
        results = search_product(product)
        print(f"🔎 Поиск '{product}': найдено {len(results)} результатов")
    
    print("\n📊 Тестирование форматирования...")
    
    # Тестируем форматирование
    test_product = "куриная грудка"
    test_data = PRODUCTS_DATABASE["похудение"]["белки"][test_product]
    formatted = format_product_info(test_product, test_data)
    print(f"📝 Форматирование для '{test_product}':")
    print(formatted)
    
    print("\n📂 Тестирование описаний категорий...")
    
    # Тестируем описания категорий
    categories = ["сложные_углеводы", "белки", "ненасыщенные_жиры"]
    for category in categories:
        description = get_category_description(category)
        print(f"📋 {category}: {description[:50]}...")
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    test_products_database() 