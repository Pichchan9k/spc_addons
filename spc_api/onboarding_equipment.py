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

def start_onboarding_equipment(employeeId):
    print 'start_onboarding_equipment'
    # models.execute_kw(DB, uid, PASSWORD,
    #     'hr.employee', 'equipment_from_onboarding',
    # ['', employeeId], {})

    # print 'start_onboarding_equipment'
    # print employeeId
    # equipment_ids = models.execute_kw(DB, uid, PASSWORD, 'hr.employee', 'read',
    #     [int(employeeId)], {'fields': ['equipment_onboarding_id']})
    # print equipment_ids

    # equipment_arr = []
    # print equipment_arr
    # equipment_ids = models.execute_kw(DB, uid, PASSWORD, 'hr.employee', 'read', [383], {'fields': ['equipment_onboarding_id']})
    # print equipment_ids
    # equipment_ids = equipment_ids[0]['equipment_onboarding_id']
    # print equipment_ids
    # for equipment_id in equipment_ids:
    #     equipment_name = models.execute_kw(DB, uid, PASSWORD, 'maintenance.equipment', 'read', [equipment_id], {'fields': ['name']})
    #     equipment_name = equipment_name[0]['name']
    #     # print equipment_name
    #     equipment_arr.append(equipment_name)
    print ['EmployeeCard', 'Notebook']

start_onboarding_equipment(sys.argv[1])
