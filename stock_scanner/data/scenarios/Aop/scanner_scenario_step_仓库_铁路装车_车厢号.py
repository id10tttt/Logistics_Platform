
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

terminal.clean_tmp_values(['train_manage_id', 'train_manage_line_id', 'layer_option', 'vin_code'])

train_manage_id = message 

#保存货线id
terminal.update_tmp_values({'train_manage_id': train_manage_id})

domain = [('train_id', '=', train_manage_id)]
lst = env['train.manage.line'].sudo().search(domain)

act = 'L'

res = [
    ('|', _('车厢号'))
]

for line in lst: 
  res.append( (line.id, line.name) )
