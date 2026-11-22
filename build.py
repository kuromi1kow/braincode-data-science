"""Generate the buildless GitHub Pages edition from student-facing course sources."""
from html import escape
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
DRIVE = "https://drive.google.com/drive/folders/1K83MMSPBBTlHrZSS0A0OPjuO8QI8KvS7"
REPO = "https://github.com/kuromi1kow/braincode-data-science"
COLAB = "https://colab.research.google.com/github/kuromi1kow/braincode-data-science/blob/main/notebooks/"
def read(name):
    return json.loads((BASE / "src" / (name + ".json")).read_text(encoding="utf-8"))
course, cases, walks, books, primers = map(read, ("course","cases","walkthroughs","books","primers"))
tags = ["данные анализ доля конверсия эксперимент", "print строки ввод числа переменные типы", "if elif else логика условие bool", "for while range цикл накопитель", "def return функция аргументы", "list dict set tuple словарь список кортеж множества", "class self объект класс ООП", "csv json файлы ошибки исключения", "numpy ndarray оси массив маска axis shape broadcast"]
descriptions = ["Как превратить вопрос в измерение и проверить свой вывод.", "Первая ячейка, переменные и арифметика на примере чека.", "Ветвление, логические выражения и проверка на границе.", "Обход списка, накопитель суммы и условие остановки.", "Параметры, область видимости и возвращаемое значение.", "Списки, словари, множества и кортежи на примере клиентов.", "Состояние объекта, методы и независимые экземпляры.", "Как прочитать CSV, сохранить JSON и учесть ошибки.", "Форма массива, индексы, маски и вычисления по осям."]
def e(value):
    return escape(str(value), quote=True)
def prose(text):
    return re.sub(r'`([^`]+)`',r'<code>\1</code>', e(text))
def p(text):
    return '<p>'+prose(text)+'</p>'
def listing(items,kind="ul"):
    return f'<{kind} class="exercise">'+''.join('<li>'+prose(x)+'</li>' for x in items)+f'</{kind}>'
def link(url,label,cls=""):
    return f'<a href="{e(url)}" class="{e(cls)}">{e(label)}</a>'
def code(source):
    return '<div class="codebox"><div class="codebar"><span>Python</span><button type="button" aria-label="Скопировать пример кода">Скопировать</button></div><pre><code>'+e(source.rstrip())+'</code></pre></div>'
def reveal(label,body):
    return '<details><summary>'+e(label)+'</summary>'+body+'</details>'
def page(title,body,depth="",description="Русскоязычные уроки Data Science для студентов Tech Orda / BrainCode."):
    home=depth+'index.html'
    nav=link(home+'#lessons','Занятия')+link(depth+'books.html','Книги')+link(DRIVE,'Google Диск','drive')
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#303fa0"><meta name="description" content="{e(description)}"><title>{e(title)} · Tech Orda / BrainCode</title><link rel="icon" href="{depth}assets/icon.png"><link rel="stylesheet" href="{depth}assets/style.css"><script src="{depth}assets/site.js" defer></script></head>
<body><a class="skip" href="#content">К содержанию</a><header class="mast"><div class="wrap"><a class="brand" href="{home}"><span class="mark" aria-hidden="true"><b></b><b></b><b></b></span>BrainCode</a><nav aria-label="Навигация курса">{nav}</nav></div></header><main id="content" class="wrap">{body}</main>
<footer class="foot"><div class="wrap"><p>Data Science · Tech Orda / BrainCode<br>Материалы преподавателя · Assylkhan Geniyat</p><nav aria-label="Ссылки на материалы">{link(home,'Курс')}{link(DRIVE,'Google Диск')}{link(REPO,'GitHub')}</nav></div></footer></body></html>'''
def lesson_url(i):
    return f"lessons/{course[i]['slug']}.html"
def chapter_links(items, with_book=False):
    return '<ul class="reading-list">'+''.join('<li>'+link(ch['url'],(b['title']+' · ' if with_book else '')+ch['label'])+'<span>'+prose(ch['task'])+'</span></li>' for b,ch in items)+'</ul>'
def section(anchor,title,body):
    return f'<section id="{anchor}"><h2>{e(title)}</h2>{body}</section>'

def simulator(i):
    if i==2:
        return '''<div class="demo"><div class="smallcap">Проверка тарифа</div><p>Введите целую сумму заказа и посмотрите, какая ветка сработает.</p><div class="controls"><label for="order-price">Сумма, ₸</label> <input id="order-price" type="number" step="1" value="4999"><button type="button" data-price="5000">5 000 ₸</button><button type="button" data-price="10000">10 000 ₸</button></div><output id="fee" for="order-price" aria-live="polite">Сумма от 0 до 4 999 ₸. Доставка стоит 1 000 ₸.</output></div>'''
    if i==3:
        return '''<div class="demo"><div class="smallcap">Пошаговый обход</div><p>Продажи в тенге: <code>[1000, 0, 2500, 500]</code>. Предскажите сумму перед следующим шагом.</p><div class="controls"><button id="loop-next" type="button">Следующий шаг</button><button id="loop-reset" type="button">Сначала</button></div><output id="loop-state" aria-live="polite">До первой итерации сумма равна 0 ₸.</output></div>'''
    if i==8:
        return '''<div id="axis-demo" class="demo"><div class="smallcap">Практикум по осям</div><h3>Как посчитать фишки по рядам и столбцам?</h3><figure><img src="../assets/array.jpg" width="1020" height="680" alt="Лоток из двух рядов по три ячейки. В верхних ячейках 1, 3, 2 фишки, в нижних 4, 2, 3."><figcaption class="photo-note">Учебная иллюстрация. Одна ячейка лотка соответствует одному элементу массива.</figcaption></figure><p>Запишите <code>A = np.array([[1, 3, 2], [4, 2, 3]])</code>. Пока ось не выбрана, попробуйте сами получить два итога по рядам и три по столбцам.</p><div class="controls"><button type="button" data-axis="1" aria-pressed="false">По рядам · axis=1</button><button type="button" data-axis="0" aria-pressed="false">По столбцам · axis=0</button></div><output aria-live="polite">Форма массива (2, 3). Выберите направление сложения.</output><noscript>По рядам получатся [6, 9]. По столбцам — [5, 5, 5].</noscript></div>'''
    return ''
def setup(i):
    if i==0:
        return '<div class="notes"><strong>Первый запуск в Colab</strong>'+p('Нажмите «Открыть в Colab», затем кнопку подключения к среде. Запускайте ячейки по очереди через Shift + Enter. Для редактирования и сохранения выберите в меню «Файл» пункт сохранения копии на Диске. Если работаете в Jupyter, скачайте .ipynb по соседней ссылке.')+'</div>'
    if i==7:
        return '<div class="notes">'+link('../data/sales.csv','Скачать учебный sales.csv')+p('В основном блокноте первая ячейка готовит такой же файл в папке braincode_practice. Его путь доступен как DATA / "sales.csv". В нём две корректные продажи и строка с ценой bad.')+'</div>'
    if i==8:
        return '<div class="notes">'+p('В Colab подключите обычную среду Python и выполните import numpy as np. Если запускаете Jupyter локально и NumPy отсутствует, выполните %pip install numpy в отдельной ячейке этого блокнота.')+'</div>'
    return ''
def lesson(i,t):
    case=cases[f'{i:02}']; primer=primers[i]; num=i+1
    body='<header class="lesson-head"><div class="eyebrow">'+link('../index.html#lessons','Все занятия')+f' &nbsp;/&nbsp; Занятие {num:02}</div><h1>'+e(t['title'])+'</h1><p class="intro">'+e(descriptions[i])+'</p><div class="actions">'+link(COLAB+t['notebook'],'Открыть в Colab','btn primary')+link('#practice','К практике','btn')+'</div></header>'
    titles=[('start','С чего начать'),('case','Разбор задачи'),('code','Код по шагам'),('practice','Практика и ДЗ'),('quiz','Самопроверка'),('reading','Что почитать')]
    nav='<aside class="rail"><div class="smallcap">В этом занятии</div>'+''.join(link('#'+a,b) for a,b in titles)+'</aside>'
    start=p(t['why'])+'<h3>'+e(primer[0])+'</h3>'+p(primer[1])+p(primer[2])+'<dl>'+''.join('<dt class="term">'+e(primer[j])+'</dt><dd>'+prose(primer[j+1])+'</dd>' for j in (3,5,7))+'</dl>'+setup(i)
    body+='<div class="layout">'+nav+'<article class="reading">'+section('start','С чего начать',start)
    body+=section('case',case['title'],''.join(p(x) for x in case['paragraphs'])+'<div class="notes"><strong>Проверьте рассуждение</strong>'+p(case['challenge'])+reveal('Сверить ответ',p(case['answer']))+'</div>')
    samples=''
    for w in walks[i]:
        samples+='<h3>'+e(w['title'])+'</h3>'+p(w['intro'])+code(w['code'])+reveal('Показать вывод и объяснение','<pre class="out">'+e(w['output'])+'</pre>'+p(w['explain']))
    body+=section('code','Код по шагам',p('Перед запуском прочитайте пример и запишите, что появится на экране. Затем откройте вывод под кодом и сравните со своим ответом.')+samples+simulator(i))
    demo=''.join(p(x) for x in t['example'])+code(t['code'])+p(t['explain'])
    practice='<h3>Пример из блокнота</h3>'+demo+'<h3>Работа на занятии</h3>'+listing(t['practice'],'ol')+'<h3>Домашнее задание</h3>'+listing(t['homework'],'ol')+p('Сохраните блокнот с выполненными ячейками, проверочными примерами и коротким выводом своими словами.')+'<div class="actions">'+link(COLAB+t['notebook'],'Открыть практику в Colab','btn primary')+link('../notebooks/'+t['notebook'],'Скачать .ipynb','btn')+link(DRIVE,'Материалы на Google Диске','btn')+'</div>'
    if (BASE/'notebooks'/(t['slug']+'-lab.ipynb')).exists():
        practice+='<h3>Для дополнительной тренировки</h3>'+p('Если основной пример уже получился, откройте ещё один набор задач по той же теме.')+link(COLAB+t['slug']+'-lab.ipynb','Практикум')+' · '+link(COLAB+t['slug']+'-homework.ipynb','Самостоятельная работа')
    body+=section('practice','Практика и домашнее задание',practice)
    body+=section('quiz','Самопроверка',''.join(reveal(q,p(a)) for q,a in zip(t['quiz'],t['answers']))+'<h3>Где легко ошибиться</h3>'+listing(t['errors']))
    pick=[(b,c) for b in books for c in b['chapters'] if num in c['lessons']]
    body+=section('reading','Что почитать',chapter_links(pick,True)+'<h3>Документация</h3>'+'<ul>'+''.join('<li>'+link(url,label)+'</li>' for label,url in t['sources'])+'</ul>'+link('../books.html','Вся книжная полка'))
    prev=link(course[i-1]['slug']+'.html','Предыдущее занятие') if i else link('../index.html','К программе')
    nxt=link(course[i+1]['slug']+'.html','Далее · '+course[i+1]['title']) if i+1<len(course) else link('../index.html#lessons','Вернуться к программе')
    return page(t['title'],body+'<nav class="pager" aria-label="Между занятиями">'+prev+nxt+'</nav></article></div>','../',descriptions[i])

def home():
    first=lesson_url(0)
    body='<section class="hero"><div><p class="eyebrow">Tech Orda / BrainCode</p><h1>Data <span>Science</span></h1><p class="intro">Учебник для студентов. От первого вопроса к данным до вычислений на Python и NumPy.</p><div class="actions">'+link(first,'Начать с введения','btn primary')+link('books.html','Книжная полка','btn')+'</div></div><figure class="herofigure"><img src="assets/study.jpg" width="1200" height="800" alt="Руки студента с карандашом над столбчатой диаграммой в тетради в клетку."><figcaption>Рабочая тетрадь по анализу данных · Иллюстрация курса</figcaption></figure></section>'
    body+='''<section id="lessons" class="catalog"><div class="sectop"><div><p class="eyebrow">Программа курса</p><h2>Занятия</h2></div><label class="search"><span class="sr">Найти занятие по теме</span><input id="lesson-search" type="search" placeholder="Найти тему или занятие"></label></div><p id="found" class="sr" role="status"></p>'''
    for group,sub,indices in [('Введение','Сначала — вопрос к данным',[0]),('Python','От переменной до файла',range(1,8)),('NumPy','Числа в массивах',[8])]:
        body+='<div class="group"><div><h3>'+group+'</h3><span class="muted">'+sub+'</span></div><div class="lessons">'
        for i in indices:
            body+=f'<a data-lesson="{e(tags[i])}" href="{lesson_url(i)}"><span class="num">{i+1:02}</span><span><strong>{e(course[i]["title"])}</strong><span class="blurb">{e(descriptions[i])}</span></span></a>'
        body+='</div></div>'
    body+='</section><section class="panel"><div><div class="eyebrow">Практикум · NumPy</div><h2>Как массив складывается по осям?</h2>'+p('Посчитайте фишки сначала по рядам, затем по столбцам. Сравните два результата и проверьте, что именно делает axis=0.')+link(lesson_url(8)+'#axis-demo','Открыть практикум','btn primary')+'</div><img src="assets/array.jpg" width="1020" height="680" loading="lazy" alt="Шесть ячеек с фишками, расположенными в два ряда по три."></section>'
    body+='<section class="home-book"><h2>Материалы группы</h2>'+p('Откройте папку преподавателя с материалами занятий. Блокноты для работы в Colab и главы книг также доступны на странице каждой темы.')+link(DRIVE,'Материалы на Google Диске','small-link')+'</section>'
    return page('Data Science для студентов',body)
def library():
    body='<header class="library-head"><div class="eyebrow">'+link('index.html','Data Science')+' &nbsp;/&nbsp; Материалы курса</div><h1>Книжная полка</h1><p class="intro">Шесть книг для первых девяти занятий. Откройте нужную главу и попробуйте ответить на вопрос к ней в своём блокноте.</p></header>'
    body+='<nav aria-label="Книги" class="chapter-nav">'+''.join(link('#'+b['id'],b['title']) for b in books)+'</nav><div class="bookgrid">'
    for b in books:
        cover=('<a href="'+e(b['url'])+'"><img src="'+e(b['cover'])+'" loading="lazy" referrerpolicy="no-referrer" alt="Обложка книги '+e(b['title'])+'"></a>') if b['cover'] else ''
        body+='<article class="book" id="'+e(b['id'])+'">'+cover+'<div class="smallcap">'+e(b['language'])+'</div><h2>'+link(b['url'],b['title'])+'</h2><div class="author">'+e(b['author'])+'</div>'+p(b['guide'])
        body+=reveal('Главы и вопросы для чтения',chapter_links([(b,ch) for ch in b['chapters']]))+link(b['url'],'Открыть книгу','book-link')+'</article>'
    return page('Книжная полка',body+'</div>')
def main():
    assert len(course)==len(walks)==len(primers)==len(cases)
    (BASE/'lessons').mkdir(exist_ok=True)
    for i,t in enumerate(course):
        (BASE/lesson_url(i)).write_text(lesson(i,t),encoding='utf-8')
    (BASE/'index.html').write_text(home(),encoding='utf-8')
    (BASE/'books.html').write_text(library(),encoding='utf-8')

if __name__ == '__main__':
    main()
