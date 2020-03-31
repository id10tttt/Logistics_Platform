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

        $carrier_badge.children('span').text(result.new_amount_delivery);
        $carrier_badge.removeClass('d-none');
        $compute_badge.addClass('d-none');
        delivery_amount.val(result.new_amount_delivery);

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
        dp.add(ajax.jsonRpc('/logistics/delivery_price', 'call', values))
            .then(_onCarrierUpdateAnswer);
    };

    let $carriers = $("#delivery_carrier input[name='logistics_delivery_type']");
    $carriers.click(_onCarrierClickInherit);
    if ($carriers.length > 0) {
        $carriers.filter(':checked').click();
    }

});