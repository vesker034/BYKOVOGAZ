# БыковоГаз

## Дизайн

Макет проекта: [Figma](https://www.figma.com/design/39GlcB4t2zxi7RuWtE8bLd/%D0%91%D0%AB%D0%9A%D0%9E%D0%92%D0%9E%D0%93%D0%90%D0%97?node-id=0-1&p=f&t=6SlQsbunR9P3YhwC-0)

## Стек

- Django
- HTML
- CSS
- Bootstrap 5

## Структура
.
|-- components/              # документация и декомпозиция UI-компонентов
|-- config/                  # настройки Django-проекта
|-- main/                    # основное приложение сайта
|-- static/
|   |-- css/
|   |-- img/
|   `-- js/
|-- templates/
|   |-- components/          # переиспользуемые template-partials
|   `-- pages/               # страницы сайта
|-- .env.example
|-- .gitignore
|-- manage.py
`-- requirements.txt

## Быстрый старт

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Командная работа

Базовая схема веток:

- `main` - стабильная ветка
- `develop` - общая ветка интеграции
- `feature/<задача>` - личные ветки участников команды

Рекомендуемый процесс:

1. Каждый разработчик создает ветку от `develop`.
2. Ветку называет по шаблону `feature/<задача>`.
3. После завершения задачи открывает Pull Request в `develop`.
4. После проверки изменения попадают в `main`.

Примеры имен веток:

- `feature/header`
- `feature/hero-section`
- `feature/footer`


