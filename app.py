
from flask import Flask, request, redirect, url_for, render_template_string
import json
import os

app = Flask(__name__)

FILE_NAME = "books.json"


def load_books():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_books():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


books = load_books()


HTML = """
<!DOCTYPE html>
<html lang="bg">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BookSpace | Дигитална библиотека</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background: #0b1020;
    color: #f5f6ff;
    min-height: 100vh;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: auto;
}

/* NAVBAR */

nav {
    padding: 25px 0;
    border-bottom: 1px solid #252b40;
}

.nav-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 25px;
    font-weight: 800;
    color: white;
}

.logo span {
    color: #9b8cff;
}

.nav-label {
    color: #a7acc2;
    font-size: 13px;
}

/* HERO */

.hero {
    padding: 75px 0 45px;
    text-align: center;
}

.tag {
    display: inline-block;
    background: #211d42;
    color: #aa9cff;
    padding: 9px 18px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: clamp(36px, 6vw, 60px);
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 20px;
}

.hero h1 span {
    background: linear-gradient(90deg, #9d8bff, #60c8ff);
    -webkit-background-clip: text;
    color: transparent;
}

.hero p {
    color: #929ab4;
    font-size: 16px;
    line-height: 1.8;
}

/* STATISTICS */

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin: 30px 0 50px;
}

.stat-card {
    background: #141b30;
    border: 1px solid #272f49;
    padding: 25px;
    border-radius: 18px;
    transition: .3s;
}

.stat-card:hover {
    transform: translateY(-5px);
    border-color: #8d7cff;
}

.stat-icon {
    font-size: 25px;
    margin-bottom: 15px;
}

.stat-number {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 7px;
}

.stat-name {
    color: #929ab4;
    font-size: 13px;
}

/* MAIN SECTION */

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    gap: 15px;
}

.section-header h2 {
    font-size: 25px;
    font-weight: 700;
}

.section-header p {
    color: #929ab4;
    font-size: 13px;
    margin-top: 8px;
}

/* SEARCH */

.search-box {
    display: flex;
    gap: 12px;
    margin-bottom: 25px;
}

.search-box input {
    flex: 1;
    min-width: 0;
    padding: 16px 20px;
    border-radius: 12px;
    border: 1px solid #303852;
    background: #141b30;
    color: white;
    outline: none;
    font-size: 14px;
}

.search-box input:focus {
    border-color: #9584ff;
}

button, .sort-btn {
    border: none;
    cursor: pointer;
    font-family: inherit;
    font-weight: 700;
    transition: .3s;
}

.search-btn {
    background: #8b78ff;
    color: white;
    border-radius: 12px;
    padding: 0 25px;
}

.search-btn:hover, .add-btn:hover {
    background: #725de8;
}

/* ADD BOOK */

.add-panel {
    background: linear-gradient(120deg, #191d3b, #202344);
    border: 1px solid #35335e;
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 35px;
}

.add-panel h3 {
    margin-bottom: 18px;
    font-size: 18px;
}

.add-form {
    display: flex;
    gap: 12px;
}

.add-form input {
    flex: 1;
    min-width: 0;
    background: #11172a;
    border: 1px solid #353d5b;
    color: white;
    padding: 15px;
    border-radius: 10px;
    outline: none;
    font-size: 14px;
}

.add-form input:focus {
    border-color: #9b8cff;
}

.add-btn {
    background: #8b78ff;
    color: white;
    padding: 0 25px;
    border-radius: 10px;
}

/* BOOK CARDS */

.books-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding-bottom: 80px;
}

.book-card {
    background: #141b30;
    border: 1px solid #272f49;
    border-radius: 18px;
    padding: 25px;
    transition: .3s;
    position: relative;
    overflow: hidden;
}

.book-card:hover {
    transform: translateY(-6px);
    border-color: #8b78ff;
}

.book-cover {
    height: 150px;
    border-radius: 12px;
    background: linear-gradient(135deg, #5145a6, #262c58);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 55px;
    margin-bottom: 22px;
}

.book-card:nth-child(3n+2) .book-cover {
    background: linear-gradient(135deg, #176b87, #24385d);
}

.book-card:nth-child(3n+3) .book-cover {
    background: linear-gradient(135deg, #884d80, #392a60);
}

.book-label {
    color: #a99aff;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
}

.book-title {
    font-size: 17px;
    font-weight: 700;
    margin: 12px 0 20px;
    word-break: break-word;
}

.book-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #29314b;
    padding-top: 16px;
}

.book-number {
    color: #929ab4;
    font-size: 12px;
}

.delete-btn {
    color: #ff8b9b;
    background: #3c202f;
    border-radius: 8px;
    padding: 9px 13px;
    font-size: 12px;
}

.delete-btn:hover {
    background: #713044;
}

/* EMPTY STATE */

.empty {
    grid-column: 1 / -1;
    text-align: center;
    background: #141b30;
    border: 1px dashed #414966;
    border-radius: 18px;
    padding: 65px 20px;
}

.empty-icon {
    font-size: 55px;
    margin-bottom: 20px;
}

.empty h3 {
    margin-bottom: 10px;
}

.empty p {
    color: #929ab4;
    font-size: 14px;
}

/* FOOTER */

footer {
    text-align: center;
    border-top: 1px solid #252b40;
    padding: 30px;
    color: #727d9b;
    font-size: 12px;
}

@media(max-width: 800px) {
    .books-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .stats {
        gap: 12px;
    }
}

@media(max-width: 550px) {
    .books-grid {
        grid-template-columns: 1fr;
    }

    .stats {
        grid-template-columns: 1fr;
    }

    .add-form {
        flex-direction: column;
    }

    .add-btn {
        padding: 15px;
    }

    .search-box {
        flex-direction: column;
    }

    .search-btn {
        padding: 15px;
    }

    .hero {
        padding-top: 50px;
    }
}
</style>
</head>

<body>

<nav>
    <div class="container nav-content">
        <div class="logo">Book<span>Space.</span></div>
        <div class="nav-label">✦ YOUR DIGITAL LIBRARY</div>
    </div>
</nav>

<div class="container">

    <section class="hero">
        <div class="tag">✦ WELCOME TO BOOKSPACE</div>

        <h1>
            Твоят свят от<br>
            <span>безкрайни истории.</span>
        </h1>

        <p>
            Открий, организирай и управлявай любимите си книги.<br>
            Всички твои истории на едно място.
        </p>
    </section>

    <section class="stats">

        <div class="stat-card">
            <div class="stat-icon">📚</div>
            <div class="stat-number">{{ total }}</div>
            <div class="stat-name">Общо книги</div>
        </div>

        <div class="stat-card">
            <div class="stat-icon">🔍</div>
            <div class="stat-number">{{ results }}</div>
            <div class="stat-name">Намерени книги</div>
        </div>

        <div class="stat-card">
            <div class="stat-icon">✨</div>
            <div class="stat-number">∞</div>
            <div class="stat-name">Нови истории</div>
        </div>

    </section>

    <section class="add-panel">
        <h3>✦ Добави нова книга</h3>

        <form class="add-form" action="/add" method="POST">
            <input
                type="text"
                name="title"
                placeholder="Въведи заглавие на книгата..."
                required
                maxlength="150"
            >
            <button class="add-btn" type="submit">
                + Добави книга
            </button>
        </form>
    </section>

    <section>

        <div class="section-header">
            <div>
                <h2>Моята библиотека</h2>
                <p>Разгледай своята колекция от книги.</p>
            </div>

            <a href="/?sort=1"
               class="sort-btn"
               style="color:#b2a5ff; text-decoration:none; font-size:13px;">
                ↕ Сортирай
            </a>
        </div>

        <form class="search-box" action="/" method="GET">
            <input
                type="text"
                name="search"
                placeholder="🔍  Търси книга по заглавие..."
                value="{{ search }}"
            >
            <button class="search-btn" type="submit">
                Търси
            </button>
        </form>

        <div class="books-grid">

            {% for book in displayed_books %}

            <div class="book-card">

                <div class="book-cover">📖</div>

                <div class="book-label">MY COLLECTION</div>

                <div class="book-title">{{ book }}</div>

                <div class="book-footer">

                    <span class="book-number">
                        BOOK #{{ loop.index }}
                    </span>

                    <form action="/delete" method="POST"
                          onsubmit="return confirm('Сигурни ли сте, че искате да изтриете книгата?')">

                        <input type="hidden" name="title" value="{{ book }}">

                        <button class="delete-btn" type="submit">
                            🗑 Изтрий
                        </button>

                    </form>

                </div>
            </div>

            {% else %}

            <div class="empty">
                <div class="empty-icon">📚</div>
                <h3>Тук все още няма книги</h3>
                <p>Добави първата си книга и започни своята колекция!</p>
            </div>

            {% endfor %}

        </div>

    </section>

</div>

<footer>
    © 2026 BookSpace · Made with ♥ for book lovers
</footer>

</body>
</html>
"""


@app.route("/")
def home():
    search = request.args.get("search", "").strip()

    displayed_books = [
        book for book in books
        if search.casefold() in book.casefold()
    ]

    if request.args.get("sort") == "1":
        displayed_books.sort(key=str.casefold)

    return render_template_string(
        HTML,
        displayed_books=displayed_books,
        total=len(books),
        results=len(displayed_books),
        search=search
    )


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()

    if title:
        books.append(title)
        save_books()

    return redirect(url_for("home"))


@app.route("/delete", methods=["POST"])
def delete_book():
    title = request.form.get("title", "")

    if title in books:
        books.remove(title)
        save_books()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
