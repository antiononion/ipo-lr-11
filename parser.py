import requests
from bs4 import BeautifulSoup
import json

URL = "https://news.ycombinator.com/"


def parse_hacker_news():
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.select(".titleline a")
    subtexts = soup.select(".subtext")

    news = []

    for i in range(min(10, len(titles))):
        title = titles[i].text
        link = titles[i]["href"]

        comments = 0
        if i < len(subtexts):
            comment_tag = subtexts[i].select_one("a:last-child")
            if comment_tag and "comment" in comment_tag.text:
                comments = int(comment_tag.text.split()[0])

        news.append({
            "title": title,
            "comments": comments,
            "link": link
        })

    return news


def save_to_json(data, filename="data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def generate_html(data, filename="index.html"):
    rows = ""
    for item in data:
        rows += f"""
        <tr>
            <td>{item['title']}</td>
            <td>{item['comments']}</td>
            <td><a href="{item['link']}" target="_blank">Перейти</a></td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Hacker News</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(120deg, #1e3c72, #2a5298);
            color: #fff;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            color: #000;
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #ff6600;
            color: white;
        }}
        tr:nth-child(even) {{
            background: #f2f2f2;
        }}
        a {{
            color: #ff6600;
            text-decoration: none;
            font-weight: bold;
        }}
    </style>
</head>
<body>

<h1>Новости Hacker News</h1>

<table>
    <tr>
        <th>Заголовок</th>
        <th>Комментарии</th>
        <th>Источник</th>
    </tr>
    {rows}
</table>

<p style="text-align:center; margin-top:20px;">
    <a href="{URL}" target="_blank">Оригинальный источник: Hacker News</a>
</p>

</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    data = parse_hacker_news()

    for i, item in enumerate(data, start=1):
        print(f"{i}. Title: {item['title']}; Comments: {item['comments']};")

    save_to_json(data)
    generate_html(data)


if __name__ == "__main__":
    main()
