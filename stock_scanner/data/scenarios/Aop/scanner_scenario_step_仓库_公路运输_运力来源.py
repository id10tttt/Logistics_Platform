
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

lst = [
	'自有大板',
	'外协大板',
	'现金大板',
	'人工地跑',
	'自有2位板',
	'自有4位板',
	'自有6位板',
	'自有10位板',
	'自有12位板',
	'自有新型4位板',
	'自有1位板',
	'自有7位板'
]

act = 'L'

res = [
    ('|', _('运力来源'))
]

for line in lst: 
  res.append(line)