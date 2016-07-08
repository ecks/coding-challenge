import time

from Node import *

class Graph:

    def __init__(self):
        self.graph = {}

        # keep track of both minimum and maximum timestamp
        self.min_ts = -1.0
        self.max_ts = -1.0

    def timestamp_to_epoch(self, timestamp):
        pattern = '%Y-%m-%dT%H:%M:%SZ'
        return time.mktime(time.strptime(timestamp, pattern))

    # when intaking a payment, need to know if there are
    # any other payments to evict or not
    # if intaking payment's timestamp is outside of 60s window
    # of minimum timestamp, we know that we need to evict at least
    # one payment, maybe more
    def is_not_in_wndw_of_min_ts(self, timestamp):
        if timestamp - self.min_ts >= 60:
            return True
        else:
            return False

    # if incoming payment is within the 60s window of
    #             max timestamp, then intake it
    # otherwise ignore it
    def is_in_wndw_of_max_ts(self, timestamp):
        if abs(timestamp - self.max_ts) < 60:
            return True
        else:
            return False

    def print_graph(self):
      for actor,node in self.graph.items():
          print(actor, node, node.target_degree())
      print

    def intake_payment(self, actor, created_time_epoch, target):
        if actor not in self.graph:
            # new actor
            self.graph[actor] = Node(created_time_epoch, target)
        else:
            self.graph[actor].append_target(created_time_epoch, target)
        
    def set_actor_in_graph(self, actor, created_time, target):
        created_time_epoch = self.timestamp_to_epoch(created_time)
     
        # initialize minimum timestamp if not initialized yet
        if self.min_ts < 0 and self.max_ts < 0:
            self.min_ts = created_time_epoch
            self.max_ts = created_time_epoch
            
            self.intake_payment(actor, created_time_epoch, target)

        else: # already initialized
            if self.is_in_wndw_of_max_ts(created_time_epoch):
                # intake payment
                if self.is_not_in_wndw_of_min_ts(created_time_epoch):
                    # evict actors outside of 60s window
                    self.evict_stale_actors(created_time_epoch)

                    # need to update min_ts
                    min_ts = self.find_new_min_ts(created_time_epoch)
                else:
                    # update min_ts if necessary
                    if created_time_epoch < self.min_ts:
                        self.min_ts = created_time_epoch

                # update max_ts if necessary
                if created_time_epoch > self.max_ts:
                    self.max_ts = created_time_epoch

                # only if we are within window of max ts do we
                # intake the payment
                self.intake_payment(actor, created_time_epoch, target)

    def evict_stale_actors(self, ts):
        for actor,node in self.graph.items():
            node.remove_stale_targets(ts)
        
        # if node has no targets, need to remove it
        graph_copy = dict(self.graph) # cannot delete item during iteration, need copy
        for actor,node in graph_copy.items():
            if not node.targets_exist():
                del self.graph[actor]
        del graph_copy

    def find_new_min_ts(self, ts):
        min_ts = ts

        for actor,node in self.graph.items():
            for target in node.targets:
                if target.created_time < min_ts:
                    min_ts = target.created_time

        return min_ts

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
