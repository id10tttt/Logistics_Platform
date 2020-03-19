
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

act = 'L'

layer_option = [ ('once', '只扫描一次'),
                ('multi', '多次扫描')
          ]


res = [
    ('|','解固/卸车步骤扫描配置'),
    
]

for item in layer_option:
    res.append((item[0], item[1]))
    