# Инструкции по запуску Kleinanzeigen Scanner

## 🚀 Облачный запуск (Railway)

1. **Push на GitHub** - система автоматически деплоится
2. **Проверить логи** в Railway Dashboard
3. **Ждать уведомление** в Telegram о запуске бота

## 💻 Локальный запуск

### Предварительные требования
```bash
pip install -r requirements.txt
```

### Запуск всей системы
```bash
python3 start.py
```

### Раздельный запуск

**Только сканер:**
```bash
python3 kleinanzeigen_scanner.py
```

**Только бот:**
```bash
python3 simple_bot.py
```

## 🔧 Настройка

### Telegram настройки
В `KleinanzeigenConfig.py`:
- `telegram_bot_token` - токен бота от @BotFather
- `telegram_chat_id` - ID группы/чата для уведомлений
- `thread_id` - ID топика в группе

### Поиск настройки
```python
"query": {
    "q": "george gina lucy",     # Что искать
    "maxPrice": "50",            # Максимальная цена
}
```

### Фильтры
```python
"exclude_keywords": "defekt,kaputt,beschädigt,fake,replica"
"require_shipping": True  # Только с доставкой
```

## 🧪 Тестирование

### Проверка подключения к Telegram
```bash
python3 -c "
import KleinanzeigenConfig
import requests
url = f'https://api.telegram.org/bot{KleinanzeigenConfig.telegram_bot_token}/getMe'
print(requests.get(url).json())
"
```

### Проверка парсинга
```bash
python3 test_kleinanzeigen.py
```

## 📋 Команды Telegram бота

- `/status2` - Статус сканера и системы
- `/log2` - Последние 20 строк лога
- `/threadid2` - Показать настроенные топики
- `/restart2` - Принудительный перезапуск сканера

## 🐛 Отладка

### Логи
```bash
tail -f kleinanzeigen_scanner.log
```

### Проверка процессов
```bash
ps aux | grep kleinanzeigen
```

### Остановка
```bash
pkill -f kleinanzeigen
```
