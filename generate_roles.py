import copy
import yaml
from permissions import (
    get_all_automation_document_names,
    generate_permissions_from_automation_document,
)


cfn_template = yaml.load(open('./cfn-template.yaml'), Loader=yaml.BaseLoader)
role_template = yaml.load(open('./role-template.yaml'), Loader=yaml.BaseLoader)


def generate_role_from_automation_document_name(document_name):
    permissions = generate_permissions_from_automation_document(document_name)

    if len(permissions) == 0:
        return

    role = copy.deepcopy(role_template)
    role['Properties']['RoleName'] = 'SSMAutomation' + document_name.replace('AWS-', '') + 'Role'
    role['Properties']['Description'] = 'SSM Automation Role for Document ' + document_name
    role['Properties']['Policies'][0]['PolicyName'] = document_name
    role['Properties']['Policies'][0]['PolicyDocument']['Statement'] = [
        {'Effect': 'Allow', 'Action': permission, 'Resource': '*'}
        for permission in permissions
    ]

    return role


def generate_cfn_template():
    automation_document_names = get_all_automation_document_names()

    stack = copy.deepcopy(cfn_template)

    for automation_document_name in automation_document_names:

        name = automation_document_name.replace('AWS-', '')

        role_obj = generate_role_from_automation_document_name(automation_document_name)

        if role_obj is not None:
            stack['Resources'][name + 'Role'] = role_obj

    return yaml.dump(stack)


if __name__ == '__main__':
    template = generate_cfn_template()
    print(template)
