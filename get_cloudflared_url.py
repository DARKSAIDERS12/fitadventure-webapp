#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения URL от cloudflared
"""

import subprocess
import time
import re

def get_cloudflared_url():
    """Получает URL от cloudflared"""
    
    print("🔍 Поиск URL от cloudflared...")
    
    # Запускаем cloudflared в фоне
    try:
        # Останавливаем предыдущий процесс
        subprocess.run(["pkill", "-f", "cloudflared"], capture_output=True)
        time.sleep(2)
        
        # Запускаем новый туннель
        process = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем и ищем URL
        for i in range(30):  # Максимум 30 секунд
            time.sleep(1)
            
            # Проверяем вывод
            if process.poll() is not None:
                break
                
            # Читаем stderr (cloudflared выводит URL туда)
            stderr_output = process.stderr.read() if process.stderr else ""
            
            # Ищем URL в выводе
            url_match = re.search(r'https://[a-zA-Z0-9\-\.]+\.trycloudflare\.com', stderr_output)
            if url_match:
                url = url_match.group(0)
                print(f"✅ URL найден: {url}")
                return url
        
        print("❌ URL не найден в выводе cloudflared")
        return None
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

if __name__ == "__main__":
    url = get_cloudflared_url()
    if url:
        # Сохраняем URL в файл
        with open('webapp_url.txt', 'w') as f:
            f.write(url)
        print(f"💾 URL сохранен в webapp_url.txt: {url}")
        
        # Обновляем main.py
        import update_webapp_url
        update_webapp_url.update_webapp_url(url)
    else:
        print("❌ Не удалось получить URL") 