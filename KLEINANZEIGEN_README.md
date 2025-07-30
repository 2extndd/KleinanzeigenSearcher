# Kleinanzeigen Scanner - Инструкция по установке и настройке

## 📋 Описание
Kleinanzeigen Scanner - это бот для автоматического мониторинга объявлений на Kleinanzeigen.de с отправкой уведомлений в Telegram. Основан на архитектуре VintedScanner.

## 🚀 Установка

### 1. Установка зависимостей
```bash
pip install beautifulsoup4 requests python-telegram-bot lxml
```

Или используйте файл requirements:
```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации
Отредактируйте файл `KleinanzeigenConfig.py`:
- Укажите ваш `telegram_bot_token`
- Укажите ваш `telegram_chat_id`
- Настройте фильтры поиска в разделе `topics`

## ⚙️ Настройка фильтров

### Структура фильтра:
```python
"Название топика": {
    "thread_id": 123,  # ID топика в Telegram
    "query": {
        "categoryId": "27",      # ID категории на Kleinanzeigen
        "q": "поисковый запрос", # Ключевые слова для поиска
        "maxPrice": "100",       # Максимальная цена
        "minPrice": "",          # Минимальная цена (оставьте пустым если не нужно)
    },
    "exclude_keywords": "defekt,kaputt",     # Исключаемые слова
    "required_keywords": "original,neu",      # Обязательные слова
    "exclude_locations": "Berlin,München"     # Исключаемые города
}
```

### Популярные ID категорий:
- `27` - Taschen (Сумки)
- `278` - Damenmode (Женская одежда)
- `280` - Herrenmode (Мужская одежда)
- `281` - Schuhe (Обувь)
- `282` - Schmuck & Uhren (Украшения и часы)

💡 **Подсказка**: Чтобы найти ID категории, откройте нужную категорию на Kleinanzeigen.de и посмотрите URL или используйте инструменты разработчика браузера.

## 🤖 Команды Telegram бота

### Основные команды:
- `/start` - Показать список команд
- `/status` - Показать статус бота и статистику
- `/help` - Подробная справка

### Управление:
- `/restart` - Перезапустить сканер
- `/log` - Показать последние 10 строк лога
- `/send_log` - Отправить файл лога

## 🏃‍♂️ Запуск

### Локальный запуск:
```bash
# Запуск сканера
python3 kleinanzeigen_scanner.py

# Запуск только Telegram бота (если сканер уже запущен)
python3 kleinanzeigen_telegram_bot.py
```

### Автоматический запуск:
Сканер автоматически запускает Telegram бот при старте.

## 📁 Файлы проекта

- `kleinanzeigen_scanner.py` - Основной скрипт сканера
- `kleinanzeigen_telegram_bot.py` - Telegram бот с командами
- `KleinanzeigenConfig.py` - Конфигурация фильтров
- `kleinanzeigen_scanner.log` - Файл логов
- `kleinanzeigen_items.txt` - База обработанных объявлений
- `kleinanzeigen_bot_restarted.flag` - Флаг перезапуска

## 🔧 Настройка для Railway/Heroku

### Procfile:
```
web: python3 kleinanzeigen_scanner.py
```

### Environment Variables:
- `TELEGRAM_BOT_TOKEN` - токен вашего бота
- `TELEGRAM_CHAT_ID` - ID чата для уведомлений

## 🐛 Отладка

### Проверка логов:
```bash
tail -f kleinanzeigen_scanner.log
```

### Проверка процесса:
```bash
ps aux | grep kleinanzeigen
```

### Ручная остановка:
```bash
pkill -f kleinanzeigen_scanner.py
```

## ⚠️ Важные замечания

1. **Селекторы HTML**: Селекторы для парсинга Kleinanzeigen могут измениться. При ошибках парсинга проверьте структуру сайта.

2. **Rate Limiting**: Kleinanzeigen может блокировать частые запросы. Настройте задержки между запросами.

3. **Капча**: Сайт может показывать капчу при частых запросах. Используйте VPN или прокси.

4. **Обновления**: Регулярно обновляйте селекторы HTML и параметры API при изменениях на сайте.

## 🔄 Обновление с VintedScanner

Если у вас уже есть VintedScanner:
1. Команда `/delete_old` удалена из VintedScanner как неактуальная
2. Kleinanzeigen Scanner использует ту же архитектуру и команды
3. Файлы конфигурации независимы - можно использовать оба бота одновременно

## 📞 Поддержка

При проблемах:
1. Проверьте логи командой `/log` в Telegram
2. Отправьте полный лог командой `/send_log`
3. Проверьте статус командой `/status`
4. Убедитесь в правильности настроек в `KleinanzeigenConfig.py`
