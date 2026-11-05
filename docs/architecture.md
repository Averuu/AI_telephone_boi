# Архитектура Taskmaster

[README](../README.md) | [Разработка](development.md) | [Проверки](testing.md) | [План развития](roadmap.md)

## Поток данных

Модуль добавляет в Odoo Project агента, который ищет риски в задачах. Два входа, один wizard:
кнопка в kanban-доске запускает анализ проекта, кнопка в форме задачи запускает анализ одной задачи.

```text
[кнопка в kanban]──┐                                   ┌─> _collect_project / _collect_task
                   ├─> ir.actions.act_window ─> wizard ─┤      (ORM, права текущего пользователя)
[кнопка в форме]───┘    (target="new")   taskmaster.     ├─> _task_snapshot  -> правила и баллы
                                         risk.wizard     ├─> _rules_html_*   -> отчёт без ИИ
                                         .action_run()   └─> _call_llm       -> текст от ИИ (если есть ключ)
                                                             _compose        -> итоговый HTML в поле result
```

Принципы безопасности и поведение без ИИ описаны в [README](../README.md#данные-и-безопасность).
Обязательные ограничения для ИИ-разработчика находятся в [AGENTS.md](../AGENTS.md).

## Карта файлов

Пути ниже указаны относительно каталога модуля `taskmaster/`:

```text
taskmaster/
├── __manifest__.py                      объявление модуля, зависимости, порядок загрузки data-файлов
├── __init__.py                          импортирует models и wizard
├── security/
│   └── ir.access.csv                    права доступа (в 20.0 это ir.access, НЕ ir.model.access.csv)
├── models/
│   ├── __init__.py
│   └── taskmaster_agent.py              ядро: модель-сервис taskmaster.agent (AbstractModel, без таблицы)
├── wizard/
│   ├── __init__.py
│   ├── taskmaster_risk_wizard.py        TransientModel taskmaster.risk.wizard
│   └── taskmaster_risk_wizard_views.xml форма wizard + window action
├── static/src/js/
│   └── risk_wizard.js                   подсказка о времени ожидания + скрытие старого результата
└── views/
    └── project_task_views.xml           наследование kanban и формы задачи: две кнопки
```

Пользовательская документация находится в `README.md`, правила для ИИ в `AGENTS.md`,
техническая документация в `docs/`.

## Ядро анализа

`models/taskmaster_agent.py` содержит бэкенд агента и является основной зоной работы над анализом.

Константы вверху файла: `STALE_DAYS`, `DUE_SOON_DAYS`, `MAX_TASKS_SCANNED`, `MAX_TASKS_IN_PROMPT`,
`LLM_TIMEOUT`, словарь `SIGNAL_WEIGHTS`.

| Метод | Роль |
|---|---|
| `analyze_project(project)` / `analyze_task(task)` | публичные точки входа, их зовёт wizard |
| `_collect_project(project)` | ищет до `MAX_TASKS_SCANNED` задач проекта, возвращает `(summary, risky)` |
| `_collect_task(task)` | снимок задачи + описание (до 1500 символов), зависимости, подзадачи |
| `_task_snapshot(task)` | **центральный метод**: превращает задачу в dict с сигналами и баллом |
| `_rules_html_project/_task` | отчёт без ИИ |
| `_call_llm(kind, payload)` | запрос к OpenAI-совместимому API; возвращает `(text, None)` или `(False, reason)` |
| `_compose(summary_html, llm_html, rules_html, llm_error=None)` | склейка итога; без ИИ показывает краткую причину |
| `_is_closed`, `_assignees`, `_val` | защита от различий полей между версиями |

Контракт `_task_snapshot` (ключи dict; от него зависят отчёт и промпт):
`id, name, stage, assignees, deadline, high_priority, allocated_hours, effective_hours,
days_since_update, closed, signals, score`.

## Сигналы риска

| Сигнал | Вес | Условие |
|---|---|---|
| `overdue` | 5 | дедлайн в прошлом, задача не закрыта |
| `blocked` | 4 | есть незакрытая зависимость (`depend_on_ids`) |
| `overallocated` | 3 | потрачено часов больше плана |
| `due_soon` | 2 | дедлайн в ближайшие `DUE_SOON_DAYS` дней |
| `no_assignee` | 2 | нет исполнителя |
| `stale` | 2 | нет изменений `STALE_DAYS`+ дней |
| `no_deadline` | 1 | нет дедлайна |

К баллу добавляется +1 за высокий приоритет, если есть хоть один сигнал.
Статус проверки необязательных полей приведён в [документе о проверках](testing.md#что-не-проверено).

## Wizard

### Модель

`wizard/taskmaster_risk_wizard.py` содержит поля `scope` ('project' | 'task', readonly),
`project_id`, `task_id`, `result` (Html, readonly).
`default_get` определяет, что подставить, из контекста: `default_scope`, `default_project_id`,
`default_task_id`, `active_model`, `active_id`. Метод `action_run` очищает старый `result`, вызывает
агента, пишет новый `result` и **возвращает action, который переоткрывает тот же wizard** (`res_id`,
`target='new'`). Без этого диалог закрылся бы после нажатия кнопки.

### Форма и результат

`wizard/taskmaster_risk_wizard_views.xml` содержит две записи: форму `taskmaster_risk_wizard_form`
(описание агента, поля, футер с кнопками) и action `taskmaster_risk_wizard_action`
(`target=new`, то есть диалог). Описание агента, которое видит пользователь, лежит именно в этой
форме (два блока `alert alert-info`, по одному на каждый scope).
Результат идёт в порядке `Open / Overdue / Unassigned` → `AI analysis` (или плашка с причиной) →
`Rule-based signals`. На время запроса показывается подсказка `Analysis may take up to a minute.`,
а старый результат скрывается; это поведение задаёт `static/src/js/risk_wizard.js`.

## Кнопки

`views/project_task_views.xml` содержит две записи-расширения.
Подробное устройство кнопок, контекста и инструкции по изменению находятся в
[руководстве по разработке](development.md#как-менять-кнопки).

## Права доступа

Файл `security/ir.access.csv`, колонки (20.0): `id,name,model_id,group_id/id,operation,domain`.
В `model_id` пишется `_name` модели (`taskmaster.risk.wizard`), а не `model_xxx`.
В `operation` буквы `c r u d`. Группа выдачи: `project.group_project_user`.
Особенности механизма и оговорки об источниках описаны в
[руководстве по разработке](development.md#особенности-odoo-200).
