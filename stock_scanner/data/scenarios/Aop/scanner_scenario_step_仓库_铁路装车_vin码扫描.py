
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

# terminal.clean_tmp_values(['vin_code'])

act = 'T'
res = [
     '|VIN码扫描({0})'.format(terminal.get_tmp_value('warehouse_name', False)),
]