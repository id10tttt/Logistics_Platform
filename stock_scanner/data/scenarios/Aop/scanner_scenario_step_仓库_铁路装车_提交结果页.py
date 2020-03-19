
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



params = terminal.get_tmp_value('params', False)

if params:
  # 
  for key in sorted(params.keys()):
      val = params.get(key, '')
      res.append("{0},{1},{2},{3}".format(key, val['product_name'] ,val['train_manage_line_name'], val['layer_option_cn']))
      
      # 准备提交给接口的数据
      tml = {'batch_id': '', 'task_id': '', 'state_flag': 'T'}
      
      tml['batch_id'] = val.get('batch_id', False)
      tml['task_id'] = val.get('stock_picking_id', False)
      data.append(tml)
      
  response = api._done_picking(data)
  
  
  
  result = '失败'
  if all(x.state == 'done' for x in response):
    result = '成功'
    res.append('')
    res.append('')
    res.append('提交结果:{0}'.format(result))
    
    # 如果装车、加固只扫一次，那么还需要找出加固任务并提交给接口去完成它
    scanner_step = terminal.get_tmp_value('scanner_step', 'once')
    jiagu_params = terminal.get_tmp_value('jiagu_params', False)
    
    if scanner_step == 'once' and jiagu_params:
      data = []
      
      for item in jiagu_params:
        tml = {'task_id': item, 'state_flag': 'T'}
        data.append(tml)
      
      response = api._done_picking(data)
      if any(x.state != 'done' for x in response):
        result = '失败'
        act = 'E'
        res = [
            '',
            '',
        ]
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
  



