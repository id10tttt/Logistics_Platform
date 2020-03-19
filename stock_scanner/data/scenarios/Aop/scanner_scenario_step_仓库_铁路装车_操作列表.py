
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

#保存步骤名称
if not terminal.get_tmp_value('picking_type_name', False):
  terminal.update_tmp_values({'picking_type_name': message})

act = 'L'

# 装车扫描配置,一步扫描完成装车加固或者装车和加固分开扫描,默认值是一步完成
scanner_step = terminal.get_tmp_value('scanner_step', 'once')
scanner_step_cn = terminal.get_tmp_value('scanner_step_cn', '只扫描一次')

# 车厢号
train_manage_line_name = terminal.get_tmp_value('train_manage_line_name', False)

# 上/下层
layer_option_cn = terminal.get_tmp_value('layer_option_cn', False)

# vin扫描数量
vin_scan_count = terminal.get_tmp_value('vin_scan_count', 0)

res = [
    ('|','操作列表'),
    
]

lst = []

if scanner_step == 'once':
  lst.append(('scanner_step', '扫描配置' + '({0})'.format(scanner_step_cn)))
else:
  lst.append(('scanner_step', '扫描配置' + '({0})'.format(scanner_step_cn)))

if train_manage_line_name:
  lst.append(('train', '车厢' + '({0})'.format(train_manage_line_name)))
else:
  lst.append(('train', '车厢'))
  
  
if layer_option_cn:
  lst.append(('layer', '上/下层' + '({0})'.format(layer_option_cn)))
else:
  lst.append(('layer', '上/下层'))
  
  
if vin_scan_count>0:
  lst.append(('vin_scan', 'VIN码扫描' + '({0})'.format(vin_scan_count))) 
else:
  lst.append(('vin_scan', 'VIN码扫描'))
  
  
lst.append(('submit', '提交'))


# lst = [
#       ('train', '车厢'),
#       ('layer', '上/下层'),
#       ('vin_scan', 'VIN码扫描'),
#       ('submit', '提交'),
#     ]

for item in lst:
    res.append((item[0], item[1]))
    