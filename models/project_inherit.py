from odoo import models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    def open_custom_wizard(self):
        """Метод для вызова мастера с главной страницы проектов"""
        return {
            'name': 'Действие из Проектов',
            'type': 'ir.actions.act_window',
            'res_model': 'task.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_message': 'Вы запустили мастер с главной страницы Проектов!'}
        }

class ProjectTask(models.Model):
    _inherit = 'project.task'

    def open_custom_wizard(self):
        """Метод для вызова мастера изнутри конкретной Задачи"""
        return {
            'name': 'Действие из Задачи',
            'type': 'ir.actions.act_window',
            'res_model': 'task.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_message': f'Вы запустили мастер из задачи: {self.name}'}
        }
