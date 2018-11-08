#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Chris Houseknecht <@chouseknecht>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

from ansible.module_utils.k8s.common import AUTH_ARG_SPEC, COMMON_ARG_SPEC, KubernetesAnsibleModule

try:
    from openshift.dynamic.exceptions import DynamicApiError
except ImportError as exc:
    class KubernetesException(Exception):
        pass


__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''

module: k8s_status

short_description: Update the status for a Kubernetes API resource

version_added: "2.7"

author:
    - "Fabian von Feilitzsch (@fabianvf)"

description:
  - Sets the status field on a Kubernetes API resource. Only should be used if you are using Ansible to
    implement a controller for the resource being modified.

options:
  api_version:
    description:
    - Use to specify the API version. Use to create, delete, or discover an object without providing a full
      resource definition. Use in conjunction with I(kind), I(name), and I(namespace) to identify a
      specific object. If I(resource definition) is provided, the I(apiVersion) from the I(resource_definition)
      will override this option.
    default: v1
    aliases:
    - api
    - version
  kind:
    description:
    - Use to specify an object model. Use to create, delete, or discover an object without providing a full
      resource definition. Use in conjunction with I(api_version), I(name), and I(namespace) to identify a
      specific object. If I(resource definition) is provided, the I(kind) from the I(resource_definition)
      will override this option.
  name:
    description:
    - Use to specify an object name. Use to create, delete, or discover an object without providing a full
      resource definition. Use in conjunction with I(api_version), I(kind) and I(namespace) to identify a
      specific object. If I(resource definition) is provided, the I(metadata.name) value from the
      I(resource_definition) will override this option.
  namespace:
    description:
    - Use to specify an object namespace. Useful when creating, deleting, or discovering an object without
      providing a full resource definition. Use in conjunction with I(api_version), I(kind), and I(name)
      to identify a specfic object. If I(resource definition) is provided, the I(metadata.namespace) value
      from the I(resource_definition) will override this option.
  host:
    description:
    - Provide a URL for accessing the API. Can also be specified via K8S_AUTH_HOST environment variable.
  api_key:
    description:
    - Token used to authenticate with the API. Can also be specified via K8S_AUTH_API_KEY environment variable.
  kubeconfig:
    description:
    - Path to an existing Kubernetes config file. If not provided, and no other connection
      options are provided, the openshift client will attempt to load the default
      configuration file from I(~/.kube/config.json). Can also be specified via K8S_AUTH_KUBECONFIG environment
      variable.
  context:
    description:
    - The name of a context found in the config file. Can also be specified via K8S_AUTH_CONTEXT environment variable.
  username:
    description:
    - Provide a username for authenticating with the API. Can also be specified via K8S_AUTH_USERNAME environment
      variable.
  password:
    description:
    - Provide a password for authenticating with the API. Can also be specified via K8S_AUTH_PASSWORD environment
      variable.
  cert_file:
    description:
    - Path to a certificate used to authenticate with the API. Can also be specified via K8S_AUTH_CERT_FILE environment
      variable.
  key_file:
    description:
    - Path to a key file used to authenticate with the API. Can also be specified via K8S_AUTH_KEY_FILE environment
      variable.
  ssl_ca_cert:
    description:
    - Path to a CA certificate used to authenticate with the API. Can also be specified via K8S_AUTH_SSL_CA_CERT
      environment variable.
  verify_ssl:
    description:
    - "Whether or not to verify the API server's SSL certificates. Can also be specified via K8S_AUTH_VERIFY_SSL
      environment variable."
    type: bool

requirements:
    - "python >= 2.7"
    - "openshift >= 0.8.1"
    - "PyYAML >= 3.11"
'''

EXAMPLES = '''
TODO
'''

RETURN = '''
result:
  description:
  - If a change was made, will return the patched object, otherwise returns the existing object.
  returned: success
  type: complex
  contains:
     api_version:
       description: The versioned schema of this representation of an object.
       returned: success
       type: str
     kind:
       description: Represents the REST resource this object represents.
       returned: success
       type: str
     metadata:
       description: Standard object metadata. Includes name, namespace, annotations, labels, etc.
       returned: success
       type: complex
     spec:
       description: Specific attributes of the object. Will vary based on the I(api_version) and I(kind).
       returned: success
       type: complex
     status:
       description: Current status details for the object.
       returned: success
       type: complex
'''


def condition_array(conditions):

    def validate_condition(condition):
        # TODO
        return True

    for condition in conditions:
        validate_condition(condition)
    return conditions


STATUS_ARG_SPEC = {
    'status': {'type': 'dict', 'required': False},
    'conditions': {'type': condition_array, 'required': False}
}


def main():
    KubernetesAnsibleStatusModule().execute_module()


class KubernetesAnsibleStatusModule(KubernetesAnsibleModule):

    def __init__(self, *args, **kwargs):
        KubernetesAnsibleModule.__init__(
            self, *args,
            supports_check_mode=True,
            **kwargs
        )
        self.kind = self.params.get('kind')
        self.api_version = self.params.get('api_version')
        self.name = self.params.get('name')
        self.namespace = self.params.get('namespace')

        self.status = self.params.get('status')
        self.conditions = self.params.get('conditions')

        # TODO: Do we want to explicitly fail if conditions is set in the status blob?
        if self.conditions:
            self.status['conditions'] = self.conditions

    def execute_module(self):
        self.client = self.get_api_client()

        return_attributes = dict(changed=False, result=dict())

        resource = self.find_resource(self.kind, self.api_version, fail=True)
        if 'status' not in resource.subresources:
            self.fail_json(msg='Resource {}.{} does not support the status subresource'.format(resource.api_version, resource.kind))

        try:
            existing = resource.get(name=name, namespace=namespace).to_dict()
            return_attributes['result'] = existing
        except DynamicApiError as exc:
            self.fail_json(msg='Failed to retrieve requested object: {0}'.format(exc),
                           error=exc.summary())

        if existing['status'] == status:
            self.exit_json(**return_attributes)

        body = {
            'apiVersion': resource.api_version,
            'kind': resource.kind,
            'metadata': {
                'name': self.name,
                'namespace': self.namespace,
            },
            'status': self.status
        }

        try:
            return_attributes['result'] = resource.status.patch(body=body, content_type='application/merge-patch+json')
        except DynamicApiError as exc:
            self.fail_json(msg='Failed to patch status: {}'.format(exc), error=exc.summary())

        self.exit_json(**return_attributes)

    @property
    def argspec(self):
        args = copy.deepcopy(COMMON_ARG_SPEC)
        args.pop('state')
        args.pop('resource_definition')
        args.pop('src')
        args.update(AUTH_ARG_SPEC)
        args.update(STATUS_ARG_SPEC)
        return args


if __name__ == '__main__':
    main()
