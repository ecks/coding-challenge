class Graph:

    def __init__(self):
        self.graph = {}
        self.oldest_timestamp = -1.0 # the current maximum timestamp

    def timestamp_to_epoch(self, timestamp):
        pattern = '%Y-%m-%dT%H:%M:%SZ'
        return time.mktime(time.strptime(timestamp, pattern))

    def print_graph(self):
      for actor,node in graph.iteritems():
          print actor, node, node.target_degree()
      print

    def set_actor_in_graph(actor, created_time, target):
        if actor not in graph:
            # new actor
            graph[actor] = Node(created_time, target)
        else:
            graph[actor].append_target(created_time, target)

    # returns a float - the median
    def median(list):
        sList = sorted(list)
        lLen = len(list)
        index = (lLen - 1) // 2 # floor division

        if(lLen % 2):
            return float(sList[index]) 
        else:
            return (sList[index] + sList[index + 1]) / 2.0

    def calculate_median():
        target_degrees = []
        for actor,node in graph.iteritems():
            target_degrees.append(node.target_degree())

        return median(target_degrees)
