import random


class CloudArm():
    def __init__(self, data):
        self.data = [1/d for d in data]
        # used to keep track
        self.counts = [0 for _ in xrange(len(self.data))]

    def draw(self):
        # find workload which has not been measured
        min_value = min(self.counts)
        # assert(min_value==0), "Every workload is evaluated"
        not_selected = [i for i,c in enumerate(self.counts) if c == min_value]
        # random.shuffle(not_selected)
        min_workload_id = not_selected[0]
        self.counts[min_workload_id] += 1
        return self.data[min_workload_id]


