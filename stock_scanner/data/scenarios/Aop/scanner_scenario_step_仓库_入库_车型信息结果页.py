
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

id = message

domain = [('id', '=', id)]
product_id = env['product.product'].sudo().search(domain)
product_name = product_id.name
product_model = product_id.default_code

terminal.update_tmp_values({
  'product_name': product_name,
  'product_model': product_model,
})

act = 'M'
res = [
    '您填写的信息是:',
    '',
    
]

res.append("{0}={1}".format('品牌', terminal.get_tmp_value('brand_name')))
res.append("{0}={1}".format('车型', terminal.get_tmp_value('product_name')))

# for key in sorted(terminal.tmp_values.keys()):
#     val = terminal.get_tmp_value(key)
#     res.append("{0}={1}".format(key, val))
