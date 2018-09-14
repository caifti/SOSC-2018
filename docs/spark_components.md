### [◀](/SOSC-2018)

## Cluster schema

Our cluster will have different components with specific tasks. For the basic functionalities we need a master node (machine) that can orchestrate and coordinate our resources. Plus, we need some worker nodes (or slaves), that will do the dirty work. Finally, we need a load balancer to manage connection from the external world.

Such schema is visible in the following picture:

![Spark Ecosystem](/img/cluster_schema.png)

As you can see we need some layers to manage in a transparent way the cluster and a little support from the [Docker](https://www.docker.com/) technology.

The [Apache Mesos](http://mesos.apache.org/) layer allows us to abstract the resources and assign to specific target. This manager can be personalized and exeded too.

On top of this we will use the [Apache Marathon](https://mesosphere.github.io/marathon/) framework to manage containers with Mesos.

This kind of organization is useful because we use the [container](https://www.docker.com/resources/what-container) paradigm to deploy our services. This recent type of software management is very commond today and allow the software to be more independent from the hardware management.


## Spark Cluster Tosca template

## Spark Ansible role

## Spark Docker image