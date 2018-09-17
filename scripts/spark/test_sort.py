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

