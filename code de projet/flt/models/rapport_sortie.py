import time

from datetime import datetime
from datetime import timedelta
from odoo.exceptions import Warning, ValidationError
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT


class rapport_sorter_vehicles(models.Model):
    _name = 'rapport.sorter.vehicles'

    image1 = fields.Binary(string="image 1")
    image2 = fields.Binary(string="image 2")
    image3 = fields.Binary(string="image 3")

    vehicle_id = fields.Many2one(related="contract_id.vehicle_id", string="vehicle")
    contract_id = fields.Many2one('vehicles.rent.contract')
    name = fields.Text(related="contract_id.name")
    matricule = fields.Char(related="contract_id.matricule", string="matricule")
    client = fields.Many2one(related="contract_id.customer_id", string="Nom de conducteur")
    cin = fields.Char(related="contract_id.cin", string="CIN")
    # Loueur = fields.Char(string="Loueur")

    etat = fields.Selection([('normal', 'Normal'), ('accidenter', 'Accidenter'), ('en_panne', 'En panne')],
                            string="Etat")
    nb_enjoliveurs = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="NB Eenjoliveurs")
    roue_de_secours = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="roue_de_secours")
    triangles = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Triangle/Extincteur/Gilet")
    jou_tapis = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Jou Tapis")
    cric = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Cric")
    kit_anti = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Kit anti crevaison")
    manivelle = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Manivelle")
    antenne = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Antenne")
    allume = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Allume cigare")
    goblet = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Goblet")
    proprete = fields.Selection([('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Proprete")
    vignette = fields.Boolean(string="Vignette")
    carte_grise = fields.Boolean(string="Carte Grise")
    carnet_entretien = fields.Boolean(string="Carnet D entretien")
    autoris_circulation = fields.Boolean(string="Autorusation de circulation")
    visite = fields.Boolean(string="Visite technique")
    att_assurance = fields.Boolean(string="Att_assurance ")
    killim_livrer = fields.Float(string="Last Odometer")
    killim_restitue = fields.Float(string="Odometer de restitue")
    date_livrer = fields.Date(string="Date de livre")
    date_restitue = fields.Date(string="Date de restitue")
    lieu_livraition = fields.Char(string="Lieu de Livraision")
    lieu_restitution = fields.Char(string="Lieu de restitution")
    rapport_creer = fields.Selection([('c', 'creer'), ('n', 'non creer')], default='n')

    notes = fields.Text()

    @api.model
    @api.depends('killim_livrer')
    def create(self, vals):
        res = super(rapport_sorter_vehicles, self).create(vals)
        contrat = self.env['vehicles.rent.contract'].browse(vals['contract_id'])
        contrat.rapport_crr = 'c'

        voiture = self.env['fleet.vehicle'].browse(vals['vehicle_id'])
        voiture.odometer = vals['killim_livrer']
        return res




