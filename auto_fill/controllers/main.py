# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Avinash Nk(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo.http import request
from odoo import http
import requests
from odoo.tools import config

url = 'https://restapi.amap.com/v3/assistant/inputtips?parameters'


class GetMatchingRecords(http.Controller):

    @http.route(['/matching/records'], type='json', auth="none")
    def get_matching_records(self, **kwargs):
        value = str(kwargs['value'])
        if not value:
            return []
        data = {
            'key': config.get('gaode_map_web_service_key'),
            'keywords': value
        }
        res = requests.get(url=url, params=data)
        result = res.json().get('tips')
        result = [x.get('name') for x in result]
        return result
