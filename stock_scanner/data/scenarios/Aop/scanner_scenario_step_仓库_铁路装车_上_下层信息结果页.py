
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

layer_option = message

if layer_option == 'upper_layer':
    layer_option_cn = '上层'
else:
    layer_option_cn = '下层'


terminal.update_tmp_values({
  'layer_option': layer_option,
  'layer_option_cn': layer_option_cn,
})

act = 'M'
res = [
    '您填写的信息是:',
    '',
    
]

res.append(layer_option_cn)
