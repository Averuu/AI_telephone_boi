# -*- coding: utf-8 -*-
"""Wizard behind both buttons (project tasks view and task form).

Docs: https://www.odoo.com/documentation/20.0/developer/reference/backend/orm.html
  - TransientModel: temporarily persistent, vacuum-cleaned; uses the same access
    rights mechanism as a regular Model -> needs ir.model.access.csv
Docs: https://www.odoo.com/documentation/20.0/developer/reference/backend/actions.html
  - an act_window with res_id + target "new" reopens a record in a dialog
"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TaskmasterRiskWizard(models.TransientModel):
    _name = 'taskmaster.risk.wizard'
    _description = 'Taskmaster risk analysis wizard'

    scope = fields.Selection(
        [('project', 'Project'), ('task', 'Task')],
        required=True, default='project', readonly=True)
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    result = fields.Html(string='Analysis', readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ctx = self.env.context
        active_model, active_id = ctx.get('active_model'), ctx.get('active_id')
        if ctx.get('default_scope') == 'task':
            if 'task_id' in fields_list and not res.get('task_id') and active_model == 'project.task':
                res['task_id'] = active_id
        elif 'project_id' in fields_list and not res.get('project_id'):
            if ctx.get('default_project_id'):
                res['project_id'] = ctx['default_project_id']
            elif active_model == 'project.project':
                res['project_id'] = active_id
        return res

    def action_run(self):
        self.ensure_one()
        # Drop the previous report immediately: the dialog may keep showing it
        # while the new (potentially slow) analysis is running.
        self.result = False
        agent = self.env['taskmaster.agent']
        if self.scope == 'task':
            if not self.task_id:
                raise UserError(_("Please select a task."))
            self.result = agent.analyze_task(self.task_id)
        else:
            if not self.project_id:
                raise UserError(_("Please select a project."))
            self.result = agent.analyze_project(self.project_id)
        # a button of type "object" closes the dialog unless an action is returned
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
