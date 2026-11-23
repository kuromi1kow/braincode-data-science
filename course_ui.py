"""Shared layout, landing page and lesson catalogue for GitHub Pages."""

from functools import lru_cache
from hashlib import sha256
from html import escape
from pathlib import Path

DRIVE = "https://drive.google.com/drive/folders/1K83MMSPBBTlHrZSS0A0OPjuO8QI8KvS7"
REPO = "https://github.com/kuromi1kow/braincode-data-science"
CATALOG = "lessons/index.html"
NAVIGATION = (
    ("home", "index.html", "Главная"),
    ("catalog", CATALOG, "Программа"),
    ("books", "books.html", "Книги"),
    ("materials", "materials.html", "Материалы"),
)


def e(value):
    return escape(str(value), quote=True)


def link(url, label, cls="", *, download=False):
    classes = f' class="{e(cls)}"' if cls else ""
    download_attr = " download" if download else ""
    return f'<a href="{e(url)}"{classes}{download_attr}>{e(label)}</a>'


@lru_cache(maxsize=None)
def asset_url(path):
    content = (Path(__file__).resolve().parent / path).read_bytes()
    return f"{path}?v={sha256(content).hexdigest()[:12]}"


def page(title, body, *, active, depth="", description="Учебник Data Science для студентов Tech Orda / BrainCode."):
    home_url = depth + "index.html"
    nav = []
    for key, path, label in NAVIGATION:
        current = ""
        if key == active:
            current = ' aria-current="page"'
        elif active == "lesson" and key == "catalog":
            current = ' aria-current="location"'
        nav.append(f'<a href="{depth}{path}"{current}>{label}</a>')

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta id="dark-chrome" name="theme-color" content="#1b272b" media="screen and (prefers-color-scheme: dark)">
  <meta name="theme-color" content="#ffffff">
  <meta name="description" content="{e(description)}">
  <title>{e(title)} · Tech Orda / BrainCode</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="{depth}assets/fonts/fonts.css">
  <link rel="stylesheet" href="{depth}{asset_url('assets/style.css')}">
  <link id="dark-palette" rel="stylesheet" href="{depth}{asset_url('assets/dark.css')}" media="screen and (prefers-color-scheme: dark)">
  <script src="{depth}{asset_url('assets/theme.js')}"></script>
  <script src="{depth}{asset_url('assets/site.js')}" defer></script>
</head>
<body data-page="{active}">
  <a class="skip" href="#content">К содержанию</a>
  <header class="mast"><div class="wrap mast-inner">
    <a class="brand" href="{home_url}"><strong>BrainCode</strong><span class="partners">Astana Hub · Tech Orda</span></a>
    <nav aria-label="Навигация курса">{''.join(nav)}</nav>
    <label class="theme-picker" title="Тема оформления" hidden>
      <select id="theme-choice" aria-label="Тема оформления">
        <option value="system">Как на устройстве</option>
        <option value="light">Светлая</option>
        <option value="dark">Тёмная</option>
      </select>
    </label>
  </div></header>
  <main id="content" class="wrap" tabindex="-1">{body}</main>
  <footer class="foot"><div class="wrap foot-inner">
    <p><strong>Data Science</strong> · Assylkhan Geniyat</p>
    <nav aria-label="Ресурсы курса">{link(depth + CATALOG, 'Программа')}{link(DRIVE, 'Google Диск')}{link(REPO, 'GitHub')}</nav>
  </div></footer>
</body></html>"""


def home():
    # Existing bookmarks may point to any of these fragments on the old landing page.
    anchors = ''.join(f'<span id="{key}" data-moved-to="{CATALOG}#{key}"></span>'
                      for key in ("lessons", "track-1", "track-2", "track-9"))
    body = f"""
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Учебник для студентов</p>
        <h1>Data <span>Science</span></h1>
        <p class="intro">От первого вопроса к данным до расчётов на Python и NumPy. Разбирайте примеры и проверяйте свои решения в Google Colab.</p>
        <div class="actions">{anchors}{link(CATALOG, 'Открыть программу', 'btn primary')}</div>
      </div>
      <img class="hero-photo" src="assets/study.jpg" width="1200" height="800"
           alt="Студент строит карандашом столбчатую диаграмму в тетради.">
    </section>
    <nav class="home-resources" aria-label="Ресурсы для учёбы">
      <a href="books.html"><strong>Книжная полка</strong><span>Главы учебников и вопросы для вдумчивого чтения.</span></a>
      <a href="materials.html"><strong>Материалы группы</strong><span>Папки занятий, установка Python и дополнительные упражнения.</span></a>
    </nav>
    <p class="attribution">В уроках используются отрывки из
      {link('https://python.swaroopch.com/', 'A Byte of Python')} (Swaroop Chitlur)
      ({link('https://creativecommons.org/licenses/by-sa/4.0/', 'CC BY-SA 4.0')}) и
      {link('https://lectures.scientific-python.org/', 'Scientific Python Lectures')}
      ({link('https://creativecommons.org/licenses/by/4.0/', 'CC BY 4.0')}).</p>"""
    return page("Data Science для студентов", body, active="home")


def catalog(course):
    groups = {}
    for number, topic in enumerate(course, start=1):
        groups.setdefault(topic["module"], []).append((number, topic))

    filters = ['<button type="button" data-module="" aria-pressed="true">Все</button>']
    sections = []
    for module, entries in groups.items():
        anchor = f"track-{entries[0][0]}"
        filters.append(f'<button type="button" data-module="{anchor}" aria-pressed="false">{e(module)}</button>')
        rows = []
        for number, topic in entries:
            rows.append(f"""
              <li data-lesson="{e(topic['keywords'])}"><a href="{e(topic['slug'])}.html">
                <span class="number">{number:02}</span>
                <span><strong>{e(topic['title'])}</strong><span class="blurb">{e(topic['summary'])}</span></span>
              </a></li>""")
        sections.append(f"""
          <section class="module" id="{anchor}" aria-labelledby="{anchor}-heading">
            <h2 id="{anchor}-heading">{e(module)}</h2>
            <ol start="{entries[0][0]}" class="lesson-list">{''.join(rows)}</ol>
          </section>""")
    body = f"""
      <header class="page-head">
        <p class="eyebrow">Курс Data Science</p>
        <h1>Программа занятий</h1>
        <p class="intro">Начните с введения или найдите тему для повторения. В каждом занятии есть разборы, практика и домашнее задание.</p>
      </header>
      <div id="lessons">
        <div id="catalog-tools" class="catalog-tools" hidden>
          <label class="search"><span>Поиск по занятиям</span>
            <input id="lesson-search" type="search" placeholder="Например, циклы или NumPy"></label>
          <div class="filters" role="group" aria-label="Раздел программы">{''.join(filters)}</div>
        </div>
        <div class="results-line"><p id="found" role="status">Занятий: {len(course)}</p>
          <button type="button" id="reset-search" hidden>Сбросить фильтры</button></div>
{''.join(sections)}
      </div>"""
    return page("Программа занятий", body, active="catalog", depth="../")


def section_menu(entries, *, reader=False):
    items = ''.join(link('#' + key, name) for key, name in entries)
    size_controls = """<div class="reader-tools" hidden>
        <span class="smallcap">Размер текста</span>
        <div class="type-buttons">
          <button id="normal-type" aria-pressed="true" type="button">Обычный</button>
          <button id="large-type" aria-pressed="false" type="button">Крупный</button>
        </div>
      </div>""" if reader else ""
    return f"""<aside class="rail"><details class="section-menu" open>
      <summary>Содержание</summary><nav aria-label="Содержание страницы">{items}</nav>
{size_controls}</details></aside>"""
