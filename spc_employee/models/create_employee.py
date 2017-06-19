import sys
import requests
import json

def create_employee(employeeId, firstName, lastName, domain, department_name):
    print 'API create_employee', employeeId, firstName, lastName, domain, department_name
    url = 'http://10.109.10.52:8888/activiti-rest/service/runtime/process-instances'
    headers = {"Content-Type": "application/json",
               "Authorization": "Basic a2VybWl0Omtlcm1pdA=="}
    data = {
        "processDefinitionKey": "onBoardingProcess",
        "variables": [
            {
                "name": "Employee ID",
                "value": employeeId
            },
            {
                "name": "Employee Firstname",
                "value": firstName 
            },
            {
                "name": "Employee Lastname",
                "value": lastName
            },
            {
                "name": "Domain",
                "value": domain
            },
            {
                "name": "Department",
                "value": department_name
            }
        ]
    }
    response = requests.post(url, headers=headers, json=json.dump(data, separators=(',', ':')))

create_employee(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])