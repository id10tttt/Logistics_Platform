
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

#保存车厢号
# terminal.update_tmp_values({'train_manage_line_id': message})

act = 'L'

layer_option = [ ('upper_layer', '上层'),
                ('lower_layer', '下层')
          ]


res = [
    ('|','上/下层'),
    
]

for item in layer_option:
    res.append((item[0], item[1]))
    