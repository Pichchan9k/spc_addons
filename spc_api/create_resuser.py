import sys
import xmlrpclib

# URL = 'http://10.109.10.52:8069'
# DB = 'spc-employee'

URL = 'http://localhost:8069'
DB = 'spc_employee'

USERNAME = 'admin'
PASSWORD = 'x'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(URL))
uid = common.authenticate(DB, USERNAME, PASSWORD, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(URL))

def create_user(employeeId, email, password):
    print '----------create_user'
    employee = models.execute_kw(DB, uid, PASSWORD,
                      'hr.employee', 'search',
                      [[['id', '=', employeeId]]])
    print 'employee', employee

    name = models.execute_kw(DB, uid, PASSWORD, 'hr.employee', 'read',
        [employee], {'fields': ['name']})
    print 'name', name

    user_id = models.execute_kw(DB, uid, PASSWORD, 'hr.employee', 'read',
        [143], {'fields': ['user_id']})
    print 'user_id', user_id

    res_user = models.execute_kw(DB, uid, PASSWORD, 'res.users', 'create', [{
        'name': name[0]['name'], 'login': email, 'password': password}])
    print 'res_user id:', res_user

    res_partner = models.execute_kw(DB, uid, PASSWORD, 'res.users', 'read',
        [res_user], {'fields': ['partner_id']})

    res_partner_id = res_partner[0]['partner_id'][0]
    print 'res_partner id:', res_partner_id

    models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'write', [[res_partner_id], {
        'email': email
    }])

    models.execute_kw(DB, uid, PASSWORD, 'hr.employee', 'write', [employee, {
        'user_id': res_user,
        'user': email[:email.index('@')],
        'email': email[email.index('@'):]
    }])

create_user(sys.argv[1], sys.argv[2], sys.argv[3])
