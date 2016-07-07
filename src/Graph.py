import time

from Node import *

class Graph:

    def __init__(self):
        self.graph = {}
        self.oldest_timestamp = -1.0 # the current maximum timestamp

    def timestamp_to_epoch(self, timestamp):
        pattern = '%Y-%m-%dT%H:%M:%SZ'
        return time.mktime(time.strptime(timestamp, pattern))

    def print_graph(self):
      for actor,node in self.graph.items():
          print(actor, node, node.target_degree())
      print

    def set_actor_in_graph(self, actor, created_time, target):
        created_time_epoch = self.timestamp_to_epoch(created_time)
        
        if actor not in self.graph:
            # new actor
            self.graph[actor] = Node(created_time_epoch, target)
        else:
            self.graph[actor].append_target(created_time_epoch, target)

    # returns a float - the median
    def median(self, list):
        sList = sorted(list)
        lLen = len(list)
        index = (lLen - 1) // 2 # floor division

        if(lLen % 2):
            return float(sList[index]) 
        else:
            return (sList[index] + sList[index + 1]) / 2.0

    def calculate_median(self):
        target_degrees = []
        for actor,node in self.graph.items():
            target_degrees.append(node.target_degree())

        return self.median(target_degrees)
