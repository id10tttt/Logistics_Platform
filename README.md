# Logistics_Platform
Logistics Platform

# 高德地图

* 在 odoo.conf 里面添加配置的key
        
        gaode_map_web_service_key=xxx
        gaode_mao_web_key=xxx
* 使用 web端 key
        
        <t t-set="web_key" t-value="request.env['ir.config_parameter'].sudo().get_param_from_config_file('gaode_mao_web_key')"/>
        https://webapi.amap.com/maps?v=1.4.15&amp;key={{web_key}}&amp;plugin=AMap.Autocomplete
        
* 使用 web服务 key
        
        <t t-set="web_service_key" t-value="request.env['ir.config_parameter'].sudo().get_param_from_config_file('gaode_map_web_service_key')"/>
        <script type="text/javascript"
                src="https://webapi.amap.com/maps?v=1.4.15&amp;key={{web_service_key}}"></script>
                

# odoo page

* 建立一个 template，inside website.layout
    
        <template id='your_template_id'>
            <t t-call="website.layout">
                xxx(Your code)
            </t>
        </template>

* request 或者其他地方，render 这个 template
        
        values = {
            xxx: xxx
        }
        return request.render("xxx_module.your_template_id", values)