"""Generate the buildless GitHub Pages edition from student-facing course sources."""
from course_ui import CATALOG, DRIVE, catalog, section_menu, e, home, link, page
from hashlib import sha256
import csv
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
COLAB = "https://colab.research.google.com/github/kuromi1kow/braincode-data-science/blob/main/notebooks/"
def read(name):
    return json.loads((BASE / "src" / (name + ".json")).read_text(encoding="utf-8"))
course, cases, walks, books, primers = map(read, ("course","cases","walkthroughs","books","primers"))
folders, resources, deep = map(read, ("folders", "resources", "chapters"))
labs, excerpts = map(read, ("labs", "excerpts"))
def prose(text):
    return re.sub(r'`([^`]+)`',r'<code>\1</code>', e(text))
def p(text):
    return '<p>'+prose(text)+'</p>'
def listing(items,kind="ul"):
    return f'<{kind} class="exercise">'+''.join('<li>'+prose(x)+'</li>' for x in items)+f'</{kind}>'
def code(source):
    return '<div class="codebox"><div class="codebar"><span>Python</span><button type="button" aria-label="Скопировать пример кода">Скопировать</button></div><pre><code>'+e(source.rstrip())+'</code></pre></div>'
def reveal(label,body):
    return '<details><summary>'+e(label)+'</summary>'+body+'</details>'
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
def dataset_details(filename):
    with (BASE / 'data' / filename).open(encoding='utf-8', newline='') as data:
        header, *rows = csv.reader(data)
    columns = ''.join('<th scope="col">' + e(col) + '</th>' for col in header)
    body = ''.join('<tr>' + ''.join('<td>' + (e(value) if value else '—') + '</td>' for value in row) + '</tr>' for row in rows)
    table = ('<div class="scroll-table"><table><caption>' + e(filename) + ' · строк: ' + str(len(rows))
             + '</caption><thead><tr>' + columns + '</tr></thead><tbody>' + body + '</tbody></table></div>')
    return ('<div class="notes">' + link('../data/' + filename, 'Скачать ' + filename, 'btn', download=True)
            + p('В Colab данные уже встроены в первую ячейку чтения. Для работы локально положите CSV рядом с блокнотом. '
                'Вам понадобятся Jupyter и pandas. При необходимости установите библиотеку в ячейке командой `%pip install pandas`.')
            + reveal('Посмотреть исходные строки', table + p('Тире в таблице обозначает пустое поле CSV.')) + '</div>')


def lesson(i,t):
    case=cases[f'{i:02}']; primer=primers[i]; num=i+1
    assignment = t.get('exercise_collection')
    homework_link = link('#numpy-homework', 'ДЗ · 100 упражнений', 'btn') if assignment else ''
    homework_nb = t.get('homework_notebook')
    if homework_nb:
        homework_link = link('#homework', 'К домашней работе', 'btn')
    body='<header class="lesson-head"><div class="eyebrow">'+link('index.html','Программа')+f' &nbsp;/&nbsp; Занятие {num:02}</div><h1>'+e(t['title'])+'</h1><p class="intro">'+e(t['summary'])+'</p><div class="actions">'+link(COLAB+t['notebook'],'Открыть в Colab','btn primary')+link('#practice','К практике','btn')+homework_link+'</div></header>'
    titles=[('start','С чего начать'),('book-text','Из книги'),('case','Разбор задачи'),('deeper','Подробный разбор'),('code','Код по шагам'),('workshop','Лаборатория'),('practice','Практика и ДЗ'),('quiz','Самопроверка'),('reading','Что почитать')]
    if assignment:
        titles.insert(-2, ('numpy-homework', 'ДЗ · 100 упражнений'))
    nav = section_menu(titles, reader=True)
    start=p(t['why'])+'<h3>'+e(primer[0])+'</h3>'+p(primer[1])+p(primer[2])+'<dl>'+''.join('<dt class="term">'+e(primer[j])+'</dt><dd>'+prose(primer[j+1])+'</dd>' for j in (3,5,7))+'</dl>'+setup(i)
    if t.get('dataset'):
        start += dataset_details(t['dataset'])
    body+='<div class="layout">'+nav+'<article class="reading">'+section('start','С чего начать',start)
    body+=section('book-text','Читаем фрагмент книги',book_text(excerpts[str(num)]))
    body+=section('case',case['title'],''.join(p(x) for x in case['paragraphs'])+'<div class="notes"><strong>Проверьте рассуждение</strong>'+p(case['challenge'])+reveal('Сверить ответ',p(case['answer']))+'</div>')
    parts=deep[str(num)]
    contents='<ol class="inside-toc">'+''.join('<li>'+link('#chapter-'+str(k),unit['title'])+'</li>' for k,unit in enumerate(parts,1))+'</ol>'
    for k,unit in enumerate(parts,1):
        contents+='<div class="unit" id="chapter-'+str(k)+'"><h3>'+e(unit['title'])+'</h3>'+''.join(p(z) for z in unit['paragraphs'])
        table=unit.get('table')
        if table:
            contents+='<div class="scroll-table"><table><caption>'+e(unit['title'])+'</caption><thead><tr>'+''.join('<th scope="col">'+e(x)+'</th>' for x in table['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+prose(x)+'</td>' for x in row)+'</tr>' for row in table['rows'])+'</tbody></table></div>'
        contents+='<div class="checkpoint"><strong>Остановитесь и проверьте себя</strong>'+p(unit['question'])+reveal('Разобрать ответ',p(unit['answer']))+'</div></div>'
    body+=section('deeper','Подробный разбор',contents)
    samples=''
    for w in walks[i]:
        samples+='<h3>'+e(w['title'])+'</h3>'+p(w['intro'])+code(w['code'])+reveal('Показать вывод и объяснение','<pre class="out">'+e(w['output'])+'</pre>'+p(w['explain']))
    body+=section('code','Код по шагам',p('Перед запуском прочитайте пример и запишите, что появится на экране. Затем откройте вывод под кодом и сравните со своим ответом.')+samples+simulator(i))
    body+=section('workshop','Лаборатория · '+labs[str(num)]['title'],workshop(num,t))
    demo=''.join(p(x) for x in t['example'])+code(t['code'])+p(t['explain'])
    homework_title = '<h3 id="homework">Домашнее задание</h3>' if homework_nb else '<h3>Домашнее задание</h3>'
    practice = '<h3>Пример из блокнота</h3>' + demo + '<h3>Работа на занятии</h3>' + listing(t['practice'], 'ol')
    practice += homework_title + listing(t['homework'], 'ol') + p('Сохраните блокнот с выполненными ячейками, проверочными примерами и коротким выводом своими словами.')
    if homework_nb:
        practice += '<div class="actions">' + link(COLAB + homework_nb, 'Решать домашнюю работу в Colab', 'btn primary') + link('../notebooks/' + homework_nb, 'Скачать тетрадь для сдачи', 'btn', download=True) + '</div>'
    practice += '<div class="actions">' + link(COLAB+t['notebook'],'Открыть практику в Colab','btn primary') + link('../notebooks/'+t['notebook'],'Скачать .ipynb','btn') + link(DRIVE,'Материалы на Google Диске','btn') + '</div>'
    if str(num) in folders:
        practice+='<div class="actions">'+link(folders[str(num)],f'Папка занятия {num} на Диске','btn')+'</div>'
    if num==2:
        practice+='<p class="more-link">'+link(GROUP_NOTEBOOK,'Блокнот «Практика Python с нуля» из группы')+'</p>'
    if (BASE/'notebooks'/(t['slug']+'-lab.ipynb')).exists():
        practice+='<h3>Для дополнительной тренировки</h3>'+p('Если основной пример уже получился, откройте ещё один набор задач по той же теме.')+link(COLAB+t['slug']+'-lab.ipynb','Практикум')+' · '+link(COLAB+t['slug']+'-homework.ipynb','Самостоятельная работа')
    body+=section('practice','Практика и домашнее задание',practice)
    if assignment:
        notebook = assignment['notebook']
        instructions = listing(assignment['steps'], 'ol')
        actions = link(COLAB + notebook, 'Решать в Google Colab', 'btn primary')
        actions += link('../notebooks/' + notebook, 'Скачать блокнот .ipynb', 'btn', download=True)
        source = link(assignment['source'], 'Оригинальный практикум на GitHub')
        body += section('numpy-homework', assignment['title'],
                        p(assignment['intro']) + instructions + '<div class="actions">' +
                        actions + '</div><p>' + source + ' · Русская редакция Александра Соколова.</p>')
    body+=section('quiz','Самопроверка',''.join(reveal(q,p(a)) for q,a in zip(t['quiz'],t['answers']))+'<h3>Где легко ошибиться</h3>'+listing(t['errors']))
    pick=[(b,c) for b in books for c in b['chapters'] if num in c['lessons']]
    recommended=[r for group in resources for r in group['items'] if num in r['lessons']]
    extras=('<h3>Ссылки от преподавателя</h3>'+resource_links(recommended)) if recommended else ''
    body+=section('reading','Что почитать',chapter_links(pick,True)+'<h3>Документация</h3>'+'<ul>'+''.join('<li>'+link(url,label)+'</li>' for label,url in t['sources'])+'</ul>'+link('../books.html','Вся книжная полка')+extras)
    prev=link(course[i-1]['slug']+'.html','Назад · '+course[i-1]['title']) if i else link('index.html','К программе')
    nxt=link(course[i+1]['slug']+'.html','Далее · '+course[i+1]['title']) if i+1<len(course) else link('index.html','Вернуться к программе')
    return page(t['title'],body+'<nav class="pager" aria-label="Между занятиями">'+prev+nxt+'</nav></article></div>',active='lesson',depth='../',description=t['summary'])

def library():
    body='<header class="library-head"><div class="eyebrow">'+link('index.html','Data Science')+' &nbsp;/&nbsp; Материалы курса</div><h1>Книжная полка</h1><p class="intro">Книги по Python, NumPy и pandas. Откройте нужную главу и попробуйте ответить на вопрос к ней в своём блокноте.</p></header>'
    body+='<nav aria-label="Книги" class="chapter-nav">'+''.join(link('#'+b['id'],b['title']) for b in books)+'</nav><div class="bookgrid">'
    for b in books:
        cover=('<a href="'+e(b['url'])+'"><img src="'+e(b['cover'])+'" loading="lazy" referrerpolicy="no-referrer" alt="Обложка книги '+e(b['title'])+'"></a>') if b['cover'] else ''
        body+='<article class="book" id="'+e(b['id'])+'">'+cover+'<div class="smallcap">'+e(b['language'])+'</div><h2>'+link(b['url'],b['title'])+'</h2><div class="author">'+e(b['author'])+'</div>'+p(b['guide'])
        body+=reveal('Главы и вопросы для чтения',chapter_links([(b,ch) for ch in b['chapters']]))+link(b['url'],'Открыть книгу','book-link')+'</article>'
    return page('Книжная полка',body+'</div><section class="home-book"><h2>Математическая полка</h2>'+p('Для самостоятельного чтения преподаватель собрал книги по матрицам, векторам и математическому анализу на русском и английском.')+link('materials.html#math','Открыть книги по математике','small-link')+'</section>', active='books')
GROUP_NOTEBOOK = 'https://drive.google.com/file/d/1xGwjMlmdmzJSehuUw6RHOLraQpyXxytF/view?usp=sharing'

def resource_links(items):
    return '<ul class="reading-list resource-list">'+''.join('<li>'+link(r['url'],r['title'])+'<span>'+prose(r['note'])+'</span></li>' for r in items)+'</ul>'

def materials():
    body='<header class="library-head"><div class="eyebrow">От преподавателя</div><h1>Материалы группы</h1><p class="intro">Здесь собраны учебные ссылки из чата. Откройте папку своего занятия, выберите тренажёр или найдите книгу для самостоятельного чтения.</p></header>'
    side = section_menu([('group-drive','Папки занятий'), *((g['id'],g['title']) for g in resources)])
    folder_links=''.join('<li>'+link(url,f'Занятие {key} · '+course[int(key)-1]['title'])+'</li>' for key,url in folders.items())
    drive_section=section('group-drive','Папки занятий',p('В общей папке преподаватель собирает лекции и материалы группы. Ниже — прямые ссылки на папки конкретных встреч из объявлений курса.')+link(DRIVE,'Открыть общий Google Диск','btn primary')+'<ul class="folders">'+folder_links+'</ul>'+link(GROUP_NOTEBOOK,'Открыть блокнот вводной практики по Python'))
    blocks=''.join(section(g['id'],g['title'],p(g['intro'])+resource_links(g['items'])) for g in resources)
    return page('Материалы группы',body+'<div class="layout">'+side+'<article class="reading">'+drive_section+blocks+'</article></div>', active='materials')

def book_text(item):
    attribution=link(item['source'],item['author']+' · '+item['book'])+' · '+link(item['license_url'],item['license'])
    return ('<div class="book-excerpt"><div class="smallcap">Перевод для курса</div><h3>'+e(item['title'])+'</h3><blockquote>'+p(item['translation'])+'</blockquote><p class="credit">Оригинал и перевод этого отрывка · '+attribution+'</p>'+reveal('Прочитать английский оригинал','<div lang="en">'+''.join(p(t) for t in item['original'])+'</div>')+'</div><h3>Как это проверить</h3>'+p(item['note']))

def workshop(num,topic):
    lab=labs[str(num)]
    body=p(lab['brief'])+'<div class="notes"><strong>Исходные данные</strong>'+p(lab['inputs'])+'</div>'+link(COLAB+topic['slug']+'-workshop.ipynb','Запустить лабораторию в Colab','btn primary')
    for k,step in enumerate(lab['steps'],1):
        body+='<h3>Шаг '+str(k)+'. '+e(step['question'])+'</h3>'+code(step['code'])+reveal('Проверить результат','<pre class="out">'+e(step['output'])+'</pre>'+p(step['why']))
    bug=lab['mistake']
    return body+'<h3>Программа выполняется. Где ошибка в выводе?</h3>'+code(bug['code'])+reveal('Разобрать ошибку','<pre class="out">'+e(bug['output'])+'</pre>'+p(bug['why']))+'<div class="checkpoint"><strong>Измените задачу</strong>'+p(lab['transfer'])+reveal('Сверить свой результат',p(lab['check']))+'</div>'

def lab_notebook(i,topic):
    lab=labs[str(i+1)]
    cells=[]
    def add(kind,source):
        c=dict(cell_type=kind,id='workshop-'+str(len(cells)),metadata={},source=source.splitlines(keepends=True))
        if kind=='code':c.update(outputs=[],execution_count=None)
        cells.append(c)
    add('markdown','# '+lab['title']+'\n\n'+lab['brief']+'\n\n'+lab['inputs']+'\n\nВыполняйте ячейки по порядку. Перед запуском попробуйте предсказать вывод.')
    for k,step in enumerate(lab['steps'],1):
        add('markdown',f"## Шаг {k}. "+step['question'])
        add('code',step['code'])
        add('markdown','**Обсуждение.** '+step['why'])
    add('markdown','## Поиск логической ошибки\nПочему результат может ввести в заблуждение?')
    add('code',lab['mistake']['code'])
    add('markdown',lab['mistake']['why']+'\n\n## Измените задачу\n'+lab['transfer'])
    add('code','# Ваше решение')
    add('markdown','Для проверки: '+lab['check'])
    doc=dict(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},nbformat=4,nbformat_minor=5)
    (BASE/'notebooks'/(topic['slug']+'-workshop.ipynb')).write_text(json.dumps(doc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')

def main():
    assert len(course)==len(walks)==len(primers)==len(cases)
    (BASE/'lessons').mkdir(exist_ok=True)
    pages = {
        'index.html': home(),
        CATALOG: catalog(course),
        'materials.html': materials(),
        'books.html': library(),
    }
    for i, topic in enumerate(course):
        lab_notebook(i, topic)
        pages[lesson_url(i)] = lesson(i, topic)

    # A shared version keeps navigation from mixing different cached editions of the header.
    version = sha256('\0'.join(pages.values()).encode('utf-8')).hexdigest()[:12]
    page_link = re.compile(r'( (?:href|data-moved-to)="(?:[\w.-]+/)*[\w.-]+\.html)(?=["#])')
    for path, html in pages.items():
        html = page_link.sub(rf'\g<1>?v={version}', html)
        (BASE / path).write_text(html, encoding='utf-8')

if __name__ == '__main__':
    main()
