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

counts = lines.flatMap(lambda x: x.split(' ')).map(lambda x: x.replace(
    ",", "").replace(".", "")).map(lambda x: (x, 1)).reduceByKey(add)

with open("output_WordCount.txt", "w") as output:
    results = counts.sortBy(lambda elm: elm[1]).collect()
    print("-----[!]-----[My Spark Application]")
    print("Word |  Count")
    print("-"*16)
    output.write("[My Spark Application]\n")
    output.write("Word |  Count\n")
    output.write("-"*16 + "\n")
    for (word, count) in results:
        print("[{:3}]-> {}".format(count, word))
        output.write("[{:3}]-> {}\n".format(count, word))
    print("-"*16)
    output.write("-"*16 + "\n")

spark.stop()
