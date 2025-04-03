import heapq

class Task:
    def __init__(self, name, priority, burst_time):
        self.name = name
        self.priority = priority
        self.burst_time = burst_time
    
    def __lt__(self, other):
        # Higher priority tasks will come first in the priority queue
        return self.priority > other.priority

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
