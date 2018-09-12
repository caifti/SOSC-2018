### [back](/)

## What is Spark?

Apache Spark is an open-source powerful distributed querying and processing engine.

Apache Spark allows the user to read, transform, and aggregate data and its APIs are accessible
in Java, Scala, Python, R and SQL.

Apache Spark exposes a host of libraries familiar to data analysts.

Further more, it can easily run locally on a laptop, deployed in
standalone mode, over YARN, or Apache Mesos - either on your local cluster or
in the cloud.

![Spark Ecosystem](/img/spark_ecosystem.png)

## How it works

Any Spark application spins off a single driver process (that can contain multiple
jobs) on the master node that then directs executor processes (that contain multiple
tasks) distributed to a number of worker nodes.

![Spark Execution](/img/spark_execution.png)

## Spark on Mesos

Apache Spark can use as manager [Apache Mesos](http://mesos.apache.org/).

The advantages of deploying Spark with Mesos include:

* dynamic partitioning between Spark and other frameworks
* scalable partitioning between multiple instances of Spark

### How it works

The Mesos master replaces the Spark master as the cluster manager, the workflow of the application doesn't have changed.

![Spark on Mesos](/img/cluster-overview.png)