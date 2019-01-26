import time

from datetime import datetime
from datetime import timedelta
from odoo.exceptions import Warning, ValidationError
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT


class facte_vehicles(models.Model):
    _inherit = 'account.invoice'
    vehicle_id = fields.Many2one(related="contract_id.vehicle_id", string="vehicle")
    contract_id = fields.Many2one('vehicles.rent.contract')

    client = fields.Many2one(related='contract_id.customer_id')
    cin = fields.Char(related="contract_id.cin", string="CIN")
    date_facture = fields.Date(string="Date de facture", required=True, default=datetime.today(),
                               track_visibility='onchange')
    prix_jour = fields.Float(string="prix de journee par DH", related="contract_id.prix")
    nb_jour = fields.Integer(string="nombre des jours", related="contract_id.nb_jour")
    total_prix = fields.Float(string="prix total par DH", related="contract_id.total_prix")
    caution = fields.Integer(string="Caution par DH", related="contract_id.caution")
    partner_id = fields.Many2one('res.partner', string='Partner', change_default=True, readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 track_visibility='always')

    @api.onchange('contract_id')
    def add(self):
        self.invoice_line_ids = [(0, 0, {'vehicle_id':self.vehicle_id,'client':self.client,'cin':self.cin,
                                         'caution': self.caution,'name': self.contract_id.name,'price_unit': self.prix_jour,'quantity': self.nb_jour,'total_prix': self.total_prix})]

    #@api.model
    #def create(self, vals):
     #   res = super(facte_vehicles, self).create(vals)
      #  contrat = self.env['vehicles.rent.contract'].browse(vals['contract_id'])
       # contrat.facture_creer = 'c'


class facte_line(models.Model):
    _inherit = 'account.invoice.line'
    vehicle_id = fields.Many2one(related="contract_id.vehicle_id", string="vehicule", store=True)
    contract_id = fields.Many2one('vehicles.rent.contract')

    client = fields.Many2one(related='contract_id.customer_id', store=True)
    cin = fields.Char(related="contract_id.cin", string="CIN", store=True)
    date_facture = fields.Date(string="Date de facture", required=True, default=datetime.today(),
                               track_visibility='onchange')
    prix_jour = fields.Float(string="prix de journee par DH", related="contract_id.prix")
    nb_jour = fields.Integer(string="nombre des jours", related="contract_id.nb_jour")
    total_prix = fields.Float(string="prix total par DH", related="contract_id.total_prix")
    caution = fields.Integer(string="Caution par DH", related="contract_id.caution")
    partner_id = fields.Many2one(related='contract_id.customer_id', store=True)



