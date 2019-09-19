import boto3
import json
import yaml


ssm = boto3.client('ssm')


def get_all_documents():
    documents = []
    request_params = {}

    while True:

        response = ssm.list_documents(**request_params)

        document_identifiers = response['DocumentIdentifiers']
        next_token = response.get('NextToken')

        documents += document_identifiers

        if next_token is None or next_token == '':
            break
        else:
            request_params['NextToken'] = next_token

    return documents


def get_all_automation_document_names():

    documents = get_all_documents()

    automation_documents = list(filter(
        lambda document: document['DocumentType'] == 'Automation',
        documents,
    ))

    automation_document_names = list(map(
        lambda document: document['Name'],
        automation_documents,
    ))

    return automation_document_names


def generate_permissions_from_automation_document(automation_document_name):

    def get_permission(inputs):
        service = inputs['Service']
        api = inputs['Api']

        if '_' in api:
            return service + ':' + (api.title().replace('_', ''))
        else:
            return service + ':' + api

    response = ssm.get_document(Name=automation_document_name)

    document_content = response['Content']
    document_format = response['DocumentFormat']

    if document_format == 'JSON':
        document = json.loads(document_content)
    else:
        document = yaml.load(document_content, Loader=yaml.BaseLoader)

    main_steps = document['mainSteps']

    steps_require_extra_permission = list(filter(
        lambda step: step['action'] == 'aws:executeAwsApi',
        main_steps,
    ))

    required_permissions = list(set(map(
        lambda step: get_permission(step['inputs']),
        steps_require_extra_permission,
    )))

    return required_permissions

