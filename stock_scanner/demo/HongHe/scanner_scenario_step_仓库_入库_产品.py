
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

domain = [('type', '=', 'product')]
lst = env['product.product'].sudo().search(domain)

act = 'L'

res = [
    ('|', '产品')
]

for line in lst: 
  res.append((line.id, '{0}/{1}'.format(line.name, line.default_code)))

