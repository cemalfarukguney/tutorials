from odoo import fields, models, api
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Title', required=True)
    
    description = fields.Text('Description')
    
    postcode = fields.Char('Postcode')
    
    date_availability = fields.Date('Available From', copy=False, default=date.today() + timedelta(days=90))
    
    expected_price = fields.Float('Expected Price', required=True)
    
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    
    bedrooms = fields.Integer('Bedrooms', default=2)
    
    living_area = fields.Integer('Living Area (sqm)')
    
    facades = fields.Integer('Facades')
    
    garage = fields.Boolean('Garage')
    
    garden = fields.Boolean('Garden')
    
    garden_area = fields.Integer('Garden Area (sqm)')
    
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    
    state = fields.Selection(
        string='Status',
        required=True,
        copy=False,
        default='new',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
    
    active = fields.Boolean('Active', default=True)

    property_type_id = fields.Many2one('estate.property.type', 'Property Type')

    buyer_id = fields.Many2one('res.partner', 'Buyer', copy=False)

    salesperson_id = fields.Many2one('res.users', 'Salesperson', default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag')

    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")

    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = min(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''