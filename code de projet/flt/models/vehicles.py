import time

from datetime import datetime
from datetime import timedelta
from odoo.exceptions import Warning, ValidationError
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT


class location_voiture(models.Model):
    _inherit = 'fleet.vehicle'
    Loueur = fields.Char(string="carte grrise")
    matricul = fields.Char(string="matricule")
    cart_img = fields.Binary("copie")
    prix_id = fields.Many2one('product.pricelist.item')
    prixx = fields.Float(string="prix")
    contract_cou = fields.Integer(compute="_compute_count_all", string='Contrat')
    #prix = fields.Char('product.pricelist.item', string="prix", related='prix_id.price')
    disponibilite = fields.Selection([('d', 'disponible'), ('n', 'non disponible')], default='d', string="disponibilte")

    @api.multi
    def return_action_to_open(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('flt', xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id, group_by=False),
                domain=[('vehicle_id', '=', self.id)]
            )
            return res
        return False

    def _compute_count_all(self):
        Odometer = self.env['fleet.vehicle.odometer']
        LogFuel = self.env['fleet.vehicle.log.fuel']
        LogService = self.env['fleet.vehicle.log.services']
        LogContract = self.env['vehicles.rent.contract']
        Cost = self.env['fleet.vehicle.cost']
        for record in self:
            record.odometer_count = Odometer.search_count([('vehicle_id', '=', record.id)])
            record.fuel_logs_count = LogFuel.search_count([('vehicle_id', '=', record.id)])
            record.service_count = LogService.search_count([('vehicle_id', '=', record.id)])
            record.contract_count = LogContract.search_count([('vehicle_id', '=', record.id)])
            record.cost_count = Cost.search_count([('vehicle_id', '=', record.id), ('parent_id', '=', False)])