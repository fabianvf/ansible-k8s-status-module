
## k8s_status

#### Update the status for a Kubernetes API resource

Author: Fabian von Feilitzsch (@fabianvf)

Version added: 2.7



---
### Table of Contents

  * [Requirements](#requirements)
  * [Synopsis](#synopsis)
* [Options](#options)
* [Examples](#examples)
* [Return](#return)



---
### Requirements
* python >= 2.7
* openshift >= 0.8.1
* PyYAML >= 3.11


---


#### Synopsis
Sets the status field on a Kubernetes API resource. Only should be used if you are using Ansible to implement a controller for the resource being modified.


#### Options

| Parameter     |  aliases     | required    | default  | choices    | comments |
| ------------- |------------- |-------------| ---------|----------- |--------- |
| api_key  |  |   |  | |  Token used to authenticate with the API. Can also be specified via K8S_AUTH_API_KEY environment variable.  |
| api_version  |  api, version  |   yes  |  | |  Use to specify the API version. Use in conjunction with I(kind), I(name), and I(namespace) to identify a specific object.  |
| cert_file  |  |   |  | |  Path to a certificate used to authenticate with the API. Can also be specified via K8S_AUTH_CERT_FILE environment variable.  |
| conditions  |  |   |  | |  A list of condition objects that will be set on the status.conditions field of the specified resource.  Unless I(force) is C(true) the specified conditions will be merged with the conditions already set on the status field of the specified resource.  Each element in the list will be validated according to the conventions specified in the [Kubernetes API conventions document](https://github.com/kubernetes/community/blob/master/contributors/devel/api-conventions.md#spec-and-status).  The fields supported for each condition are: `type` (required), `status` (required, one of "True", "False", "Unknown"), `reason` (single CamelCase word), `message`, `lastHeartbeatTime` (RFC3339 datetime string), and `lastTransitionTime` (RFC3339 datetime string).  One of I(status) or I(conditions) is required.'  |
| context  |  |   |  | |  The name of a context found in the config file. Can also be specified via K8S_AUTH_CONTEXT environment variable.  |
| force  |  |   |  False  | |  If set to C(True), the status will be set using `PUT` rather than `PATCH`, replacing the full status object.  |
| host  |  |   |  | |  Provide a URL for accessing the API. Can also be specified via K8S_AUTH_HOST environment variable.  |
| key_file  |  |   |  | |  Path to a key file used to authenticate with the API. Can also be specified via K8S_AUTH_KEY_FILE environment variable.  |
| kind  |  |   yes  |  | |  Use to specify an object model. Use in conjunction with I(api_version), I(name), and I(namespace) to identify a specific object.  |
| kubeconfig  |  |   |  | |  Path to an instance Kubernetes config file. If not provided, and no other connection options are provided, the openshift client will attempt to load the default configuration file from I(~/.kube/config.json). Can also be specified via K8S_AUTH_KUBECONFIG environment variable.  |
| name  |  |   yes  |  | |  Use to specify an object name.Use in conjunction with I(api_version), I(kind) and I(namespace) to identify a specific object.  |
| namespace  |  |   |  | |  Use to specify an object namespace.Use in conjunction with I(api_version), I(kind), and I(name) to identify a specfic object.  |
| password  |  |   |  | |  Provide a password for authenticating with the API. Can also be specified via K8S_AUTH_PASSWORD environment variable.  |
| ssl_ca_cert  |  |   |  | |  Path to a CA certificate used to authenticate with the API. Can also be specified via K8S_AUTH_SSL_CA_CERT environment variable.  |
| status  |  |   |  | |  {u'A object containing `key': u'value` pairs that will be set on the status object of the specified resource.'}  One of I(status) or I(conditions) is required.  |
| username  |  |   |  | |  Provide a username for authenticating with the API. Can also be specified via K8S_AUTH_USERNAME environment variable.  |
| verify_ssl  |  |   |  | |  Whether or not to verify the API server's SSL certificates. Can also be specified via K8S_AUTH_VERIFY_SSL environment variable.  |







#### Examples

```yaml
---

- name: Set status on TestCR Custom Resource
  k8s_status:
    api_version: apps.example.com/v1alpha1
    kind: TestCR
    name: my-test
    namespace: testing
    status:
        hello: world
    conditions:
    - type: Available
      status: "False"
      reason: FailedPing
      message: "The 'fakeservice' service did not respond to ping."
      lastTransitionTime: "{{ ansible_date_time.iso8601 }}"

```




#### Return

```yaml

result:
  description:
  - If a change was made, will return the patched object, otherwise returns the instance object.
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

```

---
