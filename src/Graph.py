import time

from Node import *

class Graph:

    def __init__(self):
        self.graph = {}
        self.oldest_timestamp = -1.0 # the current maximum timestamp

    def timestamp_to_epoch(self, timestamp):
        pattern = '%Y-%m-%dT%H:%M:%SZ'
        return time.mktime(time.strptime(timestamp, pattern))

    def is_not_in_60s_wndw(self, timestamp):
        if timestamp - self.oldest_timestamp >= 60:
            return True
        else:
            return False

    def print_graph(self):
      for actor,node in self.graph.items():
          print(actor, node, node.target_degree())
      print

    def set_actor_in_graph(self, actor, created_time, target):
        created_time_epoch = self.timestamp_to_epoch(created_time)
     
        # initialize oldest timestamp if not initialized yet
        if self.oldest_timestamp < 0:
            self.oldest_timestamp = created_time_epoch
        else:
            if self.is_not_in_60s_wndw(created_time_epoch):
                # evict actors outside of 60s window
                self.evict_stale_actors(created_time_epoch)

        if actor not in self.graph:
            # new actor
            self.graph[actor] = Node(created_time_epoch, target)
        else:
            self.graph[actor].append_target(created_time_epoch, target)

    def evict_stale_actors(self, ts):
        for actor,node in self.graph.items():
            node.remove_stale_targets(ts)
        
        graph_copy = dict(self.graph) # cannot delete item during iteration, need copy
        for actor,node in graph_copy.items():
            if not node.targets_exist():
                del self.graph[actor]
        del graph_copy

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
