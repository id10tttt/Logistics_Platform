# odoo action_client open qweb template

* add menu and action

    * menu && action
            
            <record id="action_odoo_test_view" model="ir.actions.client">
                <field name="name">Odoo test</field>
                <field name="tag">your_action_client_tag</field>
            </record>
        
            <menuitem id="test_menu_child"
                  action="odoo_test.action_odoo_test_view"
                  name="Odoo test client" parent="test_menu_root"/>
    
* define qweb template
        
        <?xml version="1.0" encoding="UTF-8" ?>
        <template>
            <t t-name="your_template_id">
                <h2>xxx</h2>
                <div class="col-md-6 col-xl-6 offset-xl-2">
                    <div>
                        <label for="xxx">xxx</label>
                        <input type="text" name="xxx" 
                        id="xxx" class="xxx">
                            <span class="xxx"></span>
                        </input>
                    </div>

                </div>
            </t>
        </template>

* define the usage in js

        odoo.define('odoo_test.action_client_open_qweb_template', function (require) {
            "use strict";
        
            let core = require('web.core');
            let _t = core._t;
            let QWeb = core.qweb;
            let Widget = require('web.Widget');
            let Model = require('web.rpc');
            let AbstractAction = require('web.AbstractAction');
        
            let OdooTestAction = AbstractAction.extend({
                template: 'your_template_id',
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
        
            core.action_registry.add('your_action_client_tag', OdooTestAction);
            return OdooTestAction;
        });