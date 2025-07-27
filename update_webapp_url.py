#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления URL Web App в main.py
"""

import re
import sys

def update_webapp_url(new_url):
    """Обновляет URL Web App в main.py"""
    
    try:
        # Читаем файл
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем URL
        pattern = r'web_app_url = "https://[^"]*"'
        replacement = f'web_app_url = "{new_url}"'
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            
            # Записываем обновленный файл
            with open('main.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ URL обновлен: {new_url}")
            return True
        else:
            print("❌ Не найден web_app_url в main.py")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка обновления: {e}")
        return False

def get_url_from_file():
    """Получает URL из файла webapp_url.txt"""
    try:
        with open('webapp_url.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # URL передан как аргумент
        url = sys.argv[1]
    else:
        # Пытаемся получить URL из файла
        url = get_url_from_file()
    
    if url:
        update_webapp_url(url)
    else:
        print("❌ URL не найден. Запустите test_webapp.sh сначала.") 