#!/usr/bin/env python3
"""
Kleinanzeigen Scanner - аналог VintedScanner для сайта Kleinanzeigen.de
Основан на архитектуре VintedScanner с адаптацией под Kleinanzeigen API/поиск
"""

import sys
import time
import json
import KleinanzeigenConfig
import logging
import requests
import os
import re
from datetime import datetime
from logging.handlers import RotatingFileHandler
import subprocess
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

RESTART_FLAG = "kleinanzeigen_bot_restarted.flag"

# Настройка логирования
file_handler = RotatingFileHandler("kleinanzeigen_scanner.log", maxBytes=5000000, backupCount=5)
console_handler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s():%(lineno)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logging.basicConfig(handlers=[file_handler, console_handler],
                    format="%(asctime)s - %(filename)s - %(funcName)s():%(lineno)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

logger = logging.getLogger(__name__)

timeoutconnection = 30
list_analyzed_items = []

# Headers для имитации реального браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

def load_analyzed_item():
    """Загружает список уже обработанных объявлений из файла"""
    list_analyzed_items.clear()
    try:
        with open("kleinanzeigen_items.txt", "r", errors="ignore") as f:
            for line in f:
                if line:
                    list_analyzed_items.append(line.rstrip())
    except IOError as e:
        logger.error(f"Error loading analyzed items: {e}")

def save_analyzed_item(item_hash):
    """Сохраняет ID обработанного объявления в файл"""
    try:
        with open("kleinanzeigen_items.txt", "a") as f:
            f.write(str(item_hash) + "\n")
    except IOError as e:
        logger.error(f"Error saving analyzed item: {e}")

def send_topic_summary(topic_name, items, thread_id, total_count):
    """Отправляет последние объявления по топику (не сводку)"""
    if not items:
        logger.info(f"No items to send for topic '{topic_name}'")
        return
    
    logger.info(f"Sending {len(items)} items for topic '{topic_name}' (total found: {total_count})")
    
    # Отправляем каждое объявление отдельным сообщением
    for i, item in enumerate(items):
        try:
            send_telegram_topic_message(item, thread_id, is_new=False)
            logger.info(f"Sent item {i+1}/{len(items)}: {item['title'][:50]}...")
            time.sleep(1)  # Пауза между сообщениями
        except Exception as e:
            logger.error(f"Error sending item {i+1}: {e}")
            continue

def send_telegram_topic_message(item, thread_id, max_retries=5, is_new=False):
    """Отправляет уведомление о новом объявлении в Telegram топик"""
    new_indicator = "⭐ " if is_new else ""
    
    # Используем название товара вместо ID
    title = item.get('title', 'Без названия')
    
    # Отладочная информация
    logger.info(f"Sending item: ID={item.get('id', 'N/A')}, Title='{title}'")
    
    caption = f"{new_indicator}<b>{title}</b>\n🏷️ {item['price']}"
    
    # Добавляем размер если есть
    if item.get("size"):
        caption += f"\n📏 Размер: {item['size']}"
    
    # Добавляем способ оплаты (исправлено)
    payment_method = item.get("payment_method", "")
    if payment_method and payment_method != "Kontakt erforderlich":
        caption += f"\n💳 {payment_method}"
    
    # Добавляем описание
    if item.get("description"):
        desc = item['description'][:150] + "..." if len(item['description']) > 150 else item['description']
        caption += f"\n📝 {desc}"
    
    # Прямая ссылка без дополнительного текста
    caption += f"\n🔗 {item['url']}"

    # Используем полное изображение если доступно, иначе превью
    image_url = item.get("full_image") or item.get("image", "")
    
    params = {
        "chat_id": KleinanzeigenConfig.telegram_chat_id,
        "caption": caption,
        "parse_mode": "HTML",
        "message_thread_id": thread_id
    }

    if image_url:
        url = f"https://api.telegram.org/bot{KleinanzeigenConfig.telegram_bot_token}/sendPhoto"
        params["photo"] = image_url
    else:
        url = f"https://api.telegram.org/bot{KleinanzeigenConfig.telegram_bot_token}/sendMessage"
        params["text"] = caption
        params.pop("caption") # caption не используется в sendMessage
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=params, timeout=timeoutconnection)
            if response.status_code == 200:
                status = "new item" if is_new else "summary item"
                logger.info(f"Telegram {status} notification sent to thread {thread_id}")
                return True
            elif response.status_code == 429:
                try:
                    retry_after = response.json().get("parameters", {}).get("retry_after", 30)
                except Exception:
                    retry_after = 30
                logger.warning(f"429 Too Many Requests. Waiting {retry_after} seconds before retry...")
                time.sleep(retry_after)
            else:
                logger.error(f"Telegram notification failed: {response.status_code}, {response.text}")
                break
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            break
        time.sleep(1)
    return False

def handle_restart_flag():
    """Обрабатывает флаг перезапуска бота"""
    if os.path.exists(RESTART_FLAG):
        logger.info("=== KleinanzeigenScanner script was restarted by Telegram command ===")
        os.remove(RESTART_FLAG)
        return True
    return False

def is_first_run():
    """Проверяет, является ли это первым запуском (пустая база объявлений)"""
    return not os.path.exists("kleinanzeigen_items.txt") or os.path.getsize("kleinanzeigen_items.txt") == 0

def filter_by_keywords(title, description, exclude_keywords, required_keywords):
    """Фильтрует объявления по ключевым словам"""
    text = f"{title} {description}".lower()
    
    if exclude_keywords:
        exclude_list = [word.strip().lower() for word in exclude_keywords.split(",") if word.strip()]
        for word in exclude_list:
            if word in text:
                logger.info(f"Item excluded by keyword '{word}': {title}")
                return False
    
    if required_keywords:
        required_list = [word.strip().lower() for word in required_keywords.split(",") if word.strip()]
        for word in required_list:
            if word not in text:
                logger.info(f"Item missing required keyword '{word}': {title}")
                return False
    
    return True

def filter_by_price(price_text, min_price, max_price):
    """Фильтрует объявления по цене"""
    try:
        # Извлекаем числовое значение цены
        price_match = re.search(r'(\d+(?:[.,]\d+)?)', price_text.replace('.', '').replace(',', '.'))
        if not price_match:
            # Если цена не найдена (например "Preis auf Anfrage"), пропускаем фильтр
            return True
        
        price = float(price_match.group(1))
        
        # Проверяем минимальную цену
        if min_price and min_price.strip():
            try:
                min_val = float(min_price)
                if price < min_val:
                    logger.info(f"Item excluded by min price {min_val}€: {price}€")
                    return False
            except ValueError:
                pass
        
        # Проверяем максимальную цену
        if max_price and max_price.strip():
            try:
                max_val = float(max_price)
                if price > max_val:
                    logger.info(f"Item excluded by max price {max_val}€: {price}€")
                    return False
            except ValueError:
                pass
        
        return True
        
    except Exception as e:
        logger.error(f"Error filtering by price '{price_text}': {e}")
        return True  # В случае ошибки не исключаем товар

def get_item_details(item_url, session):
    """Получает подробную информацию о товаре со страницы объявления"""
    details = {
        'full_image': '',
        'payment_method': '',
        'size': '',
        'shipping_available': False,
        'description': ''
    }
    
    try:
        response = session.get(item_url, headers=headers, timeout=timeoutconnection)
        if response.status_code != 200:
            return details
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        img_elem = soup.find('img', {'data-testid': 'gdpr-image'}) or soup.find('img', class_=lambda x: x and 'gallery' in x.lower() if x else False)
        if not img_elem:
            img_elem = soup.select_one('.galleryimage img, .gallery img, [class*="image"] img')
        
        if img_elem:
            for attr in ['data-src', 'src', 'data-srcset']:
                if img_elem.get(attr):
                    details['full_image'] = urljoin(item_url, img_elem[attr])
                    if 'srcset' in attr and ',' in details['full_image']:
                        srcset_images = details['full_image'].split(',')
                        details['full_image'] = urljoin(item_url, srcset_images[-1].strip().split(' ')[0])
                    break
        
        # Ищем кнопки и элементы с информацией о способах оплаты
        payment_buttons = soup.find_all(['button', 'a', 'span', 'div'], string=lambda text: text and any(keyword in text.lower() for keyword in ['kaufen', 'angebot', 'machen', 'buy', 'offer', 'preis']) if text else False)
        payment_methods = []
        
        for button in payment_buttons:
            text = button.get_text(strip=True).lower()
            if 'direkt kaufen' in text or 'sofort kaufen' in text:
                payment_methods.append('Direkt kaufen')
            elif 'angebot machen' in text or 'preisvorschlag' in text:
                payment_methods.append('Angebot machen')
            elif 'festpreis' in text:
                payment_methods.append('Festpreis')
            elif 'verhandlungsbasis' in text or 'vb' in text or 'verhandelbar' in text:
                payment_methods.append('Verhandlungsbasis')
        
        # Дополнительный поиск в описании и заголовках
        full_text = soup.get_text().lower()
        if not payment_methods:
            if 'angebot' in full_text or 'preisvorschlag' in full_text:
                payment_methods.append('Angebot machen')
            elif 'festpreis' in full_text:
                payment_methods.append('Festpreis')
            elif 'vb' in full_text or 'verhandlungsbasis' in full_text:
                payment_methods.append('Verhandlungsbasis')
        
        if payment_methods:
            details['payment_method'] = ' / '.join(set(payment_methods))
        # Убираем дефолтное "Kontakt erforderlich" - оставляем пустым если не найдено
        
        shipping_indicators = soup.find_all(string=lambda text: text and any(keyword in text.lower() for keyword in ['versand', 'shipping', 'lieferung', 'post']) if text else False)
        details['shipping_available'] = len(shipping_indicators) > 0
        
        size_elem = soup.find(string=lambda text: text and any(keyword in text.lower() for keyword in ['größe', 'size', 'gr.']) if text else False)
        if size_elem:
            size_text = size_elem.strip()
            size_match = re.search(r'(größe|size|gr\.?)\s*:?\s*([a-z0-9/\-\s]+)', size_text.lower())
            if size_match:
                details['size'] = size_match.group(2).strip()
        
        description_elem = soup.find('p', {'id': 'ad-description-text'}) or soup.find('div', class_=lambda x: x and 'description' in x.lower() if x else False)
        if description_elem:
            details['description'] = description_elem.get_text(strip=True)[:200]
        
    except Exception as e:
        logger.error(f"Error getting item details from {item_url}: {e}")
    
    return details

def parse_kleinanzeigen_search(search_url, session):
    """Парсит страницу поиска Kleinanzeigen и извлекает объявления"""
    try:
        response = session.get(search_url, headers=headers, timeout=timeoutconnection)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []
        
        article_elements = soup.select('article[data-adid]')
        logger.info(f"Found {len(article_elements)} article elements")
        
        for article in article_elements:
            try:
                item_id = article.get('data-adid')
                if not item_id:
                    continue
                
                # Ищем заголовок товара более точно
                title = ""
                title_link = None
                
                # Попробуем найти ссылку с заголовком в разных местах
                title_selectors = [
                    'a[class*="ellipsis"]',
                    'a h2',
                    'h2 a',
                    '.aditem-main--middle--title a',
                    '.aditem-main--middle a',
                    'a[href*="/s-anzeige/"]'
                ]
                
                for selector in title_selectors:
                    title_link = article.select_one(selector)
                    if title_link and title_link.get('href'):
                        title = title_link.get_text(strip=True)
                        if title and len(title) > 3:  # Минимальная длина заголовка
                            break
                
                # Если ничего не найдено, используем первую ссылку
                if not title or not title_link:
                    title_link = article.find('a', href=True)
                    if title_link:
                        title = title_link.get_text(strip=True)
                
                if not title_link or not title:
                    logger.warning(f"No title found for item {item_id}")
                    continue
                
                item_url = urljoin(KleinanzeigenConfig.kleinanzeigen_url, title_link['href'])
                
                # Отладочная информация для проблемного товара
                if item_id == "3148284434":
                    logger.info(f"DEBUG: Item {item_id} - Title: '{title}', URL: {item_url}")
                
                price_elem = article.find('p', class_='aditem-main--middle--price-shipping--price')
                price = price_elem.get_text(strip=True) if price_elem else "Preis auf Anfrage"
                
                location_elem = article.select_one('[class*="location"], [class*="aditem-main--top--left"]')
                location = location_elem.get_text(strip=True) if location_elem else ""
                
                image_url = ""
                img_elem = article.find('img')
                if img_elem:
                    for attr in ['data-src', 'src', 'data-srcset']:
                        if img_elem.get(attr):
                            image_url = urljoin(search_url, img_elem[attr])
                            if 'srcset' in attr and ',' in image_url:
                                image_url = urljoin(search_url, image_url.split(',')[0].strip().split(' ')[0])
                            break
                
                if item_id and title and item_url:
                    items.append({
                        'id': str(item_id),
                        'title': title,
                        'price': price,
                        'url': item_url,
                        'image': image_url,
                        'location': location,
                        'description': ""
                    })
                    
            except Exception as e:
                logger.error(f"Error parsing item: {e}")
                continue
                
        logger.info(f"Successfully parsed {len(items)} items from search results")
        return items
        
    except Exception as e:
        logger.error(f"Error parsing search page: {e}")
        return []

def build_search_url(topic_info):
    """Строит URL для поиска на Kleinanzeigen"""
    query_params = topic_info["query"]
    
    # Простой формат URL без лишних параметров для тестирования
    base_url = f"{KleinanzeigenConfig.kleinanzeigen_url}"
    
    # Добавляем поисковый запрос в простом формате
    if query_params.get("q"):
        search_query = query_params["q"].replace(" ", "%20")
        base_url += f"/s-{search_query}/k0"
    else:
        base_url += "/s-anzeigen/k0"
    
    logger.info(f"Built search URL: {base_url}")
    return base_url

# Глобальная переменная для отслеживания первого запуска в сессии
first_run_completed = False

def scan_all_topics():
    """Основная функция сканирования всех топиков"""
    global first_run_completed
    
    load_analyzed_item()
    session = requests.Session()
    
    # Первый запуск определяется только один раз за сессию
    first_run = is_first_run() and not first_run_completed
    if first_run:
        logger.info("=== First run detected - will show current items summary ===")
        first_run_completed = True
    
    try:
        session.get(KleinanzeigenConfig.kleinanzeigen_url, headers=headers, timeout=timeoutconnection)
    except Exception as e:
        logger.error(f"Error initializing session: {e}")
    
    for topic_name, topic_info in KleinanzeigenConfig.topics.items():
        logger.info(f"Scanning topic: {topic_name}")
        
        search_url = build_search_url(topic_info)
        thread_id = topic_info["thread_id"]
        summary_count = topic_info.get("summary_count", 5)
        require_shipping = topic_info.get("require_shipping", False)
        
        items = parse_kleinanzeigen_search(search_url, session)
        
        exclude_keywords = topic_info.get("exclude_keywords", "")
        required_keywords = topic_info.get("required_keywords", "")
        min_price = topic_info.get("query", {}).get("minPrice", "")
        max_price = topic_info.get("query", {}).get("maxPrice", "")
        
        filtered_items = []
        new_items = []
        
        for item in items:
            item_id = item["id"]
            
            # Проверяем фильтры по ключевым словам
            if not filter_by_keywords(item["title"], item["description"], exclude_keywords, required_keywords):
                continue
            
            # Проверяем фильтр по цене
            if not filter_by_price(item["price"], min_price, max_price):
                continue
            
            details = get_item_details(item["url"], session)
            
            if require_shipping and not details.get("shipping_available", False):
                logger.info(f"Item excluded (no shipping): {item['title']}")
                continue
            
            item.update(details)
            filtered_items.append(item)
            
            if item_id not in list_analyzed_items:
                new_items.append(item)
                
                time.sleep(0.5)
        
        logger.info(f"Topic '{topic_name}': found {len(filtered_items)} filtered items, {len(new_items)} new items")
        
        if first_run and filtered_items:
            # При первом запуске отправляем только сводку
            send_topic_summary(topic_name, filtered_items[:summary_count], thread_id, len(filtered_items))
            # И сохраняем ВСЕ найденные товары в базу, чтобы они не отправлялись как новые
            for item in filtered_items:
                item_id = item["id"]
                if item_id not in list_analyzed_items:
                    list_analyzed_items.append(item_id)
                    save_analyzed_item(item_id)
        
        elif not first_run and new_items:
            # При последующих запусках отправляем только новые товары
            for item in new_items:
                item_id = item["id"]
                
                if KleinanzeigenConfig.telegram_bot_token and KleinanzeigenConfig.telegram_chat_id:
                    success = send_telegram_topic_message(item, thread_id, is_new=True)
                    if success:
                        logger.info(f"New item notification sent: {item['title']}")
                    time.sleep(2) # Пауза между отправкой новых
                
                list_analyzed_items.append(item_id)
                save_analyzed_item(item_id)
        
        time.sleep(5)

def main():
    """Главная функция"""
    was_restarted = handle_restart_flag()
    if was_restarted:
        # При перезапуске очищаем старые записи, чтобы показать сводку
        if os.path.exists("kleinanzeigen_items.txt"):
            os.remove("kleinanzeigen_items.txt")
        logger.info("=== Bot was restarted - clearing item history ===")
    
    scan_all_topics()

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            logger.info("Scanner stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
        
        logger.info("Scan finished. Waiting 2 seconds for the next run.")
        time.sleep(2)
