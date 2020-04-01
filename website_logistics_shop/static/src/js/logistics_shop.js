odoo.define('website_logistics_shop.checkout', function (require) {
    'use strict';

    require('web.dom_ready');
    let ajax = require('web.ajax');
    let core = require('web.core');
    let _t = core._t;
    let concurrency = require('web.concurrency');
    let dp = new concurrency.DropPrevious();

    let _onCarrierUpdateAnswer = function (result) {

        // 经纬度
        let from_location_lnglat_obj = $('#from_location_lnglat')[0];
        let to_location_lnglat_obj = $('#to_location_lnglat')[0];

        let $carrier_badge = $('#delivery_carrier input[name="logistics_delivery_type"][value=' + result.carrier_id + '] ~ .badge:not(.o_delivery_compute)');
        let $compute_badge = $('#delivery_carrier input[name="logistics_delivery_type"][value=' + result.carrier_id + '] ~ .o_delivery_compute');

        let delivery_amount = $('#delivery_amount');

        let shortest_path = $('#route_line');

        let shortest_weight_class = $('#shortest_weight_class')[0];
        let shortest_distance_class = $('#shortest_distance_class')[0];
        let fast_speed_class = $('#fast_speed_class')[0];

        let input_shortest_weight = $('#shortest_weight')[0];

        $carrier_badge.children('span').text(result.new_amount_delivery);
        $carrier_badge.removeClass('d-none');
        $compute_badge.addClass('d-none');
        delivery_amount.val(result.new_amount_delivery);

        shortest_path.val(result.shortest_path);

        shortest_weight_class.textContent = result.shortest_path;
        input_shortest_weight.checked = true;

        shortest_distance_class.textContent = result.shortest_path;
        fast_speed_class.textContent = result.shortest_path;

        from_location_lnglat_obj.textContent = '经纬度: ' + result.from_location_lnglat;
        to_location_lnglat_obj.textContent = '经纬度: ' + result.to_location_lnglat;

    };
    let _onCarrierClickInherit = function (ev) {

        let carrier_id = $(ev.currentTarget).val();
        let from_location_name = $('#from_location_name').val();
        let to_location_name = $('#to_location_name').val();
        let values = {
            'carrier_id': carrier_id,
            'from_location_name': from_location_name,
            'to_location_name': to_location_name
        };

        if (from_location_name && to_location_name) {
            dp.add(ajax.jsonRpc('/logistics/delivery_price', 'call', values))
                .then(_onCarrierUpdateAnswer);
        }
    };

    let $carriers = $("#delivery_carrier input[name='logistics_delivery_type']");
    $carriers.click(_onCarrierClickInherit);
    if ($carriers.length > 0) {
        $carriers.filter(':checked').click();
    }

});