# БыковоГаз

Стартовый репозиторий для командной разработки сайта на `Django + HTML/CSS + Bootstrap 5`.

В репозитории намеренно нет готовой верстки: здесь подготовлена только архитектура проекта,
общие шаблоны, статические файлы и базовые правила работы команды.

## Дизайн

Макет проекта: [Figma](https://www.figma.com/design/39GlcB4t2zxi7RuWtE8bLd/%D0%91%D0%AB%D0%9A%D0%9E%D0%92%D0%9E%D0%93%D0%90%D0%97?node-id=0-1&p=f&t=6SlQsbunR9P3YhwC-0)

## Стек

- Django
- HTML
- CSS
- Bootstrap 5

## Структура

```text
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
```

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
- `feature/<суть-задачи>` — ветка под задачу (без имён людей в названии)

Рекомендуемый процесс:

1. Каждый разработчик создает ветку от `develop`.
2. Ветку называет по сути работы, например `feature/header-layout` или `fix/footer-spacing`.
3. После завершения задачи открывает Pull Request в `develop`.
4. После проверки изменения попадают в `main`.

Примеры имён веток:

- `feature/header-layout`
- `feature/hero-section`
- `feature/footer-contacts`

### Правила Git (нейтральные формулировки)

В названиях веток, сообщениях коммитов и в описаниях Pull Request **не указывать имена и никнеймы** участников — только суть работы.

- **Ветки:** что делается (`feature/header-layout`, `fix/mobile-menu`), а не «кто делает».
- **Коммиты:** формат Conventional Commits — тип, область, кратко что изменилось (`feat(templates): add site footer`).
- **PR:** что сделано и что проверить, без персональных меток в заголовке.

Папка **`.cursor/`** относится к локальной IDE и **не коммитится** (она в `.gitignore`).

### Сообщения коммитов без лишних строк

Если в конец коммита IDE автоматически добавляет строку вроде `Made-with: Cursor`, отключите это в Cursor: **Settings → Agents → Attribution** (выключить). После этого коммиты из интерфейса Cursor не будут дополняться такими трейлерами. Альтернатива — делать коммиты командой `git commit -m "..."` в терминале при отключённой подписи.

## Что уже подготовлено

- приложение `main` подключено к проекту;
- настроены общие папки `templates`, `components`, `static`;
- добавлены базовый шаблон, шаблоны компонентов и стартовая страница;
- подключен Bootstrap 5 через CDN;
- создана простая проверка страницы и GitHub Actions для `check` и `test`.
