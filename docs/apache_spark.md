### [◀](/SOSC-2018)

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

There are two different mode with which you can spawn the Spark driver on Mesos:

- Client Mode
- Cluster Mode

#### Client Mode

With this modality the driver will be launched directly on the client machine, so your computer or VM. In this case the driver needs some information about the location of Spark and the executor URI. The driver will request directly to Mesos which will create severla Mesos tasks that correspond to the Spark tasks to be executed.

You will receive the result directly because you start the driver.

#### Cluster Mode

With this mode Mesos will launch a Driver Task that will manage your Spark tasks and you will retreive the results with Mesos.

#### Mesos on Spark configuration

Spark can work with Mesos in _Coarse-Grained_ mode that means the Spark tasks match the Mesos tasks. For this reason you have to specify some sizes which concern the specifications of the individual tasks:

- _spark.executor.memory_
- _spark.executor.cores_
- _spark.cores.max_
- _spark.executor.cores_

Plus we can configure a dynamic resource allocation which can resize the number of executors based on statistics of the application and the current resources available.

> For more information you can read the [main guide](https://spark.apache.org/docs/latest/running-on-mesos.html)

## MapReduce tips

MapReduce is a model to process large data sets and is inspired to homonymous primitives of functional programming languages.

The base structure used in this model is the key-value pairs. Keys and values may be primitives or complex data structures.

MapReduce algorithms involves imposing the key-value structure on arbitrary datasets.

### Model steps

1. Split the input in key-value pairs
2. Call a defined map function (_that describes how we get the keys_) for each key-value pairs 
    > this produce an intermediate key-value pairs
3. All values are grouped by keys and sorted
4. Call a defined reduce function (_that describes how we get to see all the values for a key_) on every unique key and its list of values.
    > this produce an intermediate key-value pairs, that will be the output

![Spark on Mesos](/img/mapreduce_example.png)