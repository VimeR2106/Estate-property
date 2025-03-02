from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import _, fields, models, api
from odoo.exceptions import UserError





class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate objects"
    _order = 'id DESC'

    #model fields

    name = fields.Char(
        required=True,
        default=lambda self: _('New'))
    description = fields.Text(required=True)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(name='available from',required=True,copy=False,default= date.today() + relativedelta(months=3) ) 
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(required=True,default=2)
    living_area = fields.Integer(required=True)
    facades = fields.Integer(default=4)
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    state = fields.Selection(
        default ='new',
        selection=[('new','New'),('received','Offer Received'),('accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')]
    )



    #computed fields
    
    garden_area = fields.Integer(compute="_compute_garden",readonly=False)
    garden_orientation = fields.Selection(
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        compute="_compute_garden",readonly=False
    )
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Char(compute="_compute_best_price")
    
    # Reletions with another model

    property_type_id = fields.Many2one('estate.property.type',required=True)
    partner_id = fields.Many2one("res.partner",copy=False, name="Buyer")
    user_id = fields.Many2one("res.users",default=lambda self: self.env.user, name="Saleman")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer","property_id")
    
    

    # SQL constraints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
        'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
        'The selling price must be strictly positive')
    ]
    

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            if prices:
                best_price = max(prices)
                record.best_price = best_price
            else:
                record.best_price = False



    @api.depends("garden")
    def _compute_garden(self):
        for record in self:
            if not record.garden:
                record.update(
                    {
                        "garden_area":False,
                        "garden_orientation":False
                    }
                )
            else:
                record.update(
                    {
                        "garden_area":10, 
                        "garden_orientation":"north"
                    }
                )

    def action_cancel_property(self):

        for record in self:
            if record.state == "sold":
                raise UserError(_('Sold property can not be canceled.'))
            if record.state == "canceled":
                continue
            record.update(
                {
                    "state":"canceled"
                }
            )

    def action_sold_property(self):
        for record in self:
            record.update(
                {
                    "state":"sold"
                }
            )
            


