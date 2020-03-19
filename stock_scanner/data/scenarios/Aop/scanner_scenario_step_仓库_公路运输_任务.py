
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

vin_code = message

# 显示任务列表,测试时不加入任务状态的筛选
stock_picking = env['stock.picking'].sudo().search([
                        ('vin_id.name', '=', vin_code),
                        ('picking_type_id.name', '=', terminal.get_tmp_value('picking_type_name', False)),
                        ('picking_type_id.warehouse_id.name', '=', terminal.get_tmp_value('warehouse_name', False)),
                        # ('state', '=', 'assigned')
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
  
  params = terminal.get_tmp_value('trafficway_params', False)
  
  if not params:
    params = dict()

  # 任务id/name
  stock_picking_id = stock_picking.id
  stock_picking_name = stock_picking.name
  
  # 车辆信息
  license_plate = terminal.get_tmp_value('license_plate', False)
  
  # 运力来源
  transfer_way = terminal.get_tmp_value('transfer_way', False)
  
  params.update({vin_code: {'license_plate': license_plate,
                            'transfer_way': transfer_way,
                            'delivery_to_partner_name': stock_picking.delivery_to_partner_id.name,
                            'stock_picking_id': stock_picking_id,
                            'stock_picking_name': stock_picking_name,
                            
  }})
  terminal.update_tmp_values({'trafficway_params': params})
  
  # terminal.clean_tmp_values(['license_plate', 'transfer_way', 'vin_code'])
  
  act = 'M'
  
  res = [
      ('|', '任务')
  ]
  
  res.append('VIN码: {0}'.format(terminal.get_tmp_value('vin_code', False)))
  res.append('')  
  res.append('{0}-{1}'.format( terminal.get_tmp_value('warehouse_name', False), stock_picking.delivery_to_partner_id.name))
