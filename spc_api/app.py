import sys
import xmlrpclib

URL = 'http://localhost:8069'
DB = 'spc'
USERNAME = 'admin'
PASSWORD = 'x'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(URL))
UID = common.authenticate(DB, USERNAME, PASSWORD, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(URL))

def res_users(employee_id):
    ids = models.execute_kw(DB, UID, PASSWORD,
        'hr.employee', 'search', [[['id', '=', employee_id]]])
    [record] = models.execute_kw(DB, UID, PASSWORD,
        'hr.employee', 'read', [ids])
    print [record].first_name_en

res_users(sys.argv[1])
