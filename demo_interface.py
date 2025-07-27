#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 FitAdventure Ultra Beauty - Interface Demo
✨ Демонстрация красивого интерфейса с карточками и полосками
🌟 Показ всех визуальных элементов
"""

import time
import sys

# === УЛЬТРА КРАСИВЫЕ ЭМОДЗИ И СИМВОЛЫ ===
SPARKLES = "✨"
FIRE = "🔥"
STAR = "⭐"
ROCKET = "🚀"
GEM = "💎"
CROWN = "👑"
MAGIC = "🪄"
RAINBOW = "🌈"
LIGHTNING = "⚡"
HEARTS = "💕"

def create_animated_progress(current: int, total: int = 12, style: str = "gradient") -> str:
    """Создание красивых анимированных прогресс-баров"""
    progress_percent = min(current / total, 1.0) * 100
    filled = int(current * 20 / total)
    
    if style == "gradient":
        # Градиентный стиль
        bar_chars = ["🟣", "🔵", "🟢", "🟡", "🟠", "🔴"]
        empty_char = "⚫"
        progress_bar = ""
        for i in range(20):
            if i < filled:
                char_index = min(i // 4, len(bar_chars) - 1)
                progress_bar += bar_chars[char_index]
            else:
                progress_bar += empty_char
    elif style == "fire":
        # Огненный стиль
        fire_chars = ["🔥", "🌟", "✨", "💫"]
        progress_bar = ""
        for i in range(20):
            if i < filled:
                char_index = i % len(fire_chars)
                progress_bar += fire_chars[char_index]
            else:
                progress_bar += "⬛"
    elif style == "rainbow":
        # Радужный стиль
        rainbow_chars = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣"]
        progress_bar = ""
        for i in range(20):
            if i < filled:
                char_index = i % len(rainbow_chars)
                progress_bar += rainbow_chars[char_index]
            else:
                progress_bar += "⬜"
    else:
        # Классический красивый стиль
        progress_bar = "🟢" * filled + "⚫" * (20 - filled)
    
    return f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📊 ПРОГРЕСС: {current}/{total} ({progress_percent:.0f}%) ┃
┃ {progress_bar} ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"""

def create_beautiful_card(title: str, content: str, icon: str = "✨", style: str = "default") -> str:
    """Создание красивых информационных карточек"""
    if style == "premium":
        return f"""
╔══════════════════════════════════════╗
║ {icon} {title.upper()} {icon}                    
╠══════════════════════════════════════╣
║                                      ║
║  {content.center(36)}  ║
║                                      ║
╚══════════════════════════════════════╝"""
    elif style == "modern":
        return f"""
┌─────────────────────────────────────┐
│ {icon} {title}                           
├─────────────────────────────────────┤
│ {content}                           
└─────────────────────────────────────┘"""
    elif style == "double":
        return f"""
╔═════════════════════════════════════╗
║ {icon} {title} {icon}                        
╠═════════════════════════════════════╣
║ {content}                           
╚═════════════════════════════════════╝"""
    else:
        return f"""
🎨 ═══════════════════════════════════ 🎨
{icon} **{title}**
{content}
🎨 ═══════════════════════════════════ 🎨"""

def animate_text(text, delay=0.05):
    """Анимация вывода текста"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def show_welcome_animation():
    """Показать анимированное приветствие"""
    welcome_text = f"""
{SPARKLES}═══════════════════════════════════════════════════════════{SPARKLES}
{CROWN}                    FITADVENTURE ULTRA BEAUTY                   {CROWN}
{ROCKET}                   ДЕМОНСТРАЦИЯ ИНТЕРФЕЙСА                     {ROCKET}
{SPARKLES}═══════════════════════════════════════════════════════════{SPARKLES}

{RAINBOW} Самый красивый интерфейс в мире фитнес-ботов! {RAINBOW}

{ROCKET} Точность расчетов: **95-99%**
{GEM} Учитываем **18+ факторов**
{MAGIC} Персональный ИИ-анализ
{FIRE} Результат за **3 минуты**

{HEARTS} Наслаждайтесь красотой интерфейса! {HEARTS}
"""
    print(welcome_text)

def demo_progress_bars():
    """Демонстрация всех типов прогресс-баров"""
    print(f"\n{FIRE} ДЕМОНСТРАЦИЯ ПРОГРЕСС-БАРОВ {FIRE}")
    print("=" * 60)
    
    # Градиентный стиль
    print(f"\n{RAINBOW} 1. Градиентный стиль:")
    for i in [3, 6, 9, 12]:
        print(create_animated_progress(i, 12, "gradient"))
        time.sleep(0.5)
    
    # Огненный стиль  
    print(f"\n{FIRE} 2. Огненный стиль:")
    for i in [2, 5, 8, 11]:
        print(create_animated_progress(i, 12, "fire"))
        time.sleep(0.5)
    
    # Радужный стиль
    print(f"\n{RAINBOW} 3. Радужный стиль:")
    for i in [1, 4, 7, 10]:
        print(create_animated_progress(i, 12, "rainbow"))
        time.sleep(0.5)

def demo_beautiful_cards():
    """Демонстрация всех типов карточек"""
    print(f"\n{GEM} ДЕМОНСТРАЦИЯ КРАСИВЫХ КАРТОЧЕК {GEM}")
    print("=" * 60)
    
    # Default стиль
    print(f"\n{SPARKLES} 1. Default стиль:")
    card1 = create_beautiful_card(
        "ДОБРО ПОЖАЛОВАТЬ", 
        "Начните свой путь к идеальному телу!", 
        CROWN, 
        "default"
    )
    print(card1)
    time.sleep(1)
    
    # Modern стиль
    print(f"\n{STAR} 2. Modern стиль:")
    card2 = create_beautiful_card(
        "ШАГ 1 ИЗ 12", 
        "Выберите ваш пол для точных расчетов", 
        LIGHTNING, 
        "modern"
    )
    print(card2)
    time.sleep(1)
    
    # Premium стиль
    print(f"\n{CROWN} 3. Premium стиль:")
    card3 = create_beautiful_card(
        "РЕЗУЛЬТАТЫ ГОТОВЫ", 
        "Ваш персональный план питания", 
        FIRE, 
        "premium"
    )
    print(card3)
    time.sleep(1)
    
    # Double стиль
    print(f"\n{GEM} 4. Double стиль:")
    card4 = create_beautiful_card(
        "ФИНАЛЬНЫЙ ЭТАП", 
        "Последние штрихи анализа", 
        MAGIC, 
        "double"
    )
    print(card4)

def demo_buttons():
    """Демонстрация красивых кнопок"""
    print(f"\n{HEARTS} ДЕМОНСТРАЦИЯ КРАСИВЫХ КНОПОК {HEARTS}")
    print("=" * 60)
    
    button_examples = [
        f"🇷🇺 {CROWN} Русский {CROWN}     🇺🇸 {GEM} English {GEM}",
        "",
        f"{LIGHTNING} Мужчина          {HEARTS} Женщина",
        "",
        f"{FIRE} Похудение     {STAR} Поддержание     {ROCKET} Набор массы",
        "",
        f"{SPARKLES} Новичок (0-1 год)",
        f"{FIRE} Средний (1-3 года)", 
        f"{CROWN} Эксперт (3+ лет)",
        "",
        f"{SPARKLES} 1 день    {STAR} 2 дня    {GEM} 3 дня",
        f"{FIRE} 4 дня    {LIGHTNING} 5 дней    {CROWN} 6+ дней"
    ]
    
    for button in button_examples:
        print(f"  {button}")
        time.sleep(0.3)

def demo_final_result():
    """Демонстрация финального результата"""
    print(f"\n{CROWN} ДЕМОНСТРАЦИЯ ФИНАЛЬНОГО РЕЗУЛЬТАТА {CROWN}")
    print("=" * 60)
    
    celebration = f"""
{SPARKLES}═══════════════════════════════════{SPARKLES}
{CROWN}    ВАШ ПЛАН ГОТОВ! ПОЗДРАВЛЯЕМ!     {CROWN}
{SPARKLES}═══════════════════════════════════{SPARKLES}

{ROCKET} **ТОЧНОСТЬ РАСЧЕТА: 97%** {ROCKET}
{RAINBOW} Анализ завершен успешно! {RAINBOW}
"""
    
    result_card = f"""
╔══════════════════════════════════════╗
║ {FIRE} ВАШИ ПЕРСОНАЛЬНЫЕ РЕКОМЕНДАЦИИ {FIRE}     ║
╚══════════════════════════════════════╝

{ROCKET} **КАЛОРИИ:** `2150 ккал/день`
{GEM} **БЕЛКИ:** `130-145 г`
{STAR} **ЖИРЫ:** `72 г`
{LIGHTNING} **УГЛЕВОДЫ:** `215 г`
{HEARTS} **КЛЕТЧАТКА:** `32 г`

╔══════════════════════════════════════╗
║ {CROWN} ДЕТАЛЬНАЯ РАЗБИВКА {CROWN}                ║
╚══════════════════════════════════════╝
{MAGIC} **TDEE:** 2380 ккал
{FIRE} **BMR:** 1650 ккал  
{SPARKLES} **NEAT:** 420 ккал
{GEM} **EAT:** 240 ккал
{STAR} **TEF:** 70 ккал
{ROCKET} **Мышечная масса:** 52.3 кг

{RAINBOW}═══════════════════════════════════{RAINBOW}
{CROWN} **ВЫ ВЕЛИКОЛЕПНЫ!** {CROWN}
{SPARKLES} *Персонализировано специально для вас!* {SPARKLES}
{RAINBOW}═══════════════════════════════════{RAINBOW}"""
    
    print(celebration)
    time.sleep(2)
    print(result_card)

def main():
    """Главная функция демонстрации"""
    print("\033[2J\033[H", end="")  # Очистка экрана
    
    show_welcome_animation()
    input(f"\n{MAGIC} Нажмите Enter для демонстрации прогресс-баров...")
    
    demo_progress_bars()
    input(f"\n{SPARKLES} Нажмите Enter для демонстрации карточек...")
    
    demo_beautiful_cards()
    input(f"\n{HEARTS} Нажмите Enter для демонстрации кнопок...")
    
    demo_buttons()
    input(f"\n{CROWN} Нажмите Enter для финального результата...")
    
    demo_final_result()
    
    print(f"\n{RAINBOW}═══════════════════════════════════════════════════════════{RAINBOW}")
    print(f"{CROWN} ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА! КРАСОТА НЕВЕРОЯТНАЯ! {CROWN}")
    print(f"{SPARKLES} Теперь вы видели всю мощь Ultra Beauty интерфейса! {SPARKLES}")
    print(f"{RAINBOW}═══════════════════════════════════════════════════════════{RAINBOW}")

if __name__ == "__main__":
    main() 