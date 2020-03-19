
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

#保存步骤名称
if not terminal.get_tmp_value('picking_type_name', False):
  terminal.update_tmp_values({'picking_type_name': message})

# 运力来源不用在手持端操作，三级调度计划应在服务端完成
# 如果服务端没做计划，手持端扫描VIN码后，将创建计划。如果服务端有计划，手持端的扫描将仅仅是比对这个计划
lst = [
        ('license_plate', '车辆'),
        # ('transfer_way', '运力来源'),
        ('vin_scan', 'VIN码扫描'),
        ('submit', '提交'),
      ]

act = 'L'

res = [
    ('|', _('公路运输'))
]

for line in lst: 
  res.append((line[0], line[1]))