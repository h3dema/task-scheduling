import heapq

from tasks import create_priority_queues
from tasks import Task

class TaskStr(Task):
    
    def __lt__(self, other):
        # Task with shorter remaining burst time will have higher priority in the priority queue
        return self.burst_time < other.burst_time


"""
Priority Queue for STR Scheduling:
Each queue is implemented as a priority queue using Python's heapq.
Tasks are stored and retrieved based on their remaining burst time, ensuring that the task with the shortest remaining time is executed first.

Task Comparison: The __lt__ method in the Task class ensures that tasks are automatically prioritized by remaining burst time.

Queue Management:
Each queue operates as an independent priority queue, and tasks are dynamically re-added as they are processed.

Round-Robin Across Queues:
The scheduler processes queues cyclically, allocating each queue its respective quantum (queue_quanta).
This implementation ensures that tasks with shorter remaining times are always prioritized within their respective queue while balancing fairness across queues. Let me know if you'd like additional modifications!
"""
def multi_queue_str_priority_scheduler(queues, queue_quanta, task_quantum):
    print("Execution Order:")
    queue_count = len(queues)
    current_queue = 0

    while any(queues):  # Continue until all priority queues are empty
        if queues[current_queue]:
            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue

            while remaining_time > 0 and queues[current_queue]:
                task = heapq.heappop(queues[current_queue])  # Get the task with the shortest remaining time

                execution_time = min(task.burst_time, task_quantum, remaining_time)
                print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                task.burst_time -= execution_time
                remaining_time -= execution_time

                if task.burst_time > 0:
                    heapq.heappush(queues[current_queue], task)  # Reinsert task into the priority queue if not completed
        current_queue = (current_queue + 1) % queue_count  # Move to the next queue

# Example
tasks = [
    TaskStr("Task1", priority=2, burst_time=10),
    TaskStr("Task2", priority=5, burst_time=15),
    TaskStr("Task3", priority=8, burst_time=7),
    TaskStr("Task4", priority=4, burst_time=12),
    TaskStr("Task5", priority=6, burst_time=6)
]

# Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
priority_ranges = [(1, 3), (4, 6), (7, 10)]

# Create priority queues
queues = create_priority_queues(tasks, priority_ranges)

# Define quantum times for each queue
queue_quanta = [8, 10, 6]  # Different time quanta for each queue
task_quantum = 4           # Time allocated to each task per turn

multi_queue_str_priority_scheduler(queues, queue_quanta, task_quantum)
