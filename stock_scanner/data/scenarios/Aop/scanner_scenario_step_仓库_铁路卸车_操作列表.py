
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

#保存步骤名称
if not terminal.get_tmp_value('picking_type_name', False):
  terminal.update_tmp_values({'picking_type_name': message})

act = 'L'

# 卸车扫描配置,一步扫描完成卸车解固或者卸车和解固分开扫描,默认值是一步完成
scanner_step = terminal.get_tmp_value('scanner_step', 'once')
scanner_step_cn = terminal.get_tmp_value('scanner_step_cn', '只扫描一次')


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

if vin_scan_count>0:
  lst.append(('vin_scan', 'VIN码扫描' + '({0})'.format(vin_scan_count))) 
else:
  lst.append(('vin_scan', 'VIN码扫描'))
  
  
lst.append(('submit', '提交'))


for item in lst:
    res.append((item[0], item[1]))
    