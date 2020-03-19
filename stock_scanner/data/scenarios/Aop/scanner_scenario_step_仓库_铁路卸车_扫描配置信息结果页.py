
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

scanner_step = message

if scanner_step == 'once':
    scanner_step_cn = '只扫描一次'
else:
    scanner_step_cn = '多次扫描'


terminal.update_tmp_values({
  'scanner_step': scanner_step,
  'scanner_step_cn': scanner_step_cn,
})

act = 'M'
res = [
    '您填写的信息是:',
    '',
    
]

res.append(scanner_step_cn)
