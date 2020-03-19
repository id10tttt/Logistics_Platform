#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import werkzeug
import odoo
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import binary_content
import base64
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo import SUPERUSER_ID
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL
from odoo.addons.web.controllers.main import Home
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website_mail.controllers.main import WebsiteMail
import logging

_logger = logging.getLogger(__name__)


class AuthSignupHome(odoo.addons.web.controllers.main.Home):

    def do_signup(self, qcontext):
        _logger.info({
            'qcontext': qcontext
        })
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'user_type_id')}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()
