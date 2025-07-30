# Конфигурация для Kleinanzeigen Scanner
# Основана на структуре VintedScanner с адаптацией под Kleinanzeigen

# Telegram Token и ChatID для уведомлений
telegram_bot_token = "8218691814:AAEZzQRMxjidAMeJzmyUzkxwRciPRDpct6c"
telegram_chat_id = "-1002721134127"

# Kleinanzeigen URL
kleinanzeigen_url = "https://www.kleinanzeigen.de"

# Список топиков и параметров для поиска
# Адаптировано под реальную структуру Kleinanzeigen
topics = {
    "GGL": {
        "thread_id": 718,  # ID топика в Telegram
        "summary_count": 5,  # Количество вещей для показа при запуске/перезагрузке
        "query": {
            # Параметры поиска для Kleinanzeigen (реальные)
            "categoryId": "156",  # Категория "Accessoires & Schmuck"
            "q": "george gina lucy, ggl,GG&L,George Gina &Lucie",     # Поисковый запрос
            "maxPrice": "50",   # Максимальная цена до 50 евро
            "minPrice": "",      # Минимальная цена (пусто = без ограничений)
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",  # Исключаемые ключевые слова
        "required_keywords": "",  # Обязательные ключевые слова (пусто = любые)
        "exclude_locations": "",   # Исключаемые города/регионы
        "require_shipping": True,  # Только с возможностью доставки

        
    },
    "Rick Owens": {
        "thread_id": 718,  # ID топика в Telegram
        "summary_count": 5,  # Количество вещей для показа при запуске/перезагрузке
        "query": {
            # Параметры поиска для Kleinanzeigen (реальные)
            "categoryId": "158,160",  # Категория "Accessoires & Schmuck"
            "q": "rick owens,DRKSHDW, ",     # Поисковый запрос
            "maxPrice": "100",   # Максимальная цена до 100 евро
            "minPrice": "",      # Минимальная цена (пусто = без ограничений)
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",  # Исключаемые ключевые слова
        "required_keywords": "",  # Обязательные ключевые слова (пусто = любые)
        "exclude_locations": "",   # Исключаемые города/регионы
        "require_shipping": True,  # Только с возможностью доставки

        
    },
    "Maison Margiela": {
        "thread_id": 718,  # ID топика в Telegram
        "summary_count": 5,  # Количество вещей для показа при запуске/перезагрузке
        "query": {
            # Параметры поиска для Kleinanzeigen (реальные)
            "categoryId": "158,160,154,156",  # Категория "Accessoires & Schmuck"
            "q": "maison margiela,mm6",     # Поисковый запрос
            "maxPrice": "80",   # Максимальная цена до 80 евро
            "minPrice": "",      # Минимальная цена (пусто = без ограничений)
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",  # Исключаемые ключевые слова
        "required_keywords": "",  # Обязательные ключевые слова (пусто = любые)
        "exclude_locations": "",   # Исключаемые города/регионы
        "require_shipping": True,  # Только с возможностью доставки

    },
    "Comme des Garçons": {
        "thread_id": 718,  # ID топика в Telegram
        "summary_count": 5,  # Количество вещей для показа при запуске/перезагрузке
        "query": {
            # Параметры поиска для Kleinanzeigen (реальные)
            "categoryId": "158,160",  # Категория "Accessoires & Schmuck"
            "q": "comme des garcons, cdg",     # Поисковый запрос
            "maxPrice": "50",   # Максимальная цена до 50 евро
            "minPrice": "",      # Минимальная цена (пусто = без ограничений)
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",  # Исключаемые ключевые слова
        "required_keywords": "",  # Обязательные ключевые слова (пусто = любые)
        "exclude_locations": "",   # Исключаемые города/регионы
        "require_shipping": True,  # Только с возможностью доставки

    },
    "Raf Simons": {
        "thread_id": 718,  # ID топика в Telegram
        "summary_count": 5,  # Количество вещей для показа при запуске/перезагрузке
        "query": {
            # Параметры поиска для Kleinanzeigen (реальные)
            "categoryId": "158,160",  # Категория "Accessoires & Schmuck"
            "q": "raf simons, raf,raf by raf,raf by raf simons",     # Поисковый запрос
            "maxPrice": "100",   # Максимальная цена до 100 евро
            "minPrice": "",      # Минимальная цена (пусто = без ограничений)
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",  # Исключаемые ключевые слова
        "required_keywords": "",  # Обязательные ключевые слова (пусто = любые)
        "exclude_locations": "",   # Исключаемые города/регионы
        "require_shipping": True,  # Только с возможностью доставки

    },
    "Yohji Yamamoto": {
        "thread_id": 718,  # ID топика в Telegram
        "summary_count": 5,  # Количество вещей для показа при запуске/перезагрузке
        "query": {
            # Параметры поиска для Kleinanzeigen (реальные)
            "categoryId": "158,160,156",  # Категория "Accessoires & Schmuck"
            "q": "y-3, Yohji Yamamoto,Yohji",     # Поисковый запрос
            "maxPrice": "80",   # Максимальная цена до 80 евро
            "minPrice": "",      # Минимальная цена (пусто = без ограничений)
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",  # Исключаемые ключевые слова
        "required_keywords": "",  # Обязательные ключевые слова (пусто = любые)
        "exclude_locations": "",   # Исключаемые города/регионы
        "require_shipping": True,  # Только с возможностью доставки

    },
    "Alyx": {
        "thread_id": 718,  # ID топика в Telegram
        "summary_count": 5,  # Количество вещей для показа при запуске/перезагрузке
        "query": {
            # Параметры поиска для Kleinanzeigen (реальные)
            "categoryId": "158,160,156",  # Категория "Accessoires & Schmuck"
            "q": "Alyx",     # Поисковый запрос
            "maxPrice": "80",   # Максимальная цена до 80 евро
            "minPrice": "",      # Минимальная цена (пусто = без ограничений)
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",  # Исключаемые ключевые слова
        "required_keywords": "",  # Обязательные ключевые слова (пусто = любые)
        "exclude_locations": "",   # Исключаемые города/регионы
        "require_shipping": True,  # Только с возможностью доставки

    },
    "Dolce & Gabbana": {
        "thread_id": 718,  # ID топика в Telegram
        "summary_count": 5,  # Количество вещей для показа при запуске/перезагрузке
        "query": {
            # Параметры поиска для Kleinanzeigen (реальные)
            "categoryId": "160,156",  # Категория "Accessoires & Schmuck"
            "q": "Dolce & Gabbana,Dolce Gabbana",     # Поисковый запрос
            "maxPrice": "60",   # Максимальная цена до 60 евро
            "minPrice": "",      # Минимальная цена (пусто = без ограничений)
        },
        "exclude_keywords": "defekt,kaputt,beschädigt,fake,replica",  # Исключаемые ключевые слова
        "required_keywords": "",  # Обязательные ключевые слова (пусто = любые)
        "exclude_locations": "",   # Исключаемые города/регионы
        "require_shipping": True,  # Только с возможностью доставки


    }
    


}



# ПОДСКАЗКИ ДЛЯ НАСТРОЙКИ:
# 1. categoryId - ID категории товаров на Kleinanzeigen (нужно найти в network tab браузера)
# 2. q - поисковый запрос (ключевые слова)
# 3. exclude_keywords - слова для исключения из результатов (через запятую)
# 4. required_keywords - обязательные слова в заголовке (через запятую)
# 5. thread_id - ID топика в Telegram для отправки уведомлений
# 6. summary_count - количество вещей для показа при запуске/перезагрузке (по умолчанию 5)
# 7. require_shipping - только товары с возможностью доставки (True/False)
# 8. Цены указываются в евро
