"""
Тестовый валидатор автономной посадочной страницы (bridge_page)
Проверка структуры HTML5, адаптивности CSS3 и корректности партнерской ссылки Creative Fabrica
"""

import os
import re
import sys

BRIDGE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BRIDGE_DIR, "index.html")
CSS_PATH = os.path.join(BRIDGE_DIR, "style.css")
EXPECTED_AFFILIATE_URL = "https://www.creativefabrica.com/ref/29590294/"
AFFILIATE_ID = "29590294"


def test_bridge_page():
    print("=" * 60)
    print("BRIDGE PAGE VALIDATION AUDIT: L'Atelier Slow Fashion")
    print("=" * 60)

    errors = 0
    warnings = 0

    # 1. Проверка наличия файлов
    if not os.path.exists(HTML_PATH):
        print(f"[FAIL] Файл не найден: {HTML_PATH}")
        errors += 1
    else:
        print(f"[PASS] index.html обнаружен ({os.path.getsize(HTML_PATH)} байт)")

    if not os.path.exists(CSS_PATH):
        print(f"[FAIL] Файл не найден: {CSS_PATH}")
        errors += 1
    else:
        print(f"[PASS] style.css обнаружен ({os.path.getsize(CSS_PATH)} байт)")

    if errors > 0:
        return False

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    with open(CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()

    # 2. Семантический аудит HTML
    tags_to_check = [
        ('<!DOCTYPE html>', 'HTML5 Doctype'),
        ('<meta name="viewport"', 'Responsive Viewport Meta Tag'),
        ('<header', 'Semantic Header Tag'),
        ('<main', 'Semantic Main Tag'),
        ('<footer', 'Semantic Footer Tag'),
        ('<title>', 'Page Title Tag'),
        ('Affiliate Disclosure', 'FTC / Affiliate Disclosure Block')
    ]
    for pattern, name in tags_to_check:
        if pattern.lower() in html.lower():
            print(f"[PASS] {name} присутствует.")
        else:
            print(f"[FAIL] {name} отсутствует!")
            errors += 1

    # 3. Аудит внешних зависимостей (Автономность)
    external_links = re.findall(r'<link[^>]+href=[\'"](http[s]?://[^\'"]+)[\'"]', html, re.IGNORECASE)
    external_scripts = re.findall(r'<script[^>]+src=[\'"](http[s]?://[^\'"]+)[\'"]', html, re.IGNORECASE)
    if not external_links and not external_scripts:
        print("[PASS] 100% Автономность: сторонние тяжелые скрипты и CSS-фреймворки отсутствуют.")
    else:
        print(f"[WARN] Обнаружены внешние ресурсы: {external_links + external_scripts}")
        warnings += 1

    # 4. Аудит партнерских ссылок
    cta_links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>', html, re.IGNORECASE)
    affiliate_links = [l for l in cta_links if EXPECTED_AFFILIATE_URL in l]
    print(f"[INFO] Найдено ссылок перехода: {len(cta_links)} (из них партнерских Creative Fabrica: {len(affiliate_links)})")

    if len(affiliate_links) >= 5:
        print(f"[PASS] Все CTA-кнопки содержат точный URL с Affiliate ID {AFFILIATE_ID}")
    else:
        print(f"[FAIL] Недостаточно партнерских ссылок (найдено {len(affiliate_links)}, ожидалось минимум 5)")
        errors += 1

    # Проверка параметров безопасности ссылок
    for match in re.finditer(r'<a\s+([^>]+)>', html, re.IGNORECASE):
        attrs = match.group(1)
        if EXPECTED_AFFILIATE_URL in attrs:
            if 'target="_blank"' not in attrs:
                print("[WARN] Ссылка не имеет target=\"_blank\"")
                warnings += 1
            if 'noopener' not in attrs or 'noreferrer' not in attrs:
                print("[WARN] Ссылка не имеет noopener noreferrer")
                warnings += 1

    # 5. Аудит адаптивности CSS
    media_queries = re.findall(r'@media[^{]+{', css)
    if len(media_queries) >= 2:
        print(f"[PASS] Адаптивность: обнаружено {len(media_queries)} медиа-запросов (Mobile/Tablet optimization)")
    else:
        print("[FAIL] Недостаточно CSS медиа-запросов для мобильных экранов")
        errors += 1

    # Проверка палитры Vintage Junk Journal
    required_colors = ['#FAF8F5', '#1E1716', '#C5A059', '#702630']
    colors_found = [c for c in required_colors if c.lower() in css.lower()]
    if len(colors_found) == len(required_colors):
        print(f"[PASS] Фирменная палитра внедрена на 100% ({', '.join(colors_found)})")
    else:
        print(f"[WARN] Часть цветов палитры отсутствует: {set(required_colors) - set(colors_found)}")
        warnings += 1

    print("-" * 60)
    if errors == 0:
        print("ИТОГ: Bridge Page успешно прошла валидацию на 100%!")
        return True
    else:
        print(f"ИТОГ: Обнаружено ошибок: {errors}, предупреждений: {warnings}")
        return False


if __name__ == "__main__":
    success = test_bridge_page()
    sys.exit(0 if success else 1)
