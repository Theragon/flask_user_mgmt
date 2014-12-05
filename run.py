#!/home/logi/virtualenvs/flaskenv/bin/python

from app import app
#from OpenSSL import SSL
'''
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.cert')
app.run('0.0.0.0', debug=True, port=443, ssl_context=context)
'''
app.run(debug=True)