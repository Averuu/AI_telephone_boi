# Проверки Taskmaster

[README](../README.md) | [Архитектура](architecture.md) | [Разработка](development.md) | [План развития](roadmap.md)

## Зафиксированное состояние

Ниже сохранён статус из исходной документации на момент передачи проекта. Это не результаты
нового запуска модуля при реорганизации документации.

Состояние на момент передачи (подтверждено командой): модуль устанавливается и работает на Odoo 20.0,
обе кнопки открывают wizard, база для проверки `odoo_test1`.

**Проверено в последней итерации:** реальный вызов LLM через OpenAI-совместимый RouterAI, вывод в обоих
режимах (с ключом и без ключа). Результат переработан: сверху сводка `Open / Overdue / Unassigned`,
затем текст ИИ или причина сбоя, затем список правил.

## Что не проверено

Делать в первую очередь, когда появится время:
- Имена необязательных полей `project.task`: `depend_on_ids`, `child_ids`, `effective_hours`,
  `allocated_hours`, `is_closed`, `state`, `user_ids`. Код проверяет их наличие через `_fields`
  и при отсутствии молча пропускает сигнал, поэтому ошибки не будет, но сигнал может не работать.
- Тестов в репозитории пока нет. Ниже сохранены план и набросок, а не реализованный набор тестов.

## Команды проверки

Команды запускаются из корня исходников Odoo. Размещение модуля и цикл обновления описаны в
[руководстве по разработке](development.md#цикл-обновления).

Проверка загрузки на использованной ранее тестовой базе:

```bash
python odoo-bin -c odoo.conf -d odoo_test1 -u taskmaster --stop-after-init
```

Для проверки на чистой базе используйте другое имя, например `odoo_test2`, и `-i taskmaster`.

Запуск тестов по документации CLI: `--test-enable` включает тесты, `--test-tags` фильтрует
по формату `[-][tag][/module][:class][.method]`:

```bash
python odoo-bin -c odoo.conf -d odoo_test_tests -i taskmaster --test-enable \
    --test-tags /taskmaster --stop-after-init
```

Команда показана с переносом для Bash. В PowerShell запускайте её одной строкой:

```powershell
python odoo-bin -c odoo.conf -d odoo_test_tests -i taskmaster --test-enable --test-tags /taskmaster --stop-after-init
```

Пока тесты не добавлены, запуск команды не подтверждает покрытие поведения агента тестами.

## Набросок теста

Набросок **не запускался**: создать `taskmaster/tests/__init__.py` (`from . import test_agent`)
и `taskmaster/tests/test_agent.py`:

```python
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestTaskmasterAgent(TransactionCase):
    def test_overdue_signal(self):
        project = self.env['project.project'].create({'name': 'P'})
        task = self.env['project.task'].create({
            'name': 'T', 'project_id': project.id, 'date_deadline': '2020-01-01 10:00:00'})
        snap = self.env['taskmaster.agent']._task_snapshot(task)
        self.assertIn('overdue', snap['signals'])
```

## Приоритеты

Приоритет тестов: каждый сигнал, `default_get` wizard (оба режима), `_compose` без ключа,
`_call_llm` с замоканным `requests.post`.

Не помечайте изменение поведения модуля выполненным без проверки: нужен запуск на тестовой
БД (`odoo_test1` или чистой) либо соответствующий тест. Если проверка недоступна, явно
зафиксируйте, что именно не проверялось.
