import pickle
import sys
import time
import traceback
import uuid

import pyprind
import ipyparallel


class Task():
    def __init__(self, func, *args, **kwargs):
        self._id = uuid.uuid4()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
    @property
    def id(self):
        return self._id
    def do(self):
        try:
            return self.func(*self.args, **self.kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {}

def worker(task):
    return task.do()

def batch_execution(tasks, engines=None):
    if tasks is None or len(tasks) < 1:
        return
    clients = ipyparallel.Client()
    clients.block = False  # use asynchronous computations
    #print("Running cores: %s" % len(clients.ids))
    lview = (clients.load_balanced_view() if ((engines is None) or (engines > len(clients.ids))) else clients.load_balanced_view(engines))
    results = {}
    for task in tasks:
        results[task] = lview.apply_async(worker, task)
        task.result = results[task]

    bar = pyprind.ProgBar(len(tasks))
    completed_tasks = []
    while len(completed_tasks) < len(tasks):
        for (task, result) in results.items():
            if task not in completed_tasks and result.ready():
                bar.update(item_id=task.id)
                #print("Task finished: %s" % task.id)
                #print("\tResult: %s" % ("Successfull" if result.successful() else "Failed"))
                #print("\tElapsed Time: %s" % result.elapsed)
                #print("\tRunning Time: %s" % result.wall_time)
                #sys.stdout.flush()
                task.output = task.result.get()
                completed_tasks.append(task)
        time.sleep(1)
    #print("All the tasks are completed")
    clients.close()
