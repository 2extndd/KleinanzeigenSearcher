#!/usr/bin/env python3
"""
Простой Telegram Bot для Kleinanzeigen Scanner
Основные команды без сложных функций
"""

import os
import subprocess
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import KleinanzeigenConfig

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

LOG_FILE = "kleinanzeigen_scanner.log"
SCANNER_SCRIPT = "kleinanzeigen_scanner.py"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    help_text = """
🤖 <b>Kleinanzeigen Scanner Bot</b>

Доступные команды:
/status2 - Расширенный статус
/threadid2 - Показать ID топиков
/restart2 - Принудительный перезапуск
/log2 - Последние 20 строк лога

<i>Бот сканирует Kleinanzeigen.de и отправляет уведомления.</i>
    """
    await update.message.reply_text(help_text, parse_mode='HTML')

async def show_threadid2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать ID топиков"""
    try:
        thread_text = "🎯 <b>ID топиков в конфигурации:</b>\n\n"
        for name, config in KleinanzeigenConfig.topics.items():
            thread_text += f"• <b>{name}</b>\n"
            thread_text += f"  Thread ID: <code>{config['thread_id']}</code>\n"
            thread_text += f"  Показывать при запуске: {config.get('summary_count', 5)}\n\n"
        
        await update.message.reply_text(thread_text, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def show_log2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать последние 20 строк лога"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                last_lines = lines[-20:] if len(lines) >= 20 else lines
                log_text = ''.join(last_lines)
                
            if log_text:
                # Экранируем HTML символы для безопасного отображения
                import html
                log_text = html.escape(log_text)
                
                message = f"📋 <b>Последние 20 строк лога:</b>\n\n<pre>{log_text}</pre>"
                if len(message) > 4000:
                    message = message[:4000] + "...\n<i>[обрезано]</i>"
                await update.message.reply_text(message, parse_mode='HTML')
            else:
                await update.message.reply_text("📋 Лог файл пуст")
        else:
            await update.message.reply_text("❌ Файл лога не найден")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def show_status2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Расширенный статус"""
    try:
        scanner_running = False
        try:
            result = subprocess.run(["pgrep", "-f", SCANNER_SCRIPT], capture_output=True, text=True)
            scanner_running = bool(result.stdout.strip())
        except:
            pass
        
        # Статистика лога
        log_lines = 0
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r') as f:
                    log_lines = sum(1 for _ in f)
            except:
                pass
        
        status_text = f"""
🔍 <b>Расширенный статус Kleinanzeigen Scanner</b>

🤖 Сканер: {'🟢 Запущен' if scanner_running else '🔴 Остановлен'}
📄 Лог файл: {'🟢 Найден' if os.path.exists(LOG_FILE) else '🔴 Не найден'}
⚙️ Конфигурация: {'🟢 Найдена' if os.path.exists("KleinanzeigenConfig.py") else '🔴 Не найдена'}

📊 <b>Статистика:</b>
📝 Строк в логе: {log_lines}
🔧 Топиков настроено: {len(KleinanzeigenConfig.topics)}

💡 Используйте /restart2 для принудительного перезапуска
        """
        await update.message.reply_text(status_text, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def restart_scanner2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Принудительный перезапуск"""
    try:
        await update.message.reply_text("🔄 Принудительный перезапуск...")
        
        try:
            subprocess.run(["pkill", "-f", "kleinanzeigen"], check=False)
            await update.message.reply_text("⚠️ Все процессы остановлены")
        except:
            pass
        
        import time
        time.sleep(2)
        
        subprocess.Popen(["python3", SCANNER_SCRIPT])
        await update.message.reply_text("✅ Сканер принудительно перезапущен!")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    if "Conflict" in str(context.error):
        logger.error("Bot conflict detected - another instance may be running")

def main():
    """Запуск бота"""
    print("🤖 Kleinanzeigen Telegram Bot запущен!")
    logger.info("Kleinanzeigen Telegram Bot started")
    
    try:
        # Проверяем токен перед запуском
        print(f"📡 Проверяем подключение к Telegram API...")
        import requests
        url = f'https://api.telegram.org/bot{KleinanzeigenConfig.telegram_bot_token}/getMe'
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data.get('ok'):
            raise Exception(f"Токен не работает: {data.get('description')}")
            
        bot_info = data.get('result', {})
        print(f"✅ Бот подключен: @{bot_info.get('username')}")
        logger.info(f"Bot connected: @{bot_info.get('username')}")
        
    except Exception as e:
        print(f"❌ Ошибка подключения к Telegram: {e}")
        logger.error(f"Telegram connection error: {e}")
        return
    
    # Создаем приложение
    print("🔧 Создаем приложение бота...")
    application = Application.builder().token(KleinanzeigenConfig.telegram_bot_token).build()
    
    # Добавляем обработчики команд
    print("📝 Регистрируем команды...")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("threadid2", show_threadid2))
    application.add_handler(CommandHandler("log2", show_log2))
    application.add_handler(CommandHandler("status2", show_status2))
    application.add_handler(CommandHandler("restart2", restart_scanner2))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🚀 Запускаем polling...")
    logger.info("Starting bot polling...")
    
    # Отправляем уведомление о запуске
    async def send_startup_notification():
        try:
            from telegram import Bot
            bot = Bot(token=KleinanzeigenConfig.telegram_bot_token)
            await bot.send_message(
                chat_id=KleinanzeigenConfig.telegram_chat_id,
                text="🤖 Kleinanzeigen Bot запущен и готов к работе!\n\nДоступные команды:\n/status2 - статус\n/log2 - логи\n/threadid2 - топики\n/restart2 - перезапуск"
            )
            await bot.close()
            print("✅ Уведомление о запуске отправлено")
        except Exception as e:
            print(f"⚠️ Не удалось отправить уведомление о запуске: {e}")
    
    # Запускаем уведомление в фоне
    import asyncio
    try:
        asyncio.run(send_startup_notification())
    except Exception as e:
        print(f"⚠️ Ошибка отправки уведомления: {e}")
    
    try:
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True  # Игнорируем старые обновления
        )
    except Exception as e:
        logger.error(f"Bot error: {e}")
        print(f"❌ Ошибка бота: {e}")
        raise

if __name__ == "__main__":
    main()
