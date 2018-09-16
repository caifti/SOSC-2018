### [◀](/SOSC-2018)

## Deploy of the Spark Cluster

You can use orchent as you have seen in the previous hands-on:

``` bash
orchent depcreate  templates/hands-on-2/spark-cluster.yaml '{}'
```

## Examples

Now let's play a bit with the Spark framework.

### Calculus of pi

Let's create a file named `test_pi.py` with the following code:

```python
#!/usr/bin/env python
#! -*- coding: utf-8 -*-
from __future__ import print_function

from operator import add
from random import random

from pyspark import SparkConf, SparkContext

# Application configuration
conf = SparkConf().setAppName("PiCalc")
# Executor parameters personalization
# conf.set('spark.executor.memory', '512m')
# conf.set('spark.executor.cores', '1')
# conf.set('spark.executor.cores.max', '2')
conf.set('spark.cores.max', '4')

# Spark Context
sc = SparkContext(conf=conf)

PARTITIONS = 4
_N_ = 100000 * PARTITIONS

# Define the pi function
def foo(_):
    x = random() * 2 - 1
    y = random() * 2 - 1
    return 1 if x ** 2 + y ** 2 <= 1 else 0


with open("output_PiCalc.txt", "w") as output:
    print("-----[!]-----[My Spark Application] Start the calculus")
    output.write("[My Spark Application] Start the calculus\n")
    # Launch the application in parallel
    count = sc.parallelize(range(1, _N_ + 1), PARTITIONS).map(foo).reduce(add)

    print("-----[!]-----[My Spark Application] Pi is roughly {}".format(4.0 * count / _N_))
    output.write("[My Spark Application] Pi is roughly {}\n".format(4.0 * count / _N_))

# Exit Spark Context
sc.stop()

```

Run the application with the following command:

```bash
spark-run test_pi.py
```

### List sort

Let's create a file named `test_sort.py` with the following code:

```python
#!/usr/bin/env python
#! -*- coding: utf-8 -*-
from __future__ import print_function

from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
    
# Application configuration
conf = SparkConf().setAppName("Sort")
# Executor parameters personalization
# conf.set('spark.executor.memory', '512m')
# conf.set('spark.executor.cores', '1')
# conf.set('spark.executor.cores.max', '1')
# conf.set('spark.cores.max', '2')

# Spark Context
sc = SparkContext(conf=conf)

spark = SparkSession(sc).builder.getOrCreate()

data = sc.parallelize([
    ('Amber', 22), ('Alfred', '23'), ('Skye',4), ('Albert', '12'), ('Amber', 9)
])

# Convert all ages to int and then sort tuples by ages
sortedCount = data.map(
        lambda elm: ( elm[0], int(elm[1]) )
    ).sortBy(
    lambda elm: elm[1])

with open("output_Sort.txt", "w") as output:
    sorted_data = sortedCount.collect()
    print("-----[!]-----[My Spark Application]")
    print("Name\t|  Age")
    print("-"*16)
    output.write("[My Spark Application]\n")
    output.write("Name\t|  Age\n")
    output.write("-"*16 + "\n")
    for (name, age) in sorted_data:
        print("{}\t|  {}".format(name, age))
        output.write("{}\t|  {}\n".format(name, age))
    print("-"*16)
    output.write("-"*16 + "\n")

spark.stop()

```

Run the application with the following command:

```bash
spark-run test_sort.py
```

### Word count

Let's create a file named `test_word_count.py` with the following code:

```python
#!/usr/bin/env python
#! -*- coding: utf-8 -*-
from __future__ import print_function

import sys
from operator import add

from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext

# Application configuration
conf = SparkConf().setAppName("PythonWordCount")
# Executor parameters personalization
# conf.set('spark.executor.memory', '512m')
# conf.set('spark.executor.cores', '1')
# conf.set('spark.executor.cores.max', '1')
# conf.set('spark.cores.max', '2')

# Spark Context
sc = SparkContext(conf=conf)

spark = SparkSession(sc).builder.getOrCreate()

with open("ipsum.txt") as text_file:
    lines = sc.parallelize(text_file.readlines())

counts = lines.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)

with open("output_WordCount.txt", "w") as output:
    results = counts.sortBy(lambda elm: elm[1]).collect()
    print("-----[!]-----[My Spark Application]")
    print("Word|  Count")
    print("-"*16)
    output.write("[My Spark Application]\n")
    output.write("Word|  Count\n")
    output.write("-"*16 + "\n")
    for (word, count) in results:
        print("{}|  {}".format(word, count))
        output.write("{}|  {}\n".format(word, count))
    print("-"*16)
    output.write("-"*16 + "\n")

spark.stop()

```

Run the application with the following command:

```bash
wget https://raw.githubusercontent.com/DODAS-TS/SOSC-2018/master/data/ipsum.txt
spark-run test_word_count.py
```