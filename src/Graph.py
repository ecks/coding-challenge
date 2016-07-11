import time

from TimeStamps import *
from Node import *

class Graph:

    def __init__(self):
        self.graph = {}

        self.tsDS = TimeStamps()

    def timestamp_to_epoch(self, timestamp):
        pattern = '%Y-%m-%dT%H:%M:%SZ'
        return time.mktime(time.strptime(timestamp, pattern))

    # when intaking a payment, need to know if there are
    # any other payments to evict or not
    # if intaking payment's timestamp is outside of 60s window
    # of minimum timestamp, we know that we need to evict at least
    # one payment, maybe more
    def is_not_in_wndw_of_min_ts(self, timestamp):
        if timestamp - self.get_min_ts() >= 60:
            return True
        else:
            return False

    # if incoming payment is within the 60s window of
    #             max timestamp, then intake it
    # otherwise ignore it
    def is_in_wndw_of_max_ts(self, timestamp):
        if abs(timestamp - self.get_max_ts()) < 60:
            return True
        else:
            return False

    def is_gte_of_min_ts(self, timestamp):
        return timestamp >= self.get_min_ts()

    def print_graph(self):
      for actor,node in self.graph.items():
          print(actor, node, node.target_degree())
      print

    def intake_payment(self, actor, created_time_epoch, target):
        if actor not in self.graph:
            # new actor
            self.graph[actor] = Node(created_time_epoch, target, self.tsDS)
        else:
            self.graph[actor].append_target(created_time_epoch, target)
        

    def evict_stale_actors(self, ts):
        self.tsDS.remove_stale_targets(ts)
        
        # if node has no targets, need to remove it
        graph_copy = dict(self.graph) # cannot delete item during iteration, need copy
        for actor,node in graph_copy.items():
            if not node.targets_exist():
                del self.graph[actor]
        del graph_copy

    def get_min_ts(self):
        return self.tsDS.tsL[0] # since timestamps are ordered, min_ts should be
                                # the first entry
    def get_max_ts(self):
        return self.tsDS.tsL[-1] # since timestamps are ordered, max_ts should be
                                # the last entry

    def is_ts_unset(self):
        return len(self.tsDS.tsL) == 0

    # returns a float - the median
    def median(self, list):
        sList = sorted(list)
#        print(sList)
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

    # external method
    def set_actor_in_graph(self, actor, created_time, target):
        created_time_epoch = self.timestamp_to_epoch(created_time)
     
        # initialize minimum timestamp if not initialized yet
        if self.is_ts_unset():
            
            self.intake_payment(actor, created_time_epoch, target)

        else: # already initialized
            if self.is_in_wndw_of_max_ts(created_time_epoch) or self.is_gte_of_min_ts(created_time_epoch):
                if self.is_not_in_wndw_of_min_ts(created_time_epoch):
                    # evict actors outside of 60s window
                    self.evict_stale_actors(created_time_epoch)

                # only if we are within window of max ts do we
                # intake the payment
                self.intake_payment(actor, created_time_epoch, target)
