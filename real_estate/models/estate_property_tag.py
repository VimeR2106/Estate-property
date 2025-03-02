from random import randint
from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for property"
    _order = 'name ASC'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required = "True")
    color = fields.Integer(string='Color Index', default=_get_default_color)

    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
        'The name must be unique')
    ]


