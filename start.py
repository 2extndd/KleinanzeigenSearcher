#!/usr/bin/env python3
"""
Стартовый скрипт для запуска и сканера, и Telegram бота одновременно
"""

import subprocess
import sys
import time
import signal
import os

# Глобальные переменные для процессов
scanner_process = None
bot_process = None

def signal_handler(signum, frame):
    """Обработчик сигналов для корректного завершения"""
    print("\n🛑 Получен сигнал завершения...")
    cleanup_processes()
    sys.exit(0)

def cleanup_processes():
    """Корректное завершение всех процессов"""
    global scanner_process, bot_process
    
    if scanner_process and scanner_process.poll() is None:
        print("🔄 Останавливаем сканер...")
        scanner_process.terminate()
        scanner_process.wait()
        
    if bot_process and bot_process.poll() is None:
        print("🔄 Останавливаем бота...")
        bot_process.terminate()
        bot_process.wait()

def main():
    global scanner_process, bot_process
    
    # Регистрируем обработчик сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🎯 Kleinanzeigen Scanner System - Starting...")
    print("=" * 50)
    
    try:
        # Запускаем сканер
        print("🚀 Запускаем сканер...")
        scanner_process = subprocess.Popen([
            sys.executable, "kleinanzeigen_scanner.py"
        ])
        print(f"✅ Сканер запущен (PID: {scanner_process.pid})")
        
        # Небольшая задержка
        time.sleep(5)
        
        # Запускаем Telegram бота
        print("🤖 Запускаем Telegram бота...")
        bot_process = subprocess.Popen([
            sys.executable, "simple_bot.py"
        ])
        print(f"✅ Telegram бот запущен (PID: {bot_process.pid})")
        
        print("🎯 Система полностью запущена!")
        print("=" * 50)
        
        # Мониторим процессы
        while True:
            scanner_status = scanner_process.poll()
            bot_status = bot_process.poll()
            
            if scanner_status is not None:
                print(f"❌ Сканер завершился с кодом: {scanner_status}")
                cleanup_processes()
                break
                
            if bot_status is not None:
                print(f"❌ Telegram бот завершился с кодом: {bot_status}")
                cleanup_processes()
                break
                
            time.sleep(10)  # Проверяем каждые 10 секунд
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        cleanup_processes()
    
    print("✅ Все процессы завершены")

if __name__ == "__main__":
    main()
