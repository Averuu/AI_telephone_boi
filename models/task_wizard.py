from odoo import models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    def open_custom_wizard(self):
        """Этот метод сработает и на канбан-доске задач, и внутри формы задачи"""
        if not self:
            # Нажата кнопка на канбан-доске (запись не выбрана)
            message = "Вы запустили мастер с Канбан-доски задач проекта!"
            title = "Действие из доски задач"
        else:
            # Нажата кнопка внутри формы конкретной задачи
            message = f"Вы запустили мастер из задачи: {self.name}"
            title = "Действие из Задачи"

        return {
            'name': title,
            'type': 'ir.actions.act_window',
            'res_model': 'task.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_message': message}
        }
