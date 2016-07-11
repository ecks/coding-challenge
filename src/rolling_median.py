import sys
import json

from Graph import *

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Specify input and output arguments")
    else:
        in_file = open(sys.argv[1], 'r')
        out_file = open(sys.argv[2], 'w')

        graph = Graph()

#        i = 1
        for line in in_file:
            json_line = json.loads(line)

            actor = json_line['actor']
            created_time = json_line['created_time']
            target = json_line['target']

            graph.set_actor_in_graph(actor, created_time, target)
            graph.set_actor_in_graph(target, created_time, actor)

            calc_median = graph.calculate_median()
            calc_median_fmt = "{0:.2f}".format(calc_median)

#            print("ln: "+str(i))
#            print(calc_median_fmt)

#            graph.print_graph()

            out_file.write(calc_median_fmt+'\n')
#            i = i + 1
