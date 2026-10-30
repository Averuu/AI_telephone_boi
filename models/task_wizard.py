from odoo import models, fields

class TaskWizard(models.TransientModel):
    _name = 'task.wizard'
    _description = 'Task Master Wizard'

    # Текст, который будет отображаться внутри мастера
    message = fields.Text(string="Сообщение", default="Выберите действие для продолжения:", readonly=True)

    # Кнопки-заглушки будут вызывать методы ниже
    def action_one(self):
        # Логика для кнопки 1
        return {'type': 'ir.actions.act_window_close'}

    def action_two(self):
        # Логика для кнопки 2
        return {'type': 'ir.actions.act_window_close'}

    def action_three(self):
        # Логика для кнопки 3
        return {'type': 'ir.actions.act_window_close'}
