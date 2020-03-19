
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

from odoo.addons.aop_interface.controllers.api_interface import ApiInterface

api = ApiInterface()

vin_code = message

# 显示任务列表,测试时不加入任务状态的筛选
# 库间移库步骤不判断任务是否属于当前仓库
stock_picking = env['stock.picking'].sudo().search([
                        ('vin_id.name', '=', vin_code),
                        ('picking_type_id.name', '=', terminal.get_tmp_value('picking_type_name', False)),
                        # ('picking_type_id.warehouse_id.name', '=', terminal.get_tmp_value('warehouse_name', False)),
                        ('state', '=', 'assigned')
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
  
  terminal.update_tmp_values({'vin_code': vin_code})
  
  data = []
  
  # 任务id/name
  stock_picking_id = stock_picking.id
  stock_picking_name = stock_picking.name
  from_location_name = stock_picking.location_id.display_name
  to_location_name = stock_picking.location_dest_id.display_name
  
  tml = {'task_id': stock_picking_id, 'state_flag': 'T'}
  data.append(tml)
  
  response = api._done_picking(data)
  
  result = '失败'
  if response.state == 'done':
  
    result = '成功'
    
    act = 'M'
    
    res = [
        ('|', '任务')
    ]
    
    res.append('VIN码: {0}'.format(terminal.get_tmp_value('vin_code', False)))
    res.append('操作: {0}'.format(terminal.get_tmp_value('picking_type_name', False)))
    res.append('任务编号: {0}'.format( stock_picking_name))
    res.append('从: {0}'.format( from_location_name))
    res.append('至: {0}'.format( to_location_name))
    res.append('')
    res.append('')
    res.append('提交结果:{0}'.format(result))
  else:
    act = 'E'
    res = [
        '',
        '',
    ]
    val = True
    
    res.append('提交结果:{0}'.format(result))
