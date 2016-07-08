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

    def is_target_in_60s_wndw(self, target, ts):
        if ts - target.created_time >= 60:
            return False
        else:
            return True

    def remove_stale_targets(self, ts):
        self.targets = [target for target in self.targets if self.is_target_in_60s_wndw(target, ts)]

    def targets_exist(self):
        if len(self.targets) != 0:
            return True
        else:
            return False

    def __str__(self):
        targets = ""
        for target in self.targets:
            targets = targets + str(target) + " "
        return targets

    def target_degree(self):
        return len(self.targets)


