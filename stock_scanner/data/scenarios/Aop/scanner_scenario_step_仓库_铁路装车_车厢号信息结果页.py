
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

id = message

domain = [('id', '=', id)]
train_manage_line = env['train.manage.line'].sudo().search(domain)
train_manage_line_name = train_manage_line.name

terminal.update_tmp_values({
  'train_manage_line_id': id,
  'train_manage_line_name': train_manage_line_name,
})

act = 'M'
res = [
    '您填写的信息是:',
    '',
    
]

res.append("{0}={1}".format('车厢号', terminal.get_tmp_value('train_manage_line_name')))


# for key in sorted(terminal.tmp_values.keys()):
#     val = terminal.get_tmp_value(key)
#     res.append("{0}={1}".format(key, val))
