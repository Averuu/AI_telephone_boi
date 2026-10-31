from odoo import models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    def open_custom_wizard(self):
        """Метод вызывается и с доски задач проекта, и из карточки конкретной задачи"""
        if not self:
            # Нажата кнопка на канбан-доске задач (выбран весь проект)
            active_project_id = self.env.context.get('active_id')
            project = self.env['project.project'].browse(active_project_id)
            message = f"Запущен общий анализ рисков для задач проекта: {project.name or 'Текущий проект'}"
            title = "Анализ рисков проекта"
        else:
            # Нажата кнопка внутри формы конкретной задачи
            message = f"Запущен анализ рисков для конкретной задачи: {self.name}"
            title = "Анализ рисков задачи"

        return {
            'name': title,
            'type': 'ir.actions.act_window',
            'res_model': 'task.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_message': message}
        }
