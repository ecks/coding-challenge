import bisect

# TimeStamp class - contains a dictionary
# the index is a timestamp, and the value is a list
# of (targets, listOfWhereInserted). It is mainly used for removing stale entries
# from target list, so that the whole graph does not have to
# be searched for timestamps that match. Its secondary use is 
# for finding min_ts
class TimeStamps:
    def __init__(self):
        self.timestamps = {}
        self.tsL = []

    def append_timestamp(self, timestamp, target, targets):
        if timestamp in self.timestamps:
            self.timestamps[timestamp].append((target, targets))
        else:
            self.timestamps[timestamp] = [(target, targets)]
            bisect.insort_left(self.tsL, timestamp)
    
    def remove_stale_targets(self, ts):
        target_ts = ts - 60
        nIn60s = bisect.bisect_right(self.tsL, target_ts) # use bisect_right in order to catch something equal to "ts - 60"
#        print("stale_tses: "+str(self.tsL[0:nIn60s]))
#        print("all_tses: "+str(self.tsL))
        for stale_ts in self.tsL[0:nIn60s]:
#          print("stale_ts: "+str(stale_ts))
          stale_targetsAndLists = self.timestamps[stale_ts]
          for stale_target, targetsList in stale_targetsAndLists:
#              targets = "["
#              for target in targetsList:
#                targets = targets+str(target)+" "
#              targets = targets + "]"
#              print(targets)
#              print(stale_target)
              targetsList.remove(stale_target)
        # remove the timestamps from the list and dictionary themselves
        tsLr_copy = self.tsL[0:nIn60s]
        for tsLr in tsLr_copy:
            self.tsL.remove(tsLr)
            del self.timestamps[tsLr]
