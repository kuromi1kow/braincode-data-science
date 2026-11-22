# Data Science · Tech Orda / BrainCode

[Сайт курса](https://kuromi1kow.github.io/braincode-data-science/) · [Книжная полка](https://kuromi1kow.github.io/braincode-data-science/books.html) · [Папка преподавателя на Google Диске](https://drive.google.com/drive/folders/1K83MMSPBBTlHrZSS0A0OPjuO8QI8KvS7)

Материалы для студентов Assylkhan Geniyat. Девять занятий охватывают введение в Data Science, Python с нуля, условия, циклы, функции, структуры данных, классы, файлы и основы NumPy. В каждом уроке есть разбор, исполняемые примеры, практика, домашнее задание и чтение.

## Для преподавателя

Ссылку на любое занятие или раздел страницы можно отправить группе. В каждом занятии основной блокнот открывается прямо в Google Colab. Для локального запуска нужен Jupyter с ядром Python 3. Для последнего занятия нужен NumPy. Файл данных для упражнения с выручкой находится в `data/sales.csv`.

## Обновление сайта

Тексты и книжные ссылки находятся в `src/`, ученические блокноты — в `notebooks/`. Ссылки на Google Диск и Colab задаются в `build.py`. Изменив материалы, пересоберите страницы из корня репозитория и проверьте их локально.

```sh
python3 build.py
python3 -m http.server 8000
```

Откройте http://localhost:8000/. GitHub Pages публикует готовые HTML и CSS из корня ветки `main`. Для добавления занятия расширьте программу, наборы примеров и навигацию каталога в генераторе, затем сохраните обновлённые HTML вместе с исходниками.

## Иллюстрации и шрифты

Две иллюстрации созданы специально для курса с помощью ImageGen. Предпросмотры обложек на странице книг загружаются с авторских сайтов. Лицензии локальных шрифтов Source Sans 3 и STIX Two Text включены в каталог `assets/`.

## Чтение внутри уроков

[Материалы группы](https://kuromi1kow.github.io/braincode-data-science/materials.html) связывают папки занятий, настройку среды, видео, упражнения и дополнительное чтение. Для каждого урока сайт хранит главы в `src/chapters.json`, практикум в `src/labs.json` и фрагмент открытого издания в `src/excerpts.json`. Сборка обновляет девять блокнотов лаборатории вместе с HTML.

Встроенные переводы отрывков подготовлены для курса. Фрагменты и их переводы из книги [Swaroop Chitlur, A Byte of Python](https://python.swaroopch.com/) распространяются на условиях [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Английский текст взят из [редакции 84f4dd8 в репозитории автора](https://github.com/swaroopch/byte-of-python/tree/84f4dd8d6f09836fa58226eaafe922b8a7baabc6), оформление адаптировано для HTML. Фрагмент и перевод из [Scientific Python Lectures, The NumPy array object](https://lectures.scientific-python.org/intro/numpy/array_object.html#copies-and-views) распространяются по [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Авторство принадлежит Scientific Python developers. На страницах отдельно обозначены перевод, оригинал и комментарий курса.
