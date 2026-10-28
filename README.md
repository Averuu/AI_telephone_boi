# Taskmaster

Odoo 20 module skeleton.

## Требования

- Odoo 20 (source)
- Python 3.13 и virtualenv
- PostgreSQL
- База Odoo (например, `odoo_test`)

## Установка

1. Клонировать репозиторий в `custom_addons` Odoo:

```powershell
cd C:\path\to\odoo
git clone https://github.com/Averuu/AI_telephone_boi.git custom_addons\taskmaster
```

2. Добавить `custom_addons` в `odoo.conf`:

```ini
addons_path = addons,custom_addons
```

3. Установить модуль:

```powershell
.venv\Scripts\python.exe odoo-bin -c odoo.conf -d odoo_test -i taskmaster --stop-after-init
```

4. Запустить Odoo:

```powershell
.venv\Scripts\python.exe odoo-bin -c odoo.conf -d odoo_test
```

Открыть http://localhost:8069.

## Коммит и push

Репозиторий модуля — это сама папка `custom_addons/taskmaster`:

```powershell
cd custom_addons\taskmaster
git status
git add .
git commit -m "Краткое описание изменений"
git push
```

Проверить, с каким репозиторием идёт работа:

```powershell
git rev-parse --show-toplevel
git remote -v
```

