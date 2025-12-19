import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def parse_hacker_news():
    """Парсит новости с Hacker News"""
    url = "https://news.ycombinator.com/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        print("Ошибка при получении страницы")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = []
    
    # Находим все строки с заголовками
    titles = soup.find_all('span', class_='titleline')
    
    for i, title in enumerate(titles, 1):
        try:
            title_link = title.find('a')
            news_title = title_link.text.strip()
            news_url = title_link.get('href', '')
            
            # Ищем мета-информацию
            row = title.find_parent('tr')
            subtext = row.find_next_sibling('tr').find('td', class_='subtext')
            
            # Извлекаем комментарии
            comments = 0
            if subtext:
                comments_elem = subtext.find_all('a')[-1]
                if comments_elem and 'comment' in comments_elem.text:
                    comments_text = comments_elem.text
                    for word in comments_text.split():
                        if word.isdigit():
                            comments = int(word)
                            break
            
            # Добавляем новость
            news_list.append({
                'id': i,
                'title': news_title,
                'url': news_url if news_url.startswith('http') else f'https://news.ycombinator.com/{news_url}',
                'comments': comments
            })
            
        except:
            continue
    
    return news_list

def save_to_json(news_data, filename='data.json'):
    """Сохраняет данные в JSON файл"""
    data = {
        'last_updated': datetime.now().isoformat(),
        'source': 'https://news.ycombinator.com/',
        'news_count': len(news_data),
        'news': news_data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Данные сохранены в {filename}")

def print_news_to_console(news_data):
    """Выводит новости в консоль"""
    print("\nНовости с Hacker News:")
    print("=" * 50)
    
    for news in news_data:
        title = news['title']
        if len(title) > 50:
            title = title[:47] + "..."
        print(f"{news['id']}. Title: {title}; Comments: {news['comments']};")
    
    print(f"\nВсего новостей: {len(news_data)}")

def generate_html(news_data, filename='index.html'):
    """Генерирует HTML страницу с таблицей новостей"""
    
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hacker News</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        h1 {{
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background: #f0f0f0;
            padding: 10px;
            text-align: left;
            border: 1px solid #ccc;
        }}
        td {{
            padding: 8px;
            border: 1px solid #ccc;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .source-link {{
            text-align: center;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>Hacker News Parser</h1>
    <p>Всего новостей: {len(news_data)}</p>
    <p>Дата обновления: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <table>
        <tr>
            <th>#</th>
            <th>Заголовок</th>
            <th>Комментарии</th>
        </tr>
'''
    
    # Добавляем строки таблицы
    for news in news_data:
        html_content += f'''
        <tr>
            <td>{news['id']}</td>
            <td><a href="{news['url']}" target="_blank">{news['title']}</a></td>
            <td>{news['comments']}</td>
        </tr>
'''
    
    html_content += f'''
    </table>
    
    <div class="source-link">
        <a href="https://news.ycombinator.com/" target="_blank">
            🔗 Посетить оригинальный Hacker News
        </a>
    </div>
</body>
</html>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML страница создана: {filename}")

def main():
    """Основная функция программы"""
    print("Парсим Hacker News...")
    
    # Парсим новости
    news_data = parse_hacker_news()
    
    if not news_data:
        print("Не удалось получить новости")
        return
    
    # Выводим в консоль
    print_news_to_console(news_data)
    
    # Сохраняем в JSON
    save_to_json(news_data)
    
    # Генерируем HTML
    generate_html(news_data)
    
    print("\nЗадание выполнено!")
    print("Откройте файл index.html в браузере")

if __name__ == "__main__":
    main()