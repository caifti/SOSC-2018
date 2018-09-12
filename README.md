# SOSC-2018

Second International PhD School on Open Science Cloud.

## Hands-on-Part1

- Ansible playbook 'Hello world':
  - Install and run Apache web server
- Tosca+PaaS intro:
  - simplified tosca type
  - deploy 1 machine with Apache web server running on it
    - depcreate
    - look at the logs
    - get ip of the vm
    - log into the VM and check the apache2 service status
    - check the webserver main page
  - homework: create a custom webserver playbook and deploy it
- Container orchestration [TBC]
  - Mesos-Marathon deploy
  - WebServer deployment as Marathon app
  - Multiple app LoadBalanced

## Hands-on-Part2

- Apache Spark
  - Introduction
  - Spark on Mesos
  - Spark Cluster Tosca template
  - Spark Ansible role
  - Deploy a small cluster
    - Access to cluster
    - Spark examples
  - Scale on bigger cluster
