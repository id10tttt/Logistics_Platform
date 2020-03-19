
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

vin_code = message

scanner_step = terminal.get_tmp_value('scanner_step', 'once')
if scanner_step == 'once':
  
  # 查找解固任务,任务必须是就绪状态
  stock_picking = env['stock.picking'].sudo().search([
                          ('vin_id.name', '=', vin_code),
                          ('picking_type_id.name', '=', '解固'),
                          ('picking_type_id.warehouse_id.name', '=', terminal.get_tmp_value('warehouse_name', False)),
                          ('state', '=', 'assigned')
                      ], limit=1)
  
  jiegu_params = terminal.get_tmp_value('jiegu_params', [])
  if stock_picking:
    jiegu_params.append(stock_picking.id)
    jiegu_params = list( set(jiegu_params) )
    terminal.update_tmp_values({'jiegu_params': jiegu_params})

  xieche_params = terminal.get_tmp_value('xieche_params', dict())
  
  # 卸车任务的state
  state = ('state', 'in', ['waiting', 'assigned'])
  
else:
  state = ('state', '=', 'assigned')
  
# 查找卸车任务

stock_picking = env['stock.picking'].sudo().search([
                        ('vin_id.name', '=', vin_code),
                        ('picking_type_id.name', '=', terminal.get_tmp_value('picking_type_name', False)),
                        ('picking_type_id.warehouse_id.name', '=', terminal.get_tmp_value('warehouse_name', False)),
                        state
                    ], limit=1)
if not stock_picking:
  act = 'E'
  res = [
      '',
      '',
      'VIN: {0}, 没有查到任务'.format(vin_code),
  ]
  val = True
else:
  # 任务id/name
  stock_picking_id = stock_picking.id
  stock_picking_name = stock_picking.name
  from_location_name = stock_picking.location_id.display_name
  to_location_name = stock_picking.location_dest_id.display_name
 
  xieche_params.update({vin_code: {'stock_picking_id': stock_picking_id,
                                  'stock_picking_name': stock_picking_name,
                                  'from_location_name': from_location_name,
                                  'to_location_name': to_location_name,
                        
  }})
  terminal.update_tmp_values({'xieche_params': xieche_params})

  count = 0
  
  xieche_params = terminal.get_tmp_value('xieche_params', False)
  if xieche_params:
    params_lst = list( xieche_params.keys() )
    count = len(params_lst)
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

# from odoo.addons.aop_interface.controllers.api_interface import ApiInterface

# api = ApiInterface()

# data = []

# vin_code = message

# # 显示任务列表,测试时不加入任务状态的筛选
# # 铁路卸车允许搜索到"等待"状态的任务,扫描后如果服务端有配置，可同时完成解固+铁路卸车两个任务
# stock_picking = env['stock.picking'].sudo().search([
#                         ('vin_id.name', '=', vin_code),
#                         ('picking_type_id.name', '=', terminal.get_tmp_value('picking_type_name', False)),
#                         ('picking_type_id.warehouse_id.name', '=', terminal.get_tmp_value('warehouse_name', False)),
#                         # ('state', 'in', ['waiting', 'assigned'])
#                     ], limit=1)

# if not stock_picking:
#   act = 'E'
#   res = [
#       '',
#       '',
#       'VIN: {0}, 没有查到任务'.format(vin_code),
#   ]
#   val = True
  
# else:
  
#   # terminal.update_tmp_values({'vin_code': vin_code})
  
  
#   # 任务id/name
#   stock_picking_id = stock_picking.id
#   stock_picking_name = stock_picking.name
#   from_location_name = stock_picking.location_id.display_name
#   to_location_name = stock_picking.location_dest_id.display_name
  
  
#   act = 'M'
  
#   res = [
#       ('|', '任务')
#   ]
  
#   tml = {'task_id': stock_picking_id, 'state_flag': 'T'}
#   data.append(tml)
  
#   response = api._done_picking(data)
  
#   result = '失败'
#   if response.state == 'done':
#     result = '成功'
  
#     res.append('VIN码: {0}'.format(vin_code))
#     res.append('操作: {0}'.format(terminal.get_tmp_value('picking_type_name', False)))
#     res.append('任务编号: {0}'.format( stock_picking_name))
#     res.append('从: {0}'.format( from_location_name))
#     res.append('至: {0}'.format( to_location_name))
#     res.append('')
#     res.append('')
#     res.append('提交结果:{0}'.format(result))
#   else:
#     act = 'E'
#     res = [
#       '',
#       '',
#     ]
#     val = True
    
#     res.append('提交结果:{0}'.format(result))
