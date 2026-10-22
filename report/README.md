---
type: Курс по DevOPS Home Work
module: LLM в разработке
lesson_no: 1
lesson_theme: Практика API
---
> [!bookmark]
>
> **Домашнее задание: <%+ tp.file.title %>**

В этом задании вы сделаете первый реальный шаг в работе с большими языковыми моделями через API. Вы не просто изучите теорию — вы напишете код, который заставляет модель возвращать не просто текст, а строгие структурированные данные в формате JSON, которые можно сразу использовать в программе.

Почему это важно? Умение работать с LLM через API — базовый навык современного разработчика и специалиста по AI. Интеграция языковых моделей в реальные приложения открывает возможности для автоматизации, создания умных сервисов и повышения продуктивности.

Выполнив это задание, вы:
● настроите окружение для работы с несколькими языковыми моделями;
● научитесь формировать корректные запросы к LLM через HTTP API и обрабатывать полученные ответы в Python-коде;
● реализуете прикладной сценарий: построите мини-пайплайн для автоматического разбора резюме и вакансий, а также сравните несколько LLM по скорости и качеству извлечения структурированных данных.

##  Инструменты, которые пригодятся для выполнения задания:
● Зарегистрируйтесь на платформе [_______________](https://developers.sber.ru/docs/ru/gigachat/tariffs/individual-tariffs#terms-update) и получите API-ключ
● Python 3.10+ с установленными библиотеками: groq, python-dotenv;
● Jupyter Notebook или Google Colab.
● [Учебный ноутбук](https://u.netology.ru/backend/uploads/lms/content_assets/file/15336/praktika_groq_structured.zip) Структурированный вывод с  API

## Описание задания
Реализуйте пайплайн структурированного извлечения данных с использованием giga  API. В итоге ваша программа должна:

- извлекать структурированный JSON-профиль из текста резюме с помощью JSON-режима;
- обрабатывать батч из 7 резюме и фильтровать кандидатов по заданным критериям;
- сравнивать скорость и качество нескольких LLM-моделей на одной задаче;
- реализовать парсер вакансий по той же схеме. Решение оформите в Jupyter Notebook, следуя инструкции ниже.
- Инструкция к выполнению

### Шаг 1. 
Получите API-ключ GIGA, зарегистрируйтесь и создайте ключ в разделе API Keys.
### Шаг 2. 
Используйте учебный ноутбук. Установите зависимости: выполните pip install groq python-dotenv в терминале.
### Шаг 3. 
Создайте файл .env в папке с ноутбуком и добавьте туда строку GIGA_API_KEY=ваш_ключ.
### Шаг 4. 
Откройте предоставленный шаблон notebook praktika_groq_structured.ipynb.
### Шаг 5. 
Последовательно выполните ячейки разделов 1–4 и убедитесь, что все работают без ошибок.
### Шаг 6. 
Выполните задания раздела 5: реализуйте 5 фильтров кандидатов.
### Шаг 7. 
Запустите раздел 6 (сравнение моделей) и письменно ответьте на аналитические вопросы.
### Шаг 8. 
Реализуйте функцию parse_vacancy() для всех 3 тестовых вакансий в финальном задании.

## Разбор решения задания
### Прежде всего:
- получил ключи авторизации на ресурсе Giga от Сбера (https://developers.sber.ru/docs/ru/gigachat/tariffs/individual-tariffs#terms-update) вместо недоступного в РФ Groq с соответствующим внесением изменений  в сценарий выполнения работы.
- Скачал и сложил в репозиторий с заданием сертификаты Минцифры России, необходимые для работы Giga
- Настроил рабочее окружение:
```bash
cd ~/devops/llm_dev
sudo apt update && sudo apt install -y python3-venv python3-pip
mkdir -p certs
cp /home/vboxuser/Downloads/praktika_groq_structured.ipynb praktika_gigachat_structured.ipynb


python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install gigachat python-dotenv jupyterlab
pip freeze > requirements.txt
python3 --version && pip show gigachat | sed -n '1,2p'


cat > .gitignore <<'EOF'
.env
.venv/
certs/
.ipynb_checkpoints/
__pycache__/
EOF

cat > .env.example <<'EOF'
# Ключ авторизации GigaChat API (Client ID:Client Secret в Base64)
GIGACHAT_CREDENTIALS=
# Путь к сертификату НУЦ Минцифры
GIGACHAT_CA_BUNDLE_FILE=certs/russian_trusted_root_ca.crt
EOF

cp .env.example .env

```

![](<Pasted image 20261022141149.png>)

#### небольшой тест доступности модели и корректности подключения 
- скрипт для теста`test_connections.py`:
```python
import os

from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

credentials = os.getenv("GIGACHAT_CREDENTIALS")
ca_bundle = os.getenv("GIGACHAT_CA_BUNDLE_FILE")

print(f"Ключ авторизации: {credentials[:10]}..." if credentials else "КЛЮЧ НЕ НАЙДЕН")
print(f"CA-бандл: {ca_bundle}")

with GigaChat(
    credentials=credentials,
    scope="GIGACHAT_API_PERS",
    ca_bundle_file=ca_bundle,
    timeout=60.0,
) as client:
    token = client.get_token()
    print(f"Токен доступа получён, действует до: {token.expires_at}")

    models = client.get_models()
    print("Доступные модели:")
    for m in models.data:
        print(f"  {m.id_} (owned_by={m.owned_by})")
```

![](<Pasted image 20261022142350.png>)

#### Откорректировал ячейки в Jupirter notebook следующим образом:
##### Ячейка 0:
```text
## 0. Получение ключа авторизации GigaChat

**Пошаговая инструкция:**

1. Зарегистрируйтесь на [developers.sber.ru](https://developers.sber.ru)
2. Создайте проект **GigaChat API** (для физлиц, тариф Free)
3. В настройках проекта получите **Client ID** и **Client Secret**,
   из которых собирается ключ авторизации (Base64-строка)
4. Скопируйте ключ авторизации

> **Важно:** Python-клиенты не используют системное хранилище сертификатов,
> поэтому сертификат НУЦ Минцифры подключается в SDK напрямую через
> `ca_bundle_file`. Бесплатный тариф имеет лимиты по частоте запросов.

Создайте файл `.env` в той же папке, что и этот ноутбук:
GIGACHAT_CREDENTIALS=ВАШКЛЮЧАВТОРИЗАЦИИ
GIGACHAT_CA_BUNDLE_FILE=certs/Russian_Trusted_Root_CA.cer
```

##### Ячейка 1:
```python
!pip install gigachat python-dotenv

import os
import json
import time

from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv()

api_key = os.getenv('GIGACHAT_CREDENTIALS')
ca_bundle = os.getenv('GIGACHAT_CA_BUNDLE_FILE')

client = GigaChat(
    credentials=api_key,
    scope='GIGACHAT_API_PERS',
    ca_bundle_file=ca_bundle,
    timeout=60.0,
)

print(f'Ключ GigaChat загружен: {api_key[:10] if api_key else "Не найден"}...')
print(f'CA-бандл: {ca_bundle}')
```

![](<Pasted image 20261022161537.png>)
##### Ячейка 2
```python
resume_text = """
Привет! Меня зовут Анна Соколова, мне 28 лет. Последние 4 года работаю
бэкенд-разработчиком в финтех-компании. Основной стек: Python, FastAPI,
PostgreSQL, Redis. Есть опыт с Docker и Kubernetes. Закончила МГТУ им. Баумана
по специальности «Прикладная математика». Ищу позицию Senior Python Developer
с зарплатой от 300 000 рублей. Готова к удалённой работе или гибриду.
"""

# Обычный запрос без требования структуры — контракт v1
chat = Chat(
    model='GigaChat-2',
    messages=[
        Messages(
            role=MessagesRole.USER,
            content=f'Извлеки основную информацию из резюме:\n{resume_text}',
        )
    ],
)

response = client.chat(chat)

raw_output = response.choices[0].message.content
print('Вывод модели:')
print(raw_output)
print()

# Попытка использовать вывод в коде — неудача
print('Попытка получить зарплату из ответа:')
try:
    data = json.loads(raw_output)
    print(data['salary'])
except Exception as e:
    print(f'Ошибка: {e}')
    print('Неструктурированный текст нельзя напрямую использовать в коде!')
```

![](<Pasted image 20261022161601.png>)
##### Ячейка 3:
```text
## 3. Решение: структурированный вывод (json_schema)

У GigaChat нет режима `json_object` как у Groq — вместо «попроси JSON» здесь
передаётся **полная JSON-схема** в `response_format.schema` и параметр
`strict: True`. Схема гарантирует наличие всех полей в ответе,
а отсутствующие в тексте данные модель вернёт как `null`
(для этого в схеме у полей тип `["number", "null"]`).
```

```python
system_prompt = """
Ты — HR-ассистент. Извлекай данные из резюме и возвращай строго в формате JSON.
Схема ответа:
{
  "name": string,
  "age": number или null,
  "experience_years": number,
  "current_position": string,
  "skills": [string],
  "education": string или null,
  "target_position": string,
  "salary_from": number или null,
  "work_format": string
}
"""

# JSON-схема профиля кандидата — контрактуем ответ модели
resume_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'age': {'type': ['number', 'null']},
        'experience_years': {'type': 'number'},
        'current_position': {'type': 'string'},
        'skills': {'type': 'array', 'items': {'type': 'string'}},
        'education': {'type': ['string', 'null']},
        'target_position': {'type': 'string'},
        'salary_from': {'type': ['number', 'null']},
        'work_format': {'type': 'string'},
    },
    'required': [
        'name', 'age', 'experience_years', 'current_position', 'skills',
        'education', 'target_position', 'salary_from', 'work_format',
    ],
    'additionalProperties': False,
}

chat = Chat(
    model='GigaChat-2',
    messages=[
        Messages(role=MessagesRole.SYSTEM, content=system_prompt),
        Messages(role=MessagesRole.USER, content=f'Обработай резюме:\n{resume_text}'),
    ],
    response_format={
        'type': 'json_schema',
        'schema': resume_schema,
        'strict': True,
    },
)

response = client.chat(chat)

candidate = json.loads(response.choices[0].message.content)

print('Структурированный профиль кандидата:')
print(json.dumps(candidate, ensure_ascii=False, indent=2))
print()

# Теперь данные можно использовать в коде
print(f"Имя: {candidate['name']}")
print(f"Опыт: {candidate['experience_years']} лет")
print(f"Навыки: {', '.join(candidate['skills'])}")
print(f"Ожидаемая зарплата: {candidate['salary_from']:,} руб.".replace(',', ' '))
```

- Схема - это отдельный объект resume_schema. У Groq модель угадывала структуру из текста промпта, у GigaChat структура задана формально: типы, массивы, обязательность. Промпт при этом остаётся. Он помогает модели правильно понять текст, но форму ответа теперь диктует схема.

- strict: True + полный required: при таком сочетании ответ содержит все поля схемы, включая необязательные, а не описанные в схеме поля модель добавлять не будет («все поля присутствуют или null»).

- ['number', 'null'] в типах - так в JSON Schema выражается «может отсутствовать». Без этого строгая валидация отвергла бы ответ, где Мария не указала зарплату.

![](<Pasted image 20261022161628.png>)

##### Ячейка 4
```python
from gigachat.exceptions import RateLimitError

def parse_resume(text: str, attempts: int = 3) -> dict | None:
    """Извлекает структурированные данные из текста резюме."""
    system_prompt = """
Ты — HR-ассистент. Извлекай данные из резюме и возвращай строго в формате JSON.
"""

    chat = Chat(
        model='GigaChat-2',
        messages=[
            Messages(role=MessagesRole.SYSTEM, content=system_prompt),
            Messages(role=MessagesRole.USER, content=f'Обработай резюме:\n{text}'),
        ],
        response_format={
            'type': 'json_schema',
            'schema': resume_schema,  # единая схема из раздела 3
            'strict': True,
        },
    )

    for attempt in range(1, attempts + 1):
        try:
            response = client.chat(chat)
            return json.loads(response.choices[0].message.content)
        except RateLimitError as e:
            wait = getattr(e, 'retry_after', None) or 5
            print(f'Лимит запросов (попытка {attempt}/{attempts}). Ждём {wait} сек...')
            time.sleep(wait)
        except Exception as e:
            print(f'Ошибка: {e}')
            return None
    return None


resumes = [
    """
    Иван Петров, 32 года. 7 лет в разработке игр на Unity и C#.
    Делал мобильные игры для iOS/Android, есть опыт с Blender.
    Ищу Lead Game Developer, готов к офису в Москве. Зарплата от 250 000.
    """,
    """
    Мария Иванова. Data Scientist с опытом 3 года.
    Стек: Python, pandas, scikit-learn, PyTorch, SQL.
    Работала в e-commerce над рекомендательными системами.
    Хочу ML Engineer, только удалёнка, зарплата не принципиальна.
    """,
    """
    Дмитрий Козлов, 25 лет, junior frontend. Знаю React, TypeScript, CSS.
    Полгода коммерческого опыта в веб-студии. Ищу работу в продуктовой компании.
    Рассматриваю от 120 000, гибрид или удалёнка.
    """,
    """
    Екатерина Смирнова, 29 лет. DevOps-инженер, 5 лет опыта.
    Умею: Kubernetes, Docker, Terraform, AWS, CI/CD (GitLab, GitHub Actions).
    Работала в банковском секторе, есть опыт с highload-системами.
    Ищу Senior DevOps, удалёнка обязательно. Зарплата от 300 000.
    """,
    """
    Алексей Новиков, 35 лет. Fullstack-разработчик, 10 лет опыта.
    Стек: Python (Django, FastAPI), Vue.js, PostgreSQL, Redis, Docker.
    Последние 3 года — тимлид команды из 6 человек в SaaS-компании.
    Рассматриваю роль Engineering Manager или Staff Engineer. От 400 000, гибрид.
    """,
    """
    Юлия Белова. QA Engineer, 4 года в тестировании.
    Автотесты на Python (pytest, Selenium, Playwright), API-тестирование (Postman, requests).
    Опыт в agile-командах, знакома с нагрузочным тестированием (Locust).
    Ищу Middle/Senior QA, гибрид, зарплата от 180 000.
    """,
    """
    Сергей Орлов, 27 лет. Android-разработчик, 3 года опыта.
    Kotlin, Jetpack Compose, Room, Retrofit, Coroutines. Публиковал 2 приложения в Google Play.
    Немного знаю iOS (Swift). Ищу Middle Android Developer в продуктовую компанию.
    Только удалёнка. Зарплата от 210 000.
    """,
]

results = []
for i, resume in enumerate(resumes, 1):
    print(f'Обрабатываю резюме {i}/{len(resumes)}...')
    parsed = parse_resume(resume)
    if parsed:
        results.append(parsed)
    time.sleep(1)  

print(f'\nОбработано: {len(results)} из {len(resumes)} резюме')
print()
for r in results:
    salary = f"{r['salary_from']:,}".replace(',', ' ') + ' руб.' if r.get('salary_from') else 'не указана'
    print(f"• {r['name']} | {r['target_position']} | опыт {r['experience_years']} л. | зарплата: {salary}")
```

- Двухслойная защита от лимитов. Первый слой - `max_retries=3` в клиенте (SDK сам ретраит 429 и сетевые сбои). Второй - цикл в `parse_resume`: если `RateLimitError`  пробился, ждём столько, сколько просит сервер (e.retry_after), но не дольше трёх попыток? без бесконечного цикла. 

- Целая схема вместо урезанной. В шаблоне Groq в `parse_resume` схема урезана до шести полей - а раздел 5 потом фильтрует по `work_format` и считает по `salary_from`. В обновленной форме все девять полей на месте, фильтрам раздела 5 хватит данных.

- `time.sleep(1)` между резюме: у бесплатного тарифа жёсткие лимиты RPM, и семь запросов подряд без паузы может вызвать бан.

- Общий `except` с `return None` по заданию: одно некорректное резюме не роняет весь батч.

![](<Pasted image 20261022161719.png>)

```text
• Дмитрий Козлов | в продуктовой компания | опыт 0.5 л. | ...
```

В этой строке, в поле `target_position`: `"в продуктовой компании"`. В резюме целевая позиция не названа: «Ищу работу в продуктовой компании» - это про компанию, а не про должность. Модель не нашла данных, но поле в схеме обязательное ('string', не null) и strict: True, поэтому она была вынуждена что-то туда вставить. И вставила правдоподобный мусор. В данном случае в работе с LLM-экстракцией жёсткая схема гарантирует форму ответа, но не правдивость содержимого. Когда поле обязательно, а информации нет, модель галлюцинирует значение, а не возвращает `null`.
Для `target_position` не предусмотрено значение `null`  при заполнении схемы (шаблон Groq тоже имел строго строковое значение).

###### Исправляю в `resume_schema` (ячейка раздела 3): разрешаю `null` для целевой позиции:

```python
'target_position': {'type': ['string', 'null']},
```

И одна строка в `system_prompt` внутри `parse_resume()` (ячейка раздела 4), чтобы модель не фантазировала:

```text
Если целевая позиция в резюме не указана - верни null.
```

![](<Pasted image 20261022164112.png>)
- качество отдельных полей зависит от неоднозначности текста, в продакшене такие поля требуют пост-валидацию или ручную проверку.

##### Ячейка 5
```python
# 0. Типы полей, по которым будет идти фильтрация
for r in results:
    problems = []
    if not isinstance(r.get('experience_years'), (int, float)):
        problems.append('experience_years')
    if not isinstance(r.get('skills'), list):
        problems.append('skills')
    if r.get('salary_from') is not None and not isinstance(r['salary_from'], (int, float)):
        problems.append('salary_from')
    if not isinstance(r.get('work_format'), str):
        problems.append('work_format')
    print(f"{r['name']:20} {'OK' if not problems else 'ПРОБЛЕМЫ: ' + ', '.join(problems)}")

# Задание 1: удалёнщики с опытом 4+ лет
remote_seniors = [
    r for r in results
    if 'удалёнка' in r['work_format'].lower() and r['experience_years'] >= 4
]
print(f'\n1. Удалёнщики с опытом 4+ лет: {len(remote_seniors)}')
for r in remote_seniors:
    print(f"   → {r['name']} ({r['experience_years']} лет, {r['work_format']})")

# Задание 2: зарплатные ожидания ≤ 230 000 руб. (или не указаны)
budget_hires = [
    r for r in results
    if r['salary_from'] is None or r['salary_from'] <= 230_000
]
print(f'\n2. Бюджетный найм (≤ 230 000 руб. или не указана): {len(budget_hires)}')
for r in budget_hires:
    s = f"{r['salary_from']:,} руб.".replace(',', ' ') if r['salary_from'] else 'не указана'
    print(f"   → {r['name']} ({s})")

# Задание 3: кандидаты с Python в навыках
python_devs = [r for r in results if 'Python' in r['skills']]
print(f'\n3. Кандидаты с Python: {len(python_devs)}')
for r in python_devs:
    print(f"   → {r['name']}: {', '.join(r['skills'])}")

# Задание 4: топ-3 по опыту
top3 = sorted(results, key=lambda r: r['experience_years'], reverse=True)[:3]
print('\n4. Топ-3 по опыту:')
for i, r in enumerate(top3, 1):
    print(f"   {i}. {r['name']} — {r['experience_years']} лет")

# Задание 5: статистика зарплат среди указавших
salaries = [r['salary_from'] for r in results if r['salary_from'] is not None]
print(f'\n5. Статистика зарплат (указали {len(salaries)} из {len(results)}):')
print(f"   средняя:      {sum(salaries) / len(salaries):,.0f} руб.".replace(',', ' '))
print(f"   минимальная:  {min(salaries):,} руб.".replace(',', ' '))
print(f"   максимальная: {max(salaries):,} руб.".replace(',', ' '))
```

- Задание 1: `work_format` - свободный текст модели («удалёнка обязательно», «гибрид или удалёнка»), поэтому `in`, а не ` == `, и `.lower()` на случай «Удалёнка» с заглавной. При этом: Дмитрий с «гибрид или удалёнка» в фильтр не попадёт - опыт 0.5 меньше четырёх. Фильтры  комбинируются через `and`.

- Задание 2: `is None` проверяется первым: если бы `salary_from` был `None` и дошло до сравнения `<= 230_000`, получили бы `TypeError`. В шаблоне примера это сделано через скобки `(r['salary_from'] is None or ...)`  та же логика.

- Задание 3: `'Python' in r['skills']`  это точное совпадение элемента списка, а не подстрока: `in` для списка ищет целый элемент. Если бы модель вернула `python` с маленькой буквы, кандидат бы выпал; в продакшене  делают нормализацию регистра. 

- Задание 5: сначала отделяю «не указавших» (`is not None`), и по ним считаю, иначе `min/max` упадут на `None` или `sum` даст мусор.

![](<Pasted image 20261022164930.png>)

В полученном результате у Юлии  модель «развернула» скобки: в исходном тексте было «Python (Django, FastAPI)» и «Автотесты на Python (pytest, ...)», и GigaChat посчитала конкретные фреймворки самодостаточными навыками, а родительский Python выкинула. Это несогласованность извлечения данных. Фильтр по ` == ` совпадению элементов очень хрупок, если источник LLM. Нормализация:

```python
# Задание 3: ищем Python как подстроку в любом навыке, без учёта регистра
python_devs = [
    r for r in results
    if any('python' in s.lower() for s in r['skills'])
]
print(f'\n3. Кандидаты с Python: {len(python_devs)}')
for r in python_devs:
    print(f"   → {r['name']}: {', '.join(r['skills'])}")
```

![](<Pasted image 20261022170315.png>)

В полученном выводе: 
- Алексей: Python (Django, FastAPI) - один навык одной строкой, а не три отдельных. 
- Юлия: "Автотесты на Python (pytest, Selenium, Playwright)" - то же самое, но "Опыт в agile-командах, Знакома с нагрузочным тестированием (Locust)" - это уже вообще не навыки, а описания опыта. Модель перенесла в массив `skills` куски текста резюме.

Проблемы извлечения: LLM-экстракция без post-processing даёт данные с шумом. Навыки сворачиваются в составные строки и смешиваются с описаниями опыта. Нужна нормализация подстрокой, разбиение составных навыков регэкспом, а в продакшене - `enum` допустимых значений прямо в JSON-схеме `("skills": {"type": "array", "items": {"enum": [...]}})`, тогда модель физически не сможет вернуть ничего вне словаря.

##### Ячейка 6
```text
## 6. Сравнение моделей

GigaChat API предоставляет доступ к нескольким моделям с разными характеристиками. Сравним их по **скорости** и **качеству** извлечения структурированных данных.

В отличие от Groq, где модели различаются в первую очередь числом параметров (8B vs 70B), линейка GigaChat различается **поколением** и **классом** модели. Список получен методом `get_models()` для текущего ключа:
```

| Модель | Поколение / класс | Ожидаемая роль |
|---|---|---|
| `GigaChat-2` | 2, базовая | Быстрая модель для повседневных задач |
| `GigaChat-3-Lightning` | 3, скоростная | Минимальная задержка ответа |
| `GigaChat-2-Pro` | 2, Pro | Ресурсоёмкие задачи |
| `GigaChat-3-Ultra` | 3, топовая | Флагман для самых сложных задач |
Актуальный список моделей доступен методом `get_models()` или в документации: [developers.sber.ru/docs/ru/gigachat/models](https://developers.sber.ru/docs/ru/gigachat/models)

```

```python
import time

# Резюме для теста
test_resume = """
Андрей Захаров, 31 год. Backend-разработчик, 6 лет опыта.
Основной стек: Go, Python, gRPC, Kafka, PostgreSQL, Kubernetes.
Строил высоконагруженные сервисы в финтех и логистике.
Ищу Senior/Lead Backend Engineer. Удалёнка, зарплата от 380 000.
"""

system_prompt = """
Ты — HR-ассистент. Извлекай данные из резюме и возвращай строго в формате JSON.
"""

# Линейка GigaChat: две оси сравнения — поколение (2 vs 3) и класс (базовая vs Pro/Ultra)
models_to_compare = [
    'GigaChat-2',
    'GigaChat-3-Lightning',
    'GigaChat-2-Pro',
    'GigaChat-3-Ultra',
]

comparison_results = []

for model_name in models_to_compare:
    try:
        start = time.time()
        chat = Chat(
            model=model_name,
            messages=[
                Messages(role=MessagesRole.SYSTEM, content=system_prompt),
                Messages(role=MessagesRole.USER, content=f'Обработай резюме:\n{test_resume}'),
            ],
            response_format={
                'type': 'json_schema',
                'schema': resume_schema,
                'strict': True,
            },
        )
        response = client.chat(chat)
        elapsed = time.time() - start

        parsed = json.loads(response.choices[0].message.content)
        usage = response.usage

        comparison_results.append({
            'model': model_name,
            'time_sec': round(elapsed, 2),
            'total_tokens': usage.total_tokens,
            'tokens_per_sec': round(usage.completion_tokens / elapsed),
            'skills_found': len(parsed.get('skills', [])),
            'parsed': parsed,
        })
        print(f'OK {model_name}: {elapsed:.2f} с, {usage.total_tokens} токенов')
        time.sleep(1)  # пауза между запросами — бережём лимиты тарифа
    except Exception as e:
        print(f'ОШИБКА {model_name}: {e}')

print()
header = f"{'Модель':<20} {'Время':>8} {'Ток/с':>8} {'Навыков':>9}"
print(header)
print('-' * 50)
for r in comparison_results:
    row = f"{r['model']:<20} {r['time_sec']:>7.2f}с {r['tokens_per_sec']:>8} {r['skills_found']:>9}"
    print(row)
```

- Что меряем: `time_sec` - полное время ответа (`latency`, как его видит клиент), `tokens_per_sec` - скорость генерации (`usage.completion_tokens`, который  отдал v1-контракт). 

- Что не меряем - качество. `skills_found` - слабый прокси. У Андрея в резюме 6 технологий (Go, Python, gRPC, Kafka, PostgreSQL, Kubernetes), и разброс числа навыков между моделями как раз покажет, кто извлекает полнее. Качество оценим сравнением полей в `parsed`.   Полные JSON-ы четырёх моделей сохранены в `comparison_results`.

- `try/except` вокруг каждой модели. Если GigaChat-3-Ultra упрётся в лимит бесплатного тарифа, таблица всё равно соберётся по остальным.

![](<Pasted image 20261022173032.png>)

- GigaChat-3-Lightning выигрывает по обеим метрикам: 0.71 с `latency` и 223 ток/с. Скорость её сильная сторона.

- GigaChat-2-Pro - самая медленная (3.50 с, 41 ток/с): в пять раз медленнее Lightning. 
- Ultra быстрее Pro (1.95 с против 3.50) - последнее поколение на той же задаче обогнало «тяжёлую» модель прошлого. 
- Все четыре модели извлекли 6 навыков из 6 - по количеству расхождений нет. Качество надо смотреть в самих JSON.
##### Добавил скрипт для сравнения качества извлечения:
```python
fields = ['name', 'experience_years', 'current_position', 'target_position', 'salary_from', 'work_format']

print(f"{'Поле':<20}", end='')
for r in comparison_results:
    print(f"{r['model']:>24}", end='')
print()
print('-' * 116)

for f in fields:
    print(f"{f:<20}", end='')
    for r in comparison_results:
        val = str(r['parsed'].get(f))
        print(f"{val[:22]:>24}", end='')
    print()
```

![](<Pasted image 20261022173131.png>)

- У всех четырех моделей шесть полей - идентичный результат. Расхождение одно: `work_format` - «Удалёнка» у трёх а «удалёнка» с маленькой буквы у GigaChat-2-Pro. На таких мелочах  ломаются фильтры со строгим сравнением строк, поэтому мы в разделе 5 написан нормализатор `.lower().`

##### Дополнительное задание: ранее построенный пайплайн переносится на новый тип документа заменой схемы и промпта.
###### заменил скрипт под заглушкой:
```python
# Тестовые вакансии
vacancy_1 = """
Компания TechFlow ищет Senior Python Developer.
Обязательно: Python 5+ лет, FastAPI или Django, PostgreSQL, Docker.
Желательно: Kubernetes, опыт с микросервисами, Redis.
Условия: гибрид (Москва), зарплата до 400 000 рублей, ДМС.
"""

vacancy_2 = """
Ищем Middle Data Scientist в e-commerce стартап.
Требования: Python, pandas, scikit-learn, опыт построения ML-моделей от 2 лет.
Плюсом будет: PyTorch, опыт с рекомендательными системами, A/B-тесты.
Полная удалёнка, зарплата до 220 000. Команда 5 человек.
"""

vacancy_3 = """
Frontend Developer (React) — продуктовая компания в сфере EdTech.
Must have: React, TypeScript, REST API, опыт от 1 года.
Nice to have: Next.js, тестирование (Jest), Storybook.
Офис в СПб или удалёнка, вилка 150 000 – 200 000.
"""


def parse_vacancy(text: str, attempts: int = 3) -> dict | None:
    """
    Извлекает структурированные данные из текста вакансии.

    Args:
        text: Текст вакансии в произвольном формате

    Returns:
        Словарь с полями position, company, required_skills,
        nice_to_have, experience_required, salary_to, work_format
        или None при ошибке
    """
    # Схема вакансии: 7 полей, отсутствующие данные — null
    vacancy_schema = {
        'type': 'object',
        'properties': {
            'position': {'type': 'string'},
            'company': {'type': ['string', 'null']},
            'required_skills': {'type': 'array', 'items': {'type': 'string'}},
            'nice_to_have': {'type': 'array', 'items': {'type': 'string'}},
            'experience_required': {'type': ['string', 'null']},
            'salary_to': {'type': ['number', 'null']},
            'work_format': {'type': 'string'},
        },
        'required': [
            'position', 'company', 'required_skills', 'nice_to_have',
            'experience_required', 'salary_to', 'work_format',
        ],
        'additionalProperties': False,
    }

    system_prompt = """
Ты — HR-ассистент. Извлекай данные из вакансии и возвращай строго в формате JSON.
required_skills и nice_to_have — списки названий технологий: по одному названию
в каждом элементе, без кавычек и без пояснений. Альтернативы разделяй на отдельные
элементы: 'FastAPI или Django' — это два элемента 'FastAPI' и 'Django'.
Уточнение опыта ('5+ лет') — не часть названия навыка, его место в experience_required.
experience_required — строка вида '3-5 лет' или 'от 2 лет'.
salary_to — верхняя граница зарплаты (число) или null, если не указана.
Если поле в тексте отсутствует — верни null.
"""

    chat = Chat(
        model='GigaChat-3-Lightning',  # выбрана по итогам бенчмарка раздела 6
        messages=[
            Messages(role=MessagesRole.SYSTEM, content=system_prompt),
            Messages(role=MessagesRole.USER, content=f'Обработай вакансию:\n{text}'),
        ],
        response_format={
            'type': 'json_schema',
            'schema': vacancy_schema,
            'strict': True,
        },
    )

    for attempt in range(1, attempts + 1):
        try:
            response = client.chat(chat)
            return json.loads(response.choices[0].message.content)
        except RateLimitError as e:
            wait = getattr(e, 'retry_after', None) or 5
            print(f'Лимит запросов (попытка {attempt}/{attempts}). Ждём {wait} сек...')
            time.sleep(wait)
        except Exception as e:
            print(f'Ошибка: {e}')
            return None
    return None


# Тестирование
for i, vacancy in enumerate([vacancy_1, vacancy_2, vacancy_3], 1):
    print('=' * 55)
    print(f'Вакансия {i}')
    print('=' * 55)
    result = parse_vacancy(vacancy)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()
```

![](<Pasted image 20261022210427.png>)

![](<Pasted image 20261022210457.png>)

![](<Pasted image 20261022210518.png>)

- `salary_to` - число, а не строка. В вакансиях формулировки «до 400 000 рублей» и «вилка 150 000 – 200 000» чтобы фильтровать по зарплате в коде нужно число. 

- `experience_required` - строка. «От 2 лет», «от 1 года» - диапазоны, приводить их к числу небезопасно, оставляю строкой. Разнотипные поля (`number` против `string`) - осознанное решение схемы.

- `null` в промпте применен умышлено, по опыту предыдущего прогона.

- Структура ретраев идентична `parse_resume` для однообразной обработки ошибок по всему пайплайну.
##### Бонус ячейка `match_candidates`:
```python
def match_candidates(vacancy: dict, candidates: list) -> list:
    """
    Подбирает кандидатов из списка по совпадению навыков.

    Args:
        vacancy: Разобранная вакансия (результат parse_vacancy)
        candidates: Список разобранных резюме (результаты parse_resume)

    Returns:
        Список подходящих кандидатов (>= 2 совпадений) с полем matched_skills
    """
    required = [s.lower() for s in vacancy.get('required_skills', [])]
    matched = []

    for cand in candidates:
        cand_skills = [s.lower() for s in cand.get('skills', [])]
        hits = [
            req for req in required
            if any(req in skill for skill in cand_skills)
        ]
        if len(hits) >= 2:
            entry = dict(cand)  
            entry['matched_skills'] = hits
            matched.append(entry)

    return matched


# Демонстрация: матчинг по всем трём вакансиям
vacancies = [vacancy_1, vacancy_2, vacancy_3]
for i, vac_text in enumerate(vacancies, 1):
    vacancy = parse_vacancy(vac_text)
    if not vacancy:
        continue
    print(f"Вакансия {i}: {vacancy['position']}")
    for m in match_candidates(vacancy, results):
        print(f"   → {m['name']}: совпало {m['matched_skills']}")
    print()
```

- два решения: `.lower()` с обеих сторон (нормализация регистра) и подстрочный матчинг - потому что точное сравнение  потеряло бы кандидатов. `dict(cand)` - копия, чтобы не мутировать исходный `results`.

![](<Pasted image 20261022174102.png>)


> [!calendar] Дата
> **Добавлено:** 2026-10-22  12:45
> **Изменено: **<%+ tp.file.last_modified_date("YYYY-MM-DD HH:mm") %>
> **Тема задания:** <%+ tp.file.title %>
