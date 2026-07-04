# vibecoding-test

Статическое зеркало лендинга [usmanovafit.gymteam.ru/mainpage](https://usmanovafit.gymteam.ru/mainpage).

## GitHub Pages

После включения Pages в настройках репозитория сайт доступен по адресу:

https://themanis.github.io/vibecoding-test/

**Settings → Pages → Source: GitHub Actions**

Деплой запускается автоматически при push в `main` (workflow `.github/workflows/pages.yml`).

## Локальный запуск

```bash
cd site
python3 -m http.server 8877
```

Открыть: http://localhost:8877

## Структура

```
site/          # статические файлы сайта
├── index.html # главная страница
├── nassets/   # CSS, JS, шрифты
└── public/    # дополнительные ресурсы
```

## Примечания

- Картинки с CDN GetCourse (`fs.getcourse.ru`) подгружаются из интернета.
- Cookie-баннер закрывается локально без запроса к серверу GetCourse.
- Кнопки «Подробнее» ведут на локальную страницу `maysale2026_7`.
