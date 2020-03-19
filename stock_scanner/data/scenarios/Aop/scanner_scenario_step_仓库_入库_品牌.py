
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

domain = []
lst = env['fleet.vehicle.model.brand'].sudo().search(domain)

act = 'L'

res = [
    ('|', '品牌列表')
]

for line in lst: 
  res.append((line.name, line.name))
