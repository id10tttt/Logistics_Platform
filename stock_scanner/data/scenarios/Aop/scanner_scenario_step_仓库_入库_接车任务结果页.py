
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

task_id = message

domain = [('id', '=', task_id)]
stock_picking = env['stock.picking'].sudo().search(domain)

terminal.update_tmp_values({'task_id': task_id})
  
  
# 任务id/name
stock_picking_id = stock_picking.id
stock_picking_name = stock_picking.name
from_location_name = stock_picking.location_id.display_name
to_location_name = stock_picking.location_dest_id.display_name
picking_incoming_number = stock_picking.picking_incoming_number

act = 'M'

res = [
    ('|', '接车任务')
]

res.append('任务编号: {0}'.format( stock_picking_name))
res.append('从: {0}'.format( from_location_name))
res.append('至: {0}'.format( to_location_name))
res.append('接车数量: {0}'.format( picking_incoming_number))

  
