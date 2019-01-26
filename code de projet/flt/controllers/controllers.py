# -*- coding: utf-8 -*-
from odoo import http

# class Flt(http.Controller):
#     @http.route('/flt/flt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/flt/flt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('flt.listing', {
#             'root': '/flt/flt',
#             'objects': http.request.env['flt.flt'].search([]),
#         })

#     @http.route('/flt/flt/objects/<model("flt.flt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('flt.object', {
#             'object': obj
#         })