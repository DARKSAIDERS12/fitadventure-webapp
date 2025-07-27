#!/usr/bin/env python3
"""
Скрипт для удаления всех декоративных элементов из FitAdventure Bot v4.0
"""

import re

def clean_decorations(filename):
    """Удаление всех декоративных символов"""
    
    # Читаем файл
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Список замен для удаления декоративных элементов
    replacements = [
        # Убираем все ═══ блоки
        (r'═+', ''),
        
        # Убираем рамки ╭╰╣
        (r'╭[═\s]*╮', ''),
        (r'╰[═\s]*╯', ''),
        (r'╠[═\s]*╣', ''),
        (r'[╭╰╣│]', ''),
        
        # Убираем длинные линии из символов
        (r'[═]{10,}', ''),
        
        # Заменяем многострочные блоки на простые
        (r'{[^}]+}════+{[^}]+}\n.*?\n{[^}]+}════+{[^}]+}', lambda m: re.sub(r'====+', '', m.group())),
        
        # Убираем пустые строки с только пробелами и символами
        (r'\n[\s═╭╰╣│]*\n', '\n\n'),
        
        # Убираем лишние переносы строк
        (r'\n{3,}', '\n\n'),
    ]
    
    # Применяем замены
    for pattern, replacement in replacements:
        if callable(replacement):
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        else:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Специальные замены для конкретных блоков
    specific_replacements = [
        # Убираем декоративные блоки в уведомлениях
        (r'{NEON}══+{NEON}\n.*?\n{NEON}══+{NEON}', '{NEON} УВЕДОМЛЕНИЕ {NEON}'),
        (r'{GALAXY}═+{GALAXY}\n.*?\n{GALAXY}═+{GALAXY}', '{GALAXY} ИНФОРМАЦИЯ {GALAXY}'),
        (r'{FIRE}═+{FIRE}\n.*?\n{FIRE}═+{FIRE}', '{FIRE} ВАЖНО {FIRE}'),
        (r'{LIGHTNING}═+{LIGHTNING}\n.*?\n{LIGHTNING}═+{LIGHTNING}', '{LIGHTNING} ВНИМАНИЕ {LIGHTNING}'),
        (r'{RAINBOW}═+{RAINBOW}\n.*?\n{RAINBOW}═+{RAINBOW}', '{RAINBOW} РЕЗУЛЬТАТ {RAINBOW}'),
        (r'{SPARKLES}═+{SPARKLES}\n.*?\n{SPARKLES}═+{SPARKLES}', '{SPARKLES} ГОТОВО {SPARKLES}'),
        (r'{CRYSTAL}═+{CRYSTAL}\n.*?\n{CRYSTAL}═+{CRYSTAL}', '{CRYSTAL} АНАЛИЗ {CRYSTAL}'),
        (r'{MAGIC}═+ ПЕРСОНАЛЬНЫЕ СОВЕТЫ ═+{MAGIC}\n', '{MAGIC} ПЕРСОНАЛЬНЫЕ СОВЕТЫ {MAGIC}\n'),
    ]
    
    for pattern, replacement in specific_replacements:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Записываем обратно
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Декоративные элементы удалены успешно!")

if __name__ == "__main__":
    clean_decorations("main_ultra_ui.py") 