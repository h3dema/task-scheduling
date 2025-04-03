import heapq

from tasks import create_priority_queues


class Task:
    def __init__(self, name, priority, burst_time):
        self.name = name
        self.priority = priority
        self.burst_time = burst_time
    
    def __lt__(self, other):
        # Task with shorter remaining burst time will have higher priority in the priority queue
        return self.burst_time < other.burst_time


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
    Task("Task1", priority=2, burst_time=10),
    Task("Task2", priority=5, burst_time=15),
    Task("Task3", priority=8, burst_time=7),
    Task("Task4", priority=4, burst_time=12),
    Task("Task5", priority=6, burst_time=6)
]

# Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
priority_ranges = [(1, 3), (4, 6), (7, 10)]

# Create priority queues
queues = create_priority_queues(tasks, priority_ranges)

# Define quantum times for each queue
queue_quanta = [8, 10, 6]  # Different time quanta for each queue
task_quantum = 4           # Time allocated to each task per turn

multi_queue_str_priority_scheduler(queues, queue_quanta, task_quantum)
