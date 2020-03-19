
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

brand_name = message
terminal.update_tmp_values({'brand_name': brand_name})

domain = [('brand_id.name', '=', brand_name)]
lst = env['product.product'].sudo().search(domain)

act = 'L'

res = [
    ('|', '车型')
]

for line in lst: 
  res.append((line.id, '{0}/{1}'.format(line.name, line.default_code)))
