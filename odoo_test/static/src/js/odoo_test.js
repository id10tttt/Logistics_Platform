odoo.define('odoo_test.action_client_open_qweb_template', function (require) {
    "use strict";

    let core = require('web.core');
    let _t = core._t;
    let QWeb = core.qweb;
    let Widget = require('web.Widget');
    let Model = require('web.rpc');
    let AbstractAction = require('web.AbstractAction');

    let OdooTestAction = AbstractAction.extend({
        template: 'odoo_test_template_id',
        events: {
            // "click .odoo_input_test": "odoo_input_test",
        },

        init: function (parent, action) {
            this._super.apply(this, arguments);
        },

        start: function () {
            return true;
        },
    });

    core.action_registry.add('odoo_test_tag', OdooTestAction);
    return OdooTestAction;
});