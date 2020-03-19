
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

#清空tmp_values
terminal.clean_tmp_values([x for x in terminal.tmp_values.keys()])

# user = env['res.users'].search([('id','=', uid)])
user = env.user
# lst = env['stock.warehouse'].search([('id','in',user.allow_base_warehouse_ids.mapped('warehouse_ids').ids)  if user.allow_base_warehouse_ids else (1, '=', 1) ])

lst = env['stock.warehouse'].search([])

act = 'L'

res = [
    ('|', '仓库列表({0})'.format(user.name))
]

for line in lst: 
  res.append((line.id, line.name))
  
res.append(('exit', '退出'))
