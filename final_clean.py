#!/usr/bin/env python3
"""
Финальная очистка всех декоративных элементов
"""

import re

def final_clean(filename):
    """Полная очистка декоративных элементов"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Массовая замена всех декоративных паттернов
    patterns = [
        # Убираем все ═ символы полностью
        (r'[═]+', ''),
        
        # Убираем все рамочные символы
        (r'[╭╰╣│╠╮╯]', ''),
        
        # Убираем блоки с NEON
        (r'{NEON}[^{]*{NEON}', '{NEON} УВЕДОМЛЕНИЕ {NEON}'),
        
        # Убираем блоки с GALAXY
        (r'{GALAXY}[^{]*{GALAXY}', '{GALAXY} ИНФОРМАЦИЯ {GALAXY}'),
        
        # Убираем блоки с FIRE
        (r'{FIRE}[^{]*{FIRE}', '{FIRE} ВАЖНО {FIRE}'),
        
        # Убираем блоки с LIGHTNING
        (r'{LIGHTNING}[^{]*{LIGHTNING}', '{LIGHTNING} ВНИМАНИЕ {LIGHTNING}'),
        
        # Убираем блоки с RAINBOW
        (r'{RAINBOW}[^{]*{RAINBOW}', '{RAINBOW} РЕЗУЛЬТАТ {RAINBOW}'),
        
        # Убираем блоки с SPARKLES
        (r'{SPARKLES}[^{]*{SPARKLES}', '{SPARKLES} ГОТОВО {SPARKLES}'),
        
        # Убираем блоки с CRYSTAL
        (r'{CRYSTAL}[^{]*{CRYSTAL}', '{CRYSTAL} АНАЛИЗ {CRYSTAL}'),
        
        # Убираем блоки с MAGIC
        (r'{MAGIC}[^{]*ПЕРСОНАЛЬНЫЕ СОВЕТЫ[^{]*{MAGIC}', '{MAGIC} ПЕРСОНАЛЬНЫЕ СОВЕТЫ {MAGIC}'),
        
        # Убираем блоки с icon
        (r'{icon}[^{]*{icon}', '{icon} ИНФОРМАЦИЯ {icon}'),
        
        # Убираем простые символьные блоки
        (r'🔮[^🔮]*🔮', '🔮 МАГИЯ 🔮'),
        (r'💫[^💫]*💫', '💫 КРАСОТА 💫'),
        
        # Убираем пустые строки подряд
        (r'\n\s*\n\s*\n', '\n\n'),
        
        # Убираем строки только с пробелами
        (r'\n\s+\n', '\n\n'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    
    # Убираем специфичные многострочные блоки
    multiline_patterns = [
        (r'formatted = f"\\n{MAGIC}.*?ПЕРСОНАЛЬНЫЕ СОВЕТЫ.*?{MAGIC}\\n"[^f]*formatted \+= f"{MAGIC}.*?{MAGIC}\\n"', 
         'formatted = f"\\n{MAGIC} ПЕРСОНАЛЬНЫЕ СОВЕТЫ {MAGIC}\\n"'),
    ]
    
    for pattern, replacement in multiline_patterns:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("🧹 Финальная очистка завершена!")

if __name__ == "__main__":
    final_clean("main_ultra_ui.py") 