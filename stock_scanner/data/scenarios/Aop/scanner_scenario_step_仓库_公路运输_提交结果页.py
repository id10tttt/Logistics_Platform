
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 实际操作在这




act = 'M'
res = [
    '提交的信息是:',
    '',
]



params = terminal.get_tmp_value('trafficway_params', False)

if params:
  # 
  for key in sorted(params.keys()):
      val = params.get(key, '')
      res.append("{0},{1},{2}".format(key, val['license_plate'], val['delivery_to_partner_name']))
    
  res.append('')
  res.append('')
  res.append('提交结果:{0}'.format('成功'))
  
  
val = terminal.get_tmp_value('warehouse_id', False)

# 操作后清除vin_code这些临时数据
terminal.clean_tmp_values(['trafficway_params', 'vin_code'])

