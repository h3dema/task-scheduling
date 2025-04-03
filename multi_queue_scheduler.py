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

"""
# Explanation:
Priority Ranges and Queue Assignment: Tasks are divided into separate FIFO queues based on non-overlapping priority ranges (priority_ranges).
Round-Robin Scheduling: Queues are processed cyclically (round-robin). Each queue receives queue_quantum time.
Task Processing: Within a queue, tasks are processed using a task_quantum time slice. Remaining tasks are re-added to the end of their respective queues.
This approach ensures fairness across priority levels while maintaining a predictable execution order.
"""
def multi_queue_scheduler(queues, queue_quantum, task_quantum):
    print("Execution Order:")
    queue_count = len(queues)
    current_queue = 0

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            remaining_time = queue_quantum
            while remaining_time > 0 and queues[current_queue]:
                task = queues[current_queue].popleft()

                if task.burst_time > task_quantum:
                    execution_time = min(task_quantum, remaining_time)
                    print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                    task.burst_time -= execution_time
                    remaining_time -= execution_time
                    if task.burst_time > 0:
                        queues[current_queue].append(task)
                else:
                    execution_time = min(task.burst_time, remaining_time)
                    print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units and completed")
                    remaining_time -= execution_time
        current_queue = (current_queue + 1) % queue_count

# Example
tasks = [
    Task("Task1", priority=2, burst_time=10),
    Task("Task2", priority=5, burst_time=15),
    Task("Task3", priority=8, burst_time=7),
    Task("Task4", priority=4, burst_time=12),
    Task("Task5", priority=6, burst_time=6)
]

# Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
priority_ranges = [(1, 3), (4, 6), (7, 10)]

# Create queues
queues = create_queues(tasks, priority_ranges)

# Define quantum times
queue_quantum = 10  # Time allocated to each queue
task_quantum = 4    # Time allocated to each task per turn

multi_queue_scheduler(queues, queue_quantum, task_quantum)
