odoo.define('website_logistics_shop.checkout', function (require) {
    'use strict';

    require('web.dom_ready');
    let ajax = require('web.ajax');
    let core = require('web.core');
    let _t = core._t;
    let concurrency = require('web.concurrency');
    let dp = new concurrency.DropPrevious();

    let _onCarrierUpdateAnswer = function (result) {


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

        $("#submit_create_order_button").attr("disabled", false);
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

    let _onUpdateFromLocationLnglat = function (result) {
        // 经纬度
        let from_location_lnglat_obj = $('#from_location_lnglat')[0];

        from_location_lnglat_obj.textContent = '经纬度: ' + result.location_lng_lat;

    };

    let _onUpdateToLocationLnglat = function (result) {
        // 经纬度
        let to_location_lnglat_obj = $('#to_location_lnglat')[0];

        to_location_lnglat_obj.textContent = '经纬度: ' + result.location_lng_lat;

    };

    let _onchangeLocation = function (ev) {

        let from_location_name = $('#from_location_name').val();
        let to_location_name = $('#to_location_name').val();

        if (from_location_name) {
            let values = {
                'location_name': from_location_name
            };
            dp.add(ajax.jsonRpc('/get_location_lng_lat', 'call', values))
                .then(_onUpdateFromLocationLnglat)
        }
        if (to_location_name) {
            let values = {
                'location_name': to_location_name
            };
            dp.add(ajax.jsonRpc('/get_location_lng_lat', 'call', values))
                .then(_onUpdateToLocationLnglat)
        }
    };

    let $input_from_location = $('input[name=from_location_name]');
    $input_from_location.on('input' ,_onchangeLocation);

    let $input_to_location = $('input[name=to_location_name]');
    $input_to_location.on('input' ,_onchangeLocation);
});