# flake8: noqa
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# 清空tmp_values
terminal.clean_tmp_values([x for x in terminal.tmp_values.keys()])

# user = env['res.users'].search([('id','=', uid)])
user = env.user

warehouse_ids = env['stock.warehouse'].sudo().search([])

res = [
    ('|', 'Warehouse({0})'.format(user.name))
]

act = 'L'

for warehouse_id in warehouse_ids:
    res.append((warehouse_id.id, warehouse_id.name))

res.append(('exit', 'Exit'))
