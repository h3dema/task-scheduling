from collections import deque

class Task:
    def __init__(self, name, priority, burst_time, waiting_time=0):
        self.name = name
        self.priority = priority
        self.burst_time = burst_time
        self.waiting_time = waiting_time
        
    def __lt__(self, other):
        # Higher priority tasks will come first in the priority queue
        return self.priority > other.priority


def create_queues(tasks, priority_ranges):
    queues = [deque() for _ in range(len(priority_ranges))]
    for task in tasks:
        for i, (low, high) in enumerate(priority_ranges):
            if low <= task.priority <= high:
                queues[i].append(task)
                break
    return queues
  
