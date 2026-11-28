# Data Science · Tech Orda / BrainCode

[Сайт курса](https://kuromi1kow.github.io/braincode-data-science/) · [Программа занятий](https://kuromi1kow.github.io/braincode-data-science/lessons/index.html) · [Книжная полка](https://kuromi1kow.github.io/braincode-data-science/books.html) · [Папка преподавателя на Google Диске](https://drive.google.com/drive/folders/1K83MMSPBBTlHrZSS0A0OPjuO8QI8KvS7)

Материалы для студентов Assylkhan Geniyat. Десять занятий охватывают введение в Data Science, Python с нуля, условия, циклы, функции, структуры данных, классы, файлы, массивы NumPy и анализ таблиц с pandas. В каждом уроке есть разбор, исполняемые примеры, практика, домашнее задание и чтение.

## Для преподавателя

Ссылку на любое занятие или раздел страницы можно отправить группе. В каждом занятии основной блокнот открывается прямо в Google Colab. Для локального запуска нужен Jupyter с ядром Python 3. Для занятий 9 и 10 понадобятся NumPy и pandas соответственно. Файл данных для упражнения с выручкой находится в `data/sales.csv`.

[Домашняя работа по NumPy](https://kuromi1kow.github.io/braincode-data-science/lessons/09-numpy.html#numpy-homework) содержит 100 упражнений из [русской редакции Александра Соколова](https://github.com/alex-sokolov2011/100_Numpy_exercises_Rus_ver) по [сборнику Nicolas P. Rougier](https://github.com/rougier/numpy-100). Тетрадь `notebooks/09-numpy-100.ipynb` включает условия, пустые ячейки для ответов и обе лицензии MIT.

[Занятие 10 · pandas](https://kuromi1kow.github.io/braincode-data-science/lessons/10-pandas.html) включает файл `data/orders.csv`, основной блокнот, лабораторию по объединению таблиц и отдельную тетрадь для [домашней работы](https://kuromi1kow.github.io/braincode-data-science/lessons/10-pandas.html#homework). Студенты сдают заполненный блокнот и `city_report.csv`.

## Обновление сайта

Тексты и книжные ссылки находятся в `src/`, ученические блокноты — в `notebooks/`. Общая навигация, адрес Google Диска и каталог описаны в `course_ui.py`. Ссылки на Colab формирует `build.py`. Изменив материалы, пересоберите страницы из корня репозитория и проверьте их локально.

```sh
python3 build.py
python3 -m http.server 8000
```

Откройте http://localhost:8000/. GitHub Pages публикует готовые HTML и CSS из корня ветки `main`. Каталог собирается из `src/course.json`: поле `module` задаёт раздел, `summary` — описание, `keywords` — дополнительные слова для поиска. Для нового занятия добавьте его материалы и сохраните пересобранные HTML вместе с исходниками.

## Иллюстрации и шрифты

Две иллюстрации созданы специально для курса с помощью ImageGen. Предпросмотры обложек на странице книг загружаются с авторских сайтов. Для чтения используется Inter, для заголовков — Rubik. Файлы WOFF2 с кириллицей и латиницей и лицензии SIL Open Font License лежат в `assets/fonts/`.

## Чтение внутри уроков

[Материалы группы](https://kuromi1kow.github.io/braincode-data-science/materials.html) связывают папки занятий, настройку среды, видео, упражнения и дополнительное чтение. Для каждого урока сайт хранит главы в `src/chapters.json`, практикум в `src/labs.json` и фрагмент открытого издания в `src/excerpts.json`. Сборка обновляет блокноты лабораторий вместе с HTML.

Встроенные переводы отрывков подготовлены для курса. Фрагменты и их переводы из книги [Swaroop Chitlur, A Byte of Python](https://python.swaroopch.com/) распространяются на условиях [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Английский текст взят из [редакции 84f4dd8 в репозитории автора](https://github.com/swaroopch/byte-of-python/tree/84f4dd8d6f09836fa58226eaafe922b8a7baabc6), оформление адаптировано для HTML. Фрагмент и перевод из [Scientific Python Lectures, The NumPy array object](https://lectures.scientific-python.org/intro/numpy/array_object.html#copies-and-views) распространяются по [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Авторство принадлежит Scientific Python developers. На страницах отдельно обозначены перевод, оригинал и комментарий курса.

Для занятия о pandas переведено одно предложение из [Software Carpentry, Plotting and Programming in Python](https://swcarpentry.github.io/python-novice-gapminder/07-reading-tabular.html). Оригинал и перевод доступны по [CC BY 4.0](https://swcarpentry.github.io/python-novice-gapminder/LICENSE.html).
