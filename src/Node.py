class Target:

    def __init__(self, target, created_time):
        self.target = target
        self.created_time = created_time

    def __str__(self):
        return "("+self.target+"," + str(self.created_time) + ")"

class Node:

    def __init__(self, created_time, target):
        self.targets = []
        self.append_target(created_time, target)

    def append_target(self, created_time, target):
        target = Target(target, created_time)
        self.targets.append(target)

    def __str__(self):
        targets = ""
        for target in self.targets:
            targets = targets + str(target) + " "
        return targets

    def target_degree(self):
        return len(self.targets)


