from collections import deque

from tasks import Task
from tasks import create_queues
    

def multi_queue_sjf_scheduler(queues, queue_quanta, task_quantum):
    print("Execution Order:")
    queue_count = len(queues)
    current_queue = 0

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            # Sort the queue by burst time for SJF scheduling
            queues[current_queue] = deque(sorted(queues[current_queue], key=lambda t: t.burst_time))

            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue
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
        current_queue = (current_queue + 1) % queue_count  # Move to the next queue

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

# Define quantum times for each queue
queue_quanta = [8, 10, 6]  # Different time quanta for each queue
task_quantum = 4           # Time allocated to each task per turn

multi_queue_sjf_scheduler(queues, queue_quanta, task_quantum)
