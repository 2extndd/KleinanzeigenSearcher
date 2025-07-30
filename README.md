# Kleinanzeigen Scanner

Автоматический сканер для поиска товаров на Kleinanzeigen.de с уведомлениями в Telegram.

## 🎯 Возможности

- **Автоматическое сканирование** Kleinanzeigen.de каждые 2 секунды
- **Фильтрация по цене** (максимум 50€)
- **Исключение ключевых слов** (defekt, kaputt, beschädigt, fake, replica)
- **Telegram уведомления** с прямыми ссылками на товары
- **Telegram бот** для управления и мониторинга
- **Облачный деплой** на Railway

## 🔧 Конфигурация

Основные настройки в `KleinanzeigenConfig.py`:

```python
topics = {
    "GGL": {
        "thread_id": 718,
        "query": {
            "q": "george gina lucy",
            "maxPrice": "50",
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",
        "require_shipping": True,
    },
}
```

## 🤖 Telegram команды

- `/status2` - Показать статус сканера
- `/log2` - Последние 20 строк логов
- `/threadid2` - Показать ID топиков
- `/restart2` - Перезапустить сканер

## 🚀 Деплой

Проект автоматически деплоится на Railway при push в main ветку.

### Локальный запуск

```bash
python3 start.py
```

## 📁 Структура файлов

- `kleinanzeigen_scanner.py` - Основной сканер
- `simple_bot.py` - Telegram бот для управления
- `KleinanzeigenConfig.py` - Конфигурация
- `start.py` - Объединенный запуск сканера и бота
- `requirements.txt` - Python зависимости
- `Procfile` - Конфигурация для Railway

## ⚙️ Технологии

- Python 3
- BeautifulSoup4 для парсинга
- python-telegram-bot для Telegram API
- requests для HTTP запросов
- Railway для облачного хостинга

## 📝 Логи

Система ведет подробные логи в файл `kleinanzeigen_scanner.log` со всеми найденными товарами и действиями.
