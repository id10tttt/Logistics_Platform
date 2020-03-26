#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def signup(self, values, token=None):
        """ """
        context = dict(self._context)
        if values.get('user_type_id', False):
            context["user_type_id"] = values.get('user_type_id', False)
            values.pop("user_type_id")
        return super(ResUsers, self.with_context(context)).signup(values, token)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        user_obj = super(ResUsers, self).copy(default=default)

        if self._context.get('user_type_id', False):

            wk_value = {
                "user_type": self._context.get('user_type_id'),
            }
            user_obj.partner_id.write(wk_value)

            user_type = self._context.get('user_type_id')
            if user_type == 'logistics_user':
                logistics_group = \
                    self.env['ir.model.data'].get_object_reference('website_vendor', 'logistics_user_group')[1]
            elif user_type == 'logistics_supplier':
                portal_group_id = self.env['ir.model.data'].get_object_reference('base', 'group_portal')[1]
                user_group_id = self.env['ir.model.data'].get_object_reference('base', 'group_user')[1]
                groups_ids = user_obj.groups_id.ids

                _logger.info({
                    'user_obj': user_obj
                })
                # 去除 portal 组
                if portal_group_id in groups_ids:
                    groups_ids.remove(portal_group_id)

                # 修改魏 user 组
                groups_ids.append(user_group_id)

                # 写入
                user_obj.write({
                    'groups_id': [(6, 0, groups_ids)]
                })
                logistics_group = \
                    self.env['ir.model.data'].get_object_reference('website_vendor', 'logistics_supplier_group')[1]

            # Add user to Logistics group

            groups_obj = self.env["res.groups"].browse(logistics_group)
            if groups_obj:
                for group_obj in groups_obj:
                    group_obj.write({"users": [(4, user_obj.id, 0)]})
        return user_obj
