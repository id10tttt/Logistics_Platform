
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

from odoo.addons.aop_interface.controllers.api_interface import ApiInterface

api = ApiInterface()



data = []

vin_code = terminal.get_tmp_value('vin_code', False)
picking_type_name = terminal.get_tmp_value('picking_type_name', False)
warehouse_code = terminal.get_tmp_value('warehouse_code', False)
warehouse_name = terminal.get_tmp_value('warehouse_name', False)
brand_name = terminal.get_tmp_value('brand_name', False)
product_name = terminal.get_tmp_value('product_name', False)
from_location_name = terminal.get_tmp_value('from_location_name', False)

# lines = [
#     "{0}={1}".format('仓库', warehouse_name),
#     "{0}={1}".format('操作', picking_type_name),
#     "{0}={1}".format('VIN码', vin_code),
#     "{0}={1}".format('品牌', brand_name),
#     "{0}={1}".format('车型', product_name),
#     "{0}={1}".format('车辆来自', from_location_name),
#   ]

# for line in lines:
#     res.append(line)





act = 'M'
res = [
    '|提交结果页:',
    '',
    '提交的信息是:',
    '',
    
]
    
params = terminal.get_tmp_value('into_warehouse_params', False)

if params:
  # 
  for key in sorted(params.keys()):
      val = params.get(key, '')
      res.append("{0},{1},{2}".format(key, val.get('brand_name', ''), val.get('product_name', '')))
      
      # 准备提交给接口的数据
      tml = {'brand_model_name': '', 'product_color': '', 'product_model': '', 'state_flag': 'T',
           'vin': '', 'warehouse_code': warehouse_code, 'warehouse_name': warehouse_name}
      
      tml['vin'] = key
      tml['brand_model_name'] = val.get('from_warehouse_code', False)
      tml['product_model'] = val.get('product_model', False)
      
      # 如果有'入库'步骤的任务，需要把task_id传到接口。仅仅接车操作，task_id不会有值
      task_id = val.get('task_id', False)
      if task_id:
        tml['task_id'] = task_id
      
      data.append(tml)

res.append('')
res.append('')

# 打印接口数据
# res.append(str(data))
response = api._done_picking(data)
# 打印返回数据
# res.append(str(response))

val = terminal.get_tmp_value('warehouse_id', False)



# terminal.clean_tmp_values(['vin_code', 'product_name', 'brand_name', 'from_location_id', 'from_location_name', 'task_id', 'into_warehouse_params'])

result = '失败'
if all(x.state == 'done' for x in response):
  result = '成功'
  res.append('提交结果:{0}'.format(result))
  
else:
  act = 'E'
  res = [
      '',
      '',
  ]
  val = True
  
  res.append('提交结果:{0}'.format(result))
  



