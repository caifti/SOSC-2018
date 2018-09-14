### [◀](/SOSC-2018)

## Cluster schema

Our cluster will have different components with specific tasks. For the basic functionalities we need a master node (machine) that can orchestrate and coordinate our resources. Plus, we need some worker nodes (or slaves), that will do the dirty work. Finally, we need a load balancer to manage connection from the external world. In fact, we will not have access to the whole cluster, but only on few components to control the service and use it.

Such schema is visible in the following picture:

![Spark Ecosystem](/img/cluster_schema.png)

As you can see we need some layers to manage in a transparent way the cluster and a little support from the [Docker](https://www.docker.com/) technology.

The [Apache Mesos](http://mesos.apache.org/) layer allows us to abstract the resources and assign to specific target. This manager can be personalized and exeded too.

On top of this we will use the [Apache Marathon](https://mesosphere.github.io/marathon/) framework to manage containers with Mesos.

This kind of organization is useful because we use the [container](https://www.docker.com/resources/what-container) paradigm to deploy our services. This recent type of software management is very commond today and allow the software to be more independent from the hardware management.


## Spark Cluster Tosca template

The tosca template will have the components described above, you can find the `yaml` file [here](https://github.com/DODAS-TS/SOSC-2018/blob/master/templates/hands-on-2/spark-cluster.yaml).

In details we create some compute nodes that are simple machines with and OS:

```yaml
mesos_master_server:
    type: tosca.nodes.indigo.Compute
    [...]

mesos_slave_server:
    type: tosca.nodes.indigo.Compute
    [...]

mesos_lb_server:
    type: tosca.nodes.indigo.Compute
    [...]
```

The master server and the load balancer server will also have a public IP to be reached from outside the infrastructure.

We have to install the Mesos framework to finally use our service, and you can find this part in the following sections:

```yaml
mesos_master:
    type: tosca.nodes.indigo.MesosMaster
    [...]

mesos_slave:
    type: tosca.nodes.indigo.MesosSlave
    [...]

mesos_load_balancer:
    type: tosca.nodes.indigo.MesosLoadBalancer
    [...]
```

All the roles now are more specific and they will prepare the nodes to accomplish their duty.

After this preparation we can inject our service with the proper receipe:

```yaml
spark_application:
    type: tosca.nodes.indigo.SparkMesos
    [...]
```

This last part involves also the Personalization from the final user, that can personalize the service despite the resource manager used.

## Spark Ansible role

You can find the current Ansible role for Spark [here](https://github.com/indigo-dc/ansible-role-spark-mesos/tree/update_spark).

If you take a look on the task file you will see that is basically a launcher of Marathon application, so, it will deploy our personalized Docker images with the Spark environment.

```yaml
[...]

- name: "[Spark-Mesos] deploy app container on Marathon"
  run_once: true
  uri:
     url: "{{marathon_protocol}}://marathon.service.consul:{{marathon_port}}/v2/apps"
     user: "{{marathon_username}}"
     password: "{{marathon_password}}"
     validate_certs: "no"
     method: POST
     HEADER_Content-Type: "application/json"
     body: "{{ lookup('template', 'templates/{{app_name}}.json') }}"
     body_format: json
     status_code: 201
  register: post_result
  when: get_result.status == 404
  tags:
    - spark

[...]
```

## Spark Docker image