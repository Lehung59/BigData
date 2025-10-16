from pyspark.sql import SparkSession
import os

class Config:
    def __init__(self,
                 elasticsearch_host,
                 elasticsearch_port,
                 elasticsearch_input_json,
                 # elasticsearch_nodes_wan_only,
                 hdfs_namenode
                 ):
        self.elasticsearch_conf = {
            'es.nodes': elasticsearch_host,
            'es.port': elasticsearch_port,
            "es.input.json": elasticsearch_input_json,
            # "es.nodes.wan.only": elasticsearch_nodes_wan_only
        }
        self.hdfs_namenode = hdfs_namenode
        self.spark_app = None

    def get_elasticsearch_conf(self):
        return self.elasticsearch_conf

    def get_hdfs_namenode(self):
        return self.hdfs_namenode

    # def initialize_spark_session(self, appName):
    #     if self.spark_app == None:
    #         self.spark_app = (SparkSession
    #                           .builder.master("spark://00519018b2f8:7077")
    #                           .config("spark.es.nodes", self.elasticsearch_conf["es.nodes"])
    #                           .config("spark.es.port", self.elasticsearch_conf["es.port"])
    #                           .appName(appName)
    #                          .getOrCreate())
    #     return self.spark_app
    
    def initialize_spark_session(self, appName):
        if self.spark_app is None:
            master_url = os.getenv("SPARK_MASTER", "local[*]")  # fallback an toàn
            self.spark_app = (
                SparkSession.builder
                .master(master_url)
                .appName(appName)
                .config("spark.ui.port", "4040") 
                .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")
                .config("spark.hadoop.mapreduce.fileoutputcommitter.cleanup-failures.ignored", "true")
                .config("spark.es.nodes", self.elasticsearch_conf["es.nodes"])
                .config("spark.es.port",  self.elasticsearch_conf["es.port"])
                .getOrCreate()
            )
        return self.spark_app
