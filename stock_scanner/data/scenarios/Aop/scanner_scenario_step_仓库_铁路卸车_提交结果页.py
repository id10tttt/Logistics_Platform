
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

from odoo.addons.aop_interface.controllers.api_interface import ApiInterface

api = ApiInterface()

data = []

act = 'M'
res = [
    '提交的信息是:',
    '',
]


params = terminal.get_tmp_value('jiegu_params', False)

if params:
  # 先提交解固任务
  for item in params:
      # 准备提交给接口的数据
      tml = {'task_id': '', 'state_flag': 'T'}
      tml['task_id'] = item
      data.append(tml)
      
  response = api._done_picking(data)

params = terminal.get_tmp_value('xieche_params', False)
if params:
  # 提交卸车任务  
  
  res.append('操作: {0}'.format(terminal.get_tmp_value('picking_type_name', False)))
  
  data.clear()
  for item in list(params.values()):
    
    res.append('任务编号: {0}'.format( item.get('stock_picking_name')))
    # res.append('从: {0}'.format( item.get('from_location_name')))
    # res.append('至: {0}'.format( item.get('to_location_name')))
    # res.append('')
    
    tml = {'task_id': item.get('stock_picking_id'), 'state_flag': 'T'}
    data.append(tml)    
  
  response = api._done_picking(data)
  
  result = '失败'
  if all(x.state == 'done' for x in response):
    result = '成功'
    res.append('')
    res.append('')
    res.append('提交结果:{0}'.format(result))

  else:
    act = 'E'
    res = [
        '',
        '',
    ]
    # val = True
    
    res.append('提交结果:{0}'.format(result))  
    
val = terminal.get_tmp_value('warehouse_id', False)
  



