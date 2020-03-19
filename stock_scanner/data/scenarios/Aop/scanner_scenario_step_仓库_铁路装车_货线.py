
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 因为有页面回跳到此，message不是步骤名称了，因此需要先判断步骤名称是否已存在
if not terminal.get_tmp_value('picking_type_name', False):
  terminal.update_tmp_values({'picking_type_name': message})
  
# 货线的出发位置必须是仓库的仓库位置
domain = [('from_location_id.id', '=', terminal.get_tmp_value('lot_stock_id', False))]
lst = env['train.manage'].sudo().search(domain)

act = 'L'

res = [
    ('|', _('货线'))
]

for line in lst: 
  from_location_name = line.from_location_id.name if line.from_location_id else ''
  to_location_name = line.to_location_id.name if line.to_location_id else ''
  res.append( (line.id, '{0}({1}-{2})'.format(line.name, from_location_name, to_location_name)) )
