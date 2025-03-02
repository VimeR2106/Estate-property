from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for property"
    _order = 'price DESC'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted','Accepted'),('refused','Refused')],
        copy=False
    )
    partner_id=fields.Many2one("res.partner", required=True) #domain="[('is_company', '=',True)]",
    property_id=fields.Many2one("estate.property", required=True)
    validity=fields.Integer(default = 7)
    date_deadline=fields.Date(compute="_compute_date_deadline")

    # SQL constraints
    _sql_constraints = [
        ('check_positive', 'CHECK(price > 0)',
        'The price must be strictly positive')
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = datetime.now()
            record.date_deadline = record.create_date + relativedelta(days = record.validity)
    
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < record.property_id.expected_price * 0.9:
                raise ValidationError(_("The selling price must be at least 90%' 'of the expected price! You must reduce the expected price if you want to accept this offer."))
    
    def action_accept_property(self):
        """
        change record state accepted
        """
        
        for record in self:
            record.update(
                {
                    "status":'accepted',
                }
            )
            record.property_id.write(
                {
                    "partner_id": record.partner_id,
                    "selling_price": record.price
                }
            )
            offer = record.property_id.offer_ids
            offer -= record
            offer.write(
                {
                    "status":'refused'
                }
            )


    def action_refuse_property(self):
        """
        change record state refuse
        """
        for record in self:
            record.update(
                {
                    "status":'refused'
                }
            )


