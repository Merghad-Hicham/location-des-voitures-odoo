import time

from datetime import datetime
from datetime import timedelta
from odoo.exceptions import Warning, ValidationError
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT


class rapport_retoure_vehicles(models.Model):
    _name = 'rapport.retoure.vehicles'

    image1 = fields.Binary(string="image 1")
    image2 = fields.Binary(string="image 2")
    image3 = fields.Binary(string="image 3")

    vehicle_id = fields.Many2one(related="rapport_sorti_id.vehicle_id", string="vehicle")
    rapport_sorti_id = fields.Many2one("rapport.sorter.vehicles")
    contract_id = fields.Many2one('vehicles.rent.contract')
    matricule = fields.Char(related="rapport_sorti_id.matricule", string="matricule")
    client = fields.Many2one(related="rapport_sorti_id.client", string="Nom de conducteur")
    cin = fields.Char(related="rapport_sorti_id.cin", string="CIN")
    #Loueur = fields.Char(string="Loueur")
    #matricule = fields.Char(related="vehicle_id.matricul", string="matricule")
    # Loueur = fields.Char(string="Loueur")

    etat = fields.Selection([('normal', 'Normal'), ('accidenter', 'Accidenter'), ('en_panne', 'En panne')],
                            string="Etat")
    nb_enjoliveurs = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="NB Eenjoliveurs")
    roue_de_secours = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="roue_de_secours")
    triangles = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="Triangle/Extincteur/Gilet")
    jou_tapis = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="Jou Tapis")
    cric = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Cric")
    kit_anti = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="Kit anti crevaison")
    manivelle = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="Manivelle")
    antenne = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="Antenne")
    allume = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="Allume cigare")
    goblet = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')], string="Goblet")
    proprete = fields.Selection(
        [('casser', 'casse'), ('ravure', 'Ravure'), ('enfoncer', 'Enfonce'), ('manouant', 'Manouant')],
        string="Proprete")
    vignette = fields.Boolean(string="Vignette")
    carte_grise = fields.Boolean(string="Carte Grise")
    carnet_entretien = fields.Boolean(string="Carnet D entretien")
    autoris_circulation = fields.Boolean(string="Autorusation de circulation")
    visite = fields.Boolean(string="Visite technique")
    att_assurance = fields.Boolean(string="Att_assurance ")
    killim_livrer = fields.Float(string="Last Odometer", store=True)
    killim_restitue = fields.Float(string="Odometer de restitue")
    date_livrer = fields.Date(string="Date de livre")
    date_restitue = fields.Date(string="Date de restitue")
    lieu_livraition = fields.Char(string="Lieu de Livraision")
    lieu_restitution = fields.Char(string="Lieu de restitution")

    notes = fields.Text()

    @api.onchange('rapport_sorti_id')
    def fetch_data(self):
        self.etat = self.rapport_sorti_id.etat
        self.nb_enjoliveurs = self.rapport_sorti_id.nb_enjoliveurs
        self.roue_de_secours = self.rapport_sorti_id.roue_de_secours
        self.triangles = self.rapport_sorti_id.triangles
        self.jou_tapis = self.rapport_sorti_id.jou_tapis
        self.cric = self.rapport_sorti_id.cric
        self.kit_anti = self.rapport_sorti_id.kit_anti
        self.manivelle = self.rapport_sorti_id.manivelle
        self.antenne = self.rapport_sorti_id.antenne
        self.allume = self.rapport_sorti_id.allume
        self.goblet = self.rapport_sorti_id.goblet
        self.proprete = self.rapport_sorti_id.proprete
        self.vignette = self.rapport_sorti_id.vignette
        self.carte_grise = self.rapport_sorti_id.carte_grise
        self.carnet_entretien = self.rapport_sorti_id.carnet_entretien
        self.autoris_circulation = self.rapport_sorti_id.autoris_circulation
        self.visite = self.rapport_sorti_id.visite
        self.killim_livrer = self.rapport_sorti_id.killim_livrer
        self.att_assurance = self.rapport_sorti_id.att_assurance
        self.lieu_livraition = self.rapport_sorti_id.lieu_livraition
        self.lieu_restitution = self.rapport_sorti_id.lieu_restitution

    @api.model
    def create(self, vals):
        res = super(rapport_retoure_vehicles, self).create(vals)
        contrat = self.env['rapport.sorter.vehicles'].browse(vals['rapport_sorti_id'])
        contrat.rapport_creer = 'c'
        voiture = self.env['fleet.vehicle'].browse(vals['vehicle_id'])
        voiture.odometer = vals['killim_restitue']
        return res
