from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type"
    _order = 'sequence,name ASC'

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many('estate.property','property_type_id')

    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
        'The name must be unique')
    ]
