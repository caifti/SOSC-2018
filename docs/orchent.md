# Platform as a service

## Why a PaaS

## Example: Indigo-dc PaaS orchestrator

### Using TOSCA

### Install orchent client

The requirement here is `golang` installation that can you find [here](https://golang.org/doc/install)

```bash
go get github.com/indigo-dc/orchent
go install github.com/indigo-dc/orchent
```

### Retrieve IAM token

``` bash
./scripts/get_orchent_token.sh
```

You'll be prompted with username and password requests. Just insert the one corresponding to you Indigo-IAM account.

The output of the command should be something like

``` text
Orchent access token has to be set with the following:
 export ORCHENT_TOKEN="eyJraWQiOiJyc......."
```

Copy and paste the export command to source the correct environement along with this:

``` bash
export ORCHENT_URL=https://orchestrator.cloud.cnaf.infn.it/orchestrator
```

### Deploy webserver on the cloud: TOSCA types

Tosca types are the building blocks needed to indicate the correct procedure for the vm creation and software deployment.

During this hands on the following types are used:

``` yaml
tosca_definitions_version: tosca_simple_yaml_1_0

capability_types:

  tosca.capabilities.indigo.OperatingSystem:
    derived_from: tosca.capabilities.OperatingSystem
    properties:
      gpu_driver:
        type: boolean
        required: no
      cuda_support:
        type: boolean
        required: no
      cuda_min_version:
        type: string
        required: no
      image:
        type: string
        required: no
      credential:
        type: tosca.datatypes.Credential
        required: no

  tosca.capabilities.indigo.Scalable:
    derived_from: tosca.capabilities.Scalable
    properties:
      min_instances:
        type: integer
        default: 1
        required: no
      max_instances:
        type: integer
        default: 1
        required: no
      count:
        type: integer
        description: the number of resources
        required: no
        default: 1
      removal_list:
        type: list
        description: list of IDs of the resources to be removed
        required: no
        entry_schema:
          type: string

  tosca.capabilities.indigo.Container:
    derived_from: tosca.capabilities.Container
    properties:
      instance_type:
        type: string
        required: no
      num_gpus:
        type: integer
        required: false
      gpu_vendor:
        type: string
        required: false
      gpu_model:
        type: string
        required: false  


  tosca.capabilities.indigo.Endpoint:
    derived_from: tosca.capabilities.Endpoint
    properties:
      dns_name:
        description: The optional name to register with DNS
        type: string
        required: false
      private_ip:
        description: Flag used to specify that this endpoint will require also a private IP although it is a public one.
        type: boolean
        required: false
        default: true
    attributes:
      credential:
        type: list
        entry_schema:
          type: tosca.datatypes.Credential


artifact_types:

  tosca.artifacts.Implementation.YAML:
    derived_from: tosca.artifacts.Implementation
    description: YAML Ansible recipe artifact
    mime_type: text/yaml
    file_ext: [ yaml, yml ]

  tosca.artifacts.AnsibleGalaxy.role:
    derived_from: tosca.artifacts.Root
    description: Ansible Galaxy role to be deployed in the target node

relationship_types:

  tosca.relationships.indigo.Manages:
    derived_from: tosca.relationships.Root

node_types:

  tosca.nodes.WebServer.Apache:
    derived_from: tosca.nodes.WebServer
    interfaces:
      Standard:
        create:
          implementation:  https://raw.githubusercontent.com/DODAS-TS/SOSC-2018/master/templates/hands-on-1/ansible-role-install.yml
        start:
          implementation:  https://raw.githubusercontent.com/DODAS-TS/SOSC-2018/master/templates/hands-on-1/ansible-role-apache.yml

  tosca.nodes.indigo.Compute:
    derived_from: tosca.nodes.indigo.MonitoredCompute
    attributes:
      private_address:
        type: list
        entry_schema:
          type: string
      public_address:
        type: list
        entry_schema:
          type: string
      ctxt_log:
        type: string
    capabilities:
      scalable:
        type: tosca.capabilities.indigo.Scalable
      os:
         type: tosca.capabilities.indigo.OperatingSystem
      endpoint:
        type: tosca.capabilities.indigo.Endpoint
      host:
        type: tosca.capabilities.indigo.Container
        valid_source_types: [tosca.nodes.SoftwareComponent]

  tosca.nodes.indigo.MonitoredCompute:
    derived_from: tosca.nodes.Compute
    properties:
      # Set the current data of the zabbix server
      # but it can also specified in the TOSCA document
      zabbix_server:
        type: string
        required: no
        default: orchestrator.cloud.cnaf.infn.it
      zabbix_server_port:
        type: tosca.datatypes.network.PortDef
        required: no
        default: 10051
      zabbix_server_metadata:
        type: string
        required: no
        default: Linux      668c875e-9a39-4dc0-a710-17c41376c1e0
    artifacts:
      zabbix_agent_role:
        file: indigo-dc.zabbix-agent
        type: tosca.artifacts.AnsibleGalaxy.role
    interfaces:
      Standard:
        configure:
          implementation: https://raw.githubusercontent.com/indigo-dc/tosca-types/master/artifacts/zabbix/zabbix_agent_install.yml
          inputs:
            zabbix_server: { get_property: [ SELF, zabbix_server ] }
            zabbix_server_port: { get_property: [ SELF, zabbix_server_port ] }
            zabbix_server_metadata: { get_property: [ SELF, zabbix_server_metadata ] }
```

### Deploy command with deployment template

The deployment template makes use of the TOSCA types defined above to create and orchestrate the deployment on the cloud resources.

``` yaml
tosca_definitions_version: tosca_simple_yaml_1_0

imports:
  - indigo_custom_types:  https://raw.githubusercontent.com/DODAS-TS/SOSC-2018/master/templates/common/types.yml

description: TOSCA template for a complete CMS Site over Mesos orchestrator

topology_template:

  inputs:

    input test:
      type: string 
      default: "test"
 
  node_templates:

    create-server-vm:
      type: tosca.nodes.indigo.Compute
      capabilities:
        endpoint:
          properties:
            network_name: PUBLIC
            dns_name: apachepublic
            ports:
              apache_port:
                protocol: tcp
                source: 4880
        scalable:
          properties:
            count: 1 
        host:
          properties:
            num_cpus: 2
            mem_size: "2 GB"
        os:
          properties:
            image: "ost://cloud.recas.ba.infn.it/1113d7e8-fc5d-43b9-8d26-61906d89d479"

    apache_install:
      type: tosca.nodes.WebServer.Apache
      requirements:
        - host: create-server-vm

  outputs:
    vm_ip:
      value: { concat: [ get_attribute: [ create-server-vm, public_address, 0 ] ] }
```

To start the deployment:

``` bash
orchent depcreate  templates/hands-on-1/Handson-Part1.yaml '{}'
```

the expected output is something like:

``` text
retrieving deployment list:
  page: 0/1 [ #Elements: 1, size: 10 ]
  links:
    self [https://orchestrator.cloud.cnaf.infn.it/orchestrator/deployments?createdBy=me]


Deployment [28dc62e6-facc-4f70-bc14-4a32e1149c94]:
  status: CREATE_IN_PROGRESS
  creation time: 2018-09-05T12:47+0000
  update time: 2018-09-05T12:47+0000
  callback:
```

### Monitor the deployment process

``` bash
orchent depls --created_by=me
```

get your deployment ID then check for:

``` bash
orchent depshow <deployment ID>
```

when the deployment is completed, the output should look like: 

``` text
Deployment [28dc62e6-facc-4f70-bc14-4a32e1149c94]:
  status: CREATE_COMPLETE
  creation time: 2018-09-05T12:47+0000
  update time: 2018-09-05T13:01+0000
  callback:
  status reason:
  task: NONE
  CloudProviderName: provider-BARI
  outputs:
  {
      "vm_ip": "90.147.75.108"
  }
  links:
    self [https://orchestrator.cloud.cnaf.infn.it/orchestrator/deployments/28dc62e6-facc-4f70-bc14-4a32e1149c94]
    resources [https://orchestrator.cloud.cnaf.infn.it/orchestrator/deployments/28dc62e6-facc-4f70-bc14-4a32e1149c94/resources]
    template [https://orchestrator.cloud.cnaf.infn.it/orchestrator/deployments/28dc62e6-facc-4f70-bc14-4a32e1149c94/template]
```

TODO: login into the machine