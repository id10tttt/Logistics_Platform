
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

res.append("{0}={1}/{2}".format('产品', product_name, product_model))
