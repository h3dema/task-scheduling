import heapq

from tasks import Task
from tasks import create_queues



"""
a heapq priority queue is used to manage tasks based on their priority. The priority queue ensures that tasks with higher priority are processed first. After executing a task for the time quantum, if the task isn't finished, it is reinserted into the priority queue for further processing
"""
def priority_based_round_robin(tasks, time_quantum):
    # Create a priority queue
    priority_queue = []
    for task in tasks:
        heapq.heappush(priority_queue, task)

    print("Execution Order:")
    while priority_queue:
        task = heapq.heappop(priority_queue)

        if task.burst_time > time_quantum:
            print(f"Task {task.name} executed for {time_quantum} units")
            task.burst_time -= time_quantum
            heapq.heappush(priority_queue, task)
        else:
            print(f"Task {task.name} executed for {task.burst_time} units and completed")

# Example
tasks = [
    Task("Task1", priority=2, burst_time=10),
    Task("Task2", priority=1, burst_time=15),
    Task("Task3", priority=3, burst_time=7)
]

time_quantum = 4
priority_based_round_robin(tasks, time_quantum)
