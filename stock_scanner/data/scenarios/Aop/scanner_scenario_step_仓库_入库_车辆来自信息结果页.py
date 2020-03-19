
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

from_location_id = message

terminal.update_tmp_values({'from_location_id': from_location_id})

domain = [('id', '=', from_location_id)]
stock_location_id = env['stock.location'].sudo().search(domain, limit=1)

from_location_name = stock_location_id.name

terminal.update_tmp_values({'from_location_name': from_location_name})

# 查出位置对应的仓库编码,接口会用到，名称匹配
domain = [('property_stock_supplier.id', '=', from_location_id)]
res_partner_id = env['res.partner'].sudo().search(domain, limit=1)
if res_partner_id:
  terminal.update_tmp_values({'from_warehouse_code': res_partner_id.ref})

act = 'M'
res = [
    '车辆来自:',
    '',
    
]

res.append("{0}".format(from_location_name))
# res.append("{0}".format(terminal.get_tmp_value('from_warehouse_code', False)))

