# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    ahead = fields.Char(string="permis ")
    cin = fields.Char('cin d hicham')
    cin_img = fields.Binary("")
    pirmis_img = fields.Binary("")
    date_nais = fields.Date('date de naissance')
    #compte_banker = fields.Char('compte de banka')
