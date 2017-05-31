import sys
import requests

def start_on_boarding_process(employeeId, firstName, lastName):
    print employeeId
    url = 'http://10.109.10.52:8888/activiti-rest/service/runtime/process-instances'
    headers = {"Content-Type": "application/json", "Authorization": "Basic a2VybWl0Omtlcm1pdA=="}
    data = '{"processDefinitionKey":"onBoardingProcess","variables": [{"name":"Employee ID","value":' + employeeId + '}]}'
    response = requests.post(url, headers=headers, data=data)
    print response

start_on_boarding_process(sys.argv[1] sys.argv[2] sys.argv[3])
