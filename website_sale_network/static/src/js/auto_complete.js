odoo.define('website_sale_network.auto_complete', function (require) {
    'use strict';

    let map = new AMap.Map("map_container", {
        resizeEnable: true
    });
    //输入提示
    let auto = new AMap.Autocomplete({
        input: "tipinput"
    });

});