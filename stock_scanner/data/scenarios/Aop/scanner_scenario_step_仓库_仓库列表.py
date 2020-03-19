'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 清空tmp_values
terminal.clean_tmp_values([x for x in terminal.tmp_values.keys()])

# user = env['res.users'].search([('id','=', uid)])
user = env.user
# lst = env['stock.warehouse'].search([('id','in',user.allow_base_warehouse_ids.mapped('warehouse_ids').ids)  if user.allow_base_warehouse_ids else (1, '=', 1) ])

# 除了管理员外，其他用户不允许列出所有仓库
lst = []

if user._is_admin():
    lst = env['stock.warehouse'].search([])
else:
    if user.allow_base_warehouse_ids if hasattr(user, 'allow_base_warehouse_ids') else False:
        lst = env['stock.warehouse'].sudo().search([('id', 'in', user.allow_base_warehouse_ids.mapped('warehouse_ids').ids)])
    else:
        lst = env['stock.warehouse'].sudo().search([])

act = 'L'

res = [
    ('|', '仓库列表({0})'.format(user.name))
]

for line in lst:
    res.append((line.id, line.name))

res.append(('exit', '退出'))
