odoo.define('website_sale_network.checkout', function (require) {
    'use strict';

    require('web.dom_ready');
    let ajax = require('web.ajax');
    let core = require('web.core');
    let _t = core._t;
    let concurrency = require('web.concurrency');
    let dp = new concurrency.DropPrevious();

    /* Handle interactive carrier choice + cart update */
    let $pay_button = $('#o_payment_form_pay');

    let _onCarrierUpdateAnswer = function (result) {
        let $amount_delivery = $('#order_delivery span.oe_currency_value');
        let $amount_untaxed = $('#order_total_untaxed span.oe_currency_value');
        let $amount_tax = $('#order_total_taxes span.oe_currency_value');
        let $amount_total = $('#order_total span.oe_currency_value');
        let $carrier_badge = $('#delivery_carrier input[name="delivery_type"][value=' + result.carrier_id + '] ~ .badge:not(.o_delivery_compute)');
        let $compute_badge = $('#delivery_carrier input[name="delivery_type"][value=' + result.carrier_id + '] ~ .o_delivery_compute');
        let $discount = $('#order_discounted');

        if ($discount && result.new_amount_order_discounted) {
            // Cross module without bridge
            // Update discount of the order
            $discount.find('.oe_currency_value').text(result.new_amount_order_discounted);

            // We are in freeshipping, so every carrier is Free
            $('#delivery_carrier .badge').text(_t('Free'));
        }

        if (result.status === true) {
            $amount_delivery.text(result.new_amount_delivery);
            $amount_untaxed.text(result.new_amount_untaxed);
            $amount_tax.text(result.new_amount_tax);
            $amount_total.text(result.new_amount_total);
            $carrier_badge.children('span').text(result.new_amount_delivery);
            $carrier_badge.removeClass('d-none');
            $compute_badge.addClass('d-none');
            $pay_button.data('disabled_reasons').carrier_selection = false;
            $pay_button.prop('disabled', _.contains($pay_button.data('disabled_reasons'), true));
        } else {
            console.error(result.error_message);
            $compute_badge.text(result.error_message);
            $amount_delivery.text(result.new_amount_delivery);
            $amount_untaxed.text(result.new_amount_untaxed);
            $amount_tax.text(result.new_amount_tax);
            $amount_total.text(result.new_amount_total);
        }
    };

    let _onCarrierClickInherit = function (ev) {
        console.log('hello world: ', $('#from_location_name').val());
        $pay_button.data('disabled_reasons', $pay_button.data('disabled_reasons') || {});
        $pay_button.data('disabled_reasons').carrier_selection = true;
        $pay_button.prop('disabled', true);
        let carrier_id = $(ev.currentTarget).val();
        let from_location_name = $('#from_location_name').val();
        let to_location_name = $('#to_location_name').val();
        let values = {
            'carrier_id': carrier_id,
            'from_location_name': from_location_name,
            'to_location_name': to_location_name
        };
        dp.add(ajax.jsonRpc('/shop/update_carrier', 'call', values))
            .then(_onCarrierUpdateAnswer);
    };

    let $carriers = $("#delivery_carrier input[name='delivery_type']");
    $carriers.click(_onCarrierClickInherit);
    if ($carriers.length > 0) {
        $carriers.filter(':checked').click();
    }
    /* Handle stuff */
    $(".oe_website_sale select[name='shipping_id']").on('change', function () {
        let value = $(this).val();
        let $provider_free = $("select[name='country_id']:not(.o_provider_restricted), select[name='state_id']:not(.o_provider_restricted)");
        let $provider_restricted = $("select[name='country_id'].o_provider_restricted, select[name='state_id'].o_provider_restricted");
        if (value === 0) {
            // Ship to the same address : only show shipping countries available for billing
            $provider_free.hide().attr('disabled', true);
            $provider_restricted.show().attr('disabled', false).change();
        } else {
            // Create a new address : show all countries available for billing
            $provider_free.show().attr('disabled', false).change();
            $provider_restricted.hide().attr('disabled', true);
        }
    });

});
