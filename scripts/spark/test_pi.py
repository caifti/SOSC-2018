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

