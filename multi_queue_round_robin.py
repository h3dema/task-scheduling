"""
    Round Robin Scheduler

    Tasks within each queue are processed cyclically, with each task receiving a fixed time slice (task_quantum).
    If the task isn't completed within its allocated time slice, it is re-added to the end of the queue for further execution.

    Queues are processed in a circular fashion, with each queue receiving its predefined time quantum (queue_quanta[current_queue]).

"""
from collections import deque

from tasks import Task
from tasks import create_queues


def multi_queue_round_robin_scheduler(queues, queue_quanta, task_quantum):
    """
    Multi-queue round robin scheduler.

    Parameters:
    - queues (list): A list of lists of Task objects, where each sublist represents a queue
    - queue_quanta (list): A list of time quanta for each queue
    - task_quantum (int): Time allocated to each task per turn

    Returns:
        None
    """
    print("Execution Order:")
    queue_count = len(queues)
    current_queue = queue_count - 1  # Start with the last queue (more priority)

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue
            while remaining_time > 0 and queues[current_queue]:
                task = queues[current_queue].popleft()

                execution_time = min(task.burst_time, task_quantum, remaining_time)
                print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                task.burst_time -= execution_time
                remaining_time -= execution_time

                if task.burst_time > 0:
                    queues[current_queue].append(task)
        # Move to the next queue
        current_queue = (current_queue - 1)
        if current_queue < 0:
            current_queue = queue_count - 1


if __name__ == "__main__":
    #
    # Example
    #

    # Define tasks with dependencies
    # TODO: Add dependencies to tasks
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
    # TODO: implement this queues as priority queues, so the tasks in the queue are sorted by their priority
    queues = create_queues(tasks, priority_ranges)

    # Define quantum times for each queue
    queue_quanta = [6, 8, 10]  # Different time quanta for each queue
    # Maximum time allocated to any task in a single turn. If you want don't task_quantum to be limited, set it to a large number
    # (e.g., 1000). This is useful for tasks that may take a long time to complete.
    task_quantum = 4

    # Execute the multi-queue round robin scheduler
    multi_queue_round_robin_scheduler(queues, queue_quanta, task_quantum)
