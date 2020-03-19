
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

vin_code = message

stock_picking = env['stock.picking'].sudo().search([
                        ('vin_id.name', '=', vin_code),
                        ('picking_type_id.name', '=', terminal.get_tmp_value('picking_type_name', False)),
                        ('picking_type_id.warehouse_id.name', '=', terminal.get_tmp_value('warehouse_name', False)),
                        ('state', '=', 'assigned')
                    ], limit=1)

# terminal.update_tmp_values({'vin_code': vin_code})
  
params = terminal.get_tmp_value('into_warehouse_params', dict())


picking_type_name = terminal.get_tmp_value('picking_type_name', False)
warehouse_code = terminal.get_tmp_value('warehouse_code', False)
warehouse_name = terminal.get_tmp_value('warehouse_name', False)
brand_name = terminal.get_tmp_value('brand_name', False)
product_name = terminal.get_tmp_value('product_name', False)
from_location_name = terminal.get_tmp_value('from_location_name', False)
task_id = stock_picking.id
from_warehouse_code = terminal.get_tmp_value('from_warehouse_code', False)
product_model = terminal.get_tmp_value('product_model', False)

params.update({vin_code: {'brand_name': brand_name,
                          'product_name': product_name,
                          'from_location_name': from_location_name,
                          'task_id': task_id,
                          'from_warehouse_code': from_warehouse_code,
                          'product_model': product_model,
}})
terminal.update_tmp_values({'into_warehouse_params': params})

count = len(list( terminal.get_tmp_value('into_warehouse_params', False).keys()))

terminal.update_tmp_values({'vin_scan_count': count})

act = 'C'

res = [
    ('|', '结果页'),
    '',
    '是否继续扫描VIN码?',
    '',
    '',
    
]

res.append('VIN码: {0}'.format(vin_code))
res.append('')
res.append('合计已扫描VIN码数量: {0}'.format(count))  

  
  
