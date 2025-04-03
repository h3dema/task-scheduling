from collections import deque

class Task:
    def __init__(self, name, priority, burst_time):
        self.name = name
        self.priority = priority
        self.burst_time = burst_time

def create_queues(tasks, priority_ranges):
    queues = [deque() for _ in range(len(priority_ranges))]
    for task in tasks:
        for i, (low, high) in enumerate(priority_ranges):
            if low <= task.priority <= high:
                queues[i].append(task)
                break
    return queues
  
