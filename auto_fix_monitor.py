#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматический мониторинг и исправление ошибок сохранения
Автоматически запускается при обнаружении ошибки "Failed to save: The content of the file is newer"
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SaveConflictDetector(FileSystemEventHandler):
    """Детектор конфликтов сохранения файлов"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.last_fix_time = 0
        self.fix_cooldown = 30  # Секунды между автоисправлениями
        self.monitored_files = {'.py', '.md', '.txt', '.json', '.yaml', '.yml'}
        
    def on_modified(self, event):
        """Обработка изменения файлов"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if file_path.suffix not in self.monitored_files:
            return
            
        # Проверяем на наличие конфликтных временных файлов
        self.check_and_fix_conflicts(file_path)
    
    def check_and_fix_conflicts(self, file_path):
        """Проверка и исправление конфликтов"""
        current_time = time.time()
        
        # Предотвращаем слишком частые исправления
        if current_time - self.last_fix_time < self.fix_cooldown:
            return
            
        conflict_patterns = [
            file_path.with_suffix(file_path.suffix + '.lock'),
            file_path.with_suffix(file_path.suffix + '.tmp'),
            file_path.with_suffix(file_path.suffix + '.temp'),
        ]
        
        conflicts_found = any(p.exists() for p in conflict_patterns)
        
        if conflicts_found:
            self.auto_fix_conflicts()
            self.last_fix_time = current_time
    
    def auto_fix_conflicts(self):
        """Автоматическое исправление конфликтов"""
        print(f"🚨 [{datetime.now().strftime('%H:%M:%S')}] Обнаружен конфликт сохранения - запуск автоисправления...")
        
        try:
            # Запускаем наш скрипт исправления
            subprocess.run([
                sys.executable, 
                str(self.project_path / "simple_fix.py")
            ], cwd=self.project_path, check=False)
            
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Автоисправление завершено")
            
            # Отправляем уведомление
            self.send_notification("Конфликт сохранения устранен автоматически!")
            
        except Exception as e:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Ошибка автоисправления: {e}")
    
    def send_notification(self, message):
        """Отправка системного уведомления"""
        try:
            subprocess.run([
                'notify-send', 
                'FitAdventure Auto-Fix', 
                message,
                '--icon=info',
                '--urgency=normal'
            ], check=False)
        except:
            pass

class LogMonitor:
    """Монитор логов Cursor для обнаружения ошибок сохранения"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.running = True
        self.error_patterns = [
            "Failed to save",
            "content of the file is newer",
            "file has been changed outside",
            "conflict",
            "cannot save"
        ]
        
    def monitor_cursor_logs(self):
        """Мониторинг логов Cursor"""
        log_paths = [
            Path.home() / ".cursor" / "logs",
            Path.home() / ".config" / "cursor" / "logs",
            Path.home() / ".cache" / "cursor" / "logs"
        ]
        
        print(f"🔍 Мониторинг логов Cursor для обнаружения ошибок сохранения...")
        
        while self.running:
            try:
                for log_dir in log_paths:
                    if log_dir.exists():
                        self.scan_log_directory(log_dir)
                
                time.sleep(5)  # Проверка каждые 5 секунд
                
            except Exception as e:
                print(f"❌ Ошибка мониторинга: {e}")
                time.sleep(10)
    
    def scan_log_directory(self, log_dir):
        """Сканирование директории логов"""
        for log_file in log_dir.glob("*.log"):
            try:
                if self.check_recent_errors(log_file):
                    self.trigger_auto_fix()
            except:
                continue
    
    def check_recent_errors(self, log_file):
        """Проверка последних ошибок в лог-файле"""
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                # Читаем только последние 50 строк для производительности
                lines = f.readlines()[-50:]
                
                for line in lines:
                    line_lower = line.lower()
                    if any(pattern.lower() in line_lower for pattern in self.error_patterns):
                        # Проверяем, что ошибка свежая (не старше 30 секунд)
                        if self.is_recent_log_entry(line):
                            return True
            
        except:
            pass
            
        return False
    
    def is_recent_log_entry(self, line):
        """Проверка актуальности записи лога"""
        # Простая проверка - если линия содержит текущее время (примерно)
        current_time = datetime.now()
        time_patterns = [
            current_time.strftime('%H:%M'),
            (current_time.replace(minute=current_time.minute-1) if current_time.minute > 0 
             else current_time.replace(hour=current_time.hour-1, minute=59)).strftime('%H:%M')
        ]
        
        return any(pattern in line for pattern in time_patterns)
    
    def trigger_auto_fix(self):
        """Запуск автоматического исправления"""
        print(f"🚨 [{datetime.now().strftime('%H:%M:%S')}] Обнаружена ошибка сохранения в логах - запуск исправления...")
        
        try:
            subprocess.run([
                sys.executable, 
                str(self.project_path / "simple_fix.py")
            ], cwd=self.project_path, check=False)
            
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Автоисправление по логам завершено")
            
        except Exception as e:
            print(f"❌ Ошибка автоисправления: {e}")
    
    def stop(self):
        """Остановка мониторинга"""
        self.running = False

class AutoFixMonitor:
    """Главный класс автоматического мониторинга и исправления"""
    
    def __init__(self, project_path="/home/darksaiders/Загрузки/мой бот2"):
        self.project_path = Path(project_path)
        self.observer = None
        self.log_monitor = None
        self.log_thread = None
        
    def start(self):
        """Запуск мониторинга"""
        print("🛡️ Запуск системы автоматического исправления конфликтов сохранения")
        print(f"📁 Отслеживаемая папка: {self.project_path}")
        print("🔄 Для остановки нажмите Ctrl+C")
        print("=" * 60)
        
        # 1. Мониторинг файловой системы
        event_handler = SaveConflictDetector(self.project_path)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.project_path), recursive=True)
        self.observer.start()
        
        # 2. Мониторинг логов Cursor
        self.log_monitor = LogMonitor(self.project_path)
        self.log_thread = threading.Thread(target=self.log_monitor.monitor_cursor_logs)
        self.log_thread.daemon = True
        self.log_thread.start()
        
        # 3. Первоначальная проверка и исправление
        self.initial_check()
        
        print("✅ Система автоматического исправления активна!")
        print("💡 Теперь все конфликты сохранения будут исправляться автоматически")
        
        try:
            while True:
                time.sleep(60)  # Проверка каждую минуту
                self.routine_maintenance()
                
        except KeyboardInterrupt:
            self.stop()
    
    def initial_check(self):
        """Первоначальная проверка и исправление"""
        print("🔍 Выполнение первоначальной проверки...")
        try:
            subprocess.run([
                sys.executable, 
                str(self.project_path / "simple_fix.py")
            ], cwd=self.project_path, check=False)
        except:
            pass
    
    def routine_maintenance(self):
        """Плановое техническое обслуживание"""
        current_time = datetime.now()
        
        # Каждые 10 минут делаем профилактическую очистку
        if current_time.minute % 10 == 0:
            print(f"🧹 [{current_time.strftime('%H:%M:%S')}] Профилактическая очистка...")
            try:
                subprocess.run([
                    sys.executable, 
                    str(self.project_path / "simple_fix.py"), 
                    "clean"
                ], cwd=self.project_path, check=False, capture_output=True)
            except:
                pass
    
    def stop(self):
        """Остановка мониторинга"""
        print("\n🛑 Остановка системы автоматического исправления...")
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        if self.log_monitor:
            self.log_monitor.stop()
        
        print("✅ Система остановлена")

def signal_handler(signum, frame):
    """Обработчик сигналов системы"""
    print("\n🛑 Получен сигнал остановки")
    sys.exit(0)

def main():
    """Главная функция"""
    # Установка обработчиков сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        monitor = AutoFixMonitor()
        monitor.start()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 