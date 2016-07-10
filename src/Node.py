class Target:

    def __init__(self, target, created_time):
        self.target = target
        self.created_time = created_time

    def __str__(self):
        return "("+self.target+"," + str(self.created_time) + ")"

class Node:

    def __init__(self, created_time, target, tsDS):
        self.targets = []
        self.tsDS = tsDS
        self.append_target(created_time, target)

    def first_time_seeing_target(self, target):
        targetsOnlyList = [Target.target for Target in self.targets]
        if target in targetsOnlyList:
            return False
        else:
            return True
    
    def find_target_update_ts(self, target, created_time):
        target_found = False
        i = 0
        while not target_found and i < len(self.targets):
            if self.targets[i].target == target:
                target_found = True
                Target = self.targets[i]
                if Target.created_time != created_time:
                    old_created_time = Target.created_time
                    Target.created_time = created_time

                    # update TimeStamp ds...
                    # remove from timestamps dict and list
                    tForTs = self.tsDS.timestamps[old_created_time]
                    tForTs.remove((Target, self.targets))
                    if len(tForTs) == 0: # if there are no other targets for that ts...
                        del self.tsDs.timestamps[old_created_time]
                        self.tsL.remove(old_created_time)


                    # add new created time
                    self.tsDS.append_timestamp(created_time, Target, self.targets)
            # update iterator
            i = i + 1
                    
    def append_target(self, created_time, target):
        # if we see Target for first time, create new Target
        if self.first_time_seeing_target(target):
            target = Target(target, created_time)
            self.targets.append(target)

            # add the target to timestamp data structure
            self.tsDS.append_timestamp(created_time, target, self.targets)
        else: # Target has already been added, still need to update timestamp
            self.find_target_update_ts(target, created_time)

    def is_target_in_60s_wndw(self, target, ts):
        if ts - target.created_time >= 60:
            return False
        else:
            return True

#    def remove_stale_targets(self, ts):
#        self.targets = [target for target in self.targets if self.is_target_in_60s_wndw(target, ts)]
#       self.tsDS.find_stale_targets(ts, self.targets)

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


