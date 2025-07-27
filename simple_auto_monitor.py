#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенный автоматический мониторинг конфликтов сохранения
Работает без внешних зависимостей
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from datetime import datetime
import threading

class SimpleAutoMonitor:
    """Упрощенная система автоматического исправления"""
    
    def __init__(self, project_path="/home/darksaiders/Загрузки/мой бот2"):
        self.project_path = Path(project_path)
        self.running = True
        self.last_check = 0
        self.check_interval = 10  # Проверка каждые 10 секунд
        self.fix_cooldown = 30    # Минимальный интервал между исправлениями
        self.last_fix_time = 0
        
    def detect_conflicts(self):
        """Обнаружение конфликтов в файловой системе"""
        conflict_files = []
        
        # Ищем временные и конфликтные файлы
        patterns = ["*.lock", "*.tmp", "*.temp", "*~", "*.swp", "*.swo"]
        
        for pattern in patterns:
            for file in self.project_path.glob(pattern):
                conflict_files.append(file)
                
        return conflict_files
    
    def check_cursor_processes(self):
        """Проверка процессов Cursor на зависание"""
        try:
            result = subprocess.run(['ps', 'aux'], 
                                  capture_output=True, text=True)
            cursor_processes = [line for line in result.stdout.split('\n') 
                              if 'cursor' in line.lower()]
            
            # Проверяем на процессы, которые могут вызывать конфликты
            problem_processes = []
            for proc in cursor_processes:
                if any(keyword in proc.lower() for keyword in ['defunct', '<zombie>', 'stuck']):
                    problem_processes.append(proc)
                    
            return len(cursor_processes), problem_processes
            
        except:
            return 0, []
    
    def auto_fix(self, reason="Обнаружены конфликты"):
        """Автоматическое исправление"""
        current_time = time.time()
        
        # Проверяем cooldown
        if current_time - self.last_fix_time < self.fix_cooldown:
            return False
            
        print(f"🚨 [{datetime.now().strftime('%H:%M:%S')}] {reason} - запуск автоисправления...")
        
        try:
            # Запускаем скрипт исправления
            result = subprocess.run([
                sys.executable, 
                str(self.project_path / "simple_fix.py")
            ], cwd=self.project_path, check=False, capture_output=True, text=True)
            
            self.last_fix_time = current_time
            
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Автоисправление завершено")
            
            # Отправляем уведомление
            self.send_notification("Конфликты сохранения устранены автоматически!")
            return True
            
        except Exception as e:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Ошибка автоисправления: {e}")
            return False
    
    def send_notification(self, message):
        """Отправка уведомления"""
        try:
            subprocess.run(['notify-send', 'Auto-Fix Monitor', message], 
                         check=False, timeout=5)
        except:
            print(f"📢 {message}")
    
    def monitor_loop(self):
        """Основной цикл мониторинга"""
        print("🛡️ Запуск упрощенного автомонитора конфликтов сохранения")
        print(f"📁 Отслеживаемая папка: {self.project_path}")
        print("🔄 Для остановки нажмите Ctrl+C")
        print("=" * 60)
        
        # Первоначальная проверка
        conflicts = self.detect_conflicts()
        if conflicts:
            print(f"🔍 Найдено конфликтов при запуске: {len(conflicts)}")
            self.auto_fix("Конфликты при запуске")
        
        print("✅ Автомонитор активен!")
        
        while self.running:
            try:
                current_time = time.time()
                
                # Основная проверка
                if current_time - self.last_check >= self.check_interval:
                    self.last_check = current_time
                    
                    # 1. Проверка конфликтных файлов
                    conflicts = self.detect_conflicts()
                    if conflicts:
                        print(f"🔍 Обнаружено конфликтов: {len(conflicts)}")
                        self.auto_fix(f"Найдено {len(conflicts)} конфликтных файлов")
                    
                    # 2. Проверка процессов Cursor
                    cursor_count, problems = self.check_cursor_processes()
                    if problems:
                        print(f"⚠️ Проблемные процессы Cursor: {len(problems)}")
                        self.auto_fix("Проблемные процессы Cursor")
                    
                    # 3. Тихая проверка статуса
                    if current_time % 300 == 0:  # Каждые 5 минут
                        print(f"📊 [{datetime.now().strftime('%H:%M:%S')}] "
                              f"Статус: процессов Cursor: {cursor_count}, "
                              f"конфликтов: {len(conflicts)}")
                
                time.sleep(1)  # Основной цикл каждую секунду
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Ошибка в цикле мониторинга: {e}")
                time.sleep(5)
        
        print("\n🛑 Автомонитор остановлен")
    
    def stop(self):
        """Остановка мониторинга"""
        self.running = False

def signal_handler(signum, frame):
    """Обработчик сигналов"""
    print("\n🛑 Получен сигнал остановки")
    sys.exit(0)

def main():
    """Главная функция"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        monitor = SimpleAutoMonitor()
        monitor.monitor_loop()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 