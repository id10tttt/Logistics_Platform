
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

lst = [
	'渝ZJ1234',
	'渝AM3765',
	
]

act = 'L'

res = [
    ('|', _('车牌'))
]

for line in lst: 
  res.append(line)