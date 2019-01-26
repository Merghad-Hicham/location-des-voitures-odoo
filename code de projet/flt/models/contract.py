import time

from datetime import datetime
from datetime import timedelta
from odoo.exceptions import Warning, ValidationError
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT
from dateutil.relativedelta import relativedelta


class CarRentalContract(models.Model):
    _name = 'vehicles.rent.contract'

    image = fields.Binary(related='vehicle_id.image', string="Image of Vehicle")

    image_medium = fields.Binary(related='vehicle_id.image_medium', string="Logo (medium)")
    image_small = fields.Binary(related='vehicle_id.image_small', string="Logo (small)")

    name = fields.Text(compute='_compute_contract_name', store=True)
    reserved_fleet_id = fields.Many2one('rent.fleet.reserved', invisible=True, copy=False)
    customer_id = fields.Many2one('res.partner', required=True, string='Customer', help="Customer")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    liste_prix = fields.Many2one('product.pricelist.item', string="liste de prix", required=True,
                                 domain="[('vehicle_id','=',vehicle_id)]")
    rapport_crr = fields.Selection([('c', 'creer'), ('n', 'non creer')], default='n', string="creation de rapport")
    facture_creer = fields.Selection([('c', 'creer'), ('n', 'non creer')], default='n', string="creation de rapport")

    car_brand = fields.Many2one('fleet.vehicle.model.brand', string="Brand", size=50,
                                related='vehicle_id.model_id.brand_id', store=True, readonly=True)
    car_color = fields.Char(string="Color", size=50, related='vehicle_id.color', store=True, copy=False,
                            default='#ffffff', readonly=True)

    prix_jour = fields.Integer(string="prix de journee par DH")
    prix = fields.Float(string="prix par Dh", compute='cal_price_liste')
    methode_py = fields.Selection([('cache', 'cash'), ('cheque', 'cheque'), ('carte', 'carte bancaire')],
                                  string="Methode de paiement")
    kilometre = fields.Float(string="kilometrage", related='vehicle_id.odometer', readonly=True)
    matricule = fields.Char(string="Matricule", related='vehicle_id.license_plate', readonly=True)
    carte_grise = fields.Char(string="Certificat d'immatriculation", related='vehicle_id.Loueur', readonly=True)
    cin = fields.Char(string="CIN", related='customer_id.cin', readonly=True)
    permis = fields.Char(string="permis de conduire", related='customer_id.ahead', readonly=True)
    mobile = fields.Char(string="Mobile", related='customer_id.mobile', readonly=True)
    nb_jour = fields.Integer(string="nombre des jours", required=True, compute='_set_duree')
    total_prix = fields.Float(string="prix total par DH", compute='cal_total_price')
    caution = fields.Integer(string="Caution par DH")
    rent_start_date = fields.Date(string="Date de debut", required=True, default=datetime.today(),
                                  help="Start date of contract", track_visibility='onchange')
    rent_end_date = fields.Date(string="Date de fin", required=True, help="End date of contract",
                                track_visibility='onchange')
    state = fields.Selection(
        [('draft', 'Draft'), ('reserved', 'Reserved'), ('running', 'En cours'), ('cancel', 'Annule'),
         ('checking', 'Checking'), ('invoice', 'Invoice'), ('Terminer', 'Termine'), ('confirm', 'confirm')], string="State",
        default="draft", copy=False, track_visibility='onchange')
    notes = fields.Text(string="Details & Notes")
    first_invoice_created = fields.Boolean(string="First Invoice Created", invisible=True, copy=False)
    sales_person = fields.Many2one('res.users', string='Responsible Person', default=lambda self: self.env.uid,
                                   track_visibility='always')

    @api.model
    def create(self, vals):
        res = super(CarRentalContract, self).create(vals)
        voiture = self.env['fleet.vehicle'].browse(vals['vehicle_id'])
        if self.state != 'Terminer':
            voiture.disponibilite = 'n'
        elif self.state == 'Terminer':
            voiture.disponibilite = 'd'
        return res

    @api.depends('vehicle_id', 'rent_start_date')
    def _compute_contract_name(self):
        for record in self:
            name = record.vehicle_id.name
            if record.rent_start_date:
                name += ' / ' + record.rent_start_date
            record.name = name

    @api.multi
    def action_cancel(self):
        self.state = "cancel"
        if self.reserved_fleet_id:
            self.reserved_fleet_id.unlink()

    @api.multi
    @api.depends('vehicle_id')
    def contract_done(self):
        self.vehicle_id.disponibilite = 'd'
        for record in self:
            record.state = 'Terminer'

    @api.one
    @api.depends('vehicle_id', 'liste_prix')
    def cal_price_liste(self):

        if self.vehicle_id == self.liste_prix.vehicle_id:
            self.prix = self.liste_prix.fixed_price

    @api.one
    @api.depends('prix_jour', 'nb_jour')
    def cal_total_price(self):
        prixx = float(self.prix)
        self.total_prix = prixx * self.nb_jour

    @api.depends('rent_start_date', 'rent_end_date')
    def _set_duree(self):
        if self.rent_end_date and self.rent_start_date:
            fmt = '%Y-%m-%d'
            d1 = datetime.strptime(self.rent_start_date, fmt)
            d2 = datetime.strptime(self.rent_end_date, fmt)
            daysDiff = str((d2 - d1).days)
            self.nb_jour = str((d2 - d1).days + 1)

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('vehicles.rent.contract')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('vehicles.rent.contract', docargs)

    @api.multi
    def action_run(self):
        self.state = 'running'

    @api.multi
    def action_draft(self):
        self.state = 'draft'
